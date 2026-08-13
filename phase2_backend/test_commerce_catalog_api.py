"""Contract tests for the versioned read-only commerce catalog API."""

from __future__ import annotations

from collections.abc import Generator
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from phase2_backend.commerce.api import create_app
from phase2_backend.commerce.database import get_commerce_db
from phase2_backend.commerce.models import (
    Base,
    Category,
    CategoryTranslation,
    Price,
    PriceList,
    Product,
    ProductMedia,
    ProductTranslation,
    Sku,
)


@pytest.fixture()
def catalog_client():
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
    _seed_contract_records(factory)
    application = create_app()

    def override_db() -> Generator[Session, None, None]:
        with factory() as session:
            yield session

    application.dependency_overrides[get_commerce_db] = override_db
    try:
        with TestClient(application) as client:
            yield client
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def _seed_contract_records(factory) -> None:
    now = datetime.now(timezone.utc)
    with factory() as session:
        vegetables = Category(
            slug="vegetables",
            default_name="Vegetables",
            sort_order=1,
            is_active=True,
        )
        hidden_category = Category(
            slug="hidden",
            default_name="Hidden",
            sort_order=99,
            is_active=False,
        )
        session.add_all([vegetables, hidden_category])
        session.flush()
        session.add(
            CategoryTranslation(
                category_id=vegetables.id,
                locale="hi",
                name="सब्जियां",
            )
        )

        tomato = Product(
            category_id=vegetables.id,
            slug="tomato",
            default_name="Tomato",
            description="Approved contract-test tomato",
            storage_guidance="Keep cool",
            source_organization_name="Test FPO",
            status="active",
        )
        onion = Product(
            category_id=vegetables.id,
            slug="onion",
            default_name="Onion",
            status="active",
        )
        draft = Product(
            category_id=vegetables.id,
            slug="draft-potato",
            default_name="Draft potato",
            status="draft",
        )
        hidden = Product(
            category_id=hidden_category.id,
            slug="hidden-product",
            default_name="Hidden product",
            status="active",
        )
        session.add_all([tomato, onion, draft, hidden])
        session.flush()
        session.add(
            ProductTranslation(
                product_id=tomato.id,
                locale="hi",
                name="टमाटर",
                description="स्वीकृत परीक्षण टमाटर",
                storage_guidance="ठंडा रखें",
            )
        )
        session.add(
            ProductMedia(
                product_id=tomato.id,
                media_type="image",
                url="https://cdn.example.test/tomato.jpg",
                alt_text="Tomatoes",
                is_representative=True,
                sort_order=0,
            )
        )

        tomato_sku = Sku(
            product_id=tomato.id,
            code="TOMATO-A-1KG",
            pack_quantity=Decimal("1.000"),
            unit_of_measure="kg",
            grade="Grade A",
            origin_district="Test District",
            origin_state="Test State",
            minimum_order_quantity=Decimal("1.000"),
            quantity_step=Decimal("1.000"),
            status="active",
        )
        onion_sku = Sku(
            product_id=onion.id,
            code="ONION-1KG",
            pack_quantity=Decimal("1.000"),
            unit_of_measure="kg",
            minimum_order_quantity=Decimal("1.000"),
            quantity_step=Decimal("1.000"),
            status="active",
        )
        draft_sku = Sku(
            product_id=draft.id,
            code="DRAFT-POTATO-1KG",
            pack_quantity=Decimal("1.000"),
            unit_of_measure="kg",
            minimum_order_quantity=Decimal("1.000"),
            quantity_step=Decimal("1.000"),
            status="active",
        )
        hidden_sku = Sku(
            product_id=hidden.id,
            code="HIDDEN-1KG",
            pack_quantity=Decimal("1.000"),
            unit_of_measure="kg",
            minimum_order_quantity=Decimal("1.000"),
            quantity_step=Decimal("1.000"),
            status="active",
        )
        session.add_all([tomato_sku, onion_sku, draft_sku, hidden_sku])
        session.flush()

        consumer_prices = PriceList(
            code="consumer-inr",
            name="Consumer INR",
            audience="consumer",
            currency="INR",
            is_active=True,
        )
        session.add(consumer_prices)
        session.flush()
        session.add_all(
            [
                Price(
                    price_list_id=consumer_prices.id,
                    sku_id=tomato_sku.id,
                    amount_paise=4200,
                    compare_at_paise=5000,
                    effective_from=now - timedelta(days=1),
                    source="contract-test",
                ),
                Price(
                    price_list_id=consumer_prices.id,
                    sku_id=tomato_sku.id,
                    amount_paise=9999,
                    effective_from=now + timedelta(days=1),
                    source="future-contract-test",
                ),
            ]
        )
        session.commit()


def test_categories_are_active_sorted_and_localized(catalog_client) -> None:
    response = catalog_client.get(
        "/api/commerce/v1/catalog/categories?locale=hi",
    )
    assert response.status_code == 200
    assert response.json()["items"] == [
        {
            "id": response.json()["items"][0]["id"],
            "slug": "vegetables",
            "name": "सब्जियां",
            "parent_id": None,
            "sort_order": 1,
        }
    ]


def test_product_list_uses_cursor_and_excludes_non_sellable_records(
    catalog_client,
) -> None:
    first = catalog_client.get("/api/commerce/v1/catalog/products?category=vegetables&limit=1")
    assert first.status_code == 200
    first_body = first.json()
    assert len(first_body["items"]) == 1
    assert first_body["next_cursor"]

    second = catalog_client.get(
        "/api/commerce/v1/catalog/products",
        params={
            "category": "vegetables",
            "limit": 1,
            "cursor": first_body["next_cursor"],
        },
    )
    assert second.status_code == 200
    returned_slugs = {
        first_body["items"][0]["slug"],
        second.json()["items"][0]["slug"],
    }
    assert returned_slugs == {"tomato", "onion"}
    assert second.json()["next_cursor"] is None


def test_search_and_detail_return_localized_product_and_current_price(
    catalog_client,
) -> None:
    search = catalog_client.get(
        "/api/commerce/v1/catalog/products",
        params={"locale": "hi", "query": "टमाटर"},
    )
    assert search.status_code == 200
    assert [item["slug"] for item in search.json()["items"]] == ["tomato"]

    detail = catalog_client.get("/api/commerce/v1/catalog/products/tomato?locale=hi")
    assert detail.status_code == 200
    body = detail.json()
    assert body["name"] == "टमाटर"
    assert body["category"]["name"] == "सब्जियां"
    assert body["media"][0]["url"].endswith("tomato.jpg")
    assert body["skus"][0]["price"]["amount_paise"] == 4200
    assert body["skus"][0]["price"]["compare_at_paise"] == 5000
    assert body["skus"][0]["availability"]["status"] == "location_required"
    assert body["skus"][0]["purchasable"] is False


def test_catalog_not_found_and_validation_use_stable_error_envelope(
    catalog_client,
) -> None:
    request_id = "catalog-contract-test-123"
    missing = catalog_client.get(
        "/api/commerce/v1/catalog/products/draft-potato",
        headers={"X-Request-ID": request_id},
    )
    assert missing.status_code == 404
    assert missing.headers["x-request-id"] == request_id
    assert missing.json() == {
        "error": {
            "code": "not_found",
            "message": "Product not found",
            "request_id": request_id,
        }
    }

    invalid = catalog_client.get(
        "/api/commerce/v1/catalog/products?limit=0",
        headers={"X-Request-ID": request_id},
    )
    assert invalid.status_code == 422
    assert invalid.json()["error"]["code"] == "validation_error"
    assert invalid.json()["error"]["request_id"] == request_id
    assert invalid.json()["error"]["details"][0]["location"] == [
        "query",
        "limit",
    ]


def test_invalid_cursor_is_rejected(catalog_client) -> None:
    response = catalog_client.get("/api/commerce/v1/catalog/products?cursor=not-a-valid-cursor")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_request"


def test_hidden_category_and_blank_search_are_not_exposed(catalog_client) -> None:
    hidden = catalog_client.get("/api/commerce/v1/catalog/products/hidden-product")
    assert hidden.status_code == 404

    blank = catalog_client.get(
        "/api/commerce/v1/catalog/products",
        params={"query": "   "},
    )
    assert blank.status_code == 400
    assert blank.json()["error"]["message"] == "Search query cannot be blank"


def test_readiness_separates_database_and_authentication(catalog_client) -> None:
    response = catalog_client.get("/api/commerce/v1/readiness")
    assert response.status_code == 200
    assert response.json() == {
        "ready": False,
        "database": "ready",
        "authentication": "not_configured",
    }
