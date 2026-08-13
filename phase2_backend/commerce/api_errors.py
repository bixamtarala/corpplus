"""Stable error envelopes for the versioned commerce API."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


logger = logging.getLogger("croppulse.commerce.api")


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unavailable")


def _code_for_status(status_code: int) -> str:
    return {
        400: "invalid_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "validation_error",
        429: "rate_limited",
        503: "service_unavailable",
    }.get(status_code, "request_failed")


def error_payload(
    *,
    request: Request,
    status_code: int,
    message: str,
    details: list[dict[str, Any]] | None = None,
) -> dict[str, object]:
    error: dict[str, object] = {
        "code": _code_for_status(status_code),
        "message": message,
        "request_id": _request_id(request),
    }
    if details:
        error["details"] = details
    return {"error": error}


def install_api_error_handlers(application: FastAPI) -> None:
    @application.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return JSONResponse(
            status_code=exc.status_code,
            content=error_payload(
                request=request,
                status_code=exc.status_code,
                message=message,
            ),
            headers=exc.headers,
        )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            {
                "location": [str(part) for part in error["loc"]],
                "message": error["msg"],
                "type": error["type"],
            }
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content=error_payload(
                request=request,
                status_code=422,
                message="Request validation failed",
                details=details,
            ),
        )

    @application.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "Unhandled commerce API error request_id=%s",
            _request_id(request),
            exc_info=exc,
        )
        return JSONResponse(
            status_code=500,
            content=error_payload(
                request=request,
                status_code=500,
                message="Internal server error",
            ),
        )
