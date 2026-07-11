# Apple Ads control reference

Retrieved: 2026-07-11. Refresh official product, API, policy, and availability
sources before using this reference after its control-plane refresh date.

## Category model

The platform capability manifest supplies category weights that total 100. The
deterministic engine applies weights after scoring applicable controls within
each category; it never multiplies the category weight into each individual row.

## Controls

| ID | Category | Evidence question |
| --- | --- | --- |
| AP-M01 | Measurement | AdServices, AdAttributionKit, MMP, or internal attribution sources and limitations are declared. |
| AP-M02 | Measurement | Installs and post-install events reconcile across Apple Ads and the app analytics source. |
| AP-M03 | Measurement | Attribution privacy thresholds and missing detail are treated as uncertainty, not zero performance. |
| AP-M04 | Measurement | Campaign, placement, ad-group, keyword, search-term, and ad reports use comparable windows. |
| AP-S01 | Structure | Campaigns separate brand, category, competitor, discovery, and placement intent where material. |
| AP-S02 | Structure | Search Match discovery and manually targeted keywords do not create uncontrolled overlap. |
| AP-K01 | Keywords | Match type, negatives, search terms, and keyword movement follow observed query evidence. |
| AP-K02 | Keywords | Bid and CPT decisions consider tap-through, conversion, CPA, value, and volume together. |
| AP-A01 | Audience | Country, device, customer type, demographics, and audience choices are eligible and intentional. |
| AP-C01 | Creative | Default and custom product pages match keyword, placement, audience, and app-store promise. |
| AP-C02 | Creative | Product-page tests isolate creative or message changes and have sufficient observation time. |
| AP-B01 | Budget | Budget allocation and pacing preserve discovery while funding proven intent. |
| AP-B02 | Budget | Goal-based bidding or automation is recommended only when eligible and supported by evidence. |
| AP-R01 | Reporting | Currency, timezone, delayed attribution, and API pagination/report completeness are disclosed. |
| AP-P01 | Policy | App, market, age, privacy, and product eligibility requirements are checked. |
| AP-E01 | Experiment | Tests define hypothesis, placement, primary metric, guardrails, and readout window. |

Use `pass`, `fail`, `unknown`, or `not_applicable`. Unknown controls reduce
coverage. Optional, beta, premium, unavailable, immutable, or ineligible features
are unscored opportunities.

## Official sources

- [Apple Ads performance measurement](https://ads.apple.com/app-store/help/attribution/0028-measuring-ad-performance)
- [Apple Ads reports API](https://developer.apple.com/documentation/apple_ads/reports)
- [Apple Ads developer documentation](https://developer.apple.com/documentation/apple_ads)

Official sources override this summary when they change. Vendor case studies and
recommendations must remain labeled and contextual rather than universalized.
