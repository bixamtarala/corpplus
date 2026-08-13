# Commerce addresses and serviceability

This increment adds customer-owned saved addresses and server-authoritative delivery coverage under `/api/commerce/v1`. It is implemented and tested locally; it does not activate any hosted database or real delivery area.

## API routes

```text
GET    /api/commerce/v1/serviceability?pincode=560001
GET    /api/commerce/v1/addresses
POST   /api/commerce/v1/addresses
PATCH  /api/commerce/v1/addresses/{address_id}
DELETE /api/commerce/v1/addresses/{address_id}
POST   /api/commerce/v1/addresses/{address_id}/default
```

All address routes require an access token. The serviceability route is public so a customer can check coverage before authentication.

## Serviceability contract

The API validates a six-digit Indian pincode and returns one of three explicit states:

- `serviceable`: one enabled pincode mapping belongs to one active service zone. The response includes the zone, currency, minimum order, and delivery fee.
- `temporarily_unavailable`: a mapping exists but it or its zone is paused/disabled.
- `not_serviceable`: no usable mapping exists.

The `serviceable` boolean is included for simple mobile branching. A pincode mapped to more than one active zone fails closed with HTTP 503 so an ambiguous fulfilment route is never selected silently.

No pincode is serviceable by default. Operations must create and review service-zone mappings before launch.

## Address behavior

- The first active address becomes the default automatically.
- Creating with `make_default: true`, updating with `make_default: true`, or calling the default route moves the default atomically.
- A partial database index enforces at most one active default per user.
- Deleting is a soft delete. If the default is deleted, the oldest remaining active address becomes the default.
- Address IDs are always scoped to the authenticated owner; another customer's address returns 404.
- An unserviceable address may still be saved. Address responses always include the current serviceability decision.
- Recipient phone numbers are normalized to Indian E.164 form. Audit events contain only action metadata, not address PII.

## Validation

```powershell
python -m pytest phase2_backend/test_commerce_addresses.py -q
python -m pytest phase2_backend -q
python -m black --check phase2_backend/commerce phase2_backend/migrations
python -m flake8 phase2_backend/commerce phase2_backend/migrations --max-line-length=120
python -m mypy phase2_backend/commerce --ignore-missing-imports
```

## Operational work still required

- Decide the launch districts and approved pincodes.
- Load reviewed service zones and fees through an operations-controlled process.
- Apply migrations to the eventual hosted PostgreSQL database (currently deferred).
- Integrate the Flutter address selector and localized status messages.
- Measure delivery promises separately; this contract intentionally does not invent an ETA.
