# CropPulse Commerce Phase 1 Product Requirements Document

Document status: Proposed for approval
Product: CropPulse Mobile Commerce
Initial market: One controlled Indian city or district
Platforms: Android mobile application and web-based operations console
Phase: B2C launch with basic B2B purchasing and managed farmer/FPO supply

## 1. Executive decision

CropPulse Phase 1 will be a managed agricultural commerce service, not an unrestricted national marketplace.

The first release will let households and verified business buyers discover, order, pay for, and receive a controlled catalog of vegetables, fruits, grains, pulses, spices, and staples. Farmers, FPOs, and approved suppliers will provide stock, but CropPulse operations will control catalog quality, sellable inventory, fulfilment, customer support, refunds, and settlement approval.

The product will be designed for future B2B2C reseller and ONDC expansion, but those workflows will not delay the first operational pilot.

## 2. Product promise

> Trusted agricultural products from verified sources, with clear quality, fair units, dependable delivery, and ordering experiences for both households and businesses.

CropPulse must earn trust through accurate availability, traceable supply, transparent product information, predictable fulfilment, and prompt issue resolution. It must not make unsupported claims about freshness, organic status, farmer income, product quality, or delivery performance.

## 3. Goals

### 3.1 Customer goals

- Find locally available agricultural products quickly.
- Understand pack size, unit price, quality grade, source, and delivery promise before purchase.
- Place an order using a simple multilingual checkout.
- Pay online or use cash on delivery when eligible.
- Track fulfilment and receive useful status notifications.
- Report missing, damaged, spoiled, or incorrect products and receive a clear resolution.
- Repeat a previous order with minimal effort.

### 3.2 Business-buyer goals

- Buy in larger units at approved business prices.
- Maintain GST and delivery information for the organization.
- Select recurring or scheduled delivery.
- Attach a purchase-order reference.
- Download invoices and order statements.

### 3.3 Supplier and operations goals

- Onboard and verify farmers, FPOs, and suppliers.
- Capture expected harvest or available inventory by lot.
- Confirm procurement, collection, grading, and accepted quantity.
- Prevent overselling through inventory reservations.
- Pick, pack, dispatch, deliver, refund, and settle orders with a complete audit trail.
- Measure fill rate, wastage, quality failures, margin, and supplier performance.

## 4. Non-goals for Phase 1

- Pan-India fresh-produce delivery.
- Open self-service onboarding for unverified sellers.
- Customer-to-seller direct messaging.
- Auctions or bid-based commodity trading.
- Credit or buy-now-pay-later approval inside CropPulse.
- Automated farmer loans, insurance, or regulated financial advice.
- Pesticides, regulated fertilizers, or other licence-sensitive farm inputs.
- Live dairy, meat, fish, or frozen-product cold-chain operations.
- Multi-level marketing or unrestricted reseller price setting.
- ONDC production integration.
- iOS release.
- AI-generated price, quality, yield, or demand claims without verified data and visible provenance.

## 5. Phase 1 operating assumptions

- One launch geography with an explicit serviceable-pincode list.
- One CropPulse-controlled collection or fulfilment hub.
- Approximately 15-30 verified suppliers.
- Approximately 75-150 active SKUs.
- Standardized packs for consumer orders: for example, 250 g, 500 g, 1 kg, 5 kg, one bunch, one piece, one crate, or one bag.
- Fresh produce uses short reservations and daily availability.
- Fast-moving shelf-stable products may be stocked at the hub.
- B2B bulk products use scheduled procurement and minimum order quantities.
- CropPulse support owns the customer relationship even when a supplier fulfils part of an order.

These assumptions must be confirmed through field operations before public launch.

## 6. User and organization model

One person may hold more than one role. Roles determine permissions and available workspaces; they must not create duplicate accounts.

| Role | Purpose | Phase 1 access |
| --- | --- | --- |
| Guest | Browse serviceable catalog | Browse only |
| Household buyer | Personal orders | Full B2C checkout |
| Business buyer | Retail, hotel, restaurant, caterer, or institution | B2B pricing after verification |
| Farmer/supplier | Supply products and view fulfilment/settlement status | Controlled supplier workspace |
| FPO manager | Manage multiple farmers and lots | Assisted/approved access |
| Hub operator | Receive, grade, pack, and dispatch | Operations console |
| Delivery operator | View assigned deliveries and capture proof | Limited delivery workflow |
| Support agent | Resolve customer issues | Operations console |
| Administrator | Configure and audit the platform | Operations console |

## 7. Commerce model

### 7.1 Phase 1 model

Use a managed marketplace with hub-controlled fulfilment:

1. CropPulse approves each supplier and product.
2. Supplier or operations staff declares available quantity by lot.
3. CropPulse publishes a standardized sellable SKU and price.
4. Checkout reserves inventory for a limited time.
5. The hub receives or confirms the produce, records accepted weight and quality, and packs the order.
6. CropPulse coordinates delivery and customer support.
7. Supplier settlement occurs only against accepted and fulfilled quantity.

The contractual seller of record, invoicing model, GST treatment, and settlement structure must be approved by legal and tax professionals before live payments.

### 7.2 Future models enabled by the design

- Direct supplier fulfilment for shelf-stable goods.
- Multiple hubs and service zones.
- B2B2C reseller storefronts with controlled commissions.
- ONDC buyer or seller network participation.
- Service listings such as soil testing or equipment rental.

## 8. Catalog and product requirements

### 8.1 Category hierarchy

Initial hierarchy:

- Fresh vegetables
- Leafy greens
- Fruits
- Rice and millets
- Pulses
- Spices
- Flour and staples

Each category and SKU must support English plus configured local-language names.

### 8.2 Product and SKU separation

A product describes the general item; a SKU describes a purchasable variant.

Example:

- Product: Tomato
- SKU: Tomato, Grade A, 500 g
- SKU: Tomato, Grade A, 1 kg
- SKU: Tomato, business crate, approximately 20 kg

### 8.3 Required product information

- Product name and local-language name.
- Category and subcategory.
- Representative product image clearly marked when it is indicative.
- Description and storage guidance.
- Seller or source organization.
- Origin district and state when verified.
- Quality grade and grading standard.
- Pack quantity, unit of measure, and unit price.
- Selling price, list price where lawful, and discount explanation.
- Tax classification and invoice treatment.
- Available quantity or availability status.
- Harvest, packed, or received date when captured.
- Lot or batch identifier for internal traceability.
- Shelf-life or best-before information where applicable.
- FSSAI/licence and packaged-product declarations where applicable.
- Return, replacement, or non-returnable policy.
- B2B MOQ and tier prices where applicable.

### 8.4 Catalog quality rules

- No product becomes visible before moderation.
- Prohibited or licence-sensitive products remain blocked.
- Organic, pesticide-free, natural, GI, health, and nutritional claims require evidence.
- A disabled seller, expired compliance record, recalled lot, or unavailable SKU must not remain purchasable.
- Price and inventory changes must be auditable.

## 9. Serviceability, inventory, and price

### 9.1 Serviceability

- Customers set a pincode and delivery address before checkout.
- The catalog may remain browsable outside the service zone, but checkout is blocked with a clear explanation.
- Serviceability is determined by pincode, hub capacity, delivery date, and product restrictions.

### 9.2 Inventory

- Inventory is tracked by SKU, lot, location, status, and quantity.
- Statuses: expected, received, quality hold, available, reserved, packed, dispatched, damaged, expired, rejected, or written off.
- Checkout creates an expiring reservation.
- Payment failure or checkout expiry releases the reservation.
- Staff adjustments require a reason and actor audit record.
- Fresh stock must follow configured first-expiring-first-out rules.

### 9.3 Pricing

- Consumer, business, promotional, and negotiated price lists are separate.
- Price records have an effective time and source.
- Business tiers support MOQ and quantity breaks.
- Checkout locks a price for the reservation period.
- All fees, delivery charges, taxes, discounts, and payable totals are shown before order confirmation.

## 10. Customer functional requirements

### 10.1 Authentication

- Indian mobile-number OTP authentication.
- OTP expiry, attempt limits, request limits, replay prevention, and enumeration-safe responses.
- Session restoration and logout.
- Secure on-device token storage.
- Authentication required before checkout, account data, or issue submission.
- Guest browsing remains available.

### 10.2 Discovery

- Location-aware home feed.
- Search by product and local-language term.
- Category browsing.
- Filters for price, source, availability, pack size, grade, and relevant claims.
- Sort by relevance, price, popularity, and newest availability.
- Recently viewed and repeat-order sections may use first-party activity only.

### 10.3 Cart

- Add, remove, and change quantity.
- Show unavailable or quantity-reduced items immediately.
- Show consumer and business units correctly.
- Display subtotal, discount, delivery, tax, and estimated total.
- Persist the cart for a signed-in customer.
- Revalidate price, inventory, serviceability, and restrictions at checkout.

### 10.4 Checkout

- Select or add delivery address.
- Select an available delivery date and slot.
- Select substitution preference for fresh products: allow similar, contact me, or no substitution.
- Apply an eligible coupon.
- Select online payment or COD when eligible.
- Accept terms and applicable product policies.
- Create an idempotent order so retries cannot duplicate a purchase.

### 10.5 Orders

- Show a single customer order even when internally split into fulfilments.
- Show status timeline and item-level exceptions.
- Permit cancellation only while eligible.
- Support reorder with current-price and availability confirmation.
- Provide invoice or receipt when generated.

### 10.6 Issues and refunds

- Reasons: missing item, wrong item, damaged, spoiled, poor quality, quantity/weight issue, late delivery, or other.
- Allow photo evidence where appropriate.
- Display eligibility and expected resolution time.
- Support item-level replacement, partial refund, full refund, or rejection with reason.
- Never mark a refund complete until payment-provider confirmation is recorded.

## 11. Basic B2B requirements

- Business profile with legal name, contact person, GSTIN when applicable, billing address, and delivery locations.
- Verification state: draft, submitted, under review, approved, rejected, or suspended.
- Business catalog or price list appears only after approval.
- MOQ, bulk units, quantity breaks, and scheduled availability.
- Purchase-order reference.
- Recurring order request that operations must confirm in Phase 1.
- Invoice and statement download.
- No unsecured credit in Phase 1; any offline credit arrangement must be recorded as an explicit approved payment term.

## 12. Supplier requirements

- Supplier profile and type: farmer, FPO, wholesaler, producer, manufacturer, or distributor.
- Identity, address, bank, tax, FSSAI, and category-specific compliance records as applicable.
- Approval and suspension workflow.
- Product proposal and document upload.
- Lot declaration with expected quantity, unit, availability date, origin, grade, and asking price.
- Procurement confirmation and collection schedule.
- Accepted/rejected quantity and quality reason.
- Fulfilment history and settlement ledger.
- Supplier cannot directly change an accepted customer order.

Phase 1 may use agent-assisted onboarding and web operations for suppliers who cannot maintain the catalog themselves.

## 13. Order and fulfilment lifecycle

### 13.1 Customer order states

- pending_payment
- confirmed
- processing
- packed
- out_for_delivery
- delivered
- partially_delivered
- cancelled
- failed

### 13.2 Item and fulfilment exceptions

- substitution_requested
- substitution_approved
- unavailable
- rejected_at_qc
- short_quantity
- damaged
- returned
- refunded

### 13.3 Payment states

- initiated
- authorized
- captured
- failed
- cancelled
- partially_refunded
- refunded
- cod_due
- cod_collected
- reconciled

### 13.4 Settlement states

- pending_acceptance
- eligible
- on_hold
- approved
- processing
- paid
- failed
- adjusted

All transitions require a timestamp, actor or system source, and idempotency protection where an external provider is involved.

## 14. Fresh-produce rules

- Use standard packs during the pilot.
- Do not silently charge more than the confirmed checkout amount.
- If accepted quantity is lower, provide the item, charge, invoice, and refund outcome clearly.
- Substitutions require the customer's recorded preference and price protection rules.
- Quality checks record grade, accepted quantity, rejected quantity, reason, operator, and time.
- Customer-visible provenance must be backed by recorded data.
- Recalled or unsafe lots must be blocked from allocation and traceable to affected orders.
- Food and non-food products must use appropriate separate handling.

## 15. Notifications

Required transactional events:

- OTP requested.
- Order confirmed or payment failed.
- Material item substitution or availability problem.
- Order packed.
- Out for delivery.
- Delivered.
- Cancellation or refund update.
- Business recurring-order confirmation.
- Supplier collection and settlement update.

Push, SMS, and WhatsApp usage must follow recorded consent, template, cost, and delivery requirements. The in-app order record remains the source of truth.

## 16. Operations console requirements

- Dashboard for orders, inventory risk, fulfilment, quality, refunds, and exceptions.
- Seller and compliance approval queues.
- Product moderation and catalog publishing.
- Price-list management.
- Lot receiving, weighing, grading, and rejection.
- Pick list and pack confirmation.
- Delivery manifest and assignment.
- Customer issue and refund management.
- COD and payment reconciliation.
- Supplier settlement approval.
- User/role management.
- Immutable audit log for sensitive actions.

## 17. Data architecture

Minimum business entities:

- users, roles, sessions, consents
- organizations, organization_members, business_profiles
- addresses, service_zones, delivery_slots
- suppliers, supplier_documents, supplier_bank_accounts
- products, product_translations, skus, product_media
- lots, inventory_locations, inventory_balances, inventory_movements
- price_lists, prices, promotions, coupons
- carts, cart_items, inventory_reservations
- orders, order_items, fulfilments, fulfilment_items
- shipments, delivery_events, proof_of_delivery
- payments, payment_attempts, refunds, cod_reconciliations
- supplier_settlements, settlement_lines
- quality_inspections, recalls
- issues, issue_evidence, issue_actions
- notifications, notification_attempts
- audit_events

PostgreSQL is the source of truth. Redis may hold expiring OTPs, rate-limit state, cache, and cart/inventory reservations, but durable outcomes must be written to PostgreSQL.

## 18. API requirements

The current `/api/v2` prototype should not be treated as the production commerce contract. Establish versioned, authenticated endpoints grouped by domain.

Minimum Phase 1 API groups:

- `/auth`: OTP, refresh/session, logout, readiness.
- `/catalog`: categories, products, SKUs, search, suggestions.
- `/serviceability`: pincode, address, slot availability.
- `/cart`: cart CRUD, validation, totals.
- `/checkout`: quote, reservation, order creation.
- `/payments`: provider initiation, callback/webhook, status, refund.
- `/orders`: list, detail, timeline, cancel, reorder.
- `/issues`: eligibility, submission, evidence, status.
- `/business`: profile, verification, price list, recurring requests.
- `/supplier`: profile, documents, lots, procurement, settlements.
- `/operations`: moderation, inventory, fulfilment, delivery, refunds, settlement.

Contract requirements:

- Stable error codes plus localized client messages.
- Decimal-safe money and quantity handling; do not use binary floating point for accounting.
- Idempotency keys for checkout, payments, refunds, fulfilment callbacks, and settlements.
- Cursor pagination for growing collections.
- Authorization enforced server-side for every organization and role.
- Webhook signatures, replay prevention, and event logs.
- OpenAPI contract tests shared with the Flutter client.

## 19. Technical and security requirements

- Production API must use HTTPS; release builds must not default to emulator localhost.
- Secrets must fail closed when missing; no production fallback JWT secret.
- Tokens stored using platform-secure storage.
- OTP and sensitive endpoints rate-limited by normalized identity and network signals.
- Personally identifiable information encrypted in transit and protected at rest.
- Payment card data must not pass through CropPulse servers unless explicitly certified for it.
- Role and organization authorization covered by negative tests.
- Logs must redact tokens, OTPs, bank data, complete identity numbers, and unnecessary phone/address data.
- Backups and restore procedures tested before live orders.
- Administrative access requires stronger authentication and auditable actions.
- Accessibility: scalable text, screen-reader labels, adequate contrast, logical focus, and minimum practical touch targets.
- Localization must not break layout at 320 logical pixels.
- Core order screens must handle offline, timeout, retry, duplicate-tap, and stale-data states.

## 20. Compliance readiness

Before live transactions, complete a professional review covering:

- Inventory versus marketplace contracting and seller-of-record decision.
- FSSAI registration/licensing for CropPulse and listed food businesses.
- Seller licence display and food listing requirements.
- Legal Metrology declarations for packaged commodities.
- Consumer Protection (E-Commerce) disclosures, grievance process, returns, refunds, and seller information.
- GST registration, invoicing, product tax classification, marketplace TCS, returns, and settlement reporting.
- State-specific agricultural procurement and APMC implications.
- DPDP notice, consent, retention, user rights, processor contracts, and breach procedures.
- Payment-provider, COD, refund, and supplier-settlement terms.

No product may be labelled organic or make a regulated quality/health claim without approved evidence.

## 21. Analytics and audit events

Required product funnel events:

- location_set
- catalog_viewed
- search_submitted
- product_viewed
- add_to_cart
- cart_validated
- checkout_started
- payment_started
- order_confirmed
- fulfilment_exception
- order_delivered
- issue_submitted
- refund_completed
- reorder_started

Operations metrics:

- Gross and net merchandise value.
- Delivered order count.
- Average order value.
- Fill rate.
- On-time and in-full delivery.
- Cancellation rate.
- Item substitution rate.
- Quality rejection and complaint rate.
- Refund time.
- Wastage by SKU, lot, supplier, and reason.
- Contribution margin per order and service zone.
- B2C repeat purchase and B2B recurring-order retention.
- Supplier acceptance, quality, and settlement performance.

Analytics must not replace the financial ledger or operational source of truth.

## 22. Pilot acceptance gates

### 22.1 Product gate

- Household customer can browse, purchase, track, and report an issue end to end.
- Approved business buyer can see business units/prices and place a scheduled order.
- Guest cannot access another user's account or order data.
- Product availability, price, fees, policies, and seller/source information are visible before purchase.
- Empty, loading, offline, failure, unavailable, and retry states are implemented.

### 22.2 Operations gate

- Staff can receive, inspect, reserve, pick, pack, dispatch, deliver, refund, and settle through auditable workflows.
- Inventory cannot become negative through concurrent checkout.
- A failed payment cannot create a paid order.
- Duplicate webhook or button retries cannot duplicate orders, refunds, or settlement entries.
- A recalled lot can be traced to every affected order.

### 22.3 Validation gate

- Flutter formatting, static analysis, unit tests, widget tests, and release build pass in CI.
- Backend formatting/linting, type checks, unit tests, contract tests, migration tests, and integration tests pass in CI.
- Payment and notification provider sandbox flows pass.
- Physical Android-device testing passes on low-, mid-, and recent-version targets.
- Poor-network and interrupted-payment tests pass.
- Security review finds no unresolved critical/high-severity issue.
- Backup restore and incident runbook have been exercised.

### 22.4 External-readiness gate

- Production HTTPS backend and database are configured.
- Real OTP provider and sender templates are active.
- Payment, refund, and settlement accounts are approved.
- Android release signing and Play internal testing are configured.
- Required business, food, seller, tax, privacy, support, and grievance details are active.
- Pilot suppliers, hub, packaging, delivery coverage, and support staffing are operationally verified.

## 23. Proposed delivery sequence

### Stage A: Decisions and foundations

- Confirm launch geography, categories, hub, service hours, and buyer segments.
- Confirm legal commerce model and invoicing.
- Define catalog, SKU, unit, lot, and quality standards.
- Create final UX prototype and API contracts.
- Establish production environments and CI quality gates.

### Stage B: Commerce core

- Authentication and account security.
- Location, serviceability, catalog, search, product detail.
- Cart, checkout, inventory reservation, payment, order ledger.
- Operations catalog, inventory, fulfilment, and delivery workflows.

### Stage C: Trust and resolution

- Notifications and order timeline.
- Issue, evidence, replacement, cancellation, and refund workflows.
- Compliance display, audit logging, reconciliation, and settlement.

### Stage D: Controlled pilot

- Internal staff orders.
- Closed supplier and household tester cohort.
- Approved B2B buyers.
- Progressive pincode and catalog activation based on operating metrics.

## 24. Proposed pilot targets

These are planning targets, not current claims:

- Fill rate at or above 95%.
- On-time delivery at or above 95%.
- Cancellation below 3%.
- Fresh-product quality complaints below 2%.
- Wastage below 5% by value.
- Refunds completed within the published service level.
- Supplier settlement completed within the agreed settlement period.
- Positive contribution margin path demonstrated before geographic expansion.

Contribution margin must be measured as customer revenue less procurement, packaging, pick/pack, payment cost, delivery, promotions, refunds, and wastage.

## 25. Current application transition

Reusable foundations in the existing Flutter project:

- Flutter and Riverpod structure.
- Theme and multilingual string system.
- Basic OTP client flow, after security replacement.
- Farmer profile concepts.
- Marketplace and price-insight UI concepts.
- Android build and rolling prerelease workflow.

Required replacement or expansion:

- Replace the seven-item primary navigation with commerce navigation.
- Replace optional mock login with a real authentication gate for protected actions.
- Replace emulator-only API defaults with environment-specific HTTPS configuration.
- Replace sample backend responses with durable commerce data.
- Add catalog, SKU, serviceability, cart, checkout, order, payment, refund, inventory, fulfilment, and settlement domains.
- Move farmer/trader intelligence into role-specific workspaces rather than primary buyer navigation.
- Add an operations web console.
- Add test and analysis gates to mobile CI.

## 26. Decisions required before implementation

The product owner must approve:

1. Pilot city/district and initial pincodes.
2. First catalog categories and SKU count.
3. Inventory versus marketplace invoicing model.
4. Hub ownership and supplier collection process.
5. Initial delivery model: owned riders, third-party logistics, or hybrid.
6. Online payment, COD, refund, and supplier-settlement providers.
7. Consumer delivery fee and minimum-order policy.
8. Business verification and price-approval policy.
9. Fresh-product substitution, cancellation, replacement, and refund rules.
10. Supported launch languages.

Implementation can begin on platform foundations and non-controversial UX components, but real checkout and settlement cannot be finalized until decisions 1-9 are recorded.
