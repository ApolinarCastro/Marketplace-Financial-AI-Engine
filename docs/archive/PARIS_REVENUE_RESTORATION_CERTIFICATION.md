# Paris Revenue Restoration Certification

## 1. Restoration Certification
This document certifies that the **Paris Gross Revenue & Commission Ingestion Pipeline** has been fully restored and certified under the **Single Financial Truth** guidelines.

## 2. Revenue Source Validation
- **Operational Rule**: All revenue entries classified under the `ingresos` group originate directly from the gross transaction value (`monto_bruto` / "MONTO") from the raw seller reports.
- **Settlement Isolation**: No operational revenue category originates from the net settlement value (`monto_neto` / "MONTO A PAGAR").
- **Deduplication and Splitting**: The marketplace commission is parsed and isolated into `costos_comerciales` as a separate ledger row, ensuring that summing the `monto` column of `ingresos` yields exactly the gross sales before commissions.

## 3. Automated Test Audit
- **TEST_PARIS_001 (Revenue Source Validation)**: Passed.
- **Universal Closing Query Validation**: Checked and verified that no custom coalesce or net-value overrides are present in Paris closing queries.

---
**Certified by:** Antigravity AI Auditor Engine  
**Execution Timestamp:** 2026-06-18
