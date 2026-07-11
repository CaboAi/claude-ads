# X Ads control reference

Retrieved: 2026-07-11. Refresh official platform and policy sources before using
this reference after its control-plane refresh date.

## Category weights

Measurement 25%, structure and delivery 20%, creative 20%, audience 15%, budget
and experimentation 10%, policy and brand safety 10%. The deterministic engine
applies these weights after scoring applicable controls within each category.

## Controls

| ID | Category | Evidence question |
| --- | --- | --- |
| XA-M01 | Measurement | X Pixel, Conversions API, MMP, or offline source is declared and verified. |
| XA-M02 | Measurement | Conversion events avoid sensitive categories and comply with X data-use policy. |
| XA-M03 | Measurement | Identifiers, event values, and browser/server deduplication are documented. |
| XA-M04 | Measurement | App campaigns use a supported mobile measurement path. |
| XA-S01 | Structure | Campaign objective and optimization event match the business outcome. |
| XA-S02 | Structure | Campaign, line-item/ad-group, creative, and account eligibility are valid. |
| XA-A01 | Audience | Keyword, conversation, interest, follower-lookalike, geography, and first-party choices are evidence-based. |
| XA-A02 | Audience | Prospecting, retargeting, exclusions, and expansion avoid unintended overlap. |
| XA-C01 | Creative | Copy and media fit the selected format, placement, and landing-page promise. |
| XA-C02 | Creative | Creative diversity covers materially distinct hooks, concepts, and formats. |
| XA-C03 | Creative | Replies and conversation context are considered where the placement exposes them. |
| XA-B01 | Budget | Budget, bid, pacing, and optimization state are viable for available evidence. |
| XA-R01 | Reporting | Date window, attribution, currency, and metric definitions are consistent. |
| XA-R02 | Reporting | Organic signals remain separate from paid attribution and optimization claims. |
| XA-P01 | Policy | Brand-safety, adjacency, regulated-category, privacy, and account-status risks are reviewed. |
| XA-E01 | Experiment | Tests isolate one decision with a declared window and success measure. |

Results use `pass`, `fail`, `unknown`, or `not_applicable`. Unknown controls
reduce evidence coverage; unavailable, beta, premium, or ineligible features are
unscored opportunities.

## Official sources

- [X website conversion tracking](https://business.x.com/en/help/campaign-measurement-and-analytics/conversion-tracking-for-websites/about-conversion-tracking)
- [X measurement overview](https://business.x.com/en/advertising/measurement)
- [X Ads business resources](https://business.x.com/en/advertising)

Official product, API, policy, and regional availability sources override this
summary when they change. Practitioner material may supplement but not replace
official interface and policy evidence.
