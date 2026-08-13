"""Database configuration for the versioned commerce service."""

from __future__ import annotations

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def commerce_database_url() -> str:
    """Return the configured commerce database URL.

    Production must explicitly provide a PostgreSQL URL. Local development may
    use the documented localhost database so commands remain convenient.
    """

    url = os.getenv("COMMERCE_DATABASE_URL") or os.getenv("DATABASE_URL")
    environment = os.getenv("ENV", "development").strip().lower()

    if not url:
        if environment in {"production", "prod"}:
            raise RuntimeError("COMMERCE_DATABASE_URL or DATABASE_URL is required in production")
        url = "postgresql+psycopg2://postgres:password@localhost:5432/croppulse"

    if url.startswith("postgres://"):
        url = "postgresql+psycopg2://" + url.removeprefix("postgres://")
    elif url.startswith("postgresql://"):
        url = "postgresql+psycopg2://" + url.removeprefix("postgresql://")

    return url


def create_commerce_engine(url: str | None = None) -> Engine:
    database_url = url or commerce_database_url()
    options: dict[str, object] = {
        "pool_pre_ping": True,
        "future": True,
    }

    if database_url.startswith("postgresql"):
        options.update(
            {
                "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
                "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
                "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),
                "connect_args": {
                    "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "10")),
                    "application_name": "croppulse_commerce_api",
                },
            }
        )

    return create_engine(database_url, **options)


engine = create_commerce_engine()
CommerceSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_commerce_db() -> Generator[Session, None, None]:
    """FastAPI dependency that owns one database session per request."""

    session = CommerceSessionLocal()
    try:
        yield session
    finally:
        session.close()
