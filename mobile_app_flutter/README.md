# CropPulse Mobile Commerce

CropPulse is an Android-first agricultural commerce application for household buyers, business buyers, farmers, FPOs, suppliers, and fulfilment teams. The long-term product direction supports B2C, B2B, and B2B2C commerce, but the first operational release is intentionally a managed marketplace in one controlled launch area.

This README is the mobile app's status and delivery source of truth. Detailed product requirements and screen behavior are maintained in:

- [Commerce Phase 1 PRD](CROPPULSE_COMMERCE_PHASE1_PRD.md)
- [Commerce screen blueprint](CROPPULSE_COMMERCE_SCREEN_BLUEPRINT.md)

## Product strategy

The first live release should allow a customer to:

1. Sign in with a real mobile OTP.
2. Select a serviceable delivery address.
3. Browse a server-managed catalog of agricultural products.
4. See verified pack, price, source, quality, stock, and delivery information.
5. Add available SKUs to a persistent cart.
6. Place and track an order.
7. Report a fulfilment issue and receive a clear refund or replacement outcome.

CropPulse operations will control supplier approval, catalog moderation, sellable inventory, fulfilment, support, refunds, and settlement approval. B2B pricing and ordering will be added after the core B2C ledger is reliable. B2B2C reseller storefronts and ONDC integration are later phases.

## Current status

Status snapshot: 13 August 2026.

| Area | Current state | Production status |
| --- | --- | --- |
| Buyer navigation | Five tabs: Home, Categories, Search, Cart, Account | Preview implemented |
| Catalog | Read-only API plus an idempotent, inactive 12-product draft review seed; Flutter still shows local preview products | Final 75-150 SKUs, activation, media, suppliers, declarations, and inventory remain unapproved |
| Product discovery | Home sections, category browsing, multilingual-name search, product details | Preview implemented |
| Location | Six-digit pincode capture plus versioned service-zone validation and saved-address API | Flutter still uses the local location screen; launch zones are not operationally loaded |
| Cart | Persistent guest/authenticated backend, restoration, login merge, authoritative validation; Flutter preview cart still supports local mutations | Flutter secure-token storage and API integration remain pending |
| Checkout | Deliberately disabled | Not implemented |
| Authentication | Provider-backed OTP service, persistent challenges, rotating sessions, and `/api/commerce/v1` auth routes implemented locally | Flutter still uses legacy `/api/v2`; Twilio and hosted database are not activated |
| Commerce database | Isolated SQLAlchemy models and initial Alembic migration for 18 `commerce_*` tables | Implemented locally; not yet applied to a hosted PostgreSQL database |
| Orders and payments | Product requirements and screen states documented | Not implemented |
| Operations | Fulfilment workflow documented | No operations console or live workflow |
| B2B/B2B2C | Architecture direction documented | Not implemented |
| Legacy tools | Farmer, Trader, Intelligence, Marketplace, and Profile remain accessible through Account | Existing demo/API behavior retained |
| Android build | Debug APK built and verified | Internal testing only |
| iOS | Outside Phase 1 scope | Not available |

Approximate product maturity based on the current implementation:

- Storefront experience: 35-40%
- Production commerce backend: 10-15%
- Fulfilment and support operations: below 10%
- Overall production readiness: below 15%

These percentages describe breadth, not quality or launch approval. A working preview screen or successful APK build does not prove live inventory, payments, fulfilment, provider configuration, or physical-device readiness.

## What is implemented

### Buyer storefront foundation

- Fixed buyer navigation: Home, Categories, Search, Cart, and Account.
- Preview categories: vegetables, fruits, leafy greens, rice and millets, pulses, and spices.
- Preview catalog with product name, pack label, indicative price, grade/source placeholders, and descriptions.
- Product names in English, Hindi, and Telugu where currently supplied.
- Search across product names, localized product names, and category names.
- Product detail routes and reusable product cards.
- Pincode input with clear notice that pilot availability is not yet confirmed.
- Riverpod cart state with quantity controls and an indicative subtotal.
- Explicit preview notices and a disabled checkout button to prevent false live-commerce claims.

### Existing agriculture tools

The pre-commerce Farmer, Trader, Customer, Intelligence, Marketplace, and Profile features are preserved under the commerce Account experience. They currently depend on the existing `/api/v2` backend and should be treated as demo or pilot tools until their contracts and persistence are replaced or approved.

### Application foundation

- Flutter 3.41.9 and Dart 3.11.5.
- Riverpod state management.
- Dio HTTP client.
- English, Hindi, and Telugu localization framework.
- In-app update metadata check.
- Android package: `com.croppulse.mobile`.
- Current app version: `1.0.2+4`.

## Important limitations

- Products, prices, grades, and sources in the commerce catalog are preview data.
- Product media is represented by category icons rather than approved product images.
- A valid pincode format does not mean the location is serviceable.
- Cart contents are lost when the app process is restarted.
- Totals are calculated locally for demonstration and are not authoritative.
- There is no SKU/lot inventory reservation or protection against overselling.
- There are no delivery slots, coupons, taxes, invoices, substitutions, payments, orders, refunds, or settlements.
- Several new commerce labels still require Hindi and Telugu translations.
- The default API URL is `http://10.0.2.2:8000`, which is suitable for an Android emulator only.
- The current `/api/v2` backend contains mock/sample behavior, including non-production OTP handling and incomplete persistence.
- Authentication tokens currently use app preferences and must move to secure device storage before launch.
- No claim about freshness, organic status, quality, source, price, or delivery should be shown unless backed by reviewed operational data.

## Recommended next implementation milestone

The next milestone is **Commerce Slice 2: real identity, catalog, serviceability, and persistent cart**.

Definition of done:

> A customer authenticates with a real OTP, selects a serviceable address, loads approved products from PostgreSQL, adds available SKUs to a persistent cart, closes and reopens the app, and sees a restored cart that the server revalidates for price, stock, minimum quantity, and serviceability.

Checkout should remain disabled until this milestone is stable.

### 1. Confirm operating decisions

Before live data is entered, record these decisions:

- Pilot city/district and exact serviceable pincodes.
- Seller/invoicing model: CropPulse seller, managed marketplace, or approved hybrid.
- Initial 75-150 SKUs, standard packs, units, grades, and price owner.
- Collection/fulfilment hub and delivery operating model.
- Online payment, COD eligibility, cancellation, substitution, refund, fee, and tax policy.
- B2B verification requirements and initial buyer types.

Legal and tax professionals must approve the seller of record, GST/invoice treatment, supplier settlement structure, and regulated product scope before live payments.

### 2. Build a production commerce backend

Create a versioned commerce API backed by PostgreSQL. Do not evolve the current sample `/api/v2` service into production merely by adding checkout routes.

Database foundation status: the isolated commerce models, Alembic migrations, environment configuration, constraints, and focused tests are implemented under `phase2_backend/commerce` and `phase2_backend/migrations`. Deployment to hosted PostgreSQL and non-authentication commerce API routes are still pending.

Authentication foundation status: the versioned commerce auth routes, Twilio Verify provider integration, persistent one-time challenges, request/attempt limits, short-lived access tokens, rotating refresh tokens, logout revocation, and focused tests are implemented locally. Provider credentials, hosted migration, physical SMS verification, and Flutter integration remain pending.

Versioned API status: the `/api/commerce/v1` entrypoint now provides request IDs, stable error envelopes, liveness/readiness separation, and read-only localized category/product routes with effective consumer prices and cursor pagination. Final catalog approval, serviceability-confirmed inventory, mutations, and Flutter integration remain pending.

Pilot seed status: a 6-category, 12-product/SKU draft catalog can be previewed or applied idempotently. All records remain inactive/draft, prices remain indicative in a separate inactive price list, and no stock, serviceability, supplier, origin, grade, or product-image claims are seeded. Operational review and expansion to the final assortment remain pending.

Address and serviceability status: authenticated create/edit/delete/default address routes and a public pincode check are implemented locally. Responses distinguish `serviceable`, `temporarily_unavailable`, and `not_serviceable`; address ownership, soft deletion, default promotion, audit metadata, and ambiguous-zone fail-closed behavior are covered by tests. Launch-zone data, hosted migration, and Flutter integration remain pending. See `phase2_backend/COMMERCE_ADDRESSES.md`.

Persistent cart status: guest and authenticated carts, secure guest restoration tokens, optimistic versions, saved-address/pincode context, item mutations, login merge, and server-side price, inventory, MOQ/step, serviceability, and zone-minimum validation are implemented locally. Inventory checks do not reserve stock. Hosted migration, live inventory feeds, cleanup jobs, checkout reservation, and Flutter integration remain pending. See `phase2_backend/COMMERCE_CART.md`.

Minimum initial data model:

- `users` and authenticated sessions
- `addresses` and `service_zones`
- `categories` and translations
- `products` and product translations
- `skus` and product media
- `price_lists` and effective prices
- `inventory_locations` and inventory balances
- `carts` and `cart_items`
- `audit_events`

Later slices add inventory lots/reservations, orders, order lines, payments, refunds, fulfilment events, issues, invoices, suppliers, settlements, organizations, and B2B price tiers.

### 3. Replace mock authentication

- Integrate a real Indian mobile OTP provider.
- Enforce OTP expiry, one-time use, resend cooldown, attempt limits, and phone/IP rate limits.
- Return enumeration-safe request responses.
- Add access-token expiry, refresh/session rotation, logout, and revocation.
- Store credentials in secure platform storage, never plain preferences.
- Keep guest browsing available and restore the protected action after sign-in.
- Block mock OTP behavior and emulator API URLs in release builds.

### 4. Make the catalog server-driven

Every purchasable SKU should include:

- Product and localized names.
- Category/subcategory and approved media.
- Pack quantity, unit of measure, selling price, and unit price.
- Availability, inventory timestamp, and delivery promise.
- Source/seller, origin, quality grade, and grading standard when verified.
- Lot/batch traceability internally.
- Storage, shelf-life, return/replacement, and substitution information.
- Required FSSAI, packaged-product, tax, or licence declarations.
- B2B MOQ and tier pricing when applicable.

The UI must implement loading, empty, offline, timeout, partial-data, unavailable, stale-price, and stale-inventory states.

### 5. Implement addresses and serviceability

- Saved address create/edit/delete and default selection.
- Pincode plus service-zone, hub-capacity, delivery-date, and product-restriction checks.
- Browsing outside the service area may remain available, but checkout must be blocked with a clear reason.
- Display the selected address and earliest reliable delivery promise throughout discovery and cart.

### 6. Implement a persistent, validated cart

- Guest cart stored locally, then safely merged after sign-in.
- Signed-in cart stored on the server and restored across devices/sessions.
- Server-authoritative price, discount, fee, tax, and total calculations using decimal-safe money values.
- Revalidation for inventory, reservations, serviceability, MOQ, quantity limits, and price changes.
- Idempotent mutations and conflict handling.
- Clear user action when an item becomes unavailable or changes price.

### 7. Complete localization and accessibility

- Move every new commerce label and message into localization resources.
- Review English, Hindi, and Telugu at narrow Android widths.
- Maintain semantic labels, keyboard/focus behavior where relevant, readable contrast, and minimum touch targets.
- Use localized units, quantities, currency, dates, and delivery messages.

### 8. Strengthen mobile CI

Add these checks before treating a mobile build as releasable:

- Dart formatting check.
- `flutter analyze` with no new warnings.
- `flutter test`.
- Debug APK build on pull requests.
- Release APK/AAB build only from approved release configuration.
- API contract tests against the commerce schema.
- Guardrails that reject mock OTP and emulator/local API URLs in release builds.
- Artifact upload with commit, version, signature, and checksum evidence.

## Delivery roadmap

| Slice | Outcome | Key scope |
| --- | --- | --- |
| 1. Storefront foundation | Browse a safe preview catalog | Implemented: buyer shell, catalog, search, product details, preview cart |
| 2. Identity and reliable cart | Real customer, location, catalog, and recoverable cart | Database, OTP, shared API, read-only catalog, inactive draft seed, address/serviceability, and persistent cart APIs implemented locally; final catalog approval, hosted activation, and mobile integration remain |
| 3. Checkout and order ledger | Create a non-duplicated payable order | Delivery slots, substitution preference, coupons, tax/fees, COD/online payment, idempotent order creation, order history |
| 4. Fulfilment operations | Reliably receive, pack, dispatch, and deliver | Supplier intake, grading, lots, reservations, pick/pack, proof of delivery, notifications |
| 5. Resolution and reconciliation | Resolve failures and close financial records | Issues, partial fulfilment, replacements, refunds, invoices, supplier settlement, audit trail |
| 6. B2B commerce | Serve verified organizations | Organization/KYC/GST review, MOQ, tier prices, bulk units, PO reference, scheduled delivery, statements |
| 7. B2B2C and network expansion | Add controlled reseller/network models | Reseller storefronts, commission controls, multi-hub routing, ONDC only after core operations are proven |

### Work that should not be prioritized yet

- Adding more hardcoded products or preview prices.
- Integrating payments before inventory reservation and the order ledger exist.
- Launching nationwide or adding multiple hubs before one pilot works reliably.
- B2B2C reseller features before B2C fulfilment and refunds are stable.
- ONDC production integration.
- AI price, demand, yield, freshness, or quality claims without verified data and provenance.
- Regulated farm inputs without licences and compliance controls.
- Play Store public release before production API, signing, provider, migration, and physical-device gates pass.

## Proposed API boundary

The exact paths may change during contract design, but the client should consume a dedicated versioned commerce surface with responsibilities similar to:

```text
POST   /api/commerce/v1/auth/otp/request
POST   /api/commerce/v1/auth/otp/verify
POST   /api/commerce/v1/auth/refresh

GET    /api/commerce/v1/serviceability
GET    /api/commerce/v1/addresses
POST   /api/commerce/v1/addresses

GET    /api/commerce/v1/catalog/categories
GET    /api/commerce/v1/catalog/products
GET    /api/commerce/v1/catalog/products/{slug}

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
```

Mutation endpoints must support idempotency, authorization, audit records, and safe retries. The backend—not the app—must be authoritative for prices, inventory, eligibility, totals, and order state.

## Local development

From `mobile_app_flutter`:

```bash
flutter pub get
flutter analyze
flutter test
flutter run
```

To use a non-default API:

```bash
flutter run --dart-define=CROPPULSE_API_BASE_URL=https://api.example.com
```

The default `http://10.0.2.2:8000` points from an Android emulator to a backend running on the development computer. It is not a production endpoint.

## Local Android builds

```bash
flutter build apk --debug
flutter build apk --release
flutter build appbundle --release
```

Expected build outputs:

- `build/app/outputs/flutter-apk/app-debug.apk`
- `build/app/outputs/flutter-apk/app-release.apk`
- `build/app/outputs/bundle/release/app-release.aab`

## Latest verified internal APK

The current repository artifact is for internal review only:

- File: `artifacts/mobile/CropPulse-1.0.2-build4-e1e845c-internal.apk`
- Source commit: `e1e845cd3b8ba8423f506efe8e779ea79e7e00c9`
- Package: `com.croppulse.mobile`
- Version: `1.0.2` (`versionCode 4`)
- Minimum Android SDK: 24
- Target/compile Android SDK: 36
- Architectures: `arm64-v8a`, `armeabi-v7a`, `x86_64`
- Size: 59,663,089 bytes
- SHA-256: `32982B418063C9F4495696908155A34C441E5B949D0B6B660D90503606C24BED`
- Signature: Android debug certificate; APK Signature Scheme v2 verified

This APK is debug-signed and must not be uploaded to Google Play or described as a production release. A production artifact requires an approved upload key, production API configuration, real provider credentials, applied database migrations, release checks, and physical-device testing.

## GitHub Android delivery

The workflow at `.github/workflows/mobile-android.yml` runs on pushes to `main` and by manual dispatch. It can:

- Build a release APK.
- Publish/update the rolling prerelease `mobile-latest` with APK and update metadata.
- Build a signed AAB when Android signing secrets are configured.
- Send the APK to Firebase App Distribution when Firebase secrets are configured.
- Upload the signed AAB to Google Play internal testing when Play and signing secrets are configured.

Successful APK compilation alone does not prove Firebase or Play upload. Those steps are conditional on repository secrets and must be checked separately in the workflow run.

### Required GitHub secrets

- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`
- `FIREBASE_APP_ID_ANDROID`
- `FIREBASE_SERVICE_ACCOUNT_JSON`
- `PLAY_SERVICE_ACCOUNT_JSON`

Optional repository variables:

- `FIREBASE_TESTER_GROUPS` (defaults to `internal-testers`)
- `CROPPULSE_PLAY_STORE_URL`

Secrets must remain in the GitHub repository settings and must never be committed to this repository.

## In-app update checker

On startup, the app can read `update-metadata.json` from the rolling GitHub release.

Default values:

- `CROPPULSE_UPDATE_METADATA_URL`: `https://github.com/bixamtarala/corpplus/releases/download/mobile-latest/update-metadata.json`
- `CROPPULSE_PLAY_STORE_URL`: `https://play.google.com/store/apps/details?id=com.croppulse.mobile`

These may be overridden with Flutter `--dart-define` values. A Play Store URL being configured does not prove that a listing is published.

## Launch gates

Before any real customer pilot, verify all of the following independently:

- Business, legal, tax, privacy, terms, return/refund, and supplier policies approved.
- Production API and PostgreSQL migrations deployed.
- OTP, payment, notification, media, and delivery integrations configured with restricted credentials.
- Catalog, lots, prices, inventory, service zones, and delivery capacity populated and reviewed.
- No mock credentials, fallback business data, emulator URLs, or unsupported product claims in the release build.
- Security review covers authentication, authorization, rate limits, idempotency, audit logs, encryption, secrets, and personal data retention.
- Automated tests and release checks pass for the exact release commit.
- APK/AAB package, version, certificate, architectures, and checksum verified.
- Physical Android device testing covers supported OS versions, narrow screens, poor networks, app restart, payment interruption, duplicate taps, and update behavior.
- Firebase/Play internal testing is completed before public rollout.
- Operations rehearses stock mismatch, partial fulfilment, failed delivery, damaged/spoiled items, refund, recall, and supplier settlement scenarios.

## Definition of success for the pilot

Track operational evidence rather than unsupported marketing claims:

- Serviceability-to-checkout conversion.
- Order acceptance and inventory reservation success.
- Fill rate and substitution rate.
- On-time dispatch and delivery rate.
- Cancellation, refund, damage, spoilage, and support-resolution rate.
- Inventory adjustment and wastage rate.
- Gross margin after fulfilment, refunds, and payment costs.
- Repeat purchase by household and business cohort.
- Supplier accepted quantity, rejection reasons, and settlement timeliness.

Targets should be approved only after the pilot geography, catalog, capacity, and baseline measurements are known.
