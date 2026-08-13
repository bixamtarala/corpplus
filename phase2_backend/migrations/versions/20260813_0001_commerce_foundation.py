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


def upgrade() -> None:
    # The declarative models are the reviewed schema source. Creating from the
    # shared metadata keeps the initial migration and runtime types aligned.
    from phase2_backend.commerce.models import Base

    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)

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
    Base.metadata.drop_all(bind=bind)
