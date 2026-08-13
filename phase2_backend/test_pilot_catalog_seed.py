"""Safety and repeatability tests for the review-only pilot catalog seed."""

from __future__ import annotations

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker

from phase2_backend.commerce.catalog_service import CatalogService
from phase2_backend.commerce.models import (
    Base,
    Category,
    Price,
    PriceList,
    Product,
    ProductTranslation,
    Sku,
)
from phase2_backend.commerce.pilot_catalog_data import (
    DRAFT_CATEGORIES,
    DRAFT_PRODUCTS,
)
from phase2_backend.commerce.pilot_catalog_seed import (
    PilotCatalogSeeder,
    SeedCollision,
    seed_id,
)


def _factory():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine, sessionmaker(bind=engine, expire_on_commit=False)


def test_seed_is_idempotent_and_keeps_everything_non_sellable() -> None:
    engine, factory = _factory()
    try:
        with factory() as session:
            first = PilotCatalogSeeder(session).seed(apply=True)
            second = PilotCatalogSeeder(session).seed(apply=True)

            assert first == second
            assert first.categories == len(DRAFT_CATEGORIES)
            assert first.products == len(DRAFT_PRODUCTS)
            assert first.skus == len(DRAFT_PRODUCTS)
            assert first.prices == len(DRAFT_PRODUCTS)
            assert session.scalar(select(func.count(Category.id))) == len(DRAFT_CATEGORIES)
            assert session.scalar(select(func.count(Product.id))) == len(DRAFT_PRODUCTS)
            assert session.scalar(select(func.count(Sku.id))) == len(DRAFT_PRODUCTS)
            assert session.scalar(select(func.count(Price.id))) == len(DRAFT_PRODUCTS)
            assert set(session.scalars(select(Category.is_active))) == {False}
            assert set(session.scalars(select(Product.status))) == {"draft"}
            assert set(session.scalars(select(Sku.status))) == {"draft"}
            assert set(session.scalars(select(PriceList.is_active))) == {False}

            items, next_cursor = CatalogService(session).list_products(
                locale="en",
                category_slug=None,
                query=None,
                limit=50,
                cursor=None,
            )
            assert items == []
            assert next_cursor is None
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_preview_rolls_back_all_changes() -> None:
    engine, factory = _factory()
    try:
        with factory() as session:
            result = PilotCatalogSeeder(session).seed(apply=False)
            assert result.applied is False
            assert session.scalar(select(func.count(Category.id))) == 0
            assert session.scalar(select(func.count(Product.id))) == 0
            assert session.scalar(select(func.count(Price.id))) == 0
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_seed_refuses_natural_key_collision_and_rolls_back() -> None:
    engine, factory = _factory()
    try:
        with factory() as session:
            session.add(
                Category(
                    slug="vegetables",
                    default_name="Existing category",
                    sort_order=1,
                    is_active=True,
                )
            )
            session.commit()

            try:
                PilotCatalogSeeder(session).seed(apply=True)
            except SeedCollision as exc:
                assert "category:vegetables" in str(exc)
            else:
                raise AssertionError("Expected seed collision")

            assert session.scalar(select(func.count(Category.id))) == 1
            assert session.scalar(select(func.count(Product.id))) == 0
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_repeat_seed_preserves_reviewed_active_values() -> None:
    engine, factory = _factory()
    try:
        with factory() as session:
            PilotCatalogSeeder(session).seed(apply=True)
            tomato = session.scalar(select(Product).where(Product.slug == "tomato-1kg"))
            assert tomato is not None
            tomato.status = "active"
            tomato.default_name = "Reviewed tomato"
            translation = session.scalar(
                select(ProductTranslation).where(
                    ProductTranslation.product_id == tomato.id,
                    ProductTranslation.locale == "hi",
                )
            )
            assert translation is not None
            translation.name = "समीक्षित टमाटर"

            sku = session.scalar(select(Sku).where(Sku.code == "PILOT-TOMATO-1KG"))
            assert sku is not None
            sku.status = "active"
            sku.grade = "Reviewed grade"
            session.commit()

            PilotCatalogSeeder(session).seed(apply=True)

            session.refresh(tomato)
            session.refresh(translation)
            session.refresh(sku)
            assert tomato.status == "active"
            assert tomato.default_name == "Reviewed tomato"
            assert translation.name == "समीक्षित टमाटर"
            assert sku.status == "active"
            assert sku.grade == "Reviewed grade"
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_seed_ids_are_stable_and_translations_are_complete() -> None:
    assert seed_id("product", "tomato-1kg") == seed_id("product", "tomato-1kg")
    assert len({seed_id("product", item.slug) for item in DRAFT_PRODUCTS}) == len(DRAFT_PRODUCTS)
    assert all(set(item.translations) == {"hi", "te"} for item in DRAFT_PRODUCTS)
    assert all(set(item.translations) == {"hi", "te"} for item in DRAFT_CATEGORIES)
