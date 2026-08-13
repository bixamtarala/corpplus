# CropPulse Commerce Phase 1 Mobile Screen Blueprint

Companion document: `CROPPULSE_COMMERCE_PHASE1_PRD.md`
Scope: Android Phase 1 B2C, basic B2B, and controlled supplier access

## 1. Experience principles

- Shopping is the default experience; operational roles do not crowd the buyer navigation.
- Location and availability are visible before a customer invests time in checkout.
- Fresh-product units, quality, source, and policy are explicit.
- Important actions work in English and configured local languages at narrow screen widths.
- The app never fabricates price, stock, source, quality, delivery, or order state.
- Errors explain what happened, what remains safe, and what the user can do next.
- Protected actions request authentication at the moment it becomes necessary.
- One user can switch between Personal, Business, and Supplier workspaces when authorized.

## 2. Primary information architecture

### 2.1 Buyer bottom navigation

| Tab | Purpose |
| --- | --- |
| Home | Location-aware discovery and repeat purchase |
| Categories | Structured catalog browsing |
| Search | Search, suggestions, filters, and recent activity |
| Cart | Current cart, validation, and checkout entry |
| Account | Orders, addresses, support, language, and workspace switching |

The bottom bar remains fixed and must fit without horizontal scrolling.

### 2.2 Workspace switcher

The Account header contains a workspace selector only when the user has more than one authorized workspace:

- Personal
- Business: organization name
- Supplier: farm/FPO/business name

Changing workspace changes price lists, units, order history, actions, and home modules. It does not create a second login.

### 2.3 Secondary navigation

- Use full-screen routes for catalog, product, cart, checkout, order, and issue flows.
- Use modal sheets for short selections such as language, sort, quantity, delivery slot summary, or substitution preference.
- Do not place Farmer, Trader, Customer, Intelligence, Marketplace, and Profile as seven equal primary destinations.

## 3. Global application states

Every network screen must define:

- Initial loading with stable skeleton layout.
- Empty state with a useful next action.
- Offline state showing locally safe information only.
- Timeout and retry state.
- Partial-data state.
- Authentication-required state.
- Permission-denied state.
- Service-unavailable state.
- Stale price/inventory state requiring refresh.

Global banners:

- Offline.
- Address outside service area.
- Cart prices or availability changed.
- Business verification pending.
- Supplier compliance action required.
- Scheduled maintenance when supplied by server readiness data.

## 4. Launch, onboarding, and authentication

### S01. Launch and readiness

Purpose: Initialize secure session, configuration, update policy, language, and API readiness.

Content:

- CropPulse mark and name.
- Progress indicator with no fake percentage.
- Retry action if configuration cannot load.

Rules:

- A valid session proceeds to Home.
- An expired session becomes Guest without losing a locally recoverable cart.
- Mandatory update blocks entry with a verified store/download target.
- Optional update can be dismissed for that version.
- Production builds fail closed if the API environment is missing.

### S02. First-run introduction

Purpose: Explain the value and obtain only necessary choices.

Slides:

1. Shop trusted agricultural products.
2. See source, pack, quality, and delivery details.
3. Buy for your home or approved business.

Actions:

- Continue.
- Skip.
- Select language.

Do not request notification, location, contacts, camera, or storage permission during generic onboarding.

### S03. Location and serviceability

Purpose: Establish browsing and delivery context.

Controls:

- Pincode entry.
- Use current location, requesting permission only after the tap.
- Search saved addresses when authenticated.

Results:

- Service available: show earliest slot and enter Home.
- Limited service: explain available categories or dates.
- Not available: allow browsing, capture an optional launch-interest request, and block checkout.

### S04. Sign in

Purpose: Authenticate before checkout or account access.

Controls:

- Country code fixed or clearly selected.
- Mobile-number field.
- Request OTP.
- Terms and privacy links.

States:

- Invalid number.
- Rate limited with safe retry timing.
- Provider unavailable.
- Enumeration-safe success message.

### S05. Verify OTP

Controls:

- Six-digit code entry.
- Masked phone number.
- Resend countdown.
- Change number.
- Verify.

Rules:

- Do not display or accept a universal mock code outside explicit development builds.
- Prevent repeated submissions.
- Restore the pending protected action after success.

## 5. Buyer discovery

### S06. Home

Layout:

```text
+----------------------------------+
| Deliver to: Home, 600xxx      v  |
| [ Search vegetables, grains... ] |
| [ Personal v ]                    |
| Categories                        |
| [Veg] [Fruit] [Grain] [Pulses]   |
| Fresh today                       |
| [Product] [Product]               |
| Buy again                         |
| [Previous order/product cards]    |
| Seasonal near you                 |
| [Source-aware product cards]      |
| Home Categories Search Cart Acct  |
+----------------------------------+
```

Required modules:

- Address and delivery promise.
- Search entry.
- Category shortcuts.
- Fresh arrivals.
- Seasonal selection.
- Buy again when history exists.
- Business bulk offers only in Business workspace.

Rules:

- Modules come from server configuration with safe client defaults.
- Promotions show eligibility and do not hide the normal price.
- Out-of-stock products cannot present an active Add button.

### S07. Categories

Layout:

- Category list or compact grid.
- Selected category heading.
- Subcategory chips.
- Product list/grid toggle only if both experiences are maintained well.

Product cards show:

- Image.
- Name.
- Pack size.
- Price and unit price.
- Source/grade badge where verified.
- Delivery/availability summary.
- Add or quantity control.

### S08. Search

States:

- Empty: recent searches and popular categories.
- Typing: debounced suggestions for products, categories, and local-language synonyms.
- Results: total summary, filter, sort, and product cards.
- No result: spelling/category suggestions and request-product action.

Filters:

- Category.
- Price range.
- Pack size/unit.
- Availability date.
- Quality grade.
- Source region.
- Verified claims only.

Sort:

- Relevance.
- Price low to high.
- Price high to low.
- Recently available.
- Popular.

### S09. Product detail

Layout:

```text
+----------------------------------+
| <  Product name             Share|
| [        product media          ] |
| Grade A     Source verified      |
| Tomato                           |
| 1 kg                            v |
| Rs xxx   Rs xxx/kg               |
| Delivery tomorrow, 7-10 AM       |
| [ - ] 1 [ + ]       [ Add cart ] |
| Source and origin                |
| Quality and pack information     |
| Storage guidance                 |
| Seller/FSSAI declarations        |
| Replacement/refund policy        |
+----------------------------------+
```

Required behavior:

- Changing the variant updates price, unit, inventory, and delivery promise.
- Images are labelled indicative for variable fresh produce.
- Source, grade, organic, or other claims display only when verified.
- Sticky Add/quantity action remains reachable without covering content.
- Business workspace shows MOQ, tier pricing, tax/invoice information, and bulk availability.

## 6. Cart and checkout

### S10. Cart

Sections:

- Delivery location and serviceability.
- Items grouped only when grouping affects delivery or policy.
- Quantity controls and remove/save-for-later where implemented.
- Substitution preference summary for fresh products.
- Price breakdown.
- Checkout action.

Blocking states:

- Price changed.
- Quantity reduced.
- Out of stock.
- Delivery no longer available.
- MOQ not met.
- Compliance-restricted combination.

The customer must explicitly accept material changes before checkout.

### S11. Address list

- Saved addresses.
- Add address.
- Edit or delete.
- Serviceability status per address.
- Default address control.

Address data:

- Recipient name.
- Mobile number.
- Building/house.
- Street/locality.
- Landmark optional.
- Pincode.
- City/district and state.
- Address label.
- Delivery instructions with length limit.

### S12. Delivery slot

- Dates with availability.
- Slot time range.
- Fee and capacity status.
- Business scheduled date where applicable.

Do not show a slot as selectable after capacity is exhausted. Revalidate before order creation.

### S13. Substitution preference

Choices:

- No substitution; refund unavailable items.
- Contact me before substituting.
- Allow a similar item within the displayed protection rule.

The final choice is visible on checkout review and stored per applicable order item.

### S14. Checkout review

Sections:

- Address.
- Delivery slot.
- Item summary.
- Substitution rule.
- Coupon/promotion.
- Payment method.
- Business purchase-order reference when relevant.
- Complete price breakdown.
- Terms and policy acknowledgement.

Primary action states the amount: `Place order - Rs X`.

### S15. Payment

- Redirect or provider-controlled payment UI.
- Processing state that cannot be dismissed into accidental duplicate payment.
- Safe recovery after app backgrounding or network loss.
- Poll/status reconciliation when callback is uncertain.
- COD confirmation where eligible.

Never infer success only from a client callback.

### S16. Order confirmation

- Order number.
- Confirmed payment/COD state.
- Delivery date and slot.
- Item and total summary.
- Track order.
- Continue shopping.
- Support access.

Do not show success until the server has committed the order.

## 7. Orders, delivery, and resolution

### S17. Orders list

Tabs or filters:

- Active.
- Completed.
- Cancelled.

Cards:

- Order number and date.
- Leading product images or item count.
- Current status.
- Amount.
- Delivery promise.
- Reorder when eligible.

### S18. Order detail and timeline

Sections:

- Current status and delivery promise.
- Timeline based on recorded events.
- Item-level states, substitutions, missing quantities, and refunds.
- Address and delivery instructions.
- Payment summary.
- Invoice/receipt.
- Cancel action when eligible.
- Get help.

The customer sees one order while internal supplier/hub fulfilments remain understandable through item-level updates.

### S19. Cancellation

- Show eligible items.
- Show cancellation reason choices.
- Explain refund path and expected processing time.
- Confirm before submission.
- Show recorded cancellation and refund status afterward.

### S20. Report an issue

Flow:

1. Select order item.
2. Select reason.
3. Add description.
4. Add photos when useful, requesting camera/photo permission at that moment.
5. Show eligible proposed resolution if policy permits.
6. Submit and receive case number.

### S21. Issue detail

- Case number and status.
- Affected items.
- Submitted evidence.
- Support messages/actions.
- Approved resolution.
- Refund/replacement state.
- Escalation or grievance information.

### S22. Delivery proof

Customer-facing detail:

- Delivered time.
- Recipient or masked proof description.
- Photo only when policy and consent allow.
- Report-problem action.

Delivery operator flow:

- Assigned stop.
- Navigation handoff.
- Call through masked mechanism where available.
- OTP or approved proof capture.
- Partial-delivery and rejection reasons.
- COD collection amount and reconciliation state.

## 8. Account and settings

### S23. Account

Sections:

- Sign in or customer summary.
- Workspace switcher.
- Orders.
- Addresses.
- Business account.
- Supplier workspace when authorized.
- Notifications and communication preferences.
- Language.
- Help and support.
- Legal, privacy, returns, refund, delivery, and grievance information.
- Logout.
- Account/data request controls as required.

Every visible row must navigate or clearly display an unavailable state; no empty tap handlers.

### S24. Language

- English.
- Hindi.
- Telugu.
- Additional launch language only after complete translation and layout validation.

The chosen language applies immediately and persists. Product translations fall back visibly and safely to the available product name.

### S25. Notification preferences

- Transactional order updates cannot be disabled where required to provide the service, but channel selection may be offered.
- Marketing push, SMS, and WhatsApp consent are separate and off unless validly obtained.
- Show the consequence of disabling device-level notifications.

### S26. Help and support

- Order-related help.
- General questions.
- Phone/chat/email channels that are actually staffed.
- Service hours.
- Grievance officer and escalation information.
- Existing cases.

## 9. Business workspace

### S27. Business application

- Organization type.
- Legal and display name.
- Contact person.
- GSTIN and tax details where applicable.
- Billing address.
- Delivery locations.
- Expected purchase categories and volume.
- Documents.
- Submit and track review.

### S28. Business home

- Business price-list status.
- Reorder frequent products.
- Bulk category shortcuts.
- Scheduled and recurring orders.
- Open orders and invoices.
- Contact procurement support.

### S29. Bulk product detail

- Business unit: crate, bag, carton, quintal, or other approved unit.
- Approximate versus fixed quantity clearly distinguished.
- MOQ and price tiers.
- Tax and invoice summary.
- Available or earliest procurement date.
- Delivery schedule.
- Add to business cart or request quote when a fixed price is unavailable.

### S30. Recurring order request

- Products and quantities.
- Frequency.
- Preferred days and slots.
- Start/end date.
- Delivery location.
- Purchase-order reference.
- Operations review status.

Phase 1 recurring orders are requests until explicitly confirmed by operations.

### S31. Business documents

- Orders.
- Invoices.
- Credit notes/refunds.
- Downloadable statements by date.
- Outstanding offline terms only when approved and accurately recorded.

## 10. Supplier workspace

### S32. Supplier onboarding/status

- Supplier type.
- Identity and organization details.
- Farm/business address.
- Bank and tax details.
- FSSAI and category-specific documents.
- Review status and actionable rejection reason.

Sensitive values are masked after submission.

### S33. Supplier home

- Compliance alerts.
- Upcoming collections.
- Lots needing confirmation.
- Accepted/rejected quantity summary.
- Fulfilled value.
- Pending and completed settlement summary.
- Demand/price information only when backed by identified data.

### S34. Declare availability

- Product from approved catalog.
- Expected quantity and unit.
- Harvest/available date.
- Origin/location.
- Proposed grade.
- Asking price or procurement offer response.
- Lot photo optional.
- Notes.

The declaration is not customer-visible until approved and converted into sellable inventory.

### S35. Collection detail

- Collection location and window.
- Expected products and quantities.
- Contact/support.
- Supplier confirmation.
- Received, accepted, rejected, and pending quantities after inspection.
- Quality reason and evidence.

### S36. Settlement ledger

- Settlement period.
- Accepted fulfilment lines.
- Gross value.
- Adjustments with reasons.
- Net amount.
- Status and payment reference.
- Raise discrepancy.

## 11. Operations console blueprint

The operations console is web-first and role-controlled.

Required areas:

1. Operations dashboard.
2. Seller and compliance queue.
3. Catalog and translation moderation.
4. Price lists and promotions.
5. Procurement and collection schedule.
6. Lot receiving and quality inspection.
7. Inventory and reservation view.
8. Order control tower.
9. Pick, pack, and dispatch.
10. Delivery assignment and manifest.
11. Customer issues and refunds.
12. Payments, COD, and reconciliation.
13. Supplier settlements.
14. Recall and traceability.
15. Configuration, roles, and audit events.

No operational state may depend only on an editable free-text note.

## 12. Key interaction rules

### 12.1 Add-to-cart behavior

- First tap adds the minimum purchasable quantity.
- The card becomes a quantity stepper.
- Server-side cart validation resolves price and inventory races.
- Failure restores the previous state and explains the result.

### 12.2 Money and quantity

- Display rupee values consistently.
- Display both pack price and comparable unit price where meaningful.
- Use exact decimal rules from the server.
- Never calculate the authoritative final total only on the client.

### 12.3 Double taps and retries

- Disable or debounce actions while the same request is in flight.
- Checkout, payment, cancellation, issue, and refund requests use idempotency keys.
- Retrying after an uncertain response first fetches authoritative status.

### 12.4 Offline behavior

- Cached catalog may be browsed with a visible stale/offline label.
- Do not promise current price, inventory, or delivery while offline.
- Cart edits may be queued locally only if they are revalidated before checkout.
- Payment and final order creation require authoritative connectivity.

## 13. Responsive and accessibility rules

- Support 320 logical-pixel width without horizontal page scrolling.
- Bottom navigation must not horizontally scroll.
- Product grids collapse to a readable single column where needed.
- Business tables become cards or bounded horizontal data regions.
- Respect system text scaling without clipping critical actions.
- Use semantic labels for images, icons, steppers, status, and navigation.
- Do not communicate quality, availability, payment, or order state using color alone.
- Keep interactive targets practically touchable and separated.
- Preserve keyboard-safe forms and scroll focused fields into view.
- Validate every supported language on narrow and large Android devices.

## 14. Analytics mapping

| Screen | Primary event | Success signal |
| --- | --- | --- |
| Location | location_set | Serviceable location established |
| Home | home_viewed | Discovery modules loaded |
| Search | search_submitted | Relevant results viewed |
| Product | product_viewed | Variant and policy understood |
| Cart | cart_validated | No unresolved blocker |
| Checkout | checkout_started | Complete review reached |
| Payment | payment_started | Provider attempt created |
| Confirmation | order_confirmed | Durable order committed |
| Order detail | order_viewed | Status understood |
| Issue | issue_submitted | Case number created |
| Business application | business_profile_submitted | Review started |
| Supplier availability | supplier_lot_submitted | Lot review started |

Analytics events must exclude OTPs, tokens, bank data, complete addresses, and unnecessary personal data.

## 15. Prototype and usability-test scenarios

The clickable prototype should test:

1. New household customer sets location and orders vegetables.
2. Customer encounters an out-of-stock cart item and chooses no substitution.
3. Customer resumes after an interrupted online payment.
4. Customer reports spoiled produce with a photo.
5. Returning customer reorders with changed prices and availability.
6. Restaurant buyer selects a crate quantity and scheduled delivery.
7. Business applicant sees pending verification without accessing business prices.
8. Farmer declares a harvest lot and later sees accepted/rejected quantity.
9. User switches language on a 320-pixel-wide device.
10. User with large text and screen reader completes checkout.

## 16. Screen acceptance checklist

Every implemented screen must have:

- Product-owner-approved purpose and primary action.
- Server contract and permission definition.
- Loading, empty, error, offline, and unauthorized states.
- Analytics event definition.
- Accessibility labels and text-scale validation.
- English, Hindi, and Telugu content.
- 320-pixel layout test.
- Widget test for critical decisions and actions.
- End-to-end coverage when it changes money, inventory, order, refund, delivery, or settlement state.

## 17. Recommended implementation slices

### Slice 1: Shell and discovery

- App readiness and environment configuration.
- Commerce navigation.
- Location/serviceability.
- Home, categories, search, and product detail.

### Slice 2: Identity and cart

- Secure OTP and session.
- Account and addresses.
- Durable cart and validation.

### Slice 3: Checkout and order ledger

- Slots, substitution, quote, inventory reservation.
- Payment/COD.
- Order confirmation, list, detail, and timeline.

### Slice 4: Operations fulfilment

- Supplier/lot foundations.
- Receiving and QC.
- Pick, pack, dispatch, delivery proof.

### Slice 5: Resolution and reconciliation

- Cancellation, issues, replacements, refunds.
- Payment/COD reconciliation.
- Supplier settlements.

### Slice 6: Basic B2B

- Business verification.
- Business price lists, units, checkout, documents, and recurring-order requests.

Each slice must pass its acceptance criteria before the next slice depends on it.
