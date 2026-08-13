"""Contract tests for addresses and pincode serviceability."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from phase2_backend.commerce.api import create_app, get_current_user
from phase2_backend.commerce.database import get_commerce_db
from phase2_backend.commerce.models import (
    Address,
    Base,
    CommerceUser,
    ServiceZone,
    ServiceZonePincode,
)


@pytest.fixture()
def address_client():
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
        user = CommerceUser(phone_e164="+919876543210")
        other_user = CommerceUser(phone_e164="+919876543211")
        active = ServiceZone(
            code="BLR-CENTRAL",
            name="Bengaluru Central",
            status="active",
            state="Karnataka",
            district="Bengaluru Urban",
            minimum_order_paise=20000,
            delivery_fee_paise=4000,
        )
        paused = ServiceZone(
            code="BLR-NORTH",
            name="Bengaluru North",
            status="paused",
            state="Karnataka",
            district="Bengaluru Urban",
        )
        session.add_all([user, other_user, active, paused])
        session.flush()
        session.add_all(
            [
                ServiceZonePincode(service_zone_id=active.id, pincode="560001", is_enabled=True),
                ServiceZonePincode(service_zone_id=paused.id, pincode="560002", is_enabled=True),
                ServiceZonePincode(service_zone_id=active.id, pincode="560003", is_enabled=False),
            ]
        )
        session.commit()
        user_id = user.id
        other_user_id = other_user.id

    application = create_app()

    def override_db() -> Generator[Session, None, None]:
        with factory() as session:
            yield session

    def override_current_user() -> CommerceUser:
        with factory() as session:
            user = session.get(CommerceUser, user_id)
            assert user is not None
            session.expunge(user)
            return user

    application.dependency_overrides[get_commerce_db] = override_db
    application.dependency_overrides[get_current_user] = override_current_user
    try:
        with TestClient(application) as client:
            yield client, factory, user_id, other_user_id
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def _address_payload(*, label: str, pincode: str = "560001") -> dict[str, object]:
    return {
        "label": label,
        "recipient_name": "Asha Rao",
        "recipient_phone": "98765 43210",
        "line1": "12 Market Road",
        "line2": "",
        "landmark": "Near the mandi",
        "locality": "Central",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": pincode,
        "latitude": "12.971600",
        "longitude": "77.594600",
    }


def test_serviceability_has_clear_supported_paused_and_unsupported_responses(address_client) -> None:
    client, _, _, _ = address_client

    supported = client.get("/api/commerce/v1/serviceability", params={"pincode": "560001"})
    assert supported.status_code == 200
    assert supported.json() == {
        "pincode": "560001",
        "serviceable": True,
        "status": "serviceable",
        "reason": "Delivery is available for this pincode",
        "zone": {
            "id": supported.json()["zone"]["id"],
            "code": "BLR-CENTRAL",
            "name": "Bengaluru Central",
            "district": "Bengaluru Urban",
            "state": "Karnataka",
            "currency": "INR",
            "minimum_order_paise": 20000,
            "delivery_fee_paise": 4000,
        },
    }

    paused = client.get("/api/commerce/v1/serviceability", params={"pincode": "560002"})
    assert paused.json()["status"] == "temporarily_unavailable"
    assert paused.json()["serviceable"] is False
    assert paused.json()["zone"] is None

    unsupported = client.get("/api/commerce/v1/serviceability", params={"pincode": "110001"})
    assert unsupported.json()["status"] == "not_serviceable"
    assert unsupported.json()["serviceable"] is False

    invalid = client.get("/api/commerce/v1/serviceability", params={"pincode": "012345"})
    assert invalid.status_code == 422
    assert invalid.json()["error"]["code"] == "validation_error"


def test_address_crud_default_promotion_and_serviceability(address_client) -> None:
    client, factory, user_id, _ = address_client

    first = client.post("/api/commerce/v1/addresses", json=_address_payload(label="Home"))
    assert first.status_code == 201
    first_body = first.json()
    assert first_body["is_default"] is True
    assert first_body["recipient_phone"] == "+919876543210"
    assert first_body["line2"] is None
    assert first_body["serviceability"]["status"] == "serviceable"

    second = client.post(
        "/api/commerce/v1/addresses",
        json=_address_payload(label="Farm", pincode="110001"),
    )
    assert second.status_code == 201
    second_body = second.json()
    assert second_body["is_default"] is False
    assert second_body["serviceability"]["status"] == "not_serviceable"

    made_default = client.post(f"/api/commerce/v1/addresses/{second_body['id']}/default")
    assert made_default.status_code == 200
    assert made_default.json()["is_default"] is True

    edited = client.patch(
        f"/api/commerce/v1/addresses/{second_body['id']}",
        json={"label": "Warehouse", "pincode": "560002"},
    )
    assert edited.status_code == 200
    assert edited.json()["label"] == "Warehouse"
    assert edited.json()["serviceability"]["status"] == "temporarily_unavailable"

    deleted = client.delete(f"/api/commerce/v1/addresses/{second_body['id']}")
    assert deleted.status_code == 204
    listed = client.get("/api/commerce/v1/addresses")
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()["items"]] == [first_body["id"]]
    assert listed.json()["items"][0]["is_default"] is True

    with factory() as session:
        stored = session.get(Address, second_body["id"])
        assert stored is not None
        assert stored.user_id == user_id
        assert stored.is_active is False


def test_address_ownership_is_not_disclosed(address_client) -> None:
    client, factory, _, other_user_id = address_client
    with factory() as session:
        other_address = Address(
            user_id=other_user_id,
            label="Other",
            recipient_name="Other User",
            recipient_phone_e164="+919876543211",
            line1="Private address",
            locality="Private",
            district="Bengaluru Urban",
            state="Karnataka",
            pincode="560001",
            is_default=True,
        )
        session.add(other_address)
        session.commit()
        address_id = other_address.id

    updated = client.patch(f"/api/commerce/v1/addresses/{address_id}", json={"label": "Stolen"})
    deleted = client.delete(f"/api/commerce/v1/addresses/{address_id}")
    made_default = client.post(f"/api/commerce/v1/addresses/{address_id}/default")
    assert updated.status_code == deleted.status_code == made_default.status_code == 404


def test_conflicting_active_zone_assignments_fail_closed(address_client) -> None:
    client, factory, _, _ = address_client
    with factory() as session:
        duplicate = ServiceZone(
            code="BLR-OVERLAP",
            name="Overlapping zone",
            status="active",
            state="Karnataka",
            district="Bengaluru Urban",
        )
        session.add(duplicate)
        session.flush()
        session.add(ServiceZonePincode(service_zone_id=duplicate.id, pincode="560001", is_enabled=True))
        session.commit()

    response = client.get("/api/commerce/v1/serviceability", params={"pincode": "560001"})
    assert response.status_code == 503
    assert response.json()["error"]["message"] == "Serviceability is temporarily unavailable"
