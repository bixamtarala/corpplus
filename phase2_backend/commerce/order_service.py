"""Server-authoritative checkout, inventory reservation, and order ledger."""

from __future__ import annotations

import hashlib
import json
import secrets
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .cart_service import CartConflict, CartNotFound, CartService
from .models import (
    Address,
    AuditEvent,
    InventoryBalance,
    InventoryLocation,
    InventoryReservation,
    Order,
    OrderEvent,
    OrderItem,
    Sku,
)
from .order_schemas import (
    AddressSnapshotResponse,
    CheckoutLineResponse,
    CheckoutQuoteResponse,
    CheckoutRequest,
    OrderEventResponse,
    OrderListResponse,
    OrderResponse,
)


class CheckoutUnavailable(ValueError):
    pass


class OrderNotFound(LookupError):
    pass


class OrderConflict(RuntimeError):
    pass


class InventoryConflict(RuntimeError):
    pass


class OrderService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def quote(self, *, user_id: str, request: CheckoutRequest) -> CheckoutQuoteResponse:
        _, cart = self._validated_cart(user_id=user_id, expected_version=request.expected_cart_version)
        return self._quote_from_cart(cart, request)

    def create(
        self,
        *,
        user_id: str,
        idempotency_key: str,
        request: CheckoutRequest,
    ) -> OrderResponse:
        key_hash = self._hash(idempotency_key)
        fingerprint = self._fingerprint(request)
        replay = self.db.scalar(select(Order).where(Order.user_id == user_id, Order.idempotency_key_hash == key_hash))
        if replay is not None:
            if replay.request_fingerprint != fingerprint:
                raise OrderConflict("Idempotency key was already used with different checkout details")
            return self._response(replay)

        cart_model, cart = self._validated_cart(
            user_id=user_id,
            expected_version=request.expected_cart_version,
        )
        quote = self._quote_from_cart(cart, request)
        address = self.db.scalar(
            select(Address).where(
                Address.id == cart.address_id,
                Address.user_id == user_id,
                Address.is_active.is_(True),
            )
        )
        if address is None:
            raise CheckoutUnavailable("Select an active saved address before checkout")

        now = self._now()
        order = Order(
            order_number=self._order_number(now),
            user_id=user_id,
            source_cart_id=cart.id,
            address_id=address.id,
            service_zone_id=cart.service_zone_id,
            idempotency_key_hash=key_hash,
            request_fingerprint=fingerprint,
            address_snapshot=self._address_snapshot(address),
            status="confirmed",
            payment_method=request.payment_method,
            payment_status="pending",
            substitution_preference=request.substitution_preference,
            customer_note=request.customer_note,
            currency=quote.currency,
            subtotal_paise=quote.subtotal_paise,
            tax_paise=quote.tax_paise,
            delivery_fee_paise=quote.delivery_fee_paise,
            discount_paise=quote.discount_paise,
            total_paise=quote.total_paise,
            confirmed_at=now,
        )
        self.db.add(order)
        self.db.flush()

        for line in quote.lines:
            item = OrderItem(
                order_id=order.id,
                sku_id=line.sku_id,
                sku_code=line.sku_code,
                product_name=line.product_name,
                unit_of_measure=line.unit_of_measure,
                quantity=line.quantity,
                unit_price_paise=line.unit_price_paise,
                tax_rate_basis_points=line.tax_rate_basis_points,
                subtotal_paise=line.subtotal_paise,
                tax_paise=line.tax_paise,
                total_paise=line.total_paise,
            )
            self.db.add(item)
            self.db.flush()
            self._reserve(
                order=order,
                order_item=item,
                service_zone_id=quote.service_zone_id,
                quantity=line.quantity,
            )

        cart_model.status = "converted"
        cart_model.version += 1
        self.db.add(
            OrderEvent(
                order_id=order.id,
                sequence=1,
                event_type="order.confirmed",
                actor_user_id=user_id,
                payload={
                    "payment_method": request.payment_method,
                    "source_cart_id": cart.id,
                },
            )
        )
        self.db.add(
            AuditEvent(
                actor_user_id=user_id,
                entity_type="order",
                entity_id=order.id,
                action="order.confirmed",
                payload={"order_number": order.order_number, "source_cart_id": cart.id},
            )
        )
        self.db.add(
            AuditEvent(
                actor_user_id=user_id,
                entity_type="cart",
                entity_id=cart.id,
                action="cart.checked_out",
                payload={"order_id": order.id},
            )
        )
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            replay = self.db.scalar(
                select(Order).where(Order.user_id == user_id, Order.idempotency_key_hash == key_hash)
            )
            if replay is None:
                raise
            if replay.request_fingerprint != fingerprint:
                raise OrderConflict("Idempotency key was already used with different checkout details")
            return self._response(replay)
        self.db.refresh(order)
        return self._response(order)

    def list_orders(self, *, user_id: str, limit: int, offset: int) -> OrderListResponse:
        total = self.db.scalar(select(func.count(Order.id)).where(Order.user_id == user_id)) or 0
        orders = list(
            self.db.scalars(
                select(Order)
                .where(Order.user_id == user_id)
                .order_by(Order.created_at.desc(), Order.id.desc())
                .offset(offset)
                .limit(limit)
            )
        )
        return OrderListResponse(items=[self._response(order) for order in orders], total=total)

    def get(self, *, user_id: str, order_id: str) -> OrderResponse:
        return self._response(self._owned_order(user_id=user_id, order_id=order_id, lock=False))

    def cancel(self, *, user_id: str, order_id: str) -> OrderResponse:
        order = self._owned_order(user_id=user_id, order_id=order_id, lock=True)
        if order.status == "cancelled":
            return self._response(order)
        if order.status != "confirmed":
            raise OrderConflict("Only confirmed orders can be cancelled")

        reservations = list(
            self.db.scalars(
                select(InventoryReservation)
                .where(
                    InventoryReservation.order_id == order.id,
                    InventoryReservation.status == "active",
                )
                .order_by(InventoryReservation.id)
                .with_for_update()
            )
        )
        now = self._now()
        for reservation in reservations:
            balance = self.db.scalar(
                select(InventoryBalance)
                .where(InventoryBalance.id == reservation.inventory_balance_id)
                .with_for_update()
            )
            if balance is None or Decimal(balance.reserved_quantity) < Decimal(reservation.quantity):
                raise InventoryConflict("Inventory reservation ledger is inconsistent")
            balance.reserved_quantity -= reservation.quantity
            balance.version += 1
            reservation.status = "released"
            reservation.released_at = now

        order.status = "cancelled"
        order.payment_status = "voided"
        order.cancelled_at = now
        sequence = (
            self.db.scalar(select(func.max(OrderEvent.sequence)).where(OrderEvent.order_id == order.id)) or 0
        ) + 1
        self.db.add(
            OrderEvent(
                order_id=order.id,
                sequence=sequence,
                event_type="order.cancelled",
                actor_user_id=user_id,
                payload={"released_reservations": len(reservations)},
            )
        )
        self.db.add(
            AuditEvent(
                actor_user_id=user_id,
                entity_type="order",
                entity_id=order.id,
                action="order.cancelled",
                payload={"released_reservations": len(reservations)},
            )
        )
        self.db.commit()
        self.db.refresh(order)
        return self._response(order)

    def _validated_cart(self, *, user_id: str, expected_version: int):
        try:
            cart_model, cart = CartService(self.db).checkout_snapshot(
                user_id=user_id,
                expected_version=expected_version,
            )
        except CartConflict as exc:
            raise OrderConflict(str(exc)) from exc
        except CartNotFound as exc:
            raise CheckoutUnavailable("Authenticated cart not found") from exc
        if not cart.valid_for_checkout:
            codes = sorted(
                {issue.code for issue in cart.issues for _ in [0]}
                | {issue.code for item in cart.items for issue in item.issues if issue.severity == "error"}
            )
            reason = ", ".join(codes) if codes else "cart_invalid"
            raise CheckoutUnavailable(f"Cart is not ready for checkout: {reason}")
        if cart.address_id is None or cart.service_zone_id is None:
            raise CheckoutUnavailable("Select a serviceable saved address before checkout")
        return cart_model, cart

    def _quote_from_cart(self, cart, request: CheckoutRequest) -> CheckoutQuoteResponse:
        lines: list[CheckoutLineResponse] = []
        tax_total = 0
        for cart_line in cart.items:
            if cart_line.unit_price_paise is None or cart_line.line_total_paise is None:
                raise CheckoutUnavailable("Current pricing is unavailable")
            sku = self.db.get(Sku, cart_line.sku_id)
            if sku is None:
                raise CheckoutUnavailable("A cart item is unavailable")
            tax = self._tax(cart_line.line_total_paise, sku.tax_rate_basis_points)
            tax_total += tax
            lines.append(
                CheckoutLineResponse(
                    sku_id=cart_line.sku_id,
                    sku_code=cart_line.sku_code,
                    product_name=cart_line.product_name,
                    quantity=cart_line.quantity,
                    unit_of_measure=cart_line.unit_of_measure,
                    unit_price_paise=cart_line.unit_price_paise,
                    tax_rate_basis_points=sku.tax_rate_basis_points,
                    subtotal_paise=cart_line.line_total_paise,
                    tax_paise=tax,
                    total_paise=cart_line.line_total_paise + tax,
                )
            )
        delivery_fee = cart.delivery_fee_paise or 0
        discount = 0
        return CheckoutQuoteResponse(
            cart_id=cart.id,
            cart_version=cart.version,
            address_id=cart.address_id,
            service_zone_id=cart.service_zone_id,
            currency=cart.currency,
            payment_method=request.payment_method,
            subtotal_paise=cart.subtotal_paise,
            tax_paise=tax_total,
            delivery_fee_paise=delivery_fee,
            discount_paise=discount,
            total_paise=cart.subtotal_paise + tax_total + delivery_fee - discount,
            lines=lines,
            quoted_at=self._now(),
        )

    def _reserve(
        self,
        *,
        order: Order,
        order_item: OrderItem,
        service_zone_id: str,
        quantity: Decimal,
    ) -> None:
        balances = list(
            self.db.scalars(
                select(InventoryBalance)
                .join(InventoryLocation, InventoryLocation.id == InventoryBalance.inventory_location_id)
                .where(
                    InventoryBalance.sku_id == order_item.sku_id,
                    InventoryLocation.service_zone_id == service_zone_id,
                    InventoryLocation.is_active.is_(True),
                    InventoryLocation.location_type.in_(("hub", "supplier")),
                )
                .order_by(InventoryLocation.location_type, InventoryBalance.id)
                .with_for_update()
            )
        )
        remaining = Decimal(quantity)
        for balance in balances:
            available = Decimal(balance.on_hand_quantity) - Decimal(balance.reserved_quantity)
            allocated = min(available, remaining)
            if allocated <= 0:
                continue
            balance.reserved_quantity += allocated
            balance.version += 1
            self.db.add(
                InventoryReservation(
                    order_id=order.id,
                    order_item_id=order_item.id,
                    inventory_balance_id=balance.id,
                    quantity=allocated,
                    status="active",
                )
            )
            remaining -= allocated
            if remaining == 0:
                return
        raise InventoryConflict(f"Inventory changed for SKU {order_item.sku_code}; restore the cart and retry")

    def _owned_order(self, *, user_id: str, order_id: str, lock: bool) -> Order:
        statement = select(Order).where(Order.id == order_id, Order.user_id == user_id)
        if lock:
            statement = statement.with_for_update()
        order = self.db.scalar(statement)
        if order is None:
            raise OrderNotFound("Order not found")
        return order

    def _response(self, order: Order) -> OrderResponse:
        items = list(
            self.db.scalars(
                select(OrderItem).where(OrderItem.order_id == order.id).order_by(OrderItem.created_at, OrderItem.id)
            )
        )
        events = list(
            self.db.scalars(select(OrderEvent).where(OrderEvent.order_id == order.id).order_by(OrderEvent.sequence))
        )
        return OrderResponse(
            id=order.id,
            order_number=order.order_number,
            source_cart_id=order.source_cart_id,
            status=order.status,
            payment_method=order.payment_method,
            payment_status=order.payment_status,
            substitution_preference=order.substitution_preference,
            customer_note=order.customer_note,
            currency=order.currency,
            subtotal_paise=order.subtotal_paise,
            tax_paise=order.tax_paise,
            delivery_fee_paise=order.delivery_fee_paise,
            discount_paise=order.discount_paise,
            total_paise=order.total_paise,
            address=AddressSnapshotResponse.model_validate(order.address_snapshot),
            items=[
                CheckoutLineResponse(
                    sku_id=item.sku_id,
                    sku_code=item.sku_code,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_of_measure=item.unit_of_measure,
                    unit_price_paise=item.unit_price_paise,
                    tax_rate_basis_points=item.tax_rate_basis_points,
                    subtotal_paise=item.subtotal_paise,
                    tax_paise=item.tax_paise,
                    total_paise=item.total_paise,
                )
                for item in items
            ],
            events=[
                OrderEventResponse(
                    sequence=event.sequence,
                    event_type=event.event_type,
                    payload=event.payload,
                    occurred_at=event.occurred_at,
                )
                for event in events
            ],
            confirmed_at=order.confirmed_at,
            cancelled_at=order.cancelled_at,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

    @staticmethod
    def _address_snapshot(address: Address) -> dict[str, object]:
        return {
            "label": address.label,
            "recipient_name": address.recipient_name,
            "recipient_phone_e164": address.recipient_phone_e164,
            "line1": address.line1,
            "line2": address.line2,
            "landmark": address.landmark,
            "locality": address.locality,
            "district": address.district,
            "state": address.state,
            "pincode": address.pincode,
        }

    @staticmethod
    def _tax(subtotal_paise: int, rate_basis_points: int) -> int:
        return int(
            (Decimal(subtotal_paise) * Decimal(rate_basis_points) / Decimal(10000)).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
        )

    @staticmethod
    def _fingerprint(request: CheckoutRequest) -> str:
        canonical = json.dumps(request.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
        return OrderService._hash(canonical)

    @staticmethod
    def _hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _order_number(now: datetime) -> str:
        return f"CP{now:%Y%m%d%H%M%S}{secrets.token_hex(3).upper()}"

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)
