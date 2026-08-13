"""Add checkout reservations and the immutable customer order ledger.

Revision ID: 20260813_0005
Revises: 20260813_0004
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260813_0005"
down_revision: str | None = "20260813_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ORDER_TABLE_NAMES = {
    "commerce_orders",
    "commerce_order_items",
    "commerce_inventory_reservations",
    "commerce_order_events",
}


def upgrade() -> None:
    from phase2_backend.commerce.models import Base

    bind = op.get_bind()
    existing = set(sa.inspect(bind).get_table_names())
    for table in Base.metadata.sorted_tables:
        if table.name in ORDER_TABLE_NAMES and table.name not in existing:
            table.create(bind=bind)


def downgrade() -> None:
    from phase2_backend.commerce.models import Base

    bind = op.get_bind()
    existing = set(sa.inspect(bind).get_table_names())
    tables = [table for table in Base.metadata.sorted_tables if table.name in ORDER_TABLE_NAMES]
    for table in reversed(tables):
        if table.name in existing:
            table.drop(bind=bind)
