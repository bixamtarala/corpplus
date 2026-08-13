# Commerce checkout and order ledger

This increment adds authenticated, server-authoritative checkout and a durable
customer order ledger under `/api/commerce/v1`. It is implemented and tested
locally; it does not activate a payment gateway, hosted database, or fulfilment
operation.

## API

```text
POST /api/commerce/v1/checkout/quote
POST /api/commerce/v1/orders
GET  /api/commerce/v1/orders
GET  /api/commerce/v1/orders/{order_id}
POST /api/commerce/v1/orders/{order_id}/cancel
```

All routes require an authenticated customer. Order creation additionally
requires an `Idempotency-Key` header of 16-128 safe characters. Repeating the
same key and payload returns the original order; reusing the key with different
checkout details returns HTTP 409.

## Authoritative calculation

The client sends only the expected cart version, COD payment method,
substitution preference, and an optional note. The server locks and revalidates
the authenticated cart, current price, SKU state, serviceability, MOQ/step,
inventory, and minimum-order rules. It calculates:

- item subtotal from current integer-paise prices and decimal quantities;
- tax per line from the SKU basis-point rate with half-up paise rounding;
- service-zone delivery fee;
- discount (currently zero until an approved promotion engine exists); and
- final payable total.

No client-supplied price, tax, fee, discount, or total is accepted.

## Order and inventory transaction

Order confirmation atomically:

1. snapshots the delivery address and product/price/tax lines;
2. allocates inventory under balance row locks;
3. increments `reserved_quantity` and writes reservation rows;
4. writes the first immutable `order.confirmed` event and audit records; and
5. converts the source cart so it cannot be purchased twice.

The initial payment method is COD only. Online payment is deliberately rejected
by the API schema until a real provider, signature verification, webhook
idempotency, and reconciliation process are implemented.

Customers can list and inspect only their own orders. A confirmed order can be
cancelled idempotently; active reservations are released and an
`order.cancelled` event is appended. Processing/fulfilled cancellation policy
will be added with the operations workflow.

## Tables and migration

Migration `20260813_0005` adds:

- `commerce_orders`
- `commerce_order_items`
- `commerce_inventory_reservations`
- `commerce_order_events`

Apply the migration to the eventual hosted PostgreSQL database only after the
deployment environment is approved.

## Local verification

```powershell
python -m pytest phase2_backend/test_commerce_orders.py `
  phase2_backend/test_commerce_cart.py `
  phase2_backend/test_commerce_database.py -q
```

The focused assertions pass (16 tests). On the current Windows environment,
pytest can remain alive after printing 100% because the FastAPI TestClient
worker does not terminate; that runner-cleanup issue is separate from the
assertion results and should be fixed in CI/tooling before treating the suite as
a clean release gate.

## Still pending

- delivery-slot capacity and delivery promise selection;
- approved coupon/promotion calculations;
- online payment intents, webhooks, refunds, and reconciliation;
- fulfilment status transitions and operations authorization;
- reservation expiry/consumption workers and stock-release monitoring;
- Flutter checkout, order history, cancellation, and localized states;
- hosted PostgreSQL migration and physical-device end-to-end testing.
