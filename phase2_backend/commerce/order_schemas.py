"""Checkout quote and immutable order-ledger API contracts."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SubstitutionPreference = Literal["contact_me", "allow", "do_not_substitute"]


class CheckoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    expected_cart_version: int = Field(ge=1)
    payment_method: Literal["cod"] = "cod"
    substitution_preference: SubstitutionPreference = "contact_me"
    customer_note: str | None = Field(default=None, max_length=500)


class CheckoutLineResponse(BaseModel):
    sku_id: str
    sku_code: str
    product_name: str
    quantity: Decimal
    unit_of_measure: str
    unit_price_paise: int
    tax_rate_basis_points: int
    subtotal_paise: int
    tax_paise: int
    total_paise: int


class CheckoutQuoteResponse(BaseModel):
    cart_id: str
    cart_version: int
    address_id: str
    service_zone_id: str
    currency: str
    payment_method: Literal["cod"]
    subtotal_paise: int
    tax_paise: int
    delivery_fee_paise: int
    discount_paise: int
    total_paise: int
    lines: list[CheckoutLineResponse]
    quoted_at: datetime


class AddressSnapshotResponse(BaseModel):
    label: str
    recipient_name: str
    recipient_phone_e164: str
    line1: str
    line2: str | None = None
    landmark: str | None = None
    locality: str
    district: str
    state: str
    pincode: str


class OrderEventResponse(BaseModel):
    sequence: int
    event_type: str
    payload: dict[str, object]
    occurred_at: datetime


class OrderResponse(BaseModel):
    id: str
    order_number: str
    source_cart_id: str
    status: Literal["confirmed", "processing", "fulfilled", "cancelled"]
    payment_method: Literal["cod"]
    payment_status: Literal["pending", "collected", "failed", "refunded", "voided"]
    substitution_preference: SubstitutionPreference
    customer_note: str | None
    currency: str
    subtotal_paise: int
    tax_paise: int
    delivery_fee_paise: int
    discount_paise: int
    total_paise: int
    address: AddressSnapshotResponse
    items: list[CheckoutLineResponse]
    events: list[OrderEventResponse]
    confirmed_at: datetime
    cancelled_at: datetime | None
    created_at: datetime
    updated_at: datetime


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int
