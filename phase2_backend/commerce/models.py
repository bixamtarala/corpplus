"""SQLAlchemy models for CropPulse commerce Slice 2.

Money is stored in integer minor units (paise for INR). Product and inventory
quantities use fixed-precision decimals. Prices and availability remain
server-authoritative; mobile clients only display returned values.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _uuid() -> str:
    return str(uuid.uuid4())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )


class CommerceUser(TimestampMixin, Base):
    __tablename__ = "commerce_users"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'blocked', 'deleted')",
            name="ck_commerce_users_status",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    phone_e164: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="active", nullable=False)
    preferred_locale: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(120))
    last_authenticated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    addresses: Mapped[list["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[list["CommerceSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class CommerceSession(TimestampMixin, Base):
    __tablename__ = "commerce_sessions"
    __table_args__ = (
        CheckConstraint("expires_at > created_at", name="ck_commerce_sessions_expiry"),
        Index("ix_commerce_sessions_user_active", "user_id", "revoked_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("commerce_users.id", ondelete="CASCADE"), nullable=False)
    refresh_token_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    device_id_hash: Mapped[str | None] = mapped_column(String(128))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped[CommerceUser] = relationship(back_populates="sessions")


class OtpChallenge(TimestampMixin, Base):
    __tablename__ = "commerce_otp_challenges"
    __table_args__ = (
        CheckConstraint(
            "status IN ('requested', 'consumed', 'failed', 'expired')",
            name="ck_commerce_otp_challenges_status",
        ),
        CheckConstraint(
            "failed_attempts >= 0 AND failed_attempts <= max_attempts",
            name="ck_commerce_otp_challenges_attempts",
        ),
        CheckConstraint(
            "max_attempts >= 1 AND max_attempts <= 10",
            name="ck_commerce_otp_challenges_max_attempts",
        ),
        CheckConstraint("expires_at > created_at", name="ck_commerce_otp_challenges_expiry"),
        Index("ix_commerce_otp_phone_created", "phone_hash", "created_at"),
        Index("ix_commerce_otp_ip_created", "request_ip_hash", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    phone_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    request_ip_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    provider: Mapped[str] = mapped_column(String(32), nullable=False)
    provider_reference: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="requested", nullable=False)
    failed_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ServiceZone(TimestampMixin, Base):
    __tablename__ = "commerce_service_zones"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'active', 'paused', 'closed')",
            name="ck_commerce_service_zones_status",
        ),
        CheckConstraint("minimum_order_paise >= 0", name="ck_service_zone_minimum"),
        CheckConstraint("delivery_fee_paise >= 0", name="ck_service_zone_delivery_fee"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="draft", nullable=False)
    state: Mapped[str] = mapped_column(String(80), nullable=False)
    district: Mapped[str] = mapped_column(String(80), nullable=False)
    timezone_name: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata", nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    minimum_order_paise: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    delivery_fee_paise: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    pincodes: Mapped[list["ServiceZonePincode"]] = relationship(
        back_populates="service_zone", cascade="all, delete-orphan"
    )


class ServiceZonePincode(TimestampMixin, Base):
    __tablename__ = "commerce_service_zone_pincodes"
    __table_args__ = (
        UniqueConstraint("service_zone_id", "pincode", name="uq_service_zone_pincode"),
        CheckConstraint("length(pincode) = 6", name="ck_service_zone_pincode_length"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    service_zone_id: Mapped[str] = mapped_column(
        ForeignKey("commerce_service_zones.id", ondelete="CASCADE"), nullable=False
    )
    pincode: Mapped[str] = mapped_column(String(6), nullable=False, index=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    service_zone: Mapped[ServiceZone] = relationship(back_populates="pincodes")


class Address(TimestampMixin, Base):
    __tablename__ = "commerce_addresses"
    __table_args__ = (
        CheckConstraint("length(pincode) = 6", name="ck_commerce_addresses_pincode"),
        Index("ix_commerce_addresses_user_default", "user_id", "is_default"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("commerce_users.id", ondelete="CASCADE"), nullable=False)
    label: Mapped[str] = mapped_column(String(40), default="Home", nullable=False)
    recipient_name: Mapped[str] = mapped_column(String(120), nullable=False)
    recipient_phone_e164: Mapped[str] = mapped_column(String(16), nullable=False)
    line1: Mapped[str] = mapped_column(String(180), nullable=False)
    line2: Mapped[str | None] = mapped_column(String(180))
    landmark: Mapped[str | None] = mapped_column(String(180))
    locality: Mapped[str] = mapped_column(String(120), nullable=False)
    district: Mapped[str] = mapped_column(String(80), nullable=False)
    state: Mapped[str] = mapped_column(String(80), nullable=False)
    pincode: Mapped[str] = mapped_column(String(6), nullable=False, index=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped[CommerceUser] = relationship(back_populates="addresses")


class Category(TimestampMixin, Base):
    __tablename__ = "commerce_categories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    parent_id: Mapped[str | None] = mapped_column(ForeignKey("commerce_categories.id", ondelete="SET NULL"))
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    default_name: Mapped[str] = mapped_column(String(120), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CategoryTranslation(TimestampMixin, Base):
    __tablename__ = "commerce_category_translations"
    __table_args__ = (UniqueConstraint("category_id", "locale", name="uq_category_translation_locale"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    category_id: Mapped[str] = mapped_column(ForeignKey("commerce_categories.id", ondelete="CASCADE"), nullable=False)
    locale: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)


class Product(TimestampMixin, Base):
    __tablename__ = "commerce_products"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'active', 'paused', 'recalled', 'archived')",
            name="ck_commerce_products_status",
        ),
        Index("ix_commerce_products_category_status", "category_id", "status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    category_id: Mapped[str] = mapped_column(ForeignKey("commerce_categories.id", ondelete="RESTRICT"), nullable=False)
    slug: Mapped[str] = mapped_column(String(140), unique=True, nullable=False)
    default_name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    storage_guidance: Mapped[str | None] = mapped_column(Text)
    source_organization_name: Mapped[str | None] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(16), default="draft", nullable=False)
    claims_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ProductTranslation(TimestampMixin, Base):
    __tablename__ = "commerce_product_translations"
    __table_args__ = (UniqueConstraint("product_id", "locale", name="uq_product_translation_locale"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    product_id: Mapped[str] = mapped_column(ForeignKey("commerce_products.id", ondelete="CASCADE"), nullable=False)
    locale: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    storage_guidance: Mapped[str | None] = mapped_column(Text)


class ProductMedia(TimestampMixin, Base):
    __tablename__ = "commerce_product_media"
    __table_args__ = (
        CheckConstraint("media_type IN ('image')", name="ck_commerce_product_media_type"),
        CheckConstraint("sort_order >= 0", name="ck_product_media_sort_order"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    product_id: Mapped[str] = mapped_column(ForeignKey("commerce_products.id", ondelete="CASCADE"), nullable=False)
    media_type: Mapped[str] = mapped_column(String(16), default="image", nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    alt_text: Mapped[str] = mapped_column(String(240), nullable=False)
    is_representative: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Sku(TimestampMixin, Base):
    __tablename__ = "commerce_skus"
    __table_args__ = (
        CheckConstraint("pack_quantity > 0", name="ck_commerce_skus_pack_quantity"),
        CheckConstraint("minimum_order_quantity > 0", name="ck_commerce_skus_moq"),
        CheckConstraint("quantity_step > 0", name="ck_commerce_skus_quantity_step"),
        CheckConstraint(
            "status IN ('draft', 'active', 'paused', 'recalled', 'archived')",
            name="ck_commerce_skus_status",
        ),
        Index("ix_commerce_skus_product_status", "product_id", "status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    product_id: Mapped[str] = mapped_column(ForeignKey("commerce_products.id", ondelete="RESTRICT"), nullable=False)
    code: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    pack_quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    unit_of_measure: Mapped[str] = mapped_column(String(20), nullable=False)
    grade: Mapped[str | None] = mapped_column(String(80))
    origin_district: Mapped[str | None] = mapped_column(String(80))
    origin_state: Mapped[str | None] = mapped_column(String(80))
    hsn_code: Mapped[str | None] = mapped_column(String(16))
    tax_rate_basis_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    minimum_order_quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=Decimal("1.000"), nullable=False)
    quantity_step: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=Decimal("1.000"), nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="draft", nullable=False)


class PriceList(TimestampMixin, Base):
    __tablename__ = "commerce_price_lists"
    __table_args__ = (
        CheckConstraint(
            "audience IN ('consumer', 'business', 'promotional', 'negotiated')",
            name="ck_commerce_price_lists_audience",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    code: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    audience: Mapped[str] = mapped_column(String(20), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Price(TimestampMixin, Base):
    __tablename__ = "commerce_prices"
    __table_args__ = (
        CheckConstraint("amount_paise >= 0", name="ck_commerce_prices_amount"),
        CheckConstraint(
            "compare_at_paise IS NULL OR compare_at_paise >= amount_paise",
            name="ck_commerce_prices_compare_at",
        ),
        CheckConstraint(
            "effective_to IS NULL OR effective_to > effective_from",
            name="ck_commerce_prices_effective_range",
        ),
        UniqueConstraint("price_list_id", "sku_id", "effective_from", name="uq_price_effective_start"),
        Index("ix_commerce_prices_lookup", "price_list_id", "sku_id", "effective_from"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    price_list_id: Mapped[str] = mapped_column(
        ForeignKey("commerce_price_lists.id", ondelete="RESTRICT"), nullable=False
    )
    sku_id: Mapped[str] = mapped_column(ForeignKey("commerce_skus.id", ondelete="RESTRICT"), nullable=False)
    amount_paise: Mapped[int] = mapped_column(BigInteger, nullable=False)
    compare_at_paise: Mapped[int | None] = mapped_column(BigInteger)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    source: Mapped[str] = mapped_column(String(80), nullable=False)


class InventoryLocation(TimestampMixin, Base):
    __tablename__ = "commerce_inventory_locations"
    __table_args__ = (
        CheckConstraint(
            "location_type IN ('hub', 'supplier', 'quality_hold')",
            name="ck_inventory_locations_type",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    service_zone_id: Mapped[str | None] = mapped_column(ForeignKey("commerce_service_zones.id", ondelete="RESTRICT"))
    code: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(140), nullable=False)
    location_type: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class InventoryBalance(TimestampMixin, Base):
    __tablename__ = "commerce_inventory_balances"
    __table_args__ = (
        UniqueConstraint("inventory_location_id", "sku_id", name="uq_inventory_balance"),
        CheckConstraint("on_hand_quantity >= 0", name="ck_inventory_on_hand"),
        CheckConstraint("reserved_quantity >= 0", name="ck_inventory_reserved"),
        CheckConstraint("reserved_quantity <= on_hand_quantity", name="ck_inventory_reservation_limit"),
        Index("ix_inventory_balance_sku", "sku_id", "inventory_location_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    inventory_location_id: Mapped[str] = mapped_column(
        ForeignKey("commerce_inventory_locations.id", ondelete="RESTRICT"), nullable=False
    )
    sku_id: Mapped[str] = mapped_column(ForeignKey("commerce_skus.id", ondelete="RESTRICT"), nullable=False)
    on_hand_quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=Decimal("0.000"), nullable=False)
    reserved_quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=Decimal("0.000"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    counted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Cart(TimestampMixin, Base):
    __tablename__ = "commerce_carts"
    __table_args__ = (
        CheckConstraint(
            "(user_id IS NOT NULL AND guest_token_hash IS NULL) OR "
            "(user_id IS NULL AND guest_token_hash IS NOT NULL)",
            name="ck_commerce_carts_owner",
        ),
        CheckConstraint(
            "status IN ('active', 'converted', 'expired', 'abandoned')",
            name="ck_commerce_carts_status",
        ),
        Index("ix_commerce_carts_user_status", "user_id", "status"),
        Index("ix_commerce_carts_guest_status", "guest_token_hash", "status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("commerce_users.id", ondelete="CASCADE"))
    guest_token_hash: Mapped[str | None] = mapped_column(String(128))
    service_zone_id: Mapped[str | None] = mapped_column(ForeignKey("commerce_service_zones.id", ondelete="SET NULL"))
    address_id: Mapped[str | None] = mapped_column(ForeignKey("commerce_addresses.id", ondelete="SET NULL"))
    price_list_id: Mapped[str | None] = mapped_column(ForeignKey("commerce_price_lists.id", ondelete="SET NULL"))
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="active", nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    items: Mapped[list["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")


class CartItem(TimestampMixin, Base):
    __tablename__ = "commerce_cart_items"
    __table_args__ = (
        UniqueConstraint("cart_id", "sku_id", name="uq_commerce_cart_sku"),
        CheckConstraint("quantity > 0", name="ck_commerce_cart_items_quantity"),
        CheckConstraint(
            "unit_price_snapshot_paise IS NULL OR unit_price_snapshot_paise >= 0",
            name="ck_cart_item_price_snapshot",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    cart_id: Mapped[str] = mapped_column(ForeignKey("commerce_carts.id", ondelete="CASCADE"), nullable=False)
    sku_id: Mapped[str] = mapped_column(ForeignKey("commerce_skus.id", ondelete="RESTRICT"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    unit_price_snapshot_paise: Mapped[int | None] = mapped_column(BigInteger)
    price_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    inventory_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    cart: Mapped[Cart] = relationship(back_populates="items")


class AuditEvent(Base):
    __tablename__ = "commerce_audit_events"
    __table_args__ = (
        Index("ix_commerce_audit_entity", "entity_type", "entity_id", "occurred_at"),
        Index("ix_commerce_audit_actor", "actor_user_id", "occurred_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    actor_user_id: Mapped[str | None] = mapped_column(ForeignKey("commerce_users.id", ondelete="SET NULL"))
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(80), nullable=False)
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(80))
    payload: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)
