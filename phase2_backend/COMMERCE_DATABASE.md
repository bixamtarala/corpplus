# CropPulse Commerce Database

This directory contains the isolated PostgreSQL foundation for mobile commerce Slice 2. The tables use the `commerce_` prefix so the new catalog/cart/auth work does not silently alter the legacy farmer/trader demo schema.

## Configuration

Set one of the following environment variables:

```text
COMMERCE_DATABASE_URL=postgresql://user:password@host:5432/croppulse
DATABASE_URL=postgresql://user:password@host:5432/croppulse
```

`COMMERCE_DATABASE_URL` takes precedence. Production fails closed when neither value is configured. Credentials belong in the deployment provider's secret store, never in tracked files.

## Apply the migration

From the repository root:

```bash
alembic -c phase2_backend/alembic.ini upgrade head
```

Review the generated PostgreSQL SQL without connecting:

```bash
alembic -c phase2_backend/alembic.ini upgrade head --sql
```

Rollback is available for development only:

```bash
alembic -c phase2_backend/alembic.ini downgrade base
```

Do not run a destructive downgrade against production. Production changes require a backup, reviewed migration plan, maintenance/rollout decision, and post-migration verification.

## Foundation tables

- Customers and refresh sessions
- Persistent provider-backed OTP challenges
- Addresses and service-zone pincodes
- Categories and translations
- Products, translations, and media
- SKUs and fixed-precision pack/MOQ data
- Price lists and effective integer-paise prices
- Inventory locations and constrained balances
- Guest or signed-in carts and cart items
- Append-oriented audit events

The initial migration also creates PostgreSQL partial unique indexes that permit only one active cart for a signed-in customer or guest token while preserving historical carts.

## Verification

Focused model tests use an in-memory SQLite database for fast constraint and metadata checks:

```bash
python -m pytest phase2_backend/test_commerce_database.py -q
```

SQLite tests do not prove that a production PostgreSQL migration was applied. Before activation, run the migration against an isolated PostgreSQL environment and verify table, constraint, index, backup, restore, connection-pool, and least-privilege behavior.

## Still pending

- Hosted PostgreSQL application and production connection verification
- Inventory lots and expiring reservations
- Delivery capacity and slot tables
- Checkout quotes, orders, order lines, and state transitions
- Payments, refunds, issues, invoices, and settlements
- Organizations, memberships, business verification, and B2B price assignments
- Operations authorization and row-level access policy
- Seed data for the approved pilot geography and catalog
