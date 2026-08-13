"""Create the CropPulse commerce Slice 2 foundation.

Revision ID: 20260813_0001
Revises: None
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260813_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

FOUNDATION_TABLE_NAMES = {
    "commerce_addresses",
    "commerce_audit_events",
    "commerce_cart_items",
    "commerce_carts",
    "commerce_categories",
    "commerce_category_translations",
    "commerce_inventory_balances",
    "commerce_inventory_locations",
    "commerce_prices",
    "commerce_price_lists",
    "commerce_product_media",
    "commerce_product_translations",
    "commerce_products",
    "commerce_service_zone_pincodes",
    "commerce_service_zones",
    "commerce_sessions",
    "commerce_skus",
    "commerce_users",
}


def upgrade() -> None:
    # The declarative models are the reviewed schema source. Creating from the
    # shared metadata keeps the initial migration and runtime types aligned.
    from phase2_backend.commerce.models import Base

    bind = op.get_bind()
    for table in Base.metadata.sorted_tables:
        if table.name in FOUNDATION_TABLE_NAMES:
            table.create(bind=bind)

    # PostgreSQL-only partial indexes enforce one active cart per owner while
    # still preserving converted/expired cart history.
    if bind.dialect.name == "postgresql":
        op.create_index(
            "uq_commerce_active_cart_user",
            "commerce_carts",
            ["user_id"],
            unique=True,
            postgresql_where=sa.text("status = 'active' AND user_id IS NOT NULL"),
        )
        op.create_index(
            "uq_commerce_active_cart_guest",
            "commerce_carts",
            ["guest_token_hash"],
            unique=True,
            postgresql_where=sa.text("status = 'active' AND guest_token_hash IS NOT NULL"),
        )


def downgrade() -> None:
    from phase2_backend.commerce.models import Base

    bind = op.get_bind()
    foundation_tables = [table for table in Base.metadata.sorted_tables if table.name in FOUNDATION_TABLE_NAMES]
    for table in reversed(foundation_tables):
        table.drop(bind=bind)
