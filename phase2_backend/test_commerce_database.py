"""Focused database tests for the isolated commerce foundation."""

from __future__ import annotations

from decimal import Decimal

import pytest
from sqlalchemy import create_engine, event, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from phase2_backend.commerce.database import commerce_database_url
from phase2_backend.commerce.models import Base, Cart, CartItem, CommerceUser


EXPECTED_TABLES = {
    "commerce_addresses",
    "commerce_audit_events",
    "commerce_cart_items",
    "commerce_carts",
    "commerce_categories",
    "commerce_category_translations",
    "commerce_inventory_balances",
    "commerce_inventory_locations",
    "commerce_prices",
    "commerce_price_lists",
    "commerce_product_media",
    "commerce_product_translations",
    "commerce_products",
    "commerce_service_zone_pincodes",
    "commerce_service_zones",
    "commerce_sessions",
    "commerce_skus",
    "commerce_users",
}


@pytest.fixture()
def sqlite_engine():
    engine = create_engine("sqlite+pysqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_commerce_metadata_creates_expected_isolated_tables(sqlite_engine) -> None:
    assert set(inspect(sqlite_engine).get_table_names()) == EXPECTED_TABLES
    assert all(name.startswith("commerce_") for name in EXPECTED_TABLES)


def test_cart_requires_exactly_one_owner(sqlite_engine) -> None:
    with Session(sqlite_engine) as session:
        no_owner = Cart()
        session.add(no_owner)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

        user = CommerceUser(phone_e164="+919999999999")
        session.add(user)
        session.flush()

        two_owners = Cart(user_id=user.id, guest_token_hash="hashed-guest-token")
        session.add(two_owners)
        with pytest.raises(IntegrityError):
            session.commit()


def test_cart_rejects_non_positive_item_quantity(sqlite_engine) -> None:
    # Foreign keys are intentionally populated with missing IDs here; the cart
    # quantity check is evaluated first and proves invalid client quantities
    # cannot be persisted.
    with Session(sqlite_engine) as session:
        cart = Cart(guest_token_hash="hashed-guest-token")
        session.add(cart)
        session.flush()

        session.add(
            CartItem(
                cart_id=cart.id,
                sku_id="missing-sku",
                quantity=Decimal("0.000"),
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()


def test_production_database_url_is_required(monkeypatch) -> None:
    monkeypatch.setenv("ENV", "production")
    monkeypatch.delenv("COMMERCE_DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="required in production"):
        commerce_database_url()


def test_legacy_postgres_url_is_normalized(monkeypatch) -> None:
    monkeypatch.setenv("COMMERCE_DATABASE_URL", "postgres://user:pass@db/app")
    assert commerce_database_url() == "postgresql+psycopg2://user:pass@db/app"
