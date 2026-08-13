"""Response contracts for the read-only commerce catalog API."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: str
    slug: str
    name: str
    parent_id: str | None
    sort_order: int


class CategoryListResponse(BaseModel):
    items: list[CategoryResponse]


class ProductMediaResponse(BaseModel):
    url: str
    alt_text: str
    is_representative: bool
    sort_order: int


class PriceResponse(BaseModel):
    amount_paise: int
    compare_at_paise: int | None
    currency: str
    effective_from: datetime
    checked_at: datetime


class AvailabilityResponse(BaseModel):
    status: str
    available_quantity: Decimal | None
    checked_at: datetime | None


class SkuResponse(BaseModel):
    id: str
    code: str
    pack_quantity: Decimal
    unit_of_measure: str
    grade: str | None
    origin_district: str | None
    origin_state: str | None
    minimum_order_quantity: Decimal
    quantity_step: Decimal
    price: PriceResponse | None
    availability: AvailabilityResponse
    purchasable: bool


class ProductResponse(BaseModel):
    id: str
    slug: str
    name: str
    description: str | None
    storage_guidance: str | None
    source_organization_name: str | None
    category: CategoryResponse
    media: list[ProductMediaResponse]
    skus: list[SkuResponse]


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    next_cursor: str | None
