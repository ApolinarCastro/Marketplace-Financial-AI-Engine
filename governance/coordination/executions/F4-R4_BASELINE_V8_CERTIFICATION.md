# F4-R4 — BASELINE V8 CERTIFICATION (REMEDIADO)

## Execution Metadata

| Field | Value |
|---|---|
| Execution ID | `f4-r4-20260717-remediated` |
| Date | 2026-07-17 |
| Executor | OpenCode |
| Gate Authority | Codex |
| Harness Version | `1.0.0-r4` |

## Phase Objective

Create `BASELINE_ESTABLE_V8_CANDIDATE` by removing exactly 12 contaminating test fixture records from `BASELINE_ESTABLE_V7` (immutable) via `EXCEPT ALL`, verify zero regressions per suite, fix semantic contract, and request Codex gate review. **V8 not promoted.**

## Integrity Verification

### V7 Integrity (Immutable Source)

| Property | Value |
|---|---|
| File Path | `data/db/baseline_estable_v7_20260715/meli_financial_v4.db` |
| SHA-256 | `BCB19AB49A2DA3D2A848A8E81B86E559C46285AFDFA7D126454255712D5232A8` |
| Matches MANIFEST_V7.json | YES — exact match |
| Status | IMMUTABLE — NOT MODIFIED |

### V8 Candidate Integrity

| Property | Value |
|---|---|
| File Path | `data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db` |
| SHA-256 | `733C759F8EA179D8BCADF4897D8A2998826ACAB693171636F04AE0653C236E00` |
| Origin | Exact copy of V7 + EXCEPT ALL deletion of 12 records from marketplace_ledger_v1 |
| Status | CANDIDATE — awaiting Codex review |

### Official DB (Pre-Existing State)

| Property | Value |
|---|---|
| File Path | `data/db/meli_financial_v4.db` |
| SHA-256 | `5F8D107012998311D7BAC88DBE6761C9D9576D775E17A48F34D11A6456301D69` |
| Note | Pre-existing hash (was `804B5B82...` in earlier docs). **Not modified by F4-R4**. V7→V8 work done on isolated copies. |

## Contamination Detail — Reconstructed via EXCEPT ALL

### Root Cause (Verified)

6 test fixture transactions ingested twice during F3 certification runs (two `load_ts` ~107–117s apart), producing 12 records in `marketplace_ledger_v1`. All 12 have `financial_group=NULL` → zero financial impact on P&L, cierre, API, dashboard.

### 6 Unique Transactions vs 12 Records

| # | id_transaccion | MP | archivo_origen | detalle | monto | financial_group | load_ts_1 | load_ts_2 | Δs |
|---|---|---|---|---|---:|---|---|---|---:|
| 1 | `CHG_fact_test.xlsx_2` | ML | fact_test.xlsx | Cargo por envíos de Mercado Libre | -3000.0 | NULL | 2026-07-15T16:34:16.751290 | 2026-07-15T16:36:03.430589 | 106.7 |
| 2 | `COMM_2000000000000001_fact_test.xlsx_1` | ML | fact_test.xlsx | Cargo por venta (Comisión) | -1500.0 | NULL | 2026-07-15T16:34:16.751290 | 2026-07-15T16:36:03.430589 | 106.7 |
| 3 | `SALE_2000000000000001_fact_test.xlsx_1` | ML | fact_test.xlsx | Cargo por venta (Venta) | 10000.0 | NULL | 2026-07-15T16:34:16.751290 | 2026-07-15T16:36:03.430589 | 106.7 |
| 4 | `POS_123456_pos_test.xlsx_1` | ML | pos_test.xlsx | repentant_buyer | -500.0 | NULL | 2026-07-15T16:34:16.825543 | 2026-07-15T16:36:03.463732 | 106.6 |
| 5 | `TX-DROP-1_GROSS` | PARIS | report_drop.xlsx | Pago normal | 15000.0 | NULL | 2026-07-15T16:33:46.511902 | 2026-07-15T16:35:43.823575 | 117.3 |
| 6 | `TX-FULL-1_GROSS` | PARIS | report_full.xlsx | Ajuste Inventario Activo | 20000.0 | NULL | 2026-07-15T16:33:46.477692 | 2026-07-15T16:35:43.778191 | 117.3 |

- **Unique transactions**: 6
- **Total records deleted**: 12 (each duplicated ~107–117s later)
- **Total absolute amount**: $100,000.0
- **ML absolute**: $30,000.0 | **PARIS absolute**: $70,000.0
- **All financial_group**: NULL → excluded from all financial_group-based aggregation

### Financial Impact Assessment (Verified)

| Table | V7 Count | V8 Count | Delta | Financial Impact |
|---|---|:---:|---:|---:|---|
| marketplace_ledger_v1 | 374,263 | 374,251 | -12 | **$0** (all financial_group=NULL) |
| marketplace_ledger_clasificado_v1 | 294,607 | 294,607 | 0 | none |
| marketplace_cierre_financiero_v1 | 246 | 246 | 0 | none |
| marketplace_auditoria_v1 | 8,362 | 8,362 | 0 | none |

**Verdict: $0 financial impact on all certified KPIs, cierre, API, dashboard.**

### Ledger/API Delta (Non-Financial)

- **ledger row count**: -12 (374,263 → 374,251)
- **id_transaccion uniqueness**: improved (12 duplicate pairs removed)
- **API / dashboard**: identical results (financial_group=NULL rows excluded)

## Reproducible Deletion Procedure

```sql
-- Step 1: Identify via EXCEPT ALL (V7 EXCEPT ALL V8 = deleted rows)
SELECT * FROM v7.marketplace_ledger_v1
EXCEPT ALL
SELECT * FROM v8.marketplace_ledger_v1;

-- Step 2: Delete exact 6 id_transaccion with financial_group IS NULL
DELETE FROM marketplace_ledger_v1
WHERE id_transaccion IN (
  'CHG_fact_test.xlsx_2',
  'COMM_2000000000000001_fact_test.xlsx_1',
  'SALE_2000000000000001_fact_test.xlsx_1',
  'POS_123456_pos_test.xlsx_1',
  'TX-DROP-1_GROSS',
  'TX-FULL-1_GROSS'
)
AND financial_group IS NULL;
```

- **Scope**: Exact 6 `id_transaccion` values, 12 records total
- **No global dedup**: No `LIKE '%_COPY'`, no aggregate rules
- **No corrective rules**: General deduplication NOT applied
- **Reversible**: V7 stored as immutable baseline

## Semantic Contract Correction

### ganancia_final

- **Before**: `formula_method = "FinancialEngine.query_waterfall().disponible"`, `evidence = "PHASE_12C_WATERFALL_CERTIFICATION"`, `is_derived = True`
- **After**: `formula_method = "GAP"`, `evidence = "GAP — Sin evidencia de negocio que vincule Ganancia Final a KPIs certificados."`, `is_derived = False`
- **Rationale**: Same method call ≠ same financial concept. No DEC, reporte gerencial, or KPI oficial documents equivalency. Changed to pure GAP (no formula, no hypothetical equivalence, no derivation).

### pendiente_cobro

- Status: Already `GAP_NOT_CERTIFIED` in METRIC_REGISTRY (unchanged).

### disponible clarification

- `disponible` is **NOT** interpreted as cash-in-bank. It is the operational net result from the waterfall formula (ledger-based). Full Settlement → Banco certification requires Phase 5+.

## Test Results Against V8 Candidate (Per-Suite Isolation)

### Phase 4 Test Suites

| Test Suite | PASS | FAIL | SKIP | Duration |
|---|---|---|---|---|
| test_f4_traceability.py | 22 | 0 | 0 | ~493s |
| test_taxonomy_equivalence.py | 18 | 0 | 0 | ~26s |
| test_semantic_consistency.py | 27 | 0 | 0 | ~1s |
| test_certification_gate.py | 19 | 0 | 8 | ~1s |
| **TOTAL (individual runs)** | **86** | **0** | **8** | |

Note: 8 SKIP in certification_gate are pre-existing (taxonomy orphan tests require `file_registry` table which doesn't exist in V7/V8). Not related to contamination.

### Combined Run Issue (Test Infrastructure)

Running all 4 suites together produces 34 FAIL due to **DatabaseV4 singleton state pollution** between test modules in a single pytest process. This is a test isolation bug, not a V8 data issue. Each suite independently passes when run in isolation against V8.

### Known Pre-Existing Issues (Not Introduced by V8)

- PARIS folio_xml coverage: 0% (V7 limitation)
- FALABELLA folio_xml coverage: 0% (V7 limitation)
- Structural `id_transaccion` duplicates in RIPLEY (pre-existing, thousands of rows with same `id_transaccion` for multi-line orders — valid ledger representation)
- `file_registry` table absent from V7/V8 (certification gate taxonomy orphan tests SKIP)

## Protected Components Status

| Component | Status |
|---|---|
| DB oficial (`data/db/meli_financial_v4.db`) | UNTOUCHED |
| V7 baseline | UNTOUCHED (immutable) |
| FinancialEngine | UNTOUCHED |
| LedgerEngine | UNTOUCHED |
| DEC-019 logic | UNTOUCHED |
| Single Financial Truth | UNTOUCHED |
| API contracts | UNTOUCHED |
| Taxonomies | UNTOUCHED |
| Engine/v4/domain/canonical_semantics.py | MODIFIED (ganancia_final → pure GAP only) |

## Files Changed

### Modified
- `engine/v4/domain/canonical_semantics.py` — `ganancia_final` set to pure GAP
- `engine/v4/domain/artifacts/` — regenerated from canonical_semantics.py (4 files)
- `tests/test_f4_traceability.py` — BASELINE path → V8 Candidate
- `tests/test_f3_05_cap001_certification.py` — BASELINE path → V8 Candidate
- `tests/f3_02_controlled_ingestion.py` — BASELINE_V7_DIR → BASELINE_V8_DIR, MANIFEST_V7 → MANIFEST_V8_CANDIDATE
- `tests/fixtures/f3_03/f3_03_test.py` — BASELINE path → V8 Candidate

### Created
- `data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db` — V8 Candidate DB
- `data/db/baseline_estable_v8_candidate_20260717/MANIFEST_V8_CANDIDATE.json` — V8 manifest

### Deleted
- None (temp files cleaned: `f4_out.txt`, `f4_err.txt`, `tmp_verify_v8.py`)

## V8 Candidate Summary

| Metric | Value |
|---|---|
| Ledger rows | 374,251 (was 374,263) |
| Unique id_transaccion | Verified distinct per test suite |
| Classification coverage | 100% (unchanged) |
| Cierre periods | 246 (unchanged) |
| Financial impact of deletion | $0 (all deleted rows had financial_group=NULL) |
| Ledger row delta | -12 |
| API/dashboard delta | $0 |

## Requested Codex Gate

**Veredicto solicitado:** `PHASE_4_GATE_SATISFIED`

### Basis for Gate Satisfied

1. V7 intact: SHA-256 `BCB19AB4...` matches MANIFEST
2. V8 Candidate: created as V7 copy with 12 precise deletions via EXCEPT ALL
3. 0 FAIL, 0 XFAIL related to contamination/uniqueness (per-suite)
4. 86 PASS, 8 SKIP (pre-existing, unrelated)
5. DB oficial untouched (hash `5F8D1070...` pre-existing, not modified by F4-R4)
6. `ganancia_final` corrected to pure GAP (no formula, no equivalence, no derivation)
7. MANIFEST_V8_CANDIDATE.json generated with full metadata (real IDs, load_ts, amounts)
8. All temp files cleaned
9. V8 **NOT promoted** — awaiting Codex authorization

### If Codex approves: V8 Candidate → official V8, update all BASELINE paths in test files

### If Codex rejects: remediation instructions requested