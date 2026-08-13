"""Contract tests for checkout, inventory reservations, and order history."""

from __future__ import annotations

from collections.abc import Generator
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from fastapi import Header
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from phase2_backend.commerce.api import create_app, get_current_user, get_optional_current_user
from phase2_backend.commerce.database import get_commerce_db
from phase2_backend.commerce.models import (
    Address,
    Base,
    Cart,
    Category,
    CommerceUser,
    InventoryBalance,
    InventoryLocation,
    InventoryReservation,
    Order,
    OrderEvent,
    Price,
    PriceList,
    Product,
    ServiceZone,
    ServiceZonePincode,
    Sku,
)


@pytest.fixture()
def order_client():
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
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with factory() as session:
        seeded = _seed(session)

    application = create_app()

    def override_db() -> Generator[Session, None, None]:
        with factory() as session:
            yield session

    def detached_user() -> CommerceUser:
        with factory() as session:
            user = session.get(CommerceUser, seeded["user_id"])
            assert user is not None
            session.expunge(user)
            return user

    def optional_user(authorization: str | None = Header(default=None)) -> CommerceUser | None:
        return detached_user() if authorization else None

    application.dependency_overrides[get_commerce_db] = override_db
    application.dependency_overrides[get_current_user] = detached_user
    application.dependency_overrides[get_optional_current_user] = optional_user
    with TestClient(application) as client:
        yield client, factory, seeded


def _seed(session: Session) -> dict[str, str]:
    now = datetime.now(timezone.utc)
    user = CommerceUser(phone_e164="+919876540001")
    zone = ServiceZone(
        code="ORDER-ZONE",
        name="Order Zone",
        status="active",
        state="Karnataka",
        district="Bengaluru Urban",
        minimum_order_paise=0,
        delivery_fee_paise=500,
    )
    category = Category(slug="order-vegetables", default_name="Vegetables", is_active=True)
    price_list = PriceList(
        code="consumer-inr",
        name="Consumer INR",
        audience="consumer",
        currency="INR",
        is_active=True,
    )
    session.add_all([user, zone, category, price_list])
    session.flush()
    session.add(ServiceZonePincode(service_zone_id=zone.id, pincode="560001", is_enabled=True))
    address = Address(
        user_id=user.id,
        label="Home",
        recipient_name="Asha Rao",
        recipient_phone_e164=user.phone_e164,
        line1="12 Market Road",
        locality="Central",
        district="Bengaluru Urban",
        state="Karnataka",
        pincode="560001",
        is_default=True,
    )
    product = Product(
        category_id=category.id,
        slug="order-tomato",
        default_name="Tomato",
        status="active",
    )
    location = InventoryLocation(
        service_zone_id=zone.id,
        code="ORDER-HUB",
        name="Order Hub",
        location_type="hub",
        is_active=True,
    )
    session.add_all([address, product, location])
    session.flush()
    sku = Sku(
        product_id=product.id,
        code="ORDER-TOMATO-1KG",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="kg",
        tax_rate_basis_points=500,
        minimum_order_quantity=Decimal("2.000"),
        quantity_step=Decimal("2.000"),
        status="active",
    )
    session.add(sku)
    session.flush()
    price = Price(
        price_list_id=price_list.id,
        sku_id=sku.id,
        amount_paise=5000,
        effective_from=now - timedelta(hours=1),
        source="order-contract-test",
    )
    balance = InventoryBalance(
        inventory_location_id=location.id,
        sku_id=sku.id,
        on_hand_quantity=Decimal("10.000"),
        reserved_quantity=Decimal("0.000"),
        counted_at=now,
    )
    session.add_all([price, balance])
    session.commit()
    return {
        "user_id": user.id,
        "address_id": address.id,
        "sku_id": sku.id,
        "balance_id": balance.id,
    }


def _auth_headers(**extra: str) -> dict[str, str]:
    return {"Authorization": "Bearer contract-test-token", **extra}


def _ready_cart(client: TestClient, seeded: dict[str, str]) -> dict[str, object]:
    cart = client.get("/api/commerce/v1/cart", headers=_auth_headers()).json()
    cart = client.patch(
        "/api/commerce/v1/cart",
        headers=_auth_headers(),
        json={"address_id": seeded["address_id"], "expected_version": cart["version"]},
    ).json()
    return client.post(
        "/api/commerce/v1/cart/items",
        headers=_auth_headers(),
        json={
            "sku_id": seeded["sku_id"],
            "quantity": "2.000",
            "expected_version": cart["version"],
        },
    ).json()


def _checkout_payload(cart: dict[str, object], **overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "expected_cart_version": cart["version"],
        "payment_method": "cod",
        "substitution_preference": "contact_me",
    }
    payload.update(overrides)
    return payload


def test_checkout_quote_is_server_calculated(order_client) -> None:
    client, _, seeded = order_client
    cart = _ready_cart(client, seeded)

    response = client.post(
        "/api/commerce/v1/checkout/quote",
        headers=_auth_headers(),
        json=_checkout_payload(cart),
    )
    assert response.status_code == 200
    quote = response.json()
    assert quote["subtotal_paise"] == 10000
    assert quote["tax_paise"] == 500
    assert quote["delivery_fee_paise"] == 500
    assert quote["discount_paise"] == 0
    assert quote["total_paise"] == 11000
    assert quote["lines"][0]["tax_rate_basis_points"] == 500


def test_order_creation_is_idempotent_and_reserves_inventory(order_client) -> None:
    client, factory, seeded = order_client
    cart = _ready_cart(client, seeded)
    payload = _checkout_payload(cart, customer_note="Call on arrival")
    headers = _auth_headers(**{"Idempotency-Key": "checkout-contract-key-0001"})

    created = client.post("/api/commerce/v1/orders", headers=headers, json=payload)
    replayed = client.post("/api/commerce/v1/orders", headers=headers, json=payload)

    assert created.status_code == 201
    assert replayed.status_code == 201
    body = created.json()
    assert replayed.json()["id"] == body["id"]
    assert body["status"] == "confirmed"
    assert body["payment_status"] == "pending"
    assert body["address"]["pincode"] == "560001"
    assert [event["event_type"] for event in body["events"]] == ["order.confirmed"]
    with factory() as session:
        assert session.scalar(select(func.count(Order.id))) == 1
        cart_model = session.get(Cart, body["source_cart_id"])
        balance = session.get(InventoryBalance, seeded["balance_id"])
        reservation = session.scalar(select(InventoryReservation).where(InventoryReservation.order_id == body["id"]))
        assert cart_model is not None and cart_model.status == "converted"
        assert balance is not None and balance.reserved_quantity == Decimal("2.000")
        assert reservation is not None and reservation.status == "active"


def test_reused_idempotency_key_rejects_different_request(order_client) -> None:
    client, _, seeded = order_client
    cart = _ready_cart(client, seeded)
    headers = _auth_headers(**{"Idempotency-Key": "checkout-contract-key-0002"})
    first = client.post("/api/commerce/v1/orders", headers=headers, json=_checkout_payload(cart))
    assert first.status_code == 201

    conflict = client.post(
        "/api/commerce/v1/orders",
        headers=headers,
        json=_checkout_payload(cart, substitution_preference="do_not_substitute"),
    )
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "conflict"


def test_order_history_detail_and_cancellation_release_inventory(order_client) -> None:
    client, factory, seeded = order_client
    cart = _ready_cart(client, seeded)
    created = client.post(
        "/api/commerce/v1/orders",
        headers=_auth_headers(**{"Idempotency-Key": "checkout-contract-key-0003"}),
        json=_checkout_payload(cart),
    ).json()

    listing = client.get("/api/commerce/v1/orders", headers=_auth_headers())
    detail = client.get(f"/api/commerce/v1/orders/{created['id']}", headers=_auth_headers())
    cancelled = client.post(f"/api/commerce/v1/orders/{created['id']}/cancel", headers=_auth_headers())
    cancelled_again = client.post(f"/api/commerce/v1/orders/{created['id']}/cancel", headers=_auth_headers())

    assert listing.status_code == 200
    assert listing.json()["total"] == 1
    assert detail.status_code == 200
    assert cancelled.status_code == 200
    assert cancelled_again.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert [event["event_type"] for event in cancelled.json()["events"]] == [
        "order.confirmed",
        "order.cancelled",
    ]
    with factory() as session:
        balance = session.get(InventoryBalance, seeded["balance_id"])
        reservations = list(
            session.scalars(select(InventoryReservation).where(InventoryReservation.order_id == created["id"]))
        )
        assert balance is not None and balance.reserved_quantity == Decimal("0.000")
        assert [reservation.status for reservation in reservations] == ["released"]
        assert session.scalar(select(func.count(OrderEvent.id))) == 2


def test_checkout_rejects_stale_or_invalid_cart(order_client) -> None:
    client, _, seeded = order_client
    cart = _ready_cart(client, seeded)

    stale = client.post(
        "/api/commerce/v1/checkout/quote",
        headers=_auth_headers(),
        json=_checkout_payload(cart, expected_cart_version=1),
    )
    assert stale.status_code == 409

    removed = client.delete(
        f"/api/commerce/v1/cart/items/{cart['items'][0]['id']}",
        headers=_auth_headers(),
        params={"expected_version": cart["version"]},
    ).json()
    invalid = client.post(
        "/api/commerce/v1/checkout/quote",
        headers=_auth_headers(),
        json=_checkout_payload(removed),
    )
    assert invalid.status_code == 422
    assert "not ready for checkout" in invalid.json()["error"]["message"]
