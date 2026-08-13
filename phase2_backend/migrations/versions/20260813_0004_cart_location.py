"""Persist cart delivery pincode for restoration-time validation.

Revision ID: 20260813_0004
Revises: 20260813_0003
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op


revision: str = "20260813_0004"
down_revision: str | None = "20260813_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Migration 0001 uses the current declarative metadata for a brand-new
    # database, so fresh installs already have this column. Existing databases
    # created before the cart increment require the explicit ALTER below.
    if context.is_offline_mode():
        op.execute("ALTER TABLE commerce_carts ADD COLUMN IF NOT EXISTS delivery_pincode VARCHAR(6)")
        return
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns("commerce_carts")}
    if "delivery_pincode" not in columns:
        op.add_column(
            "commerce_carts",
            sa.Column("delivery_pincode", sa.String(length=6), nullable=True),
        )


def downgrade() -> None:
    if context.is_offline_mode():
        op.execute("ALTER TABLE commerce_carts DROP COLUMN IF EXISTS delivery_pincode")
        return
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns("commerce_carts")}
    if "delivery_pincode" in columns:
        op.drop_column("commerce_carts", "delivery_pincode")
