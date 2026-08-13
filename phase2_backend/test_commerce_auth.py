"""Focused tests for provider-backed commerce mobile authentication."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from phase2_backend.commerce.api import (
    create_app,
    get_auth_settings,
    get_commerce_db,
    get_otp_provider,
)
from phase2_backend.commerce.auth_config import (
    AuthNotConfigured,
    CommerceAuthSettings,
)
from phase2_backend.commerce.models import Base, CommerceSession, OtpChallenge
from phase2_backend.commerce.otp_provider import (
    OtpProviderError,
    ProviderChallenge,
)


class RecordingOtpProvider:
    name = "test_provider"

    def __init__(self, *, accepted_code: str = "654321") -> None:
        self.accepted_code = accepted_code
        self.requests: list[str] = []

    def request_code(self, phone_e164: str) -> ProviderChallenge:
        self.requests.append(phone_e164)
        return ProviderChallenge(
            reference=f"test-reference-{len(self.requests)}",
            expires_in_seconds=300,
        )

    def verify_code(self, phone_e164: str, code: str) -> bool:
        return phone_e164 in self.requests and code == self.accepted_code


class FailingOtpProvider(RecordingOtpProvider):
    def request_code(self, phone_e164: str) -> ProviderChallenge:
        raise OtpProviderError("provider unavailable")


@pytest.fixture()
def auth_settings() -> CommerceAuthSettings:
    return CommerceAuthSettings(
        jwt_secret="jwt-test-secret-that-is-longer-than-thirty-two-characters",
        otp_hash_secret="otp-test-secret-that-is-longer-than-thirty-two-characters",
        access_token_minutes=5,
        refresh_token_days=7,
        otp_expiry_seconds=300,
        resend_cooldown_seconds=60,
        rate_window_seconds=900,
        max_requests_per_phone=3,
        max_requests_per_ip=10,
        max_verify_attempts=3,
    )


@pytest.fixture()
def session_factory():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
    try:
        yield factory
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture()
def auth_client(session_factory, auth_settings):
    provider = RecordingOtpProvider()
    application = create_app()

    def override_db() -> Generator[Session, None, None]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    application.dependency_overrides[get_commerce_db] = override_db
    application.dependency_overrides[get_auth_settings] = lambda: auth_settings
    application.dependency_overrides[get_otp_provider] = lambda: provider

    with TestClient(application) as client:
        yield client, provider, session_factory


def test_auth_flow_consumes_otp_rotates_refresh_and_revokes_session(
    auth_client,
) -> None:
    client, provider, session_factory = auth_client
    request_response = client.post(
        "/api/commerce/v1/auth/otp/request",
        json={"phone": "9876543210"},
    )
    assert request_response.status_code == 200
    requested = request_response.json()
    assert requested["phone"] == "+91******3210"
    assert "654321" not in request_response.text
    assert provider.requests == ["+919876543210"]

    wrong_response = client.post(
        "/api/commerce/v1/auth/otp/verify",
        json={
            "challenge_id": requested["challenge_id"],
            "phone": "9876543210",
            "code": "111111",
        },
    )
    assert wrong_response.status_code == 401

    verify_response = client.post(
        "/api/commerce/v1/auth/otp/verify",
        json={
            "challenge_id": requested["challenge_id"],
            "phone": "+919876543210",
            "code": "654321",
        },
    )
    assert verify_response.status_code == 200
    first_tokens = verify_response.json()
    assert first_tokens["token_type"] == "bearer"
    assert first_tokens["access_token"]
    assert first_tokens["refresh_token"]

    replay_response = client.post(
        "/api/commerce/v1/auth/otp/verify",
        json={
            "challenge_id": requested["challenge_id"],
            "phone": "9876543210",
            "code": "654321",
        },
    )
    assert replay_response.status_code == 401

    me_response = client.get(
        "/api/commerce/v1/auth/me",
        headers={"Authorization": f"Bearer {first_tokens['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["phone_e164"] == "+919876543210"

    refresh_response = client.post(
        "/api/commerce/v1/auth/refresh",
        json={"refresh_token": first_tokens["refresh_token"]},
    )
    assert refresh_response.status_code == 200
    rotated_tokens = refresh_response.json()
    assert rotated_tokens["refresh_token"] != first_tokens["refresh_token"]

    reused_refresh_response = client.post(
        "/api/commerce/v1/auth/refresh",
        json={"refresh_token": first_tokens["refresh_token"]},
    )
    assert reused_refresh_response.status_code == 401

    logout_response = client.post(
        "/api/commerce/v1/auth/logout",
        json={"refresh_token": rotated_tokens["refresh_token"]},
    )
    assert logout_response.status_code == 204

    revoked_response = client.get(
        "/api/commerce/v1/auth/me",
        headers={"Authorization": f"Bearer {rotated_tokens['access_token']}"},
    )
    assert revoked_response.status_code == 401

    with session_factory() as session:
        challenge = session.scalar(select(OtpChallenge))
        stored_session = session.scalar(select(CommerceSession))
        assert challenge is not None and challenge.status == "consumed"
        assert challenge.failed_attempts == 1
        assert stored_session is not None and stored_session.revoked_at is not None
        assert first_tokens["refresh_token"] not in stored_session.refresh_token_hash
        assert rotated_tokens["refresh_token"] not in stored_session.refresh_token_hash


def test_resend_cooldown_returns_retry_after(auth_client) -> None:
    client, _, _ = auth_client
    first = client.post(
        "/api/commerce/v1/auth/otp/request",
        json={"phone": "9876543210"},
    )
    second = client.post(
        "/api/commerce/v1/auth/otp/request",
        json={"phone": "+919876543210"},
    )

    assert first.status_code == 200
    assert second.status_code == 429
    assert int(second.headers["retry-after"]) >= 1


def test_invalid_phone_is_rejected_without_calling_provider(auth_client) -> None:
    client, provider, _ = auth_client
    response = client.post(
        "/api/commerce/v1/auth/otp/request",
        json={"phone": "1234567890"},
    )
    assert response.status_code == 422
    assert provider.requests == []


def test_provider_failure_returns_generic_unavailable(session_factory, auth_settings) -> None:
    application = create_app()

    def override_db() -> Generator[Session, None, None]:
        with session_factory() as session:
            yield session

    application.dependency_overrides[get_commerce_db] = override_db
    application.dependency_overrides[get_auth_settings] = lambda: auth_settings
    application.dependency_overrides[get_otp_provider] = lambda: FailingOtpProvider()

    with TestClient(application) as client:
        response = client.post(
            "/api/commerce/v1/auth/otp/request",
            json={"phone": "9876543210"},
        )

    assert response.status_code == 503
    assert response.json()["error"]["message"] == "Could not send verification code"
    assert response.json()["error"]["code"] == "service_unavailable"


def test_auth_configuration_has_no_insecure_secret_fallback(monkeypatch) -> None:
    monkeypatch.delenv("COMMERCE_JWT_SECRET", raising=False)
    monkeypatch.delenv("COMMERCE_OTP_HASH_SECRET", raising=False)
    with pytest.raises(AuthNotConfigured):
        CommerceAuthSettings.from_env()


def test_auth_configuration_rejects_placeholder_and_reused_secrets(
    monkeypatch,
) -> None:
    monkeypatch.setenv("COMMERCE_JWT_SECRET", "replace_with_a_unique_32_plus_character_secret")
    monkeypatch.setenv("COMMERCE_OTP_HASH_SECRET", "a-real-looking-distinct-secret-value-123456")
    with pytest.raises(AuthNotConfigured):
        CommerceAuthSettings.from_env()

    shared = "a-shared-secret-value-that-is-long-enough-123456"
    monkeypatch.setenv("COMMERCE_JWT_SECRET", shared)
    monkeypatch.setenv("COMMERCE_OTP_HASH_SECRET", shared)
    with pytest.raises(AuthNotConfigured):
        CommerceAuthSettings.from_env()


def test_production_disables_api_docs_by_default(monkeypatch) -> None:
    monkeypatch.setenv("ENV", "production")
    monkeypatch.delenv("COMMERCE_ENABLE_DOCS", raising=False)
    application = create_app()
    with TestClient(application) as client:
        assert client.get("/api/commerce/v1/docs").status_code == 404
        health = client.get("/api/commerce/v1/health")
        assert health.status_code == 200
        assert health.headers["cache-control"] == "no-store"
