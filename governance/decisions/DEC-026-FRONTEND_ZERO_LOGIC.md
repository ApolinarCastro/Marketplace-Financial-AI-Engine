# DEC-026: Frontend Zero Logic

**Status**: ENFORCED  
**Date**: 2026-06-16  
**Author**: System (Phase 11)

## Decision

**Zero financial logic in frontend code.** All taxonomy mappings, calculations, and data transformations must occur server-side.

## Rationale

- `mapDetalleToConcept()` removed from `executive_dashboard.html` (35+ JS mappings)
- Waterfall `cobros` field now computed server-side in `/api/v4/exec/waterfall`
- `||` operator corrected to `??` in dashboard.html (was hiding $0 values)
- FINANCIAL_LABEL_TRUTH remediation: `const aju` now reads from `currentDesglose` not `window._cierreCertified`

## Scope

- Templates: `templates/executive_dashboard.html`, `templates/dashboard.html`
- API: `/api/v4/exec/cobros-breakdown` (server-classified), `/api/v4/exec/waterfall` (server-computed cobros)
- Zero new endpoints needed for financial logic

## Verification

- `test_zero_heuristics` in test_regression_contracts.py checks api.py for `startswith` patterns and dashboard.html for `catmap` patterns
- 14/14 regression tests must PASS after any frontend change

## Enforcement

Any new frontend code that contains:
- Hardcoded concept names
- Financial calculations (`+`, `-`, `*`, `/` on monetary values)
- `if/else` chains based on detalle or marketplace
- Regex or string matching on financial data

...will be **rejected** in code review.

## Rollback

N/A — this is a policy decision, not a code toggle.
