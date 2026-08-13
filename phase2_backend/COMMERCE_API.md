# CropPulse Versioned Commerce API

The isolated commerce service is exposed under `/api/commerce/v1`. It is separate from the legacy `/api/v1` and demo `/api/v2` surfaces so mobile commerce contracts can evolve without silently changing farmer/trader tools.

## Run locally

```bash
uvicorn phase2_backend.commerce.api:app --reload
```

Local interactive documentation is available at:

```text
/api/commerce/v1/docs
```

Documentation is disabled by default when `ENV=production`. It may be enabled only through the explicit `COMMERCE_ENABLE_DOCS=true` setting in a reviewed environment.

## Current endpoints

```text
GET  /api/commerce/v1/health
GET  /api/commerce/v1/readiness

GET  /api/commerce/v1/auth/readiness
POST /api/commerce/v1/auth/otp/request
POST /api/commerce/v1/auth/otp/verify
POST /api/commerce/v1/auth/refresh
POST /api/commerce/v1/auth/logout
GET  /api/commerce/v1/auth/me

GET  /api/commerce/v1/catalog/categories
GET  /api/commerce/v1/catalog/products
GET  /api/commerce/v1/catalog/products/{slug}

GET    /api/commerce/v1/serviceability?pincode={pincode}
GET    /api/commerce/v1/addresses
POST   /api/commerce/v1/addresses
PATCH  /api/commerce/v1/addresses/{address_id}
DELETE /api/commerce/v1/addresses/{address_id}
POST   /api/commerce/v1/addresses/{address_id}/default

POST   /api/commerce/v1/cart/guest
GET    /api/commerce/v1/cart
PATCH  /api/commerce/v1/cart
POST   /api/commerce/v1/cart/items
PATCH  /api/commerce/v1/cart/items/{item_id}
DELETE /api/commerce/v1/cart/items/{item_id}
POST   /api/commerce/v1/cart/validate
POST   /api/commerce/v1/cart/merge
POST   /api/commerce/v1/checkout/quote
POST   /api/commerce/v1/orders
GET    /api/commerce/v1/orders
GET    /api/commerce/v1/orders/{order_id}
POST   /api/commerce/v1/orders/{order_id}/cancel
```

Catalog browsing is intentionally available to guests. Account and future mutation endpoints require authenticated server-side authorization.

## Request IDs and errors

Every response contains an `X-Request-ID`. A client-supplied identifier is accepted only when it matches the constrained format; otherwise the API generates a UUID.

Errors use one stable envelope:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "request_id": "catalog-contract-test-123",
    "details": [
      {
        "location": ["query", "limit"],
        "message": "Input should be greater than or equal to 1",
        "type": "greater_than_equal"
      }
    ]
  }
}
```

Unhandled exceptions are logged with the request ID, while responses contain no stack trace or internal exception text.

## Catalog contract

Category and product names use the requested locale when an approved translation exists, with the default name as fallback.

Product listing supports:

- `locale`: `en` or another configured language code.
- `category`: exact category slug.
- `query`: product-name search, including localized names.
- `limit`: 1-50 products.
- `cursor`: opaque keyset cursor returned by the previous page.

Only active categories, products, and SKUs are returned. Draft, paused, recalled, archived, or otherwise non-sellable records remain hidden.

Effective consumer pricing is read from the active price list configured by `COMMERCE_CONSUMER_PRICE_LIST_CODE`, which defaults to `consumer-inr`. Prices are returned as integer minor units (`amount_paise`) with currency and effective timestamps.

Pincode serviceability can now be checked independently, but catalog inventory is still not inferred from it. Until the client supplies a selected service zone to a future inventory-aware catalog/cart contract, every SKU returns:

```json
{
  "availability": {
    "status": "location_required",
    "available_quantity": null,
    "checked_at": null
  },
  "purchasable": false
}
```

This prevents a catalog record or price from being mistaken for confirmed sellable stock.

## Readiness semantics

- `/health` is a process liveness check and does not claim external readiness.
- `/readiness` reports database and authentication configuration separately.
- `ready=true` requires a database connection and configured authentication provider.
- Provider credentials being present does not prove SMS delivery or hosted production activation.

## Current boundary

Implemented locally:

- Versioned API entrypoint.
- Request correlation and stable error contracts.
- Authentication endpoints.
- Read-only localized category/product endpoints.
- Effective consumer-price selection.
- Cursor pagination and constrained query inputs.
- Liveness/readiness separation.

Implemented as a separate review-only increment:

- An idempotent draft seed containing 6 categories and 12 product/SKU candidates.
- The seed remains hidden, inactive, and separate from consumer pricing until operational approval.

Still separate future increments:

- Expansion and operational approval of the final 75-150 SKU pilot catalog.
- Location-aware inventory availability.
- Checkout, orders, payments, fulfilment, and refunds.
- Flutter API integration.

## Verification

```bash
python -m pytest phase2_backend -q
python -m black --check phase2_backend/commerce phase2_backend/migrations
python -m flake8 phase2_backend/commerce phase2_backend/migrations --max-line-length=120
python -m mypy phase2_backend/commerce --ignore-missing-imports
```

Catalog tests create temporary contract records in an isolated database. They do not install or imply approval of the future pilot catalog.
