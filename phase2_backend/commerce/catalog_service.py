"""Database-backed read model for categories and active catalog products."""

from __future__ import annotations

import base64
import os
import uuid
from collections import defaultdict
from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, aliased

from .catalog_schemas import (
    AvailabilityResponse,
    CategoryResponse,
    PriceResponse,
    ProductMediaResponse,
    ProductResponse,
    SkuResponse,
)
from .models import (
    Category,
    CategoryTranslation,
    Price,
    PriceList,
    Product,
    ProductMedia,
    ProductTranslation,
    Sku,
)


class InvalidCatalogCursor(ValueError):
    pass


class CatalogProductNotFound(LookupError):
    pass


class CatalogService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.consumer_price_list_code = os.getenv("COMMERCE_CONSUMER_PRICE_LIST_CODE", "consumer-inr")

    def list_categories(self, *, locale: str) -> list[CategoryResponse]:
        translation = aliased(CategoryTranslation)
        rows = self.db.execute(
            select(Category, translation.name)
            .outerjoin(
                translation,
                (translation.category_id == Category.id) & (translation.locale == locale),
            )
            .where(Category.is_active.is_(True))
            .order_by(Category.sort_order, Category.default_name, Category.id)
        ).all()
        return [
            CategoryResponse(
                id=category.id,
                slug=category.slug,
                name=translated_name or category.default_name,
                parent_id=category.parent_id,
                sort_order=category.sort_order,
            )
            for category, translated_name in rows
        ]

    def list_products(
        self,
        *,
        locale: str,
        category_slug: str | None,
        query: str | None,
        limit: int,
        cursor: str | None,
    ) -> tuple[list[ProductResponse], str | None]:
        translation = aliased(ProductTranslation)
        statement = (
            select(Product.id)
            .join(Category, Category.id == Product.category_id)
            .join(Sku, Sku.product_id == Product.id)
            .outerjoin(
                translation,
                (translation.product_id == Product.id) & (translation.locale == locale),
            )
            .where(
                Product.status == "active",
                Category.is_active.is_(True),
                Sku.status == "active",
            )
            .distinct()
            .order_by(Product.id)
        )
        if category_slug:
            statement = statement.where(Category.slug == category_slug)
        if query:
            normalized = query.strip().lower()
            pattern = f"%{self._escape_like(normalized)}%"
            statement = statement.where(
                or_(
                    Product.default_name.ilike(pattern, escape="\\"),
                    translation.name.ilike(pattern, escape="\\"),
                )
            )
        if cursor:
            statement = statement.where(Product.id > self._decode_cursor(cursor))

        ids = list(self.db.scalars(statement.limit(limit + 1)).all())
        has_more = len(ids) > limit
        page_ids = ids[:limit]
        products = self._load_products(product_ids=page_ids, locale=locale)
        next_cursor = self._encode_cursor(page_ids[-1]) if has_more and page_ids else None
        return products, next_cursor

    def get_product(self, *, slug: str, locale: str) -> ProductResponse:
        product_id = self.db.scalar(
            select(Product.id)
            .join(Category, Category.id == Product.category_id)
            .join(Sku, Sku.product_id == Product.id)
            .where(
                Product.slug == slug,
                Product.status == "active",
                Category.is_active.is_(True),
                Sku.status == "active",
            )
            .limit(1)
        )
        if product_id is None:
            raise CatalogProductNotFound(slug)
        products = self._load_products(product_ids=[product_id], locale=locale)
        if not products:
            raise CatalogProductNotFound(slug)
        return products[0]

    def _load_products(self, *, product_ids: list[str], locale: str) -> list[ProductResponse]:
        if not product_ids:
            return []

        product_translation = aliased(ProductTranslation)
        category_translation = aliased(CategoryTranslation)
        rows = self.db.execute(
            select(
                Product,
                Category,
                product_translation.name,
                product_translation.description,
                product_translation.storage_guidance,
                category_translation.name,
            )
            .join(Category, Category.id == Product.category_id)
            .outerjoin(
                product_translation,
                (product_translation.product_id == Product.id) & (product_translation.locale == locale),
            )
            .outerjoin(
                category_translation,
                (category_translation.category_id == Category.id) & (category_translation.locale == locale),
            )
            .where(Product.id.in_(product_ids))
        ).all()
        row_by_id = {row[0].id: row for row in rows}

        media_by_product: dict[str, list[ProductMediaResponse]] = defaultdict(list)
        media_rows = self.db.scalars(
            select(ProductMedia)
            .where(ProductMedia.product_id.in_(product_ids))
            .order_by(ProductMedia.product_id, ProductMedia.sort_order, ProductMedia.id)
        ).all()
        for media in media_rows:
            media_by_product[media.product_id].append(
                ProductMediaResponse(
                    url=media.url,
                    alt_text=media.alt_text,
                    is_representative=media.is_representative,
                    sort_order=media.sort_order,
                )
            )

        sku_rows = list(
            self.db.scalars(
                select(Sku)
                .where(Sku.product_id.in_(product_ids), Sku.status == "active")
                .order_by(Sku.product_id, Sku.code, Sku.id)
            ).all()
        )
        prices_by_sku = self._current_prices([sku.id for sku in sku_rows])
        skus_by_product: dict[str, list[SkuResponse]] = defaultdict(list)
        checked_at = datetime.now(timezone.utc)
        for sku in sku_rows:
            current_price = prices_by_sku.get(sku.id)
            price_response = (
                PriceResponse(
                    amount_paise=current_price[0].amount_paise,
                    compare_at_paise=current_price[0].compare_at_paise,
                    currency=current_price[1],
                    effective_from=current_price[0].effective_from,
                    checked_at=checked_at,
                )
                if current_price is not None
                else None
            )
            skus_by_product[sku.product_id].append(
                SkuResponse(
                    id=sku.id,
                    code=sku.code,
                    pack_quantity=sku.pack_quantity,
                    unit_of_measure=sku.unit_of_measure,
                    grade=sku.grade,
                    origin_district=sku.origin_district,
                    origin_state=sku.origin_state,
                    minimum_order_quantity=sku.minimum_order_quantity,
                    quantity_step=sku.quantity_step,
                    price=price_response,
                    availability=AvailabilityResponse(
                        status="location_required",
                        available_quantity=None,
                        checked_at=None,
                    ),
                    purchasable=False,
                )
            )

        results: list[ProductResponse] = []
        for product_id in product_ids:
            row = row_by_id.get(product_id)
            product_skus = skus_by_product.get(product_id, [])
            if row is None or not product_skus:
                continue
            product, category, name, description, storage, category_name = row
            results.append(
                ProductResponse(
                    id=product.id,
                    slug=product.slug,
                    name=name or product.default_name,
                    description=description or product.description,
                    storage_guidance=storage or product.storage_guidance,
                    source_organization_name=product.source_organization_name,
                    category=CategoryResponse(
                        id=category.id,
                        slug=category.slug,
                        name=category_name or category.default_name,
                        parent_id=category.parent_id,
                        sort_order=category.sort_order,
                    ),
                    media=media_by_product.get(product.id, []),
                    skus=product_skus,
                )
            )
        return results

    def _current_prices(self, sku_ids: list[str]) -> dict[str, tuple[Price, str]]:
        if not sku_ids:
            return {}
        now = datetime.now(timezone.utc)
        rows = self.db.execute(
            select(Price, PriceList.currency)
            .join(PriceList, PriceList.id == Price.price_list_id)
            .where(
                Price.sku_id.in_(sku_ids),
                PriceList.code == self.consumer_price_list_code,
                PriceList.is_active.is_(True),
                Price.effective_from <= now,
                or_(Price.effective_to.is_(None), Price.effective_to > now),
            )
            .order_by(Price.sku_id, Price.effective_from.desc(), Price.id.desc())
        ).all()
        current: dict[str, tuple[Price, str]] = {}
        for price, currency in rows:
            current.setdefault(price.sku_id, (price, currency))
        return current

    @staticmethod
    def _escape_like(value: str) -> str:
        return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

    @staticmethod
    def _encode_cursor(product_id: str) -> str:
        return base64.urlsafe_b64encode(product_id.encode("utf-8")).decode("ascii").rstrip("=")

    @staticmethod
    def _decode_cursor(cursor: str) -> str:
        try:
            padding = "=" * (-len(cursor) % 4)
            product_id = base64.b64decode(cursor + padding, altchars=b"-_", validate=True).decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise InvalidCatalogCursor("Invalid catalog cursor") from exc
        if len(product_id) != 36:
            raise InvalidCatalogCursor("Invalid catalog cursor")
        try:
            uuid.UUID(product_id)
        except ValueError as exc:
            raise InvalidCatalogCursor("Invalid catalog cursor") from exc
        return product_id
