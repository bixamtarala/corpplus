"""Persistent cart routes for guests and authenticated customers."""

from __future__ import annotations

from typing import Annotated, Callable

from fastapi import APIRouter, Depends, Header, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from .api import get_current_user, get_optional_current_user
from .cart_schemas import (
    CartContextBody,
    CartItemCreateBody,
    CartItemUpdateBody,
    CartMergeBody,
    CartMutationBody,
    CartResponse,
    GuestCartCreateBody,
)
from .cart_service import (
    CartConflict,
    CartItemNotFound,
    CartNotFound,
    CartRuleViolation,
    CartService,
)
from .database import get_commerce_db
from .models import CommerceUser


router = APIRouter(prefix="/api/commerce/v1/cart", tags=["cart"])
GuestToken = Annotated[str | None, Header(alias="X-Guest-Cart-Token", min_length=32, max_length=128)]


def get_cart_service(db: Session = Depends(get_commerce_db)) -> CartService:
    return CartService(db)


def _execute(operation: Callable[[], CartResponse]) -> CartResponse:
    try:
        return operation()
    except CartNotFound as exc:
        raise HTTPException(status_code=404, detail="Cart not found") from exc
    except CartItemNotFound as exc:
        raise HTTPException(status_code=404, detail="Cart item not found") from exc
    except CartConflict as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except CartRuleViolation as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/guest", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def create_guest_cart(
    payload: GuestCartCreateBody,
    service: CartService = Depends(get_cart_service),
) -> CartResponse:
    return _execute(lambda: service.create_guest(payload.pincode))


@router.get("", response_model=CartResponse)
def restore_cart(
    guest_token: GuestToken = None,
    user: CommerceUser | None = Depends(get_optional_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartResponse:
    return _execute(lambda: service.restore(user_id=user.id if user else None, guest_token=guest_token))


@router.patch("", response_model=CartResponse)
def update_cart_context(
    payload: CartContextBody,
    guest_token: GuestToken = None,
    user: CommerceUser | None = Depends(get_optional_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartResponse:
    return _execute(
        lambda: service.set_context(
            user_id=user.id if user else None,
            guest_token=guest_token,
            address_id=payload.address_id,
            pincode=payload.pincode,
            expected_version=payload.expected_version,
        )
    )


@router.post("/items", response_model=CartResponse)
def add_cart_item(
    payload: CartItemCreateBody,
    guest_token: GuestToken = None,
    user: CommerceUser | None = Depends(get_optional_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartResponse:
    return _execute(
        lambda: service.add_item(
            user_id=user.id if user else None,
            guest_token=guest_token,
            sku_id=payload.sku_id,
            quantity=payload.quantity,
            expected_version=payload.expected_version,
        )
    )


@router.patch("/items/{item_id}", response_model=CartResponse)
def update_cart_item(
    payload: CartItemUpdateBody,
    item_id: Annotated[str, Path(min_length=36, max_length=36)],
    guest_token: GuestToken = None,
    user: CommerceUser | None = Depends(get_optional_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartResponse:
    return _execute(
        lambda: service.update_item(
            user_id=user.id if user else None,
            guest_token=guest_token,
            item_id=item_id,
            quantity=payload.quantity,
            expected_version=payload.expected_version,
        )
    )


@router.delete("/items/{item_id}", response_model=CartResponse)
def delete_cart_item(
    item_id: Annotated[str, Path(min_length=36, max_length=36)],
    expected_version: Annotated[int, Query(ge=1)],
    guest_token: GuestToken = None,
    user: CommerceUser | None = Depends(get_optional_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartResponse:
    return _execute(
        lambda: service.delete_item(
            user_id=user.id if user else None,
            guest_token=guest_token,
            item_id=item_id,
            expected_version=expected_version,
        )
    )


@router.post("/validate", response_model=CartResponse)
def validate_cart(
    payload: CartMutationBody,
    guest_token: GuestToken = None,
    user: CommerceUser | None = Depends(get_optional_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartResponse:
    return _execute(
        lambda: service.validate(
            user_id=user.id if user else None,
            guest_token=guest_token,
            expected_version=payload.expected_version,
        )
    )


@router.post("/merge", response_model=CartResponse)
def merge_guest_cart(
    payload: CartMergeBody,
    guest_token: Annotated[str, Header(alias="X-Guest-Cart-Token", min_length=32, max_length=128)],
    user: CommerceUser = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartResponse:
    return _execute(
        lambda: service.merge_guest(
            user_id=user.id,
            guest_token=guest_token,
            expected_version=payload.expected_version,
        )
    )
