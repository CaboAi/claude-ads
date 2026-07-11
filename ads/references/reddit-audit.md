# Reddit Ads control reference

Retrieved: 2026-07-11. Refresh official platform and policy sources before using
this reference after its control-plane refresh date.

## Category weights

Measurement 25%, structure and delivery 20%, creative 20%, audience 15%, budget
and experimentation 10%, policy and brand safety 10%. The deterministic engine
applies these weights after scoring applicable controls within each category.

## Controls

| ID | Category | Evidence question |
| --- | --- | --- |
| RD-M01 | Measurement | Primary conversion source and ownership are identified. |
| RD-M02 | Measurement | Reddit Pixel or Conversions API events match the business conversion taxonomy. |
| RD-M03 | Measurement | Pixel and server events use deduplication when both paths send the same event. |
| RD-M04 | Measurement | Events Manager diagnostics and representative test events have been reviewed. |
| RD-S01 | Structure | Campaign objective and optimization event match the business outcome. |
| RD-S02 | Structure | Prospecting and retargeting intent are distinguishable and exclusions prevent avoidable overlap. |
| RD-A01 | Audience | Community, interest, keyword, or first-party targeting is supported by the offer and evidence. |
| RD-A02 | Audience | Audience expansion is deliberate and measured rather than assumed beneficial. |
| RD-C01 | Creative | Creative reads naturally in the selected Reddit placement and community context. |
| RD-C02 | Creative | Materially different concepts, hooks, and formats are available for testing. |
| RD-C03 | Creative | Ad promise, comment context, and landing-page experience remain consistent. |
| RD-R01 | Retail | Catalog fields, availability, prices, links, and refresh behavior are healthy when commerce formats are used. |
| RD-R02 | Retail | Dynamic product advertising maps the relevant catalog and measurement source. |
| RD-B01 | Budget | Budget and bid strategy are viable for the objective, data volume, and test design. |
| RD-P01 | Policy | Brand-safety, placement, regulated-category, and privacy controls have been reviewed. |
| RD-E01 | Experiment | Tests isolate a decision, define success criteria, and avoid overlapping changes. |

Results use `pass`, `fail`, `unknown`, or `not_applicable`. Unknown controls
reduce evidence coverage; unavailable, beta, premium, or ineligible features are
unscored opportunities.

## Official sources

- [Reddit catalogs](https://business.reddithelp.com/articles/Knowledge/catalogs)
- [Reddit dynamic product ads](https://business.reddithelp.com/articles/Knowledge/dynamic-product-ads)
- [Reddit conversion events](https://business.reddithelp.com/articles/Knowledge/supported-conversion-events)

Official product, API, policy, and regional availability sources override this
summary when they change. Practitioner material may supplement but not replace
official interface and policy evidence.
