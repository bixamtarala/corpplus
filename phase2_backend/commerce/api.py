"""Dedicated versioned API entrypoint for CropPulse commerce."""

from __future__ import annotations

import os
import re
import uuid

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .auth_config import AuthNotConfigured, CommerceAuthSettings
from .auth_service import (
    CommerceAuthService,
    InvalidOtp,
    InvalidPhone,
    InvalidSession,
    OtpRateLimited,
)
from .api_errors import install_api_error_handlers
from .catalog_router import router as catalog_router
from .database import get_commerce_db
from .models import CommerceUser
from .otp_provider import OtpProvider, OtpProviderError, build_otp_provider
from .schemas import (
    AuthReadinessResponse,
    CurrentUserResponse,
    OtpRequestBody,
    OtpRequestResponse,
    OtpVerifyBody,
    RefreshBody,
    ServiceReadinessResponse,
    TokenResponse,
)


API_PREFIX = "/api/commerce/v1"
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{8,64}$")


def get_auth_settings() -> CommerceAuthSettings:
    try:
        return CommerceAuthSettings.from_env()
    except (AuthNotConfigured, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Mobile authentication is not configured",
        ) from exc


def get_otp_provider(
    settings: CommerceAuthSettings = Depends(get_auth_settings),
) -> OtpProvider:
    try:
        return build_otp_provider(expiry_seconds=settings.otp_expiry_seconds)
    except AuthNotConfigured as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Mobile authentication is not configured",
        ) from exc


def get_auth_service(
    db: Session = Depends(get_commerce_db),
    settings: CommerceAuthSettings = Depends(get_auth_settings),
    provider: OtpProvider = Depends(get_otp_provider),
) -> CommerceAuthService:
    return CommerceAuthService(db=db, settings=settings, provider=provider)


def bearer_token(authorization: str = Header(...)) -> str:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Valid bearer token required",
        )
    return token


def get_current_user(
    token: str = Depends(bearer_token),
    service: CommerceAuthService = Depends(get_auth_service),
) -> CommerceUser:
    try:
        return service.authenticate_access_token(token)
    except InvalidSession as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        ) from exc


def create_app() -> FastAPI:
    environment = os.getenv("ENV", "development").strip().lower()
    docs_enabled = (
        environment not in {"production", "prod"} or os.getenv("COMMERCE_ENABLE_DOCS", "false").lower() == "true"
    )
    application = FastAPI(
        title="CropPulse Commerce API",
        version="1.0.0",
        docs_url=f"{API_PREFIX}/docs" if docs_enabled else None,
        openapi_url=f"{API_PREFIX}/openapi.json" if docs_enabled else None,
    )
    install_api_error_handlers(application)
    application.include_router(catalog_router)

    allowed_origins = [
        origin.strip() for origin in os.getenv("COMMERCE_ALLOWED_ORIGINS", "").split(",") if origin.strip()
    ]
    if allowed_origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST"],
            allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
            expose_headers=["X-Request-ID"],
        )

    @application.middleware("http")
    async def security_headers(request: Request, call_next):
        supplied_request_id = request.headers.get("X-Request-ID", "")
        request.state.request_id = (
            supplied_request_id if REQUEST_ID_PATTERN.fullmatch(supplied_request_id) else str(uuid.uuid4())
        )
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Request-ID"] = request.state.request_id
        return response

    @application.get(f"{API_PREFIX}/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "croppulse-commerce"}

    @application.get(f"{API_PREFIX}/readiness", response_model=ServiceReadinessResponse)
    def readiness(db: Session = Depends(get_commerce_db)) -> ServiceReadinessResponse:
        try:
            db.execute(select(1))
            database_status = "ready"
        except SQLAlchemyError:
            database_status = "unavailable"

        try:
            settings = CommerceAuthSettings.from_env()
            build_otp_provider(expiry_seconds=settings.otp_expiry_seconds)
            authentication_status = "configured"
        except (AuthNotConfigured, ValueError):
            authentication_status = "not_configured"

        return ServiceReadinessResponse(
            ready=(database_status == "ready" and authentication_status == "configured"),
            database=database_status,
            authentication=authentication_status,
        )

    @application.get(f"{API_PREFIX}/auth/readiness", response_model=AuthReadinessResponse)
    def auth_readiness() -> AuthReadinessResponse:
        try:
            settings = CommerceAuthSettings.from_env()
            provider = build_otp_provider(expiry_seconds=settings.otp_expiry_seconds)
        except (AuthNotConfigured, ValueError):
            return AuthReadinessResponse(
                ready=False,
                provider=None,
                detail="Mobile authentication is not configured",
            )
        return AuthReadinessResponse(
            ready=True,
            provider=provider.name,
            detail="Mobile authentication is configured",
        )

    @application.post(f"{API_PREFIX}/auth/otp/request", response_model=OtpRequestResponse)
    def request_otp(
        payload: OtpRequestBody,
        request: Request,
        service: CommerceAuthService = Depends(get_auth_service),
    ) -> OtpRequestResponse:
        try:
            result = service.request_otp(
                phone=payload.phone,
                request_ip=request.client.host if request.client else "unknown",
            )
        except InvalidPhone as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except OtpRateLimited as exc:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Please wait before requesting another code",
                headers={"Retry-After": str(exc.retry_after_seconds)},
            ) from exc
        except OtpProviderError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not send verification code",
            ) from exc

        return OtpRequestResponse(
            challenge_id=result.challenge_id,
            phone=result.masked_phone,
            message="If the number can receive SMS, a verification code was sent",
            expires_in_seconds=result.expires_in_seconds,
            resend_after_seconds=result.resend_after_seconds,
        )

    @application.post(f"{API_PREFIX}/auth/otp/verify", response_model=TokenResponse)
    def verify_otp(
        payload: OtpVerifyBody,
        service: CommerceAuthService = Depends(get_auth_service),
    ) -> TokenResponse:
        try:
            tokens = service.verify_otp(
                challenge_id=payload.challenge_id,
                phone=payload.phone,
                code=payload.code,
            )
        except (InvalidPhone, InvalidOtp) as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired verification code",
            ) from exc
        except InvalidSession as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc
        except OtpProviderError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not verify code",
            ) from exc
        return TokenResponse(**tokens.__dict__)

    @application.post(f"{API_PREFIX}/auth/refresh", response_model=TokenResponse)
    def refresh(
        payload: RefreshBody,
        service: CommerceAuthService = Depends(get_auth_service),
    ) -> TokenResponse:
        try:
            tokens = service.refresh(payload.refresh_token)
        except InvalidSession as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session",
            ) from exc
        return TokenResponse(**tokens.__dict__)

    @application.post(f"{API_PREFIX}/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
    def logout(
        payload: RefreshBody,
        service: CommerceAuthService = Depends(get_auth_service),
    ) -> Response:
        service.logout(payload.refresh_token)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @application.get(f"{API_PREFIX}/auth/me", response_model=CurrentUserResponse)
    def me(user: CommerceUser = Depends(get_current_user)) -> CommerceUser:
        return user

    return application


app = create_app()
