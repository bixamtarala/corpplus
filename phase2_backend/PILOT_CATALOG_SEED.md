# CropPulse Pilot Draft Catalog Seed

This seed provides a reviewable starting catalog for the commerce database. It is intentionally non-sellable and must not be treated as an approved launch assortment.

## Seed scope

- 6 draft categories
- English, Hindi, and Telugu category names
- 12 draft products based on the current mobile preview
- English, Hindi, and Telugu product names
- 12 standardized draft SKUs
- 12 indicative prices in an inactive draft price list
- No inventory balances
- No service zone or delivery promise
- No supplier, origin, grade, organic, freshness, or quality claims
- No product images or packaged-product declarations

The seed is a review set, not the planned final 75-150 SKU pilot assortment.

## Safety model

- Categories are created with `is_active=false`.
- Products and SKUs are created with `status=draft`.
- The `pilot-draft-inr` price list is inactive and separate from the API's `consumer-inr` price list.
- Prices are labelled with source `pilot-draft-seed-v1` and remain indicative.
- Stable UUIDv5 identifiers make repeated runs idempotent.
- A natural-key collision with a non-seed category, product, SKU, price list, or price stops and rolls back the transaction.
- Existing manually created translations are preserved.
- Once a seeded category, product, SKU, or price list is manually activated after review, repeat runs preserve its reviewed values and activation state.
- Dry-run is the default. Production execution requires a separate explicit flag.

## Preview without saving

Set a local commerce database URL, apply migrations, and run:

```bash
python -m phase2_backend.seed_pilot_catalog
```

The command validates and builds the entire seed transaction, prints counts, and rolls it back.

## Apply draft records

```bash
python -m phase2_backend.seed_pilot_catalog --apply
```

Expected result:

```text
Pilot draft catalog applied: 6 categories, 12 products, 12 SKUs, 12 prices.
All seeded categories, products, SKUs, and price lists remain inactive/draft.
```

The production guard rejects execution when `ENV=production`. `--allow-production` only unlocks the command; it is not approval by itself. Before any hosted application, require a backup, reviewed change plan, exact database target verification, and an approved catalog owner.

## Required review before activation

For every product/SKU, operations must approve:

- Launch service zone and fulfilment hub
- Supplier and seller of record
- Product image rights and representative-image labelling
- Pack quantity, unit, weight tolerance, and grade standard
- Final selling price, price owner, tax and invoice treatment
- Available stock or procurement plan
- Source/origin evidence before displaying origin
- Storage, shelf-life, substitution, return, and replacement policy
- FSSAI, HSN, packaged-product, and other mandatory declarations where applicable
- Hindi and Telugu translation quality

Activation should be performed through a future audited moderation workflow, not by changing the seed defaults.

## Validation

```bash
python -m pytest phase2_backend/test_pilot_catalog_seed.py -q
```

Tests cover repeatability, dry-run rollback, collision rollback, non-visibility through the catalog API, stable IDs/translations, and preservation of manually reviewed active values.
