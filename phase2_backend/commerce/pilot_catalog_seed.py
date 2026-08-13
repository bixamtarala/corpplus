"""Idempotent transactional seeder for review-only pilot catalog candidates."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import (
    Category,
    CategoryTranslation,
    Price,
    PriceList,
    Product,
    ProductTranslation,
    Sku,
)
from .pilot_catalog_data import DRAFT_CATEGORIES, DRAFT_PRODUCTS, DraftProduct


SEED_NAMESPACE = uuid.UUID("1defdcba-f0e6-45f6-9f56-5b20e1f29cb7")
SEED_PRICE_LIST_CODE = "pilot-draft-inr"
SEED_PRICE_SOURCE = "pilot-draft-seed-v1"
SEED_EFFECTIVE_FROM = datetime(2026, 8, 13, tzinfo=timezone.utc)
DRAFT_DESCRIPTION = (
    "Draft pilot catalog candidate. Source, grade, declarations, availability, "
    "serviceability, and final price require operations approval before activation."
)


class SeedCollision(RuntimeError):
    """Raised when a natural key is already owned by a non-seed record."""


@dataclass(frozen=True)
class SeedResult:
    categories: int
    products: int
    skus: int
    prices: int
    applied: bool


def seed_id(kind: str, natural_key: str) -> str:
    return str(uuid.uuid5(SEED_NAMESPACE, f"{kind}:{natural_key}"))


class PilotCatalogSeeder:
    def __init__(self, db: Session) -> None:
        self.db = db

    def seed(self, *, apply: bool) -> SeedResult:
        try:
            categories = self._seed_categories()
            price_list = self._seed_price_list()
            products, skus, prices = self._seed_products(
                categories=categories,
                price_list=price_list,
            )
            self.db.flush()
            result = SeedResult(
                categories=len(categories),
                products=products,
                skus=skus,
                prices=prices,
                applied=apply,
            )
            if apply:
                self.db.commit()
            else:
                self.db.rollback()
            return result
        except Exception:
            self.db.rollback()
            raise

    def _seed_categories(self) -> dict[str, Category]:
        result: dict[str, Category] = {}
        for definition in DRAFT_CATEGORIES:
            expected_id = seed_id("category", definition.slug)
            category = self.db.scalar(select(Category).where(Category.slug == definition.slug))
            if category is None:
                category = Category(
                    id=expected_id,
                    slug=definition.slug,
                    default_name=definition.name,
                    sort_order=definition.sort_order,
                    is_active=False,
                )
                self.db.add(category)
            else:
                self._assert_owned(
                    actual_id=category.id,
                    expected_id=expected_id,
                    record=f"category:{definition.slug}",
                )
                if not category.is_active:
                    category.default_name = definition.name
                    category.sort_order = definition.sort_order

            self.db.flush()
            for locale, name in definition.translations.items():
                self._upsert_category_translation(
                    category_id=category.id,
                    locale=locale,
                    name=name,
                    preserve_existing=category.is_active,
                )
            result[definition.slug] = category
        return result

    def _seed_price_list(self) -> PriceList:
        expected_id = seed_id("price-list", SEED_PRICE_LIST_CODE)
        price_list = self.db.scalar(select(PriceList).where(PriceList.code == SEED_PRICE_LIST_CODE))
        if price_list is None:
            price_list = PriceList(
                id=expected_id,
                code=SEED_PRICE_LIST_CODE,
                name="Pilot draft indicative prices",
                audience="promotional",
                currency="INR",
                is_active=False,
            )
            self.db.add(price_list)
        else:
            self._assert_owned(
                actual_id=price_list.id,
                expected_id=expected_id,
                record=f"price-list:{SEED_PRICE_LIST_CODE}",
            )
            if not price_list.is_active:
                price_list.name = "Pilot draft indicative prices"
                price_list.audience = "promotional"
                price_list.currency = "INR"
        self.db.flush()
        return price_list

    def _seed_products(
        self,
        *,
        categories: dict[str, Category],
        price_list: PriceList,
    ) -> tuple[int, int, int]:
        product_count = 0
        sku_count = 0
        price_count = 0
        for definition in DRAFT_PRODUCTS:
            expected_product_id = seed_id("product", definition.slug)
            product = self.db.scalar(select(Product).where(Product.slug == definition.slug))
            if product is None:
                product = Product(
                    id=expected_product_id,
                    category_id=categories[definition.category_slug].id,
                    slug=definition.slug,
                    default_name=definition.name,
                    description=DRAFT_DESCRIPTION,
                    storage_guidance=None,
                    source_organization_name=None,
                    status="draft",
                    claims_verified_at=None,
                )
                self.db.add(product)
            else:
                self._assert_owned(
                    actual_id=product.id,
                    expected_id=expected_product_id,
                    record=f"product:{definition.slug}",
                )
                if product.status == "draft":
                    product.category_id = categories[definition.category_slug].id
                    product.default_name = definition.name
                    product.description = DRAFT_DESCRIPTION

            self.db.flush()
            for locale, name in definition.translations.items():
                self._upsert_product_translation(
                    product_id=product.id,
                    locale=locale,
                    name=name,
                    preserve_existing=product.status != "draft",
                )
            product_count += 1

            sku = self._upsert_sku(product=product, definition=definition)
            sku_count += 1
            self._upsert_price(
                price_list_id=price_list.id,
                sku_id=sku.id,
                amount_paise=definition.indicative_price_paise,
                preserve_existing=price_list.is_active,
            )
            price_count += 1
        return product_count, sku_count, price_count

    def _upsert_category_translation(
        self,
        *,
        category_id: str,
        locale: str,
        name: str,
        preserve_existing: bool,
    ) -> None:
        expected_id = seed_id("category-translation", f"{category_id}:{locale}")
        translation = self.db.scalar(
            select(CategoryTranslation).where(
                CategoryTranslation.category_id == category_id,
                CategoryTranslation.locale == locale,
            )
        )
        if translation is None:
            translation = CategoryTranslation(
                id=expected_id,
                category_id=category_id,
                locale=locale,
                name=name,
            )
            self.db.add(translation)
        elif translation.id == expected_id and not preserve_existing:
            translation.name = name

    def _upsert_product_translation(
        self,
        *,
        product_id: str,
        locale: str,
        name: str,
        preserve_existing: bool,
    ) -> None:
        expected_id = seed_id("product-translation", f"{product_id}:{locale}")
        translation = self.db.scalar(
            select(ProductTranslation).where(
                ProductTranslation.product_id == product_id,
                ProductTranslation.locale == locale,
            )
        )
        if translation is None:
            translation = ProductTranslation(
                id=expected_id,
                product_id=product_id,
                locale=locale,
                name=name,
                description=DRAFT_DESCRIPTION,
                storage_guidance=None,
            )
            self.db.add(translation)
        elif translation.id == expected_id and not preserve_existing:
            translation.name = name
            if translation.description == DRAFT_DESCRIPTION or not translation.description:
                translation.description = DRAFT_DESCRIPTION

    def _upsert_sku(self, *, product: Product, definition: DraftProduct) -> Sku:
        expected_id = seed_id("sku", definition.sku_code)
        sku = self.db.scalar(select(Sku).where(Sku.code == definition.sku_code))
        if sku is None:
            sku = Sku(
                id=expected_id,
                product_id=product.id,
                code=definition.sku_code,
                pack_quantity=definition.pack_quantity,
                unit_of_measure=definition.unit_of_measure,
                grade=None,
                origin_district=None,
                origin_state=None,
                hsn_code=None,
                tax_rate_basis_points=0,
                minimum_order_quantity=1,
                quantity_step=1,
                status="draft",
            )
            self.db.add(sku)
        else:
            self._assert_owned(
                actual_id=sku.id,
                expected_id=expected_id,
                record=f"sku:{definition.sku_code}",
            )
            if sku.status == "draft":
                sku.product_id = product.id
                sku.pack_quantity = definition.pack_quantity
                sku.unit_of_measure = definition.unit_of_measure
        self.db.flush()
        return sku

    def _upsert_price(
        self,
        *,
        price_list_id: str,
        sku_id: str,
        amount_paise: int,
        preserve_existing: bool,
    ) -> None:
        expected_id = seed_id("price", f"{price_list_id}:{sku_id}:{SEED_PRICE_SOURCE}")
        price = self.db.scalar(
            select(Price).where(
                Price.price_list_id == price_list_id,
                Price.sku_id == sku_id,
                Price.effective_from == SEED_EFFECTIVE_FROM,
            )
        )
        if price is None:
            price = Price(
                id=expected_id,
                price_list_id=price_list_id,
                sku_id=sku_id,
                amount_paise=amount_paise,
                compare_at_paise=None,
                effective_from=SEED_EFFECTIVE_FROM,
                effective_to=None,
                source=SEED_PRICE_SOURCE,
            )
            self.db.add(price)
        else:
            self._assert_owned(
                actual_id=price.id,
                expected_id=expected_id,
                record=f"price:{sku_id}",
            )
            if not preserve_existing:
                price.amount_paise = amount_paise

    @staticmethod
    def _assert_owned(*, actual_id: str, expected_id: str, record: str) -> None:
        if actual_id != expected_id:
            raise SeedCollision(f"Refusing to overwrite non-seed record for {record}")
