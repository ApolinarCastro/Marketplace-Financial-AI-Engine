# PFO FA-005 — LEVEL 1 vs TREASURY SCOPE RCA + REPAIR

## Task Info

```
TASK_ID: PFO-FA005-L1-TREASURY-RCA-001
DATE: 2026-10-06
HEAD_BEFORE: 535790ec11ade44f255e61333449159f1e8d9831
BRANCH: main
```

## Root Cause (demonstrated, not inferred)

```
ROOT_CAUSE: LEVEL_1_SCOPE_INCLUDES_NON_OPERATIONAL_TREASURY_FOR_ML
```

ReconciliationEngine Level 3 requires `operational_total + treasury_total ≈ 0`,
so a valid treasury row (financial_group='tesoreria', op_pnl=FALSE) is
mandatory. But Level 1 `_level_1_internal` exempted ML from the operational
scope filter (`if marketplace != "ML"`), so the same valid row raised
`UNEXPECTED_GROUP:tesoreria`.

Pre-repair demonstration (isolated fresh TEMP DB, op +20800 / treasury -20800,
cierre neto 20800):

```
PRE_REPAIR_LEVEL_1_STATUS: ALERTA
PRE_REPAIR_LEVEL_1_ALERTS: [('UNEXPECTED_GROUP:tesoreria', -20800.0)]
PRE_REPAIR_LEVEL_3_STATUS: PASS
PRE_REPAIR_LEVEL_3_DELTA: 0.0
```

## Contract Evidence (Option A demonstrated)

- `run_financial_closing` aggregates `include_in_operational_pnl = TRUE` only
  (marketplace_auditor.py line 672).
- Tesoreria rows carry op_pnl=FALSE (auditor lines 543, 549-550).
- P40_EVIDENCE_GRAPH: ML cierre built exclusively from op_pnl=1 rows.
- Therefore cierre (Level 1 target) never contains tesoreria; Level 1 source
  must scope identically. No justification found for the ML exception
  (single-commit file history; governance docs uniformly describe ML
  operational semantics as op_pnl=1-based: DEC-019, P40, PHASE_15A).

```
CLOSING_SCOPE: include_in_operational_pnl = TRUE (all MPs incl. ML)
TREASURY_SCOPE: op_pnl = FALSE by design (required by Level 3 mirror)
```

## Repair Selected

File: `engine/v4/reconciliation/reconciliation_engine.py` (comment + 1 filter line).

```python
op_filter = "AND include_in_operational_pnl = TRUE"
```

Uniform operational scope for all marketplaces (ML exception removed).
Aligns Level 1 source scope with the cierre target scope.

## Repair Rejected (alternative)

Excluding only `tesoreria` from `extra_groups`: rejected as band-aid —
leaves other current/future op_pnl=0 groups able to raise the same false
UNEXPECTED_GROUP. The op_filter is the principled scope alignment.
Only one repair applied (never both).

## Post-Repair Verification (same isolated scenario)

```
POST_REPAIR_LEVEL_1_STATUS: PASS
POST_REPAIR_LEVEL_1_DELTA: 0.0 (alerts: [])
POST_REPAIR_LEVEL_3_STATUS: PASS
POST_REPAIR_LEVEL_3_DELTA: 0.0
```

## Negative Control (treasury -15000 vs operational +20800)

```
NEGATIVE_CONTROL_STATUS: LEVEL_3 = ALERTA (repair does not mask real mismatch)
NEGATIVE_CONTROL_DELTA: 5800.0
LEVEL_1 with broken mirror: still PASS (treasury correctly out of L1 scope)
```

## Regression Results

```
New scope tests (tests/test_reconciliation_l1_treasury_scope.py): 2/2 PASS
Reconciliation engine suite: 6/6 PASS
Document match writer: 10/10 PASS
Golden E2E_V1 integrity: 11/11 PASS
ML audit: 1/1 PASS
```

## Change Summary

```
ENGINE_FILES_MODIFIED: engine/v4/reconciliation/reconciliation_engine.py (1)
  (+6/-3 lines: comment + uniform op_filter; no formula, rule, or threshold changed)
TESTS_ADDED: tests/test_reconciliation_l1_treasury_scope.py (2 tests)
NO FINANCIAL FORMULA CHANGED / NO CLOSING FORMULA CHANGED / NO GOLDEN MODIFIED
PRODUCTION_DB_MODIFIED: FALSE / REAL_RAW_MODIFIED: FALSE
```

## Effect on FA-005

```
FA-005_STATUS: FAIL (unchanged until E2E_V2 re-execution; prior 05_ evidence stands)
E2E_V2_STATUS: READY (treasury-scope conflict resolved; document path resolved earlier)
```

## Next Exact Action

Build and execute E2E_V2 (treasury row + writer-created CONCILIATED matches
on fresh TEMP_DB with new DDL table), precompute expected reconciliation in
engine vocabulary, execute ReconciliationEngine, compare.
