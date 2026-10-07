# PFO FA-006 — EXPECTED = ACTUAL EVIDENCE

## Task Info

```
TASK_ID: PFO-FA006-EXPECTED-ACTUAL-001
DATE: 2026-10-07
HEAD: 335dd5d009232c59dbd7ec98b403a894f0699ded
BRANCH: main
```

## Formal Definition

```
FA-006: Expected = Actual for the certified Golden E2E result.
```

No re-execution performed: `11_FA005_E2E_V2_R1_*` evidence contains every
required value (REEXECUTION_REQUIRED = NO). Sources below are that evidence
plus the versioned golden files (read-only verification).

## Ledger (§4)

Source: `11_FA005_E2E_V2_R1_COMPARISON.json` (raw parity block, checks.raw_parity).

```
EXPECTED_LEDGER_ROWS: 9 (expected_ledger.csv)
ACTUAL_LEDGER_ROWS: 9 (TEMP_DB marketplace_ledger_v1, archivo_origen filter)
MISSING_ROWS: 0 / UNEXPECTED_ROWS: 0 / FIELD_MISMATCHES: 0
ROW_BY_ROW_EQUAL: TRUE
```

## Financial Values (§5)

```
EXPECTED_OPERATIONAL_NET: 20800.0 / ACTUAL: 20800.0 (closing_result.neto)
EXPECTED_TREASURY: -20800.0 / ACTUAL: -20800.0 (treasury_detail sum)
EXPECTED_TREASURY_MIRROR_DELTA: 0.0 / ACTUAL: 0.0
EXPECTED_DOCUMENT_COVERAGE: 100.0 / ACTUAL: 100.0 (9/9, 0 orphans)
```

## Reconciliation (§6)

```
LEVEL_1 EXPECTED PASS delta 0.0 / ACTUAL PASS delta 0.0 (20800 vs 20800, 0 alerts)
LEVEL_2 EXPECTED PASS delta 0.0 / ACTUAL PASS delta 0.0 (20800 vs 20800)
LEVEL_3 EXPECTED PASS delta 0.0 / ACTUAL PASS delta 0.0 (-20800 vs -20800)
LEVEL_4 EXPECTED PASS delta 0.0 / ACTUAL PASS delta 0.0 (9 vs 9, coverage 100.0)
RECONCILIATION_FIELD_MISMATCHES: 0 (missing_levels 0, unexpected_levels 0)
```

## Aggregate (§7)

```
EXPECTED_AGGREGATE_STATUS: CERTIFICADO / ACTUAL: CERTIFICADO
EXPECTED_AGGREGATE_DELTA: 0 / ACTUAL: 0.0
EXPECTED_TAXONOMY_COVERAGE: 100 / ACTUAL: 100.0
EXPECTED_DOCUMENT_COVERAGE: 100 / ACTUAL: 100.0
```

## Totals

```
TOTAL_FIELD_MISMATCHES: 0 (ledger 0 + reconciliation 0)
MISSING_ROWS/LEVELS: 0 / UNEXPECTED_ROWS/LEVELS: 0
```

## Boundaries (§8, unchanged)

```
DOCUMENTAL_XML_TRACEABILITY: PASS
FINANCIAL_DTE_MATCH: PASS
XML_DTE_E2E: PASS
ELECTRONIC_SIGNATURE_CERTIFICATION: NOT_IMPLEMENTED (does not block FA-006)
```

## Verdict (§10)

```
LEDGER_EXPECTED_ACTUAL: TRUE
FINANCIAL_EXPECTED_ACTUAL: TRUE
RECONCILIATION_EXPECTED_ACTUAL: TRUE
AGGREGATE_EXPECTED_ACTUAL: TRUE
FA-006: PASS
FA-007_STATUS: READY
FIRST_BLOCKER: NONE
```

## Next Exact Action

PFO-FA007-RESTART-REPRODUCIBILITY-001. No FA-007 auto-run.
