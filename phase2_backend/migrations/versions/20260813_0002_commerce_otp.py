"""Add persistent commerce OTP challenges.

Revision ID: 20260813_0002
Revises: 20260813_0001
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260813_0002"
down_revision: str | None = "20260813_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "commerce_otp_challenges",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("phone_hash", sa.String(length=64), nullable=False),
        sa.Column("request_ip_hash", sa.String(length=64), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("provider_reference", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("failed_attempts", sa.Integer(), nullable=False),
        sa.Column("max_attempts", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('requested', 'consumed', 'failed', 'expired')",
            name="ck_commerce_otp_challenges_status",
        ),
        sa.CheckConstraint(
            "failed_attempts >= 0 AND failed_attempts <= max_attempts",
            name="ck_commerce_otp_challenges_attempts",
        ),
        sa.CheckConstraint(
            "max_attempts >= 1 AND max_attempts <= 10",
            name="ck_commerce_otp_challenges_max_attempts",
        ),
        sa.CheckConstraint("expires_at > created_at", name="ck_commerce_otp_challenges_expiry"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider_reference"),
    )
    op.create_index(
        "ix_commerce_otp_phone_created",
        "commerce_otp_challenges",
        ["phone_hash", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_commerce_otp_ip_created",
        "commerce_otp_challenges",
        ["request_ip_hash", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_commerce_otp_ip_created", table_name="commerce_otp_challenges")
    op.drop_index("ix_commerce_otp_phone_created", table_name="commerce_otp_challenges")
    op.drop_table("commerce_otp_challenges")
