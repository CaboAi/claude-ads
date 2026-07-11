# Amazon Ads control reference

Retrieved: 2026-07-11. Refresh official product, API, policy, and availability
sources before using this reference after its control-plane refresh date.

## Category model

The platform capability manifest supplies category weights that total 100. The
deterministic engine applies weights after scoring applicable controls within
each category; it never multiplies the category weight into each individual row.

## Controls

| ID | Category | Evidence question |
| --- | --- | --- |
| AMZ-M01 | Measurement | Profile, marketplace, region, currency, timezone, and attribution window are explicit. |
| AMZ-M02 | Measurement | Orders, sales, ACOS, ROAS, TACOS, new-to-brand, and retail metrics are not conflated. |
| AMZ-M03 | Measurement | Async report lifecycle, status, download, pagination, and missing rows are validated. |
| AMZ-M04 | Measurement | Amazon Ads attribution is reconciled with Seller/Vendor and business-level outcomes. |
| AMZ-S01 | Structure | Portfolios, campaign types, targeting, and naming reflect product and objective ownership. |
| AMZ-S02 | Structure | Sponsored Products, Brands, Display, DSP, and video roles are separately evaluated. |
| AMZ-T01 | Targeting | Automatic, keyword, product, audience, and defensive targeting have explicit purposes. |
| AMZ-T02 | Targeting | Search-term harvesting and negatives are based on sufficient query and conversion evidence. |
| AMZ-R01 | Retail | Buy Box, inventory, price, reviews, detail-page quality, and suppression risks are checked. |
| AMZ-R02 | Retail | Catalog and variation relationships support the advertised ASINs and landing experience. |
| AMZ-C01 | Creative | Sponsored Brands, video, display, and Store assets match format and product promise. |
| AMZ-C02 | Creative | Materially different value propositions and formats are available for testing. |
| AMZ-B01 | Budget | Budget, bid, placement adjustments, and pacing reflect margin, stock, objective, and evidence. |
| AMZ-B02 | Budget | Automation changes respect profile/region scope, learning impact, and account ceilings. |
| AMZ-P01 | Policy | Product eligibility, claims, creative, audience, and marketplace policy constraints are checked. |
| AMZ-E01 | Experiment | Tests isolate one lever and account for retail, organic, price, and inventory changes. |

Use `pass`, `fail`, `unknown`, or `not_applicable`. Unknown controls reduce
coverage. Optional, beta, premium, unavailable, immutable, or ineligible features
are unscored opportunities.

## Official sources

- [Amazon Ads API overview](https://advertising.amazon.com/about-api/)
- [Amazon Ads learning console](https://advertising.amazon.com/academy/library)
- [Amazon Ads support center](https://advertising.amazon.com/resources/ad-policy)

Official sources override this summary when they change. Vendor case studies and
recommendations must remain labeled and contextual rather than universalized.
