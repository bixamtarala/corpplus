"""Persistent, provider-backed mobile OTP authentication service."""

from __future__ import annotations

import hashlib
import hmac
import re
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .auth_config import CommerceAuthSettings
from .models import CommerceSession, CommerceUser, OtpChallenge
from .otp_provider import OtpProvider


class InvalidPhone(ValueError):
    pass


class OtpRateLimited(RuntimeError):
    def __init__(self, retry_after_seconds: int) -> None:
        super().__init__("OTP request limit reached")
        self.retry_after_seconds = max(1, retry_after_seconds)


class InvalidOtp(RuntimeError):
    pass


class InvalidSession(RuntimeError):
    pass


@dataclass(frozen=True)
class OtpRequestResult:
    challenge_id: str
    masked_phone: str
    expires_in_seconds: int
    resend_after_seconds: int


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    access_expires_in_seconds: int
    refresh_expires_in_seconds: int


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def normalize_indian_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    if not re.fullmatch(r"[6-9]\d{9}", digits):
        raise InvalidPhone("Enter a valid Indian mobile number")
    return f"+91{digits}"


def mask_phone(phone_e164: str) -> str:
    return f"+91******{phone_e164[-4:]}"


class CommerceAuthService:
    def __init__(
        self,
        *,
        db: Session,
        settings: CommerceAuthSettings,
        provider: OtpProvider | None = None,
    ) -> None:
        self.db = db
        self.settings = settings
        self.provider = provider

    def request_otp(self, *, phone: str, request_ip: str) -> OtpRequestResult:
        provider = self._require_provider()
        phone_e164 = normalize_indian_phone(phone)
        phone_hash = self._identifier_hash("phone", phone_e164)
        ip_hash = self._identifier_hash("ip", request_ip or "unknown")
        now = utcnow()
        window_start = now - timedelta(seconds=self.settings.rate_window_seconds)

        latest = self.db.scalar(
            select(OtpChallenge)
            .where(OtpChallenge.phone_hash == phone_hash)
            .order_by(OtpChallenge.created_at.desc())
            .limit(1)
        )
        if latest is not None:
            elapsed = int((now - self._aware(latest.created_at)).total_seconds())
            if elapsed < self.settings.resend_cooldown_seconds:
                raise OtpRateLimited(self.settings.resend_cooldown_seconds - elapsed)

        phone_requests = self.db.scalar(
            select(func.count(OtpChallenge.id)).where(
                OtpChallenge.phone_hash == phone_hash,
                OtpChallenge.created_at >= window_start,
            )
        )
        ip_requests = self.db.scalar(
            select(func.count(OtpChallenge.id)).where(
                OtpChallenge.request_ip_hash == ip_hash,
                OtpChallenge.created_at >= window_start,
            )
        )
        if (phone_requests or 0) >= self.settings.max_requests_per_phone:
            raise OtpRateLimited(self.settings.rate_window_seconds)
        if (ip_requests or 0) >= self.settings.max_requests_per_ip:
            raise OtpRateLimited(self.settings.rate_window_seconds)

        provider_challenge = provider.request_code(phone_e164)
        expiry_seconds = min(
            provider_challenge.expires_in_seconds,
            self.settings.otp_expiry_seconds,
        )
        challenge = OtpChallenge(
            phone_hash=phone_hash,
            request_ip_hash=ip_hash,
            provider=provider.name,
            provider_reference=provider_challenge.reference,
            status="requested",
            failed_attempts=0,
            max_attempts=self.settings.max_verify_attempts,
            expires_at=now + timedelta(seconds=expiry_seconds),
        )
        self.db.add(challenge)
        self.db.commit()
        self.db.refresh(challenge)

        return OtpRequestResult(
            challenge_id=challenge.id,
            masked_phone=mask_phone(phone_e164),
            expires_in_seconds=expiry_seconds,
            resend_after_seconds=self.settings.resend_cooldown_seconds,
        )

    def verify_otp(self, *, challenge_id: str, phone: str, code: str) -> TokenPair:
        provider = self._require_provider()
        phone_e164 = normalize_indian_phone(phone)
        phone_hash = self._identifier_hash("phone", phone_e164)
        now = utcnow()

        challenge = self.db.scalar(
            select(OtpChallenge)
            .where(
                OtpChallenge.id == challenge_id,
                OtpChallenge.phone_hash == phone_hash,
            )
            .with_for_update()
        )
        if challenge is None or challenge.status != "requested":
            raise InvalidOtp("Invalid or expired verification code")

        latest_challenge_id = self.db.scalar(
            select(OtpChallenge.id)
            .where(
                OtpChallenge.phone_hash == phone_hash,
                OtpChallenge.status == "requested",
            )
            .order_by(OtpChallenge.created_at.desc(), OtpChallenge.id.desc())
            .limit(1)
        )
        if latest_challenge_id != challenge.id:
            challenge.status = "expired"
            self.db.commit()
            raise InvalidOtp("Invalid or expired verification code")
        if self._aware(challenge.expires_at) <= now:
            challenge.status = "expired"
            self.db.commit()
            raise InvalidOtp("Invalid or expired verification code")
        if challenge.failed_attempts >= challenge.max_attempts:
            challenge.status = "failed"
            self.db.commit()
            raise InvalidOtp("Invalid or expired verification code")

        if not provider.verify_code(phone_e164, code):
            challenge.failed_attempts += 1
            if challenge.failed_attempts >= challenge.max_attempts:
                challenge.status = "failed"
            self.db.commit()
            raise InvalidOtp("Invalid or expired verification code")

        challenge.status = "consumed"
        challenge.consumed_at = now
        user = self.db.scalar(select(CommerceUser).where(CommerceUser.phone_e164 == phone_e164))
        if user is None:
            user = CommerceUser(phone_e164=phone_e164, status="active")
            self.db.add(user)
            self.db.flush()
        elif user.status != "active":
            challenge.status = "failed"
            self.db.commit()
            raise InvalidSession("Account is unavailable")

        user.last_authenticated_at = now
        token_pair = self._create_session(user=user, now=now)
        self.db.commit()
        return token_pair

    def refresh(self, refresh_token: str) -> TokenPair:
        now = utcnow()
        refresh_hash = self._token_hash(refresh_token)
        session = self.db.scalar(
            select(CommerceSession).where(CommerceSession.refresh_token_hash == refresh_hash).with_for_update()
        )
        if session is None or session.revoked_at is not None or self._aware(session.expires_at) <= now:
            raise InvalidSession("Invalid or expired session")

        user = self.db.get(CommerceUser, session.user_id)
        if user is None or user.status != "active":
            raise InvalidSession("Invalid or expired session")

        raw_refresh = secrets.token_urlsafe(48)
        session.refresh_token_hash = self._token_hash(raw_refresh)
        session.last_used_at = now
        session.expires_at = now + timedelta(days=self.settings.refresh_token_days)
        token_pair = self._token_pair(
            user=user,
            session=session,
            raw_refresh_token=raw_refresh,
            now=now,
        )
        self.db.commit()
        return token_pair

    def logout(self, refresh_token: str) -> None:
        session = self.db.scalar(
            select(CommerceSession).where(CommerceSession.refresh_token_hash == self._token_hash(refresh_token))
        )
        if session is not None and session.revoked_at is None:
            session.revoked_at = utcnow()
            self.db.commit()

    def authenticate_access_token(self, access_token: str) -> CommerceUser:
        try:
            payload = jwt.decode(
                access_token,
                self.settings.jwt_secret,
                algorithms=[self.settings.jwt_algorithm],
                options={"require_sub": True, "require_exp": True},
            )
        except JWTError as exc:
            raise InvalidSession("Invalid access token") from exc

        if payload.get("type") != "access":
            raise InvalidSession("Invalid access token")
        session_id = payload.get("sid")
        user_id = payload.get("sub")
        if not isinstance(session_id, str) or not isinstance(user_id, str):
            raise InvalidSession("Invalid access token")

        session = self.db.get(CommerceSession, session_id)
        user = self.db.get(CommerceUser, user_id)
        if (
            session is None
            or session.user_id != user_id
            or session.revoked_at is not None
            or self._aware(session.expires_at) <= utcnow()
            or user is None
            or user.status != "active"
        ):
            raise InvalidSession("Invalid access token")
        return user

    def _create_session(self, *, user: CommerceUser, now: datetime) -> TokenPair:
        raw_refresh = secrets.token_urlsafe(48)
        session = CommerceSession(
            user_id=user.id,
            refresh_token_hash=self._token_hash(raw_refresh),
            expires_at=now + timedelta(days=self.settings.refresh_token_days),
            last_used_at=now,
        )
        self.db.add(session)
        self.db.flush()
        return self._token_pair(
            user=user,
            session=session,
            raw_refresh_token=raw_refresh,
            now=now,
        )

    def _token_pair(
        self,
        *,
        user: CommerceUser,
        session: CommerceSession,
        raw_refresh_token: str,
        now: datetime,
    ) -> TokenPair:
        access_seconds = self.settings.access_token_minutes * 60
        refresh_seconds = self.settings.refresh_token_days * 24 * 60 * 60
        access_token = jwt.encode(
            {
                "sub": user.id,
                "sid": session.id,
                "type": "access",
                "jti": secrets.token_hex(16),
                "iat": now,
                "exp": now + timedelta(seconds=access_seconds),
            },
            self.settings.jwt_secret,
            algorithm=self.settings.jwt_algorithm,
        )
        return TokenPair(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            access_expires_in_seconds=access_seconds,
            refresh_expires_in_seconds=refresh_seconds,
        )

    def _identifier_hash(self, namespace: str, value: str) -> str:
        return hmac.new(
            self.settings.otp_hash_secret.encode("utf-8"),
            f"{namespace}:{value}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    @staticmethod
    def _token_hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _aware(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    def _require_provider(self) -> OtpProvider:
        if self.provider is None:
            raise RuntimeError("OTP provider is required for verification operations")
        return self.provider
