"""Authenticated address CRUD and public serviceability routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from sqlalchemy.orm import Session

from .address_schemas import (
    AddressCreateBody,
    AddressListResponse,
    AddressResponse,
    AddressUpdateBody,
    ServiceabilityResponse,
)
from .address_service import AddressNotFound, AddressService
from .api import get_current_user
from .auth_service import InvalidPhone
from .database import get_commerce_db
from .models import Address, CommerceUser
from .serviceability_service import (
    InvalidPincode,
    ServiceabilityConfigurationError,
    ServiceabilityService,
)


router = APIRouter(prefix="/api/commerce/v1", tags=["addresses"])


def get_address_service(db: Session = Depends(get_commerce_db)) -> AddressService:
    return AddressService(db)


def get_serviceability_service(db: Session = Depends(get_commerce_db)) -> ServiceabilityService:
    return ServiceabilityService(db)


def _check(service: ServiceabilityService, pincode: str) -> ServiceabilityResponse:
    try:
        return service.check(pincode)
    except InvalidPincode as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ServiceabilityConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviceability is temporarily unavailable",
        ) from exc


def _check_for_address(service: ServiceabilityService, pincode: str) -> ServiceabilityResponse:
    try:
        return service.check(pincode)
    except ServiceabilityConfigurationError:
        # Saving an address must not claim coverage, but an operations mapping
        # conflict should not make an otherwise valid address unusable.
        return ServiceabilityResponse(
            pincode=pincode,
            serviceable=False,
            status="temporarily_unavailable",
            reason="Delivery confirmation is temporarily unavailable for this pincode",
        )


def _response(
    address: Address,
    service: ServiceabilityService,
    serviceability: ServiceabilityResponse | None = None,
) -> AddressResponse:
    return AddressResponse(
        id=address.id,
        label=address.label,
        recipient_name=address.recipient_name,
        recipient_phone=address.recipient_phone_e164,
        line1=address.line1,
        line2=address.line2,
        landmark=address.landmark,
        locality=address.locality,
        district=address.district,
        state=address.state,
        pincode=address.pincode,
        latitude=address.latitude,
        longitude=address.longitude,
        is_default=address.is_default,
        created_at=address.created_at,
        updated_at=address.updated_at,
        serviceability=serviceability or _check_for_address(service, address.pincode),
    )


@router.get("/serviceability", response_model=ServiceabilityResponse, tags=["serviceability"])
def check_serviceability(
    pincode: Annotated[str, Query(min_length=6, max_length=6)],
    service: ServiceabilityService = Depends(get_serviceability_service),
) -> ServiceabilityResponse:
    return _check(service, pincode)


@router.get("/addresses", response_model=AddressListResponse)
def list_addresses(
    user: CommerceUser = Depends(get_current_user),
    addresses: AddressService = Depends(get_address_service),
    serviceability: ServiceabilityService = Depends(get_serviceability_service),
) -> AddressListResponse:
    cache: dict[str, ServiceabilityResponse] = {}
    items = []
    for address in addresses.list(user.id):
        if address.pincode not in cache:
            cache[address.pincode] = _check_for_address(serviceability, address.pincode)
        items.append(_response(address, serviceability, cache[address.pincode]))
    return AddressListResponse(items=items)


@router.post("/addresses", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(
    payload: AddressCreateBody,
    user: CommerceUser = Depends(get_current_user),
    addresses: AddressService = Depends(get_address_service),
    serviceability: ServiceabilityService = Depends(get_serviceability_service),
) -> AddressResponse:
    try:
        address = addresses.create(user.id, payload)
    except InvalidPhone as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _response(address, serviceability)


@router.patch("/addresses/{address_id}", response_model=AddressResponse)
def update_address(
    payload: AddressUpdateBody,
    address_id: Annotated[str, Path(min_length=36, max_length=36)],
    user: CommerceUser = Depends(get_current_user),
    addresses: AddressService = Depends(get_address_service),
    serviceability: ServiceabilityService = Depends(get_serviceability_service),
) -> AddressResponse:
    try:
        address = addresses.update(user.id, address_id, payload)
    except AddressNotFound as exc:
        raise HTTPException(status_code=404, detail="Address not found") from exc
    except InvalidPhone as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _response(address, serviceability)


@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: Annotated[str, Path(min_length=36, max_length=36)],
    user: CommerceUser = Depends(get_current_user),
    addresses: AddressService = Depends(get_address_service),
) -> Response:
    try:
        addresses.delete(user.id, address_id)
    except AddressNotFound as exc:
        raise HTTPException(status_code=404, detail="Address not found") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/addresses/{address_id}/default", response_model=AddressResponse)
def set_default_address(
    address_id: Annotated[str, Path(min_length=36, max_length=36)],
    user: CommerceUser = Depends(get_current_user),
    addresses: AddressService = Depends(get_address_service),
    serviceability: ServiceabilityService = Depends(get_serviceability_service),
) -> AddressResponse:
    try:
        address = addresses.set_default(user.id, address_id)
    except AddressNotFound as exc:
        raise HTTPException(status_code=404, detail="Address not found") from exc
    return _response(address, serviceability)
