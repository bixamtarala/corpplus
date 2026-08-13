"""Server-authoritative pincode and service-zone resolution."""

from __future__ import annotations

import re

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from .address_schemas import ServiceabilityResponse, ServiceZoneResponse
from .models import ServiceZonePincode


class InvalidPincode(ValueError):
    pass


class ServiceabilityConfigurationError(RuntimeError):
    pass


def normalize_pincode(value: str) -> str:
    pincode = value.strip()
    if not re.fullmatch(r"[1-9][0-9]{5}", pincode):
        raise InvalidPincode("Enter a valid 6-digit Indian pincode")
    return pincode


class ServiceabilityService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def check(self, pincode: str) -> ServiceabilityResponse:
        normalized = normalize_pincode(pincode)
        mappings = list(
            self.db.scalars(
                select(ServiceZonePincode)
                .options(joinedload(ServiceZonePincode.service_zone))
                .where(ServiceZonePincode.pincode == normalized)
                .order_by(ServiceZonePincode.created_at, ServiceZonePincode.id)
            )
        )
        active = [mapping for mapping in mappings if mapping.is_enabled and mapping.service_zone.status == "active"]
        if len(active) > 1:
            raise ServiceabilityConfigurationError(f"Pincode {normalized} is assigned to multiple active service zones")
        if active:
            zone = active[0].service_zone
            return ServiceabilityResponse(
                pincode=normalized,
                serviceable=True,
                status="serviceable",
                reason="Delivery is available for this pincode",
                zone=ServiceZoneResponse(
                    id=zone.id,
                    code=zone.code,
                    name=zone.name,
                    district=zone.district,
                    state=zone.state,
                    currency=zone.currency,
                    minimum_order_paise=zone.minimum_order_paise,
                    delivery_fee_paise=zone.delivery_fee_paise,
                ),
            )

        temporarily_unavailable = any(
            mapping.service_zone.status == "paused" or not mapping.is_enabled for mapping in mappings
        )
        if temporarily_unavailable:
            return ServiceabilityResponse(
                pincode=normalized,
                serviceable=False,
                status="temporarily_unavailable",
                reason="Delivery is temporarily unavailable for this pincode",
            )
        return ServiceabilityResponse(
            pincode=normalized,
            serviceable=False,
            status="not_serviceable",
            reason="Delivery is not currently available for this pincode",
        )
