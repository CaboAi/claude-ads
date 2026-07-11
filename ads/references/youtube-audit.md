# YouTube Ads control reference

Retrieved: 2026-07-11. Refresh official product, API, policy, and availability
sources before using this reference after its control-plane refresh date.

## Category model

The platform capability manifest supplies category weights that total 100. The
deterministic engine applies weights after scoring applicable controls within
each category; it never multiplies the category weight into each individual row.

## Controls

| ID | Category | Evidence question |
| --- | --- | --- |
| YT-M01 | Measurement | Primary conversion or engagement goal and its counting role are explicit. |
| YT-M02 | Measurement | Google Ads, GA4, channel-link, view-through, and assisted measurement choices are reconciled. |
| YT-M03 | Measurement | YouTube and non-YouTube Demand Gen inventory are separated in reporting where needed. |
| YT-M04 | Measurement | Brand-lift or incrementality methods are used when direct response cannot answer the objective. |
| YT-S01 | Structure | Campaign subtype, channel controls, objective, bidding, and inventory match the intended outcome. |
| YT-S02 | Structure | Migrated or legacy Video Action Campaign state and incompatible settings are reviewed. |
| YT-A01 | Audience | Audience signals or segments match intent and first-party exclusions avoid overlap. |
| YT-A02 | Audience | Content suitability, placements, topics, and inventory controls are intentionally governed. |
| YT-C01 | Creative | The opening earns attention before skip behavior and communicates the offer clearly. |
| YT-C02 | Creative | Horizontal, vertical, square, short, and long formats cover intended inventory. |
| YT-C03 | Creative | Materially different concepts and hooks are available, not cosmetic variants. |
| YT-C04 | Creative | Demand Gen asset and product-feed choices are deliberate and eligible. |
| YT-B01 | Budget | Bid and budget strategy fit the objective, evidence volume, and campaign maturity. |
| YT-R01 | Reporting | View, engagement, click, conversion, and cost metrics use a consistent window and definition. |
| YT-P01 | Policy | Content suitability, brand safety, disclosures, and regulated-category obligations are checked. |
| YT-E01 | Experiment | Creative or audience experiments isolate one decision and account for conversion lag. |

Use `pass`, `fail`, `unknown`, or `not_applicable`. Unknown controls reduce
coverage. Optional, beta, premium, unavailable, immutable, or ineligible features
are unscored opportunities.

## Official sources

- [Demand Gen campaigns](https://support.google.com/google-ads/answer/13695777?hl=en)
- [VAC to Demand Gen migration](https://support.google.com/google-ads/answer/15110871?hl=en)
- [YouTube Engagement goals](https://support.google.com/google-ads/answer/12301500?hl=en)
- [Demand Gen creative guide](https://support.google.com/google-ads/answer/14733311?hl=en)

Official sources override this summary when they change. Vendor case studies and
recommendations must remain labeled and contextual rather than universalized.
