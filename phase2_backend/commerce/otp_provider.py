"""OTP provider abstraction and Twilio Verify implementation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

from .auth_config import AuthNotConfigured


class OtpProviderError(RuntimeError):
    """Provider failure that is safe to translate to a generic API response."""


@dataclass(frozen=True)
class ProviderChallenge:
    reference: str
    expires_in_seconds: int


class OtpProvider(Protocol):
    name: str

    def request_code(self, phone_e164: str) -> ProviderChallenge:
        ...

    def verify_code(self, phone_e164: str, code: str) -> bool:
        ...


class TwilioVerifyProvider:
    name = "twilio_verify"

    def __init__(
        self,
        *,
        account_sid: str,
        auth_token: str,
        service_sid: str,
        expiry_seconds: int,
    ) -> None:
        try:
            from twilio.rest import Client
        except ImportError as exc:  # pragma: no cover - deployment dependency guard
            raise AuthNotConfigured("The twilio package is not installed") from exc

        self._client = Client(account_sid, auth_token)
        self._service_sid = service_sid
        self._expiry_seconds = expiry_seconds

    def request_code(self, phone_e164: str) -> ProviderChallenge:
        try:
            verification = self._client.verify.v2.services(self._service_sid).verifications.create(
                to=phone_e164, channel="sms"
            )
        except Exception as exc:  # Twilio exposes several transport/API errors
            raise OtpProviderError("OTP delivery provider unavailable") from exc

        return ProviderChallenge(
            reference=verification.sid,
            expires_in_seconds=self._expiry_seconds,
        )

    def verify_code(self, phone_e164: str, code: str) -> bool:
        try:
            check = self._client.verify.v2.services(self._service_sid).verification_checks.create(
                to=phone_e164, code=code
            )
        except Exception as exc:
            raise OtpProviderError("OTP verification provider unavailable") from exc
        return bool(check.status == "approved")


def build_otp_provider(*, expiry_seconds: int) -> OtpProvider:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    service_sid = os.getenv("TWILIO_VERIFY_SERVICE_SID", "").strip()

    if (
        not account_sid.startswith("AC")
        or len(account_sid) < 10
        or len(auth_token) < 20
        or not service_sid.startswith("VA")
        or len(service_sid) < 10
    ):
        raise AuthNotConfigured("TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and " "TWILIO_VERIFY_SERVICE_SID are required")

    return TwilioVerifyProvider(
        account_sid=account_sid,
        auth_token=auth_token,
        service_sid=service_sid,
        expiry_seconds=expiry_seconds,
    )
