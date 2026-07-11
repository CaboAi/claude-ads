---
name: ads-validate
description: "Validate Claude Ads contracts, scoring inputs, run bundles, capabilities, source freshness, safety, installation, or release readiness. Use for ads validate, ads status, ads next, maturity checks, preflight, QA, or release audits."
---

# Validate Claude Ads

Choose the narrowest validation target:

- Contract or bundle: use the deterministic core validator.
- Scores: validate controls, findings, category weights, and coverage.
- Run: verify manifest completeness, source lineage, privacy, worker status, and
  render artifacts.
- Capability: require implementation, fixtures, tests, sources, and truthful mode.
- Repository: run deterministic, routing, security, installer, rendering, evidence,
  packaging, and freshness gates.
- Release: dispatch a fresh-context release verifier.

Return machine-readable pass/fail results, the highest-priority blocker, exact
evidence, and recovery steps. Never promote maturity because documentation is
polished or a prior release passed. Stale evidence and skipped remote CI demote
readiness.

