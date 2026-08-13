"""Authenticated checkout and customer order-ledger routes."""

from __future__ import annotations

from typing import Annotated, Callable, TypeVar

from fastapi import APIRouter, Depends, Header, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from .api import get_current_user
from .cart_service import CartConflict
from .database import get_commerce_db
from .models import CommerceUser
from .order_schemas import CheckoutQuoteResponse, CheckoutRequest, OrderListResponse, OrderResponse
from .order_service import (
    CheckoutUnavailable,
    InventoryConflict,
    OrderConflict,
    OrderNotFound,
    OrderService,
)


router = APIRouter(prefix="/api/commerce/v1", tags=["checkout", "orders"])
T = TypeVar("T")


def get_order_service(db: Session = Depends(get_commerce_db)) -> OrderService:
    return OrderService(db)


def _execute(operation: Callable[[], T]) -> T:
    try:
        return operation()
    except OrderNotFound as exc:
        raise HTTPException(status_code=404, detail="Order not found") from exc
    except (OrderConflict, CartConflict, InventoryConflict) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except CheckoutUnavailable as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/checkout/quote", response_model=CheckoutQuoteResponse)
def quote_checkout(
    payload: CheckoutRequest,
    user: CommerceUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
) -> CheckoutQuoteResponse:
    return _execute(lambda: service.quote(user_id=user.id, request=payload))


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: CheckoutRequest,
    idempotency_key: Annotated[
        str,
        Header(alias="Idempotency-Key", min_length=16, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$"),
    ],
    user: CommerceUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    return _execute(lambda: service.create(user_id=user.id, idempotency_key=idempotency_key, request=payload))


@router.get("/orders", response_model=OrderListResponse)
def list_orders(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    user: CommerceUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
) -> OrderListResponse:
    return service.list_orders(user_id=user.id, limit=limit, offset=offset)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: Annotated[str, Path(min_length=36, max_length=36)],
    user: CommerceUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    return _execute(lambda: service.get(user_id=user.id, order_id=order_id))


@router.post("/orders/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: Annotated[str, Path(min_length=36, max_length=36)],
    user: CommerceUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    return _execute(lambda: service.cancel(user_id=user.id, order_id=order_id))
