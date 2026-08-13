"""Enforce one active default address per commerce user.

Revision ID: 20260813_0003
Revises: 20260813_0002
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260813_0003"
down_revision: str | None = "20260813_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "uq_commerce_addresses_active_default",
        "commerce_addresses",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("is_active AND is_default"),
        sqlite_where=sa.text("is_active = 1 AND is_default = 1"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_commerce_addresses_active_default",
        table_name="commerce_addresses",
    )
