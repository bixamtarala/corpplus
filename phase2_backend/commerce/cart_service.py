"""Persistent guest and authenticated carts with server-side validation."""

from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from .cart_schemas import CartIssueResponse, CartItemResponse, CartResponse
from .models import (
    Address,
    AuditEvent,
    Cart,
    CartItem,
    Category,
    CommerceUser,
    InventoryBalance,
    InventoryLocation,
    Price,
    PriceList,
    Product,
    ServiceZone,
    Sku,
)
from .serviceability_service import ServiceabilityConfigurationError, ServiceabilityService


class CartNotFound(LookupError):
    pass


class CartItemNotFound(LookupError):
    pass


class CartConflict(RuntimeError):
    pass


class CartRuleViolation(ValueError):
    pass


class CartService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.price_list_code = os.getenv("COMMERCE_CONSUMER_PRICE_LIST_CODE", "consumer-inr")
        self.guest_ttl_days = max(1, int(os.getenv("COMMERCE_GUEST_CART_TTL_DAYS", "30")))

    def create_guest(self, pincode: str | None) -> CartResponse:
        raw_token = secrets.token_urlsafe(32)
        cart = Cart(
            guest_token_hash=self._token_hash(raw_token),
            status="active",
            expires_at=self._now() + timedelta(days=self.guest_ttl_days),
        )
        self.db.add(cart)
        self.db.flush()
        if pincode:
            self._apply_pincode(cart, pincode)
        self._audit(cart, "cart.guest_created")
        return self._render(cart, guest_token=raw_token)

    def restore(self, *, user_id: str | None, guest_token: str | None) -> CartResponse:
        cart = self._resolve(user_id=user_id, guest_token=guest_token, create_user=True, lock=False)
        return self._render(cart)

    def set_context(
        self,
        *,
        user_id: str | None,
        guest_token: str | None,
        address_id: str | None,
        pincode: str | None,
        expected_version: int,
    ) -> CartResponse:
        cart = self._resolve(user_id=user_id, guest_token=guest_token, create_user=True, lock=True)
        self._check_version(cart, expected_version)
        if address_id is not None:
            if user_id is None:
                raise CartRuleViolation("Guest carts must select a pincode")
            address = self.db.scalar(
                select(Address).where(
                    Address.id == address_id,
                    Address.user_id == user_id,
                    Address.is_active.is_(True),
                )
            )
            if address is None:
                raise CartRuleViolation("Saved address not found")
            cart.address_id = address.id
            self._apply_pincode(cart, address.pincode)
        else:
            if user_id is not None:
                raise CartRuleViolation("Authenticated carts must select a saved address")
            assert pincode is not None
            cart.address_id = None
            self._apply_pincode(cart, pincode)
        self._changed(cart, "cart.location_updated")
        return self._render(cart)

    def add_item(
        self,
        *,
        user_id: str | None,
        guest_token: str | None,
        sku_id: str,
        quantity: Decimal,
        expected_version: int,
    ) -> CartResponse:
        cart = self._resolve(user_id=user_id, guest_token=guest_token, create_user=True, lock=True)
        self._check_version(cart, expected_version)
        sku = self._sellable_sku(sku_id)
        self._validate_quantity(sku, quantity)
        price = self._current_price(sku.id)
        if price is None:
            raise CartRuleViolation("SKU does not have an active consumer price")
        existing = self.db.scalar(
            select(CartItem).where(CartItem.cart_id == cart.id, CartItem.sku_id == sku.id).with_for_update()
        )
        if existing is None:
            self.db.add(CartItem(cart_id=cart.id, sku_id=sku.id, quantity=quantity))
        else:
            combined = existing.quantity + quantity
            self._validate_quantity(sku, combined)
            existing.quantity = combined
        self._changed(cart, "cart.item_added", {"sku_id": sku.id})
        return self._render(cart)

    def update_item(
        self,
        *,
        user_id: str | None,
        guest_token: str | None,
        item_id: str,
        quantity: Decimal,
        expected_version: int,
    ) -> CartResponse:
        cart = self._resolve(user_id=user_id, guest_token=guest_token, create_user=False, lock=True)
        self._check_version(cart, expected_version)
        item = self._owned_item(cart, item_id)
        sku = self._sellable_sku(item.sku_id)
        self._validate_quantity(sku, quantity)
        item.quantity = quantity
        self._changed(cart, "cart.item_updated", {"sku_id": sku.id})
        return self._render(cart)

    def delete_item(
        self,
        *,
        user_id: str | None,
        guest_token: str | None,
        item_id: str,
        expected_version: int,
    ) -> CartResponse:
        cart = self._resolve(user_id=user_id, guest_token=guest_token, create_user=False, lock=True)
        self._check_version(cart, expected_version)
        item = self._owned_item(cart, item_id)
        sku_id = item.sku_id
        self.db.delete(item)
        self._changed(cart, "cart.item_removed", {"sku_id": sku_id})
        return self._render(cart)

    def validate(
        self,
        *,
        user_id: str | None,
        guest_token: str | None,
        expected_version: int,
    ) -> CartResponse:
        cart = self._resolve(user_id=user_id, guest_token=guest_token, create_user=False, lock=True)
        self._check_version(cart, expected_version)
        return self._render(cart)

    def merge_guest(
        self,
        *,
        user_id: str,
        guest_token: str,
        expected_version: int | None,
    ) -> CartResponse:
        guest = self.db.scalar(
            select(Cart)
            .where(
                Cart.guest_token_hash == self._token_hash(guest_token),
                Cart.status.in_(("active", "converted")),
            )
            .with_for_update()
        )
        if guest is None:
            raise CartNotFound("Cart not found")
        if guest.status == "converted":
            audit_events = self.db.scalars(
                select(AuditEvent)
                .where(
                    AuditEvent.actor_user_id == user_id,
                    AuditEvent.action == "cart.guest_merged",
                )
                .order_by(AuditEvent.occurred_at.desc(), AuditEvent.id.desc())
            )
            merged_target_id = next(
                (event.entity_id for event in audit_events if event.payload.get("source_cart_id") == guest.id),
                None,
            )
            merged_target = self.db.scalar(
                select(Cart).where(
                    Cart.id == merged_target_id,
                    Cart.user_id == user_id,
                    Cart.status == "active",
                )
            )
            if merged_target is None:
                raise CartNotFound("Cart not found")
            return self._render(merged_target)
        if guest.expires_at is not None and self._aware(guest.expires_at) <= self._now():
            guest.status = "expired"
            self.db.commit()
            raise CartNotFound("Cart not found")

        target = self._resolve(user_id=user_id, guest_token=None, create_user=True, lock=True)
        if expected_version is not None:
            self._check_version(target, expected_version)

        target_items = {
            item.sku_id: item
            for item in self.db.scalars(select(CartItem).where(CartItem.cart_id == target.id).with_for_update())
        }
        guest_items = list(self.db.scalars(select(CartItem).where(CartItem.cart_id == guest.id).with_for_update()))
        for item in guest_items:
            existing = target_items.get(item.sku_id)
            if existing is None:
                copied = CartItem(cart_id=target.id, sku_id=item.sku_id, quantity=item.quantity)
                self.db.add(copied)
                target_items[item.sku_id] = copied
            else:
                existing.quantity += item.quantity

        guest.status = "converted"
        guest.version += 1
        target.version += 1
        self._audit(target, "cart.guest_merged", {"source_cart_id": guest.id})
        return self._render(target)

    def _resolve(
        self,
        *,
        user_id: str | None,
        guest_token: str | None,
        create_user: bool,
        lock: bool,
    ) -> Cart:
        if user_id is None and not guest_token:
            raise CartRuleViolation("X-Guest-Cart-Token is required for a guest cart")
        if user_id is not None:
            self.db.scalar(select(CommerceUser.id).where(CommerceUser.id == user_id).with_for_update())
            statement = select(Cart).where(Cart.user_id == user_id, Cart.status == "active")
        else:
            statement = select(Cart).where(
                Cart.guest_token_hash == self._token_hash(guest_token or ""),
                Cart.status == "active",
            )
        if lock:
            statement = statement.with_for_update()
        cart = self.db.scalar(statement)
        if cart is None and user_id is not None and create_user:
            cart = Cart(user_id=user_id, status="active")
            self.db.add(cart)
            self.db.flush()
            self._audit(cart, "cart.authenticated_created")
        if cart is None:
            raise CartNotFound("Cart not found")
        if cart.expires_at is not None and self._aware(cart.expires_at) <= self._now():
            cart.status = "expired"
            self.db.commit()
            raise CartNotFound("Cart not found")
        return cart

    def _render(self, cart: Cart, *, guest_token: str | None = None) -> CartResponse:
        self.db.flush()
        now = self._now()
        cart_issues: list[CartIssueResponse] = []
        zone: ServiceZone | None = None
        if cart.user_id is not None:
            address = (
                self.db.scalar(
                    select(Address).where(
                        Address.id == cart.address_id,
                        Address.user_id == cart.user_id,
                        Address.is_active.is_(True),
                    )
                )
                if cart.address_id is not None
                else None
            )
            if address is None:
                cart.address_id = None
                cart.delivery_pincode = None
                cart.service_zone_id = None
            else:
                cart.delivery_pincode = address.pincode
        if cart.delivery_pincode is None:
            cart_issues.append(self._issue("location_required", "Select a delivery location"))
        else:
            try:
                decision = ServiceabilityService(self.db).check(cart.delivery_pincode)
            except ServiceabilityConfigurationError:
                decision = None
            if decision is None or not decision.serviceable or decision.zone is None:
                cart.service_zone_id = None
                cart_issues.append(self._issue("not_serviceable", "Delivery is unavailable for the selected pincode"))
            else:
                cart.service_zone_id = decision.zone.id
                zone = self.db.get(ServiceZone, decision.zone.id)

        price_list = self.db.scalar(
            select(PriceList).where(
                PriceList.code == self.price_list_code,
                PriceList.is_active.is_(True),
                PriceList.audience == "consumer",
            )
        )
        cart.price_list_id = price_list.id if price_list else None
        if price_list is None:
            cart_issues.append(self._issue("pricing_unavailable", "Consumer pricing is temporarily unavailable"))
        else:
            cart.currency = price_list.currency
            if zone is not None and zone.currency != price_list.currency:
                cart_issues.append(self._issue("currency_mismatch", "Zone and price currency do not match"))

        item_models = list(
            self.db.scalars(
                select(CartItem).where(CartItem.cart_id == cart.id).order_by(CartItem.created_at, CartItem.id)
            )
        )
        items: list[CartItemResponse] = []
        subtotal = 0
        for item in item_models:
            response, line_total = self._render_item(item, cart, price_list, now)
            items.append(response)
            if line_total is not None:
                subtotal += line_total

        if zone is not None and items and subtotal < zone.minimum_order_paise:
            cart_issues.append(
                self._issue(
                    "minimum_order_not_met",
                    f"Minimum order is {zone.minimum_order_paise} {zone.currency} minor units",
                )
            )

        all_issues = cart_issues + [issue for item in items for issue in item.issues]
        has_errors = any(issue.severity == "error" for issue in all_issues)
        if not items:
            validation_status: Literal["valid", "requires_action", "location_required", "empty"] = "empty"
        elif any(issue.code == "location_required" for issue in cart_issues):
            validation_status = "location_required"
        elif has_errors:
            validation_status = "requires_action"
        else:
            validation_status = "valid"

        self.db.commit()
        return CartResponse(
            id=cart.id,
            owner_type="authenticated" if cart.user_id else "guest",
            guest_token=guest_token,
            status=cart.status,
            version=cart.version,
            currency=cart.currency,
            address_id=cart.address_id,
            delivery_pincode=cart.delivery_pincode,
            service_zone_id=cart.service_zone_id,
            subtotal_paise=subtotal,
            minimum_order_paise=zone.minimum_order_paise if zone else None,
            delivery_fee_paise=zone.delivery_fee_paise if zone else None,
            total_paise=subtotal + zone.delivery_fee_paise if zone else None,
            item_count=len(items),
            valid_for_checkout=bool(items) and not has_errors,
            validation_status=validation_status,
            issues=cart_issues,
            items=items,
            validated_at=now,
        )

    def _render_item(
        self,
        item: CartItem,
        cart: Cart,
        price_list: PriceList | None,
        now: datetime,
    ) -> tuple[CartItemResponse, int | None]:
        row = self.db.execute(
            select(Sku, Product, Category)
            .join(Product, Product.id == Sku.product_id)
            .join(Category, Category.id == Product.category_id)
            .where(Sku.id == item.sku_id)
        ).one()
        sku, product, category = row
        issues: list[CartIssueResponse] = []
        if sku.status != "active" or product.status != "active" or not category.is_active:
            issues.append(self._issue("sku_unavailable", "This item is no longer available", item.id))
        try:
            self._validate_quantity(sku, item.quantity)
        except CartRuleViolation as exc:
            issues.append(self._issue("quantity_invalid", str(exc), item.id))

        price = self._current_price(sku.id, price_list=price_list)
        line_total: int | None = None
        if price is None:
            issues.append(self._issue("price_unavailable", "Current price is unavailable", item.id))
            unit_price = None
        else:
            unit_price = price.amount_paise
            if item.unit_price_snapshot_paise is not None and item.unit_price_snapshot_paise != unit_price:
                issues.append(
                    self._issue("price_changed", "Price changed since the cart was last checked", item.id, "info")
                )
            item.unit_price_snapshot_paise = unit_price
            item.price_checked_at = now
            line_total = int((Decimal(unit_price) * item.quantity).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

        available: Decimal | None = None
        if cart.service_zone_id is not None:
            available = self.db.scalar(
                select(
                    func.coalesce(func.sum(InventoryBalance.on_hand_quantity - InventoryBalance.reserved_quantity), 0)
                )
                .join(InventoryLocation, InventoryLocation.id == InventoryBalance.inventory_location_id)
                .where(
                    InventoryBalance.sku_id == sku.id,
                    InventoryLocation.service_zone_id == cart.service_zone_id,
                    InventoryLocation.is_active.is_(True),
                    InventoryLocation.location_type.in_(("hub", "supplier")),
                )
            )
            available = Decimal(available or 0)
            item.inventory_checked_at = now
            if available < item.quantity:
                issues.append(self._issue("insufficient_inventory", "Requested quantity is unavailable", item.id))

        return (
            CartItemResponse(
                id=item.id,
                sku_id=sku.id,
                sku_code=sku.code,
                product_name=product.default_name,
                quantity=item.quantity,
                unit_of_measure=sku.unit_of_measure,
                minimum_order_quantity=sku.minimum_order_quantity,
                quantity_step=sku.quantity_step,
                unit_price_paise=unit_price,
                line_total_paise=line_total,
                available_quantity=available,
                issues=issues,
            ),
            line_total,
        )

    def _sellable_sku(self, sku_id: str) -> Sku:
        sku = self.db.scalar(
            select(Sku)
            .join(Product, Product.id == Sku.product_id)
            .join(Category, Category.id == Product.category_id)
            .where(
                Sku.id == sku_id,
                Sku.status == "active",
                Product.status == "active",
                Category.is_active.is_(True),
            )
        )
        if sku is None:
            raise CartRuleViolation("SKU is unavailable")
        return sku

    def _current_price(self, sku_id: str, *, price_list: PriceList | None = None) -> Price | None:
        if price_list is None:
            price_list = self.db.scalar(
                select(PriceList).where(
                    PriceList.code == self.price_list_code,
                    PriceList.is_active.is_(True),
                    PriceList.audience == "consumer",
                )
            )
        if price_list is None:
            return None
        now = self._now()
        return self.db.scalar(
            select(Price)
            .where(
                Price.price_list_id == price_list.id,
                Price.sku_id == sku_id,
                Price.effective_from <= now,
                or_(Price.effective_to.is_(None), Price.effective_to > now),
            )
            .order_by(Price.effective_from.desc(), Price.id.desc())
            .limit(1)
        )

    @staticmethod
    def _validate_quantity(sku: Sku, quantity: Decimal) -> None:
        minimum = Decimal(sku.minimum_order_quantity)
        step = Decimal(sku.quantity_step)
        if quantity < minimum:
            raise CartRuleViolation(f"Minimum quantity is {minimum}")
        if (quantity - minimum) % step != 0:
            raise CartRuleViolation(f"Quantity must increase from {minimum} in steps of {step}")

    def _apply_pincode(self, cart: Cart, pincode: str) -> None:
        cart.delivery_pincode = pincode
        try:
            decision = ServiceabilityService(self.db).check(pincode)
        except ServiceabilityConfigurationError:
            decision = None
        cart.service_zone_id = decision.zone.id if decision and decision.serviceable and decision.zone else None

    def _owned_item(self, cart: Cart, item_id: str) -> CartItem:
        item = self.db.scalar(
            select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart.id).with_for_update()
        )
        if item is None:
            raise CartItemNotFound("Cart item not found")
        return item

    @staticmethod
    def _check_version(cart: Cart, expected_version: int) -> None:
        if cart.version != expected_version:
            raise CartConflict("Cart changed; restore it and retry")

    def _changed(self, cart: Cart, action: str, payload: dict[str, object] | None = None) -> None:
        cart.version += 1
        self._audit(cart, action, payload)

    def _audit(self, cart: Cart, action: str, payload: dict[str, object] | None = None) -> None:
        self.db.add(
            AuditEvent(
                actor_user_id=cart.user_id,
                entity_type="cart",
                entity_id=cart.id,
                action=action,
                payload=payload or {},
            )
        )

    @staticmethod
    def _issue(
        code: str,
        message: str,
        item_id: str | None = None,
        severity: Literal["error", "info"] = "error",
    ) -> CartIssueResponse:
        return CartIssueResponse(code=code, message=message, item_id=item_id, severity=severity)

    @staticmethod
    def _token_hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def _aware(value: datetime) -> datetime:
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
