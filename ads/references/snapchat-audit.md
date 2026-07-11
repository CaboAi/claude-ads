# Snapchat Ads control reference

Retrieved: 2026-07-11. Refresh official platform and policy sources before using
this reference after its control-plane refresh date.

## Category weights

Measurement 25%, structure and delivery 20%, creative 20%, audience 15%, budget
and experimentation 10%, policy and brand safety 10%. The deterministic engine
applies these weights after scoring applicable controls within each category.

## Controls

| ID | Category | Evidence question |
| --- | --- | --- |
| SC-M01 | Measurement | Snap Pixel, Conversions API, MMP, or offline source is declared and verified. |
| SC-M02 | Measurement | Events and values match the objective and use documented deduplication when needed. |
| SC-M03 | Measurement | App campaigns include the required app measurement configuration. |
| SC-M04 | Measurement | Attribution windows and report fields are explicit and comparable. |
| SC-R01 | Reporting | Date boundaries use the ad-account timezone and the data-finalization window is disclosed. |
| SC-R02 | Reporting | Large or product-level reports use the supported asynchronous lifecycle. |
| SC-S01 | Structure | Campaign, ad-squad, ad, creative, and objective relationships are valid. |
| SC-S02 | Structure | Optimization, placements, and delivery choices match the declared outcome. |
| SC-A01 | Audience | Audience, geography, device, and first-party targeting are intentional and eligible. |
| SC-C01 | Creative | Creative is mobile-first and native to the selected Snap placement. |
| SC-C02 | Creative | Materially different hooks, formats, and concepts are available for testing. |
| SC-C03 | Creative | AR, Lens, Story, collection, or lead formats use their required assets and destinations. |
| SC-D01 | Retail | Catalog mappings, product availability, and product-level reporting validate when DPA is used. |
| SC-B01 | Budget | Budget, bid, pacing, and campaign caps are viable and use correct currency units. |
| SC-P01 | Policy | Brand-safety, age, privacy, regulated-category, and review-status constraints are checked. |
| SC-E01 | Experiment | Tests isolate one decision and account for reporting latency. |

Results use `pass`, `fail`, `unknown`, or `not_applicable`. Unknown controls
reduce evidence coverage; unavailable, beta, premium, or ineligible features are
unscored opportunities.

## Official sources

- [Snapchat Marketing API](https://developers.snap.com/marketing-api/home)
- [Snap Ads API](https://developers.snap.com/marketing-api/Ads-API/introduction)
- [Snap measurement API](https://developers.snap.com/marketing-api/Ads-API/measurement)
- [Snap Pixel](https://forbusiness.snapchat.com/advertising/snap-pixel)

Official product, API, policy, and regional availability sources override this
summary when they change. Practitioner material may supplement but not replace
official interface and policy evidence.
