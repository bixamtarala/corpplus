"""API contracts for customer addresses and delivery serviceability."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


PINCODE_PATTERN = r"^[1-9][0-9]{5}$"


class ServiceZoneResponse(BaseModel):
    id: str
    code: str
    name: str
    district: str
    state: str
    currency: str
    minimum_order_paise: int
    delivery_fee_paise: int


class ServiceabilityResponse(BaseModel):
    pincode: str
    serviceable: bool
    status: Literal["serviceable", "temporarily_unavailable", "not_serviceable"]
    reason: str
    zone: ServiceZoneResponse | None = None


class AddressFields(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    label: str = Field(default="Home", min_length=1, max_length=40)
    recipient_name: str = Field(min_length=1, max_length=120)
    recipient_phone: str = Field(min_length=10, max_length=24)
    line1: str = Field(min_length=1, max_length=180)
    line2: str | None = Field(default=None, max_length=180)
    landmark: str | None = Field(default=None, max_length=180)
    locality: str = Field(min_length=1, max_length=120)
    district: str = Field(min_length=1, max_length=80)
    state: str = Field(min_length=1, max_length=80)
    pincode: str = Field(pattern=PINCODE_PATTERN)
    latitude: Decimal | None = Field(default=None, ge=Decimal("-90"), le=Decimal("90"))
    longitude: Decimal | None = Field(default=None, ge=Decimal("-180"), le=Decimal("180"))

    @field_validator("line2", "landmark", mode="after")
    @classmethod
    def blank_optional_text_is_none(cls, value: str | None) -> str | None:
        return value or None


class AddressCreateBody(AddressFields):
    make_default: bool = False


class AddressUpdateBody(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    label: str | None = Field(default=None, min_length=1, max_length=40)
    recipient_name: str | None = Field(default=None, min_length=1, max_length=120)
    recipient_phone: str | None = Field(default=None, min_length=10, max_length=24)
    line1: str | None = Field(default=None, min_length=1, max_length=180)
    line2: str | None = Field(default=None, max_length=180)
    landmark: str | None = Field(default=None, max_length=180)
    locality: str | None = Field(default=None, min_length=1, max_length=120)
    district: str | None = Field(default=None, min_length=1, max_length=80)
    state: str | None = Field(default=None, min_length=1, max_length=80)
    pincode: str | None = Field(default=None, pattern=PINCODE_PATTERN)
    latitude: Decimal | None = Field(default=None, ge=Decimal("-90"), le=Decimal("90"))
    longitude: Decimal | None = Field(default=None, ge=Decimal("-180"), le=Decimal("180"))
    make_default: bool | None = None

    @model_validator(mode="after")
    def require_at_least_one_change(self) -> "AddressUpdateBody":
        if not self.model_fields_set:
            raise ValueError("At least one address field is required")
        return self

    @field_validator("line2", "landmark", mode="after")
    @classmethod
    def blank_optional_text_is_none(cls, value: str | None) -> str | None:
        return value or None


class AddressResponse(BaseModel):
    id: str
    label: str
    recipient_name: str
    recipient_phone: str
    line1: str
    line2: str | None
    landmark: str | None
    locality: str
    district: str
    state: str
    pincode: str
    latitude: Decimal | None
    longitude: Decimal | None
    is_default: bool
    created_at: datetime
    updated_at: datetime
    serviceability: ServiceabilityResponse


class AddressListResponse(BaseModel):
    items: list[AddressResponse]
