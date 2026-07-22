# P32R7 — Regression Certification

**Date:** 2026-07-07
**Scope:** Surgical regression audit of Marketplace Financial AI Engine test suite

## Test Suite Results

| Metric | P30 (Previous) | P32R7 (Current) | Delta |
|--------|---------------|-----------------|-------|
| Collected | 278 | 278 | 0 |
| PASS | 268 | 265 | -3 |
| FAIL | 2 | 5 | +3 |
| SKIP | 8 | 8 | 0 |
| PASS Rate | 96.4% | 95.3% | -1.1% |

## PASSING (265/278)

All core financial engine tests continue to pass:
- `test_clean_records` ✅
- `test_list_periods` ✅
- `test_query_cierre` ✅
- `test_query_cierre_all` ✅
- `test_query_ledger` ✅
- `test_query_waterfall_v3` ✅
- `test_certify_single_financial_truth` ✅
- `test_certification_gate` ✅ (27 sub-tests)
- Full Phase 12 suite (39 tests) ✅

## FAILING ANALYSIS (5 tests)

### ❌ NEW REGRESSION — `test_map_detalle_to_concept`
**Root Cause:** `FinancialEngine.map_detalle_to_concept()` at `engine/v4/domain/financial_engine.py:276` is defined as:
```python
def map_detalle_to_concept(detalle: str) -> str:
```
The `self` parameter is missing. The test calls `fe.map_detalle_to_concept(detalle)` which Python translates to `FinancialEngine.map_detalle_to_concept(self, detalle)` — 2 positional args, method only accepts 1.

**Impact:** BREAKING. The server-side detalle→concept mapping is unreachable via instance. Frontend Cobros breakdown depends on this mapping indirectly via the `/api/v4/exec/cobros-breakdown` endpoint.

**Fix:** Add `self` as first parameter.

### ❌ ENVIRONMENT — `test_query_cobros_breakdown`
**Root Cause:** DB locked by PID 8284 (external DuckDB connection)

### ❌ ENVIRONMENT — `test_query_cobros_breakdown_by_mp`
**Root Cause:** Same DB lock (PID 8284)

### ❌ ENVIRONMENT — `test_recursive_glob_ingests_from_subdirectories`
**Root Cause:** Same DB lock (PID 8284)

### ❌ ENVIRONMENT — `test_full_pipeline_ingestion_classification_and_audit`
**Root Cause:** Same DB lock (PID 8284)

## SKIP ANALYSIS (8 tests)

All 8 skipped tests are due to taxonomy path mismatch:
- Tests expect taxonomies at `knowledge/taxonomy/`
- Files are at `KnowledgeBase/Marketplace/Taxonomy/`
- This affects Phase 13/15B taxonomy tests only
- No financial logic impact

## Critical vs Non-Critical Regression

| Category | Count | Critical |
|----------|-------|----------|
| P0 (data corruption) | 0 | — |
| P1 (broken feature) | 1 | `map_detalle_to_concept` |
| P2 (environment) | 4 | DB lock |
| P3 (config/path) | 8 | Taxonomy path |

## Verdict

**FAIL** ❌ — 1 new real regression (`map_detalle_to_concept` method signature) downgrades from P30 status. The server-side concept mapping contract is broken.
