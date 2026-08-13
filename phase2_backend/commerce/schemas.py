"""Pydantic contracts for the versioned commerce authentication API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OtpRequestBody(BaseModel):
    phone: str = Field(min_length=10, max_length=18)


class OtpRequestResponse(BaseModel):
    challenge_id: str
    phone: str
    message: str
    expires_in_seconds: int
    resend_after_seconds: int


class OtpVerifyBody(BaseModel):
    challenge_id: str = Field(min_length=36, max_length=36)
    phone: str = Field(min_length=10, max_length=18)
    code: str = Field(pattern=r"^\d{4,10}$")


class RefreshBody(BaseModel):
    refresh_token: str = Field(min_length=32, max_length=512)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_expires_in_seconds: int
    refresh_expires_in_seconds: int


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    phone_e164: str
    status: str
    preferred_locale: str
    display_name: str | None


class AuthReadinessResponse(BaseModel):
    ready: bool
    provider: str | None
    detail: str


class ServiceReadinessResponse(BaseModel):
    ready: bool
    database: str
    authentication: str
