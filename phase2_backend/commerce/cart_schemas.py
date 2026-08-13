"""Request and response contracts for persistent commerce carts."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .address_schemas import PINCODE_PATTERN


class CartIssueResponse(BaseModel):
    code: str
    message: str
    severity: Literal["error", "info"] = "error"
    item_id: str | None = None


class CartItemResponse(BaseModel):
    id: str
    sku_id: str
    sku_code: str
    product_name: str
    quantity: Decimal
    unit_of_measure: str
    minimum_order_quantity: Decimal
    quantity_step: Decimal
    unit_price_paise: int | None
    line_total_paise: int | None
    available_quantity: Decimal | None
    issues: list[CartIssueResponse]


class CartResponse(BaseModel):
    id: str
    owner_type: Literal["guest", "authenticated"]
    guest_token: str | None = None
    status: str
    version: int
    currency: str
    address_id: str | None
    delivery_pincode: str | None
    service_zone_id: str | None
    subtotal_paise: int
    minimum_order_paise: int | None
    delivery_fee_paise: int | None
    total_paise: int | None
    item_count: int
    valid_for_checkout: bool
    validation_status: Literal["valid", "requires_action", "location_required", "empty"]
    issues: list[CartIssueResponse]
    items: list[CartItemResponse]
    validated_at: datetime


class GuestCartCreateBody(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    pincode: str | None = Field(default=None, pattern=PINCODE_PATTERN)


class CartContextBody(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    address_id: str | None = Field(default=None, min_length=36, max_length=36)
    pincode: str | None = Field(default=None, pattern=PINCODE_PATTERN)
    expected_version: int = Field(ge=1)

    @model_validator(mode="after")
    def require_one_location(self) -> "CartContextBody":
        if (self.address_id is None) == (self.pincode is None):
            raise ValueError("Provide exactly one of address_id or pincode")
        return self


class CartItemCreateBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sku_id: str = Field(min_length=36, max_length=36)
    quantity: Decimal = Field(gt=0, max_digits=14, decimal_places=3)
    expected_version: int = Field(ge=1)


class CartItemUpdateBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantity: Decimal = Field(gt=0, max_digits=14, decimal_places=3)
    expected_version: int = Field(ge=1)


class CartMutationBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_version: int = Field(ge=1)


class CartMergeBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_version: int | None = Field(default=None, ge=1)
