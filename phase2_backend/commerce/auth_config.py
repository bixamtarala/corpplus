"""Fail-closed configuration for commerce mobile authentication."""

from __future__ import annotations

import os
import hmac
from dataclasses import dataclass


class AuthNotConfigured(RuntimeError):
    """Raised when production authentication dependencies are unavailable."""


def _required_secret(name: str) -> str:
    value = os.getenv(name, "").strip()
    normalized = value.lower()
    if len(value) < 32 or any(marker in normalized for marker in ("replace_with", "change_me", "your_")):
        raise AuthNotConfigured(f"{name} must be configured with at least 32 characters")
    return value


@dataclass(frozen=True)
class CommerceAuthSettings:
    jwt_secret: str
    otp_hash_secret: str
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 15
    refresh_token_days: int = 30
    otp_expiry_seconds: int = 600
    resend_cooldown_seconds: int = 60
    rate_window_seconds: int = 900
    max_requests_per_phone: int = 3
    max_requests_per_ip: int = 10
    max_verify_attempts: int = 5

    def __post_init__(self) -> None:
        if len(self.jwt_secret) < 32 or len(self.otp_hash_secret) < 32:
            raise AuthNotConfigured("Commerce authentication secrets are too short")
        if hmac.compare_digest(self.jwt_secret, self.otp_hash_secret):
            raise AuthNotConfigured("Commerce authentication secrets must differ")
        if self.jwt_algorithm not in {"HS256", "HS384", "HS512"}:
            raise AuthNotConfigured("COMMERCE_JWT_ALGORITHM is not supported")

        bounded_values = {
            "COMMERCE_ACCESS_TOKEN_MINUTES": (self.access_token_minutes, 1, 60),
            "COMMERCE_REFRESH_TOKEN_DAYS": (self.refresh_token_days, 1, 90),
            "COMMERCE_OTP_EXPIRY_SECONDS": (self.otp_expiry_seconds, 120, 900),
            "COMMERCE_OTP_RESEND_SECONDS": (
                self.resend_cooldown_seconds,
                30,
                600,
            ),
            "COMMERCE_OTP_RATE_WINDOW_SECONDS": (
                self.rate_window_seconds,
                self.resend_cooldown_seconds,
                3600,
            ),
            "COMMERCE_OTP_MAX_REQUESTS_PER_PHONE": (
                self.max_requests_per_phone,
                1,
                10,
            ),
            "COMMERCE_OTP_MAX_REQUESTS_PER_IP": (
                self.max_requests_per_ip,
                1,
                100,
            ),
            "COMMERCE_OTP_MAX_VERIFY_ATTEMPTS": (
                self.max_verify_attempts,
                1,
                10,
            ),
        }
        for name, (value, minimum, maximum) in bounded_values.items():
            if not minimum <= value <= maximum:
                raise AuthNotConfigured(f"{name} must be between {minimum} and {maximum}")

    @classmethod
    def from_env(cls) -> "CommerceAuthSettings":
        jwt_secret = _required_secret("COMMERCE_JWT_SECRET")
        otp_hash_secret = _required_secret("COMMERCE_OTP_HASH_SECRET")
        if hmac.compare_digest(jwt_secret, otp_hash_secret):
            raise AuthNotConfigured("COMMERCE_JWT_SECRET and COMMERCE_OTP_HASH_SECRET must differ")

        algorithm = os.getenv("COMMERCE_JWT_ALGORITHM", "HS256")
        if algorithm not in {"HS256", "HS384", "HS512"}:
            raise AuthNotConfigured("COMMERCE_JWT_ALGORITHM is not supported")

        return cls(
            jwt_secret=jwt_secret,
            otp_hash_secret=otp_hash_secret,
            jwt_algorithm=algorithm,
            access_token_minutes=int(os.getenv("COMMERCE_ACCESS_TOKEN_MINUTES", "15")),
            refresh_token_days=int(os.getenv("COMMERCE_REFRESH_TOKEN_DAYS", "30")),
            otp_expiry_seconds=int(os.getenv("COMMERCE_OTP_EXPIRY_SECONDS", "600")),
            resend_cooldown_seconds=int(os.getenv("COMMERCE_OTP_RESEND_SECONDS", "60")),
            rate_window_seconds=int(os.getenv("COMMERCE_OTP_RATE_WINDOW_SECONDS", "900")),
            max_requests_per_phone=int(os.getenv("COMMERCE_OTP_MAX_REQUESTS_PER_PHONE", "3")),
            max_requests_per_ip=int(os.getenv("COMMERCE_OTP_MAX_REQUESTS_PER_IP", "10")),
            max_verify_attempts=int(os.getenv("COMMERCE_OTP_MAX_VERIFY_ATTEMPTS", "5")),
        )
