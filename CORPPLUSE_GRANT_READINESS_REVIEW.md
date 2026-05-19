# Corppluse Grant Readiness Review

Date: May 19, 2026

## Findings

1. Corppluse is not yet a credible "unified agriculture infrastructure platform" as a current-state claim; it is a strong Phase 1 intelligence MVP with a large Phase 2 roadmap. Your own readiness doc marks overall readiness at 12%, with Farmer OS at 0%, Marketplace at 0%, Logistics at 0%, and Finance at 0%. See [croppulse/CURRENT_VS_VISION.md](croppulse/CURRENT_VS_VISION.md#L141) and [croppulse/CURRENT_VS_VISION.md](croppulse/CURRENT_VS_VISION.md#L156).

2. The backend supports the grant story direction, but key grant-critical workflows are still scaffolds, not working production flows. OTP auth still has TODOs for SMS, Redis storage, expiry, brute-force protection, and real JWT generation; the current verify endpoint returns a placeholder token. Marketplace order creation, browsing, and matching are also TODO-backed stubs returning fixed IDs or empty lists. See [phase2_backend/main.py](phase2_backend/main.py#L388), [phase2_backend/main.py](phase2_backend/main.py#L410), and [phase2_backend/main.py](phase2_backend/main.py#L648).

3. The frontend currently presents several capabilities as if they exist end-to-end, but much of that surface is narrative/demo UI rather than proven workflow. The Streamlit app advertises weather and disease alerts, buyer discovery, smart matching, negotiations, and secure transactions, but the repo evidence shows those are ahead of actual backend completion. See [croppulse/croppulse_app.py](croppulse/croppulse_app.py#L714), [croppulse/croppulse_app.py](croppulse/croppulse_app.py#L815), and [croppulse/croppulse_app.py](croppulse/croppulse_app.py#L845).

4. Your traction is real enough to support an innovation-grant application, but the evidence is narrow. The strongest validated proof today is 500 rice traders in Tamil Nadu on a Streamlit MVP, not a multi-sided national ecosystem. See [PROJECT_STATUS.md](PROJECT_STATUS.md#L11) and [croppulse/EXECUTIVE_SUMMARY.md](croppulse/EXECUTIVE_SUMMARY.md#L25).

5. There is a credibility gap in the narrative package because core business metrics are inconsistent across strategy documents. One document says Phase 1 is at $5K/month revenue, while another says revenue is $0 at MVP stage. Grant reviewers may not call this out directly, but it weakens trust. See [PROJECT_STATUS.md](PROJECT_STATUS.md#L12) and [croppulse/EXECUTIVE_SUMMARY.md](croppulse/EXECUTIVE_SUMMARY.md#L32).

## Where Corppluse Stands

Corppluse stands in a good position for an agri innovation grant if you pitch it as:

"a validated Phase 1 agricultural intelligence platform with trader traction, now building the farmer-market coordination layer."

That is strong.

Corppluse does not yet stand in a strong position if you pitch it as:

"already the operating system for Indian agriculture."

That will overstate maturity and create diligence risk.

The practical assessment is:

- Strong on problem relevance
- Strong on strategic vision
- Moderate on innovation narrative
- Moderate on early traction
- Weak on full ecosystem execution today
- Weak on proof of working farmer-to-market workflow today

So the right answer is: Corppluse is grantable, but only if you position it as an AI-led agri coordination platform in transition from intelligence MVP to unified ecosystem, not as a completed super-platform.

## Best Grant Posture

Use this framing:

"Corppluse has proven early demand for agricultural intelligence among traders and is now building the next layer: AI-assisted farmer onboarding, market linkage, and transaction coordination. The long-term vision is a unified agriculture operating system, but the current grant will fund the core coordination MVP."

That aligns much better with the actual repo state in [PROJECT_STATUS.md](PROJECT_STATUS.md#L11), [croppulse/EXECUTIVE_SUMMARY.md](croppulse/EXECUTIVE_SUMMARY.md#L36), and [croppulse/CURRENT_VS_VISION.md](croppulse/CURRENT_VS_VISION.md#L150).

## Notes

This assessment is based on the current repo docs and implementation surfaces.