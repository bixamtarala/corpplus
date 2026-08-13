# Persistent commerce cart

This increment provides persistent guest and authenticated carts under `/api/commerce/v1/cart`. Cart contents, current prices, inventory availability, quantity rules, and delivery serviceability are owned and recalculated by the server. It is implemented and tested locally; no hosted database or inventory operation is activated.

## Routes

```text
POST   /api/commerce/v1/cart/guest
GET    /api/commerce/v1/cart
PATCH  /api/commerce/v1/cart
POST   /api/commerce/v1/cart/items
PATCH  /api/commerce/v1/cart/items/{item_id}
DELETE /api/commerce/v1/cart/items/{item_id}?expected_version={version}
POST   /api/commerce/v1/cart/validate
POST   /api/commerce/v1/cart/merge
```

Authenticated requests use `Authorization: Bearer ...`. Guest requests use `X-Guest-Cart-Token`. When an Authorization header is present, authenticated ownership takes precedence; the guest token is consumed only by `/cart/merge`.

## Guest restoration and login merge

`POST /cart/guest` creates an opaque, high-entropy token. The raw token is returned only in that creation response; the database stores only its SHA-256 hash. The Flutter client must retain the raw token in secure device storage and send it when restoring or mutating the guest cart. Guest carts expire after 30 days by default through `COMMERCE_GUEST_CART_TTL_DAYS`.

After OTP login, call `POST /cart/merge` with both the access token and guest-cart token. Quantities for matching SKUs are added without silently rounding or discarding either cart. The source guest cart becomes `converted`, so the same token cannot merge twice. The returned authenticated cart is revalidated and may require the customer to correct an invalid combined quantity or select a saved address.

## Location rules

- Guest carts select a six-digit pincode.
- Authenticated carts select an active saved address owned by that customer.
- The pincode is persisted and rechecked on every restoration or validation.
- A deleted authenticated address clears the cart location.
- A paused, disabled, missing, or ambiguous service-zone mapping prevents checkout.
- Guest location is not copied into an authenticated cart during login merge; the customer must use a saved address.

## Server validation

Every response contains `valid_for_checkout`, `validation_status`, cart-level issues, item-level issues, current subtotal and `validated_at`.

The server checks:

- category, product, and SKU active status;
- active consumer price and price changes;
- minimum order quantity and quantity-step alignment;
- available quantity summed only across active hub/supplier locations in the selected service zone;
- pincode serviceability and service-zone minimum order value.

Price changes are informational and immediately reflected in the returned subtotal. Missing price, invalid quantity, insufficient inventory, missing location, unserviceable location, and unmet zone minimums are blocking errors. Inventory validation is a point-in-time check, not a reservation; checkout must validate and reserve stock transactionally in a later increment.

Mutations require `expected_version`. A stale version returns HTTP 409, forcing the client to restore the latest cart before retrying and preventing silent lost updates.

## Validation

```powershell
python -m pytest phase2_backend/test_commerce_cart.py -q
python -m pytest phase2_backend -q
python -m black --check phase2_backend/commerce phase2_backend/migrations
python -m flake8 phase2_backend/commerce phase2_backend/migrations --max-line-length=120
python -m mypy phase2_backend/commerce --ignore-missing-imports
```

## Still required

- Apply migrations to the eventual hosted PostgreSQL database (currently deferred).
- Load approved service zones, active catalog pricing, and real inventory balances.
- Add infrastructure-level abuse/rate controls for guest-cart creation.
- Integrate Flutter secure token storage, cart restoration, merge, address selection, and localized issue messages.
- Implement checkout quoting, inventory reservation, order idempotency, and expiry cleanup jobs.
