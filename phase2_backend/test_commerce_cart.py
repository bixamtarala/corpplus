"""Contract tests for persistent guest and authenticated carts."""

from __future__ import annotations

from collections.abc import Generator
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from fastapi import Header
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, select
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
    Price,
    PriceList,
    Product,
    ServiceZone,
    ServiceZonePincode,
    Sku,
)


@pytest.fixture()
def cart_client():
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
        seeded = _seed_cart_records(session)
        user_id = seeded["user_id"]
        sku_id = seeded["sku_id"]
        address_id = seeded["address_id"]
        inventory_id = seeded["inventory_id"]
        price_id = seeded["price_id"]

    application = create_app()

    def override_db() -> Generator[Session, None, None]:
        with factory() as session:
            yield session

    def detached_user() -> CommerceUser:
        with factory() as session:
            user = session.get(CommerceUser, user_id)
            assert user is not None
            session.expunge(user)
            return user

    def override_optional_user(authorization: str | None = Header(default=None)) -> CommerceUser | None:
        return detached_user() if authorization else None

    application.dependency_overrides[get_commerce_db] = override_db
    application.dependency_overrides[get_optional_current_user] = override_optional_user
    application.dependency_overrides[get_current_user] = detached_user
    try:
        with TestClient(application) as client:
            yield client, factory, sku_id, address_id, inventory_id, price_id
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def _seed_cart_records(session: Session) -> dict[str, str]:
    now = datetime.now(timezone.utc)
    user = CommerceUser(phone_e164="+919876540000")
    zone = ServiceZone(
        code="TEST-ZONE",
        name="Test Zone",
        status="active",
        state="Karnataka",
        district="Bengaluru Urban",
        minimum_order_paise=0,
        delivery_fee_paise=0,
    )
    category = Category(slug="vegetables", default_name="Vegetables", is_active=True)
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
        recipient_phone_e164="+919876540000",
        line1="12 Market Road",
        locality="Central",
        district="Bengaluru Urban",
        state="Karnataka",
        pincode="560001",
        is_default=True,
    )
    product = Product(
        category_id=category.id,
        slug="tomato",
        default_name="Tomato",
        status="active",
    )
    location = InventoryLocation(
        service_zone_id=zone.id,
        code="TEST-HUB",
        name="Test Hub",
        location_type="hub",
        is_active=True,
    )
    session.add_all([address, product, location])
    session.flush()
    sku = Sku(
        product_id=product.id,
        code="TOMATO-1KG",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="kg",
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
        source="contract-test",
    )
    inventory = InventoryBalance(
        inventory_location_id=location.id,
        sku_id=sku.id,
        on_hand_quantity=Decimal("10.000"),
        reserved_quantity=Decimal("0.000"),
        counted_at=now,
    )
    session.add_all([price, inventory])
    session.commit()
    return {
        "user_id": user.id,
        "sku_id": sku.id,
        "address_id": address.id,
        "inventory_id": inventory.id,
        "price_id": price.id,
    }


def _guest_headers(token: str) -> dict[str, str]:
    return {"X-Guest-Cart-Token": token}


def _auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer contract-test-token"}


def test_guest_cart_creation_mutation_and_restoration(cart_client) -> None:
    client, _, sku_id, _, _, _ = cart_client
    created = client.post("/api/commerce/v1/cart/guest", json={"pincode": "560001"})
    assert created.status_code == 201
    body = created.json()
    token = body["guest_token"]
    assert token
    assert body["owner_type"] == "guest"
    assert body["validation_status"] == "empty"

    added = client.post(
        "/api/commerce/v1/cart/items",
        headers=_guest_headers(token),
        json={"sku_id": sku_id, "quantity": "2.000", "expected_version": body["version"]},
    )
    assert added.status_code == 200
    added_body = added.json()
    assert added_body["version"] == 2
    assert added_body["subtotal_paise"] == 10000
    assert added_body["total_paise"] == 10000
    assert added_body["minimum_order_paise"] == 0
    assert added_body["valid_for_checkout"] is True
    assert added_body["items"][0]["available_quantity"] == "10.000"

    restored = client.get("/api/commerce/v1/cart", headers=_guest_headers(token))
    assert restored.status_code == 200
    assert restored.json()["id"] == body["id"]
    assert restored.json()["guest_token"] is None
    assert restored.json()["items"][0]["quantity"] == "2.000"

    invalid_quantity = client.patch(
        f"/api/commerce/v1/cart/items/{added_body['items'][0]['id']}",
        headers=_guest_headers(token),
        json={"quantity": "3.000", "expected_version": added_body["version"]},
    )
    assert invalid_quantity.status_code == 422
    assert invalid_quantity.json()["error"]["code"] == "validation_error"


def test_cart_revalidates_price_inventory_and_version(cart_client) -> None:
    client, factory, sku_id, _, inventory_id, price_id = cart_client
    created = client.post("/api/commerce/v1/cart/guest", json={"pincode": "560001"}).json()
    token = created["guest_token"]
    added = client.post(
        "/api/commerce/v1/cart/items",
        headers=_guest_headers(token),
        json={"sku_id": sku_id, "quantity": "2.000", "expected_version": 1},
    ).json()

    stale = client.post(
        "/api/commerce/v1/cart/items",
        headers=_guest_headers(token),
        json={"sku_id": sku_id, "quantity": "2.000", "expected_version": 1},
    )
    assert stale.status_code == 409

    with factory() as session:
        price = session.get(Price, price_id)
        inventory = session.get(InventoryBalance, inventory_id)
        assert price is not None and inventory is not None
        price.amount_paise = 6000
        inventory.on_hand_quantity = Decimal("1.000")
        session.commit()

    validated = client.post(
        "/api/commerce/v1/cart/validate",
        headers=_guest_headers(token),
        json={"expected_version": added["version"]},
    )
    assert validated.status_code == 200
    validated_body = validated.json()
    assert validated_body["subtotal_paise"] == 12000
    codes = {issue["code"]: issue["severity"] for issue in validated_body["items"][0]["issues"]}
    assert codes == {"price_changed": "info", "insufficient_inventory": "error"}
    assert validated_body["valid_for_checkout"] is False


def test_authenticated_cart_uses_saved_address_and_merges_guest(cart_client) -> None:
    client, factory, sku_id, address_id, _, _ = cart_client
    guest = client.post("/api/commerce/v1/cart/guest", json={"pincode": "560001"}).json()
    token = guest["guest_token"]
    guest_with_item = client.post(
        "/api/commerce/v1/cart/items",
        headers=_guest_headers(token),
        json={"sku_id": sku_id, "quantity": "2.000", "expected_version": 1},
    ).json()
    assert guest_with_item["valid_for_checkout"] is True

    auth_cart = client.get("/api/commerce/v1/cart", headers=_auth_headers())
    assert auth_cart.status_code == 200
    assert auth_cart.json()["owner_type"] == "authenticated"
    assert auth_cart.json()["validation_status"] == "empty"

    located = client.patch(
        "/api/commerce/v1/cart",
        headers=_auth_headers(),
        json={"address_id": address_id, "expected_version": auth_cart.json()["version"]},
    )
    assert located.status_code == 200
    assert located.json()["delivery_pincode"] == "560001"

    auth_item = client.post(
        "/api/commerce/v1/cart/items",
        headers=_auth_headers(),
        json={"sku_id": sku_id, "quantity": "2.000", "expected_version": located.json()["version"]},
    ).json()
    merged = client.post(
        "/api/commerce/v1/cart/merge",
        headers={**_auth_headers(), **_guest_headers(token)},
        json={"expected_version": auth_item["version"]},
    )
    assert merged.status_code == 200
    merged_body = merged.json()
    assert merged_body["items"][0]["quantity"] == "4.000"
    assert merged_body["subtotal_paise"] == 20000
    assert merged_body["valid_for_checkout"] is True

    replayed = client.post(
        "/api/commerce/v1/cart/merge",
        headers={**_auth_headers(), **_guest_headers(token)},
        json={"expected_version": auth_item["version"]},
    )
    assert replayed.status_code == 200
    assert replayed.json()["id"] == merged_body["id"]
    assert replayed.json()["items"][0]["quantity"] == "4.000"

    guest_after_merge = client.get("/api/commerce/v1/cart", headers=_guest_headers(token))
    assert guest_after_merge.status_code == 404
    with factory() as session:
        converted = session.scalar(select(Cart).where(Cart.id == guest["id"]))
        assert converted is not None
        assert converted.status == "converted"


def test_unserviceable_cart_is_restored_but_not_checkout_valid(cart_client) -> None:
    client, _, sku_id, _, _, _ = cart_client
    created = client.post("/api/commerce/v1/cart/guest", json={"pincode": "110001"}).json()
    added = client.post(
        "/api/commerce/v1/cart/items",
        headers=_guest_headers(created["guest_token"]),
        json={"sku_id": sku_id, "quantity": "2.000", "expected_version": created["version"]},
    )
    assert added.status_code == 200
    assert added.json()["validation_status"] == "requires_action"
    assert added.json()["issues"][0]["code"] == "not_serviceable"
    assert added.json()["valid_for_checkout"] is False


def test_deleted_saved_address_invalidates_restored_authenticated_cart(cart_client) -> None:
    client, factory, sku_id, address_id, _, _ = cart_client
    cart = client.get("/api/commerce/v1/cart", headers=_auth_headers()).json()
    cart = client.patch(
        "/api/commerce/v1/cart",
        headers=_auth_headers(),
        json={"address_id": address_id, "expected_version": cart["version"]},
    ).json()
    cart = client.post(
        "/api/commerce/v1/cart/items",
        headers=_auth_headers(),
        json={"sku_id": sku_id, "quantity": "2.000", "expected_version": cart["version"]},
    ).json()
    assert cart["valid_for_checkout"] is True

    with factory() as session:
        address = session.get(Address, address_id)
        assert address is not None
        address.is_active = False
        address.is_default = False
        session.commit()

    restored = client.get("/api/commerce/v1/cart", headers=_auth_headers())
    assert restored.status_code == 200
    assert restored.json()["address_id"] is None
    assert restored.json()["delivery_pincode"] is None
    assert restored.json()["validation_status"] == "location_required"
    assert restored.json()["valid_for_checkout"] is False
