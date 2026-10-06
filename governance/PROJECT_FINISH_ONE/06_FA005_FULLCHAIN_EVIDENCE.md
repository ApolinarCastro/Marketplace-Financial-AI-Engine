# PFO FA-005 FULL-CHAIN GOLDEN — INVESTIGATION EVIDENCE

## Task Info

```
TASK_ID: PFO-FA005-GOLDEN-FULLCHAIN-001
DATE: 2026-10-06
HEAD: b14a5e9f91b6640bb75c2379e52a5ea173bd768b
BRANCH: main
STATUS: BLOCKED (document ingestion path does not exist)
```

No engine code modified. No golden files created. Read-only contract recovery.
E2E_V1 preserved untouched. No E2E_V2 directory created.

---

## FASE 1 — Real Contracts Recovered

### LEVEL_1 (INTERNA): clasificado vs cierre

```
LEVEL_1_SOURCE: marketplace_ledger_clasificado_v1 (SUM per financial_group)
LEVEL_1_TARGET: marketplace_cierre_financiero_v1 (resultado_neto + group totals)
```

### LEVEL_2 (OPERACIONAL): op_pnl vs resultado_neto

```
LEVEL_2_SOURCE: clasificado_v1 WHERE include_in_operational_pnl=1 (SUM monto)
LEVEL_2_TARGET: cierre_v1 resultado_neto (SUM)
```

### LEVEL_3 (TESORERÍA): P&L mirror

```
LEVEL_3_SOURCE: clasificado_v1 WHERE financial_group='tesoreria' (SUM monto)
LEVEL_3_TARGET: mirror of Level 2 operational_total (equation: op + treasury ≈ 0)
Source: reconciliation_engine.py lines 418-474.
```

### LEVEL_4 (DOCUMENTAL): ledger vs document_match

```
LEVEL_4_SOURCE: clasificado_v1 (COUNT) + document_match_v1
  JOIN ON (marketplace, id_transaccion = ledger_id)
  WHERE match_status = 'CONCILIATED' (matched count)
LEVEL_4_TARGET: total clasificado rows (coverage denominator)
Source: reconciliation_engine.py lines 480-582.
```

### LEVEL_5 (AGGREGATE)

```
LEVEL_5_AGGREGATION: _determine_status(total_delta, taxonomy, document)
  via reconciliation_rules.yaml thresholds.
Source: reconciliation_engine.py lines 94-116, 164-184.
```

### Tables

```
ledger: marketplace_ledger_v1 (SurgicalLoader LEDGER_COLS, 9 cols, no financial_group)
classified ledger: marketplace_ledger_clasificado_v1 (MarketplaceAuditor, HAS financial_group)
financial closing: marketplace_cierre_financiero_v1 (run_financial_closing derives from clasificado)
treasury / settlement: clasificado_v1 rows with financial_group='tesoreria' (no separate table)
document_match: document_match_v1 (15 cols; key marketplace+ledger_id; status CONCILIATED counted)
DTE truth: dte_truth_v1 (read by matchers; NOT read by Level 4 / coverage helpers)
```

---

## FASE 2 — Treasury Contract (PROVEN PATH EXISTS)

```
TREASURY_TABLE: marketplace_ledger_clasificado_v1 (financial_group='tesoreria')
TREASURY_AMOUNT_FIELD: monto (SUM)
TREASURY_SIGN_CONVENTION: negative sums against positive operational P&L
  (mirror: op + treasury ≈ 0; op=20800 requires treasury=-20800)
TREASURY_TRANSACTION_KEY: id_transaccion (loader-generated CHG_... pattern)
TREASURY_PERIOD_FIELD: fecha (range-filtered >= start AND <= end)
TREASURY_MARKETPLACE_FIELD: marketplace (= 'ML')
```

Classification path (real, code-verified, no execution in this task):

```
- Input detalle "Retiro de dinero" → loader else-branch → CARGO row, det_orig preserved
- normalize_detail → NORMALIZED_CLASSIFICATION_MAP → "Retiro de dinero"
- FINANCIAL_STRUCTURE["tesoreria"] contains "Retiro de dinero" (auditor line 377-382)
- CLASIFICACION_TO_FINANCIAL_GROUP → 'tesoreria' (auditor line 580)
- op_pnl exclusions: ML mask line 543 (contains 'retiro de dinero') + general
  exclusions line 549-550 ("Retiro de dinero") → op_flag = FALSE
- Result: tesoreria row EXCLUDED from Level 2 operational sum, INCLUDED in Level 3
```

Expected treasury input (not created — blocked before FASE 6):

```
("E2E-TES", "Retiro de dinero", 20800.0, 0.0, "2026-06-20")
→ ledger monto = -20800.0 → treasury sum = -20800.0
→ mirror: 20800 + (-20800) = 0 ✓ (mathematically derived, never executed)
```

No existing fixture needed: the ML Facturacion loader else-branch + auditor
map already handle this detalle. Format reuse confirmed (same XLSX columns).

---

## FASE 3 — Document Contract (NO SAFE PATH — BLOCKER)

```
DOCUMENT_MATCH_KEY: (marketplace, ledger_id = id_transaccion)
DOCUMENT_STATUS_REQUIRED: 'CONCILIATED' (Level 4 matched count);
  _document_coverage counts any non-null match_id (LEFT JOIN).
DOCUMENT_COVERAGE_FORMULA: matched / total * 100 over clasificado_v1 period scope.
MINIMUM_MATCH_REQUIRED: 8/8 E2E_V1 rows (100% ≥ 95 CERTIFICADO threshold).
```

Writer search (engine/, tools/, api/, tests/):

```
MISSING_COMPONENT: no component writes document_match_v1.
  - engine/v4/matching/dte_ledger_matcher.py READS dte_truth_v1 + document_match_v1
    (ML direct match requires real SII folio_xml '033-...' + amount tolerance).
  - engine/v4/xml_matcher.py, dte_matcher.py: match runners, no document_match writer found.
  - tests/: zero fixtures reference document_match_v1.
  - tools/, api/: readers only.
  - Existing 9,431 rows: match_source='deterministic_engine', created_by='system_auditor'
    (offline/manual provenance, not a runnable tested component).
MISSING_FIXTURE: no test or fixture populates document_match_v1 for synthetic data.
MISSING_CONTRACT: no defined contract for creating synthetic document matches;
  direct INSERT is not an officially tested mechanism (task prohibition applies).
```

DTE synthetic chain assessed and rejected:

```
- Would require: synthetic DTE XML → DTEIndexer → dte_truth_v1 →
  DTELedgerMatcher (folio format + amount tolerance) → document_match_v1.
- Each link unproven for synthetic data; folio/matcher tolerances target real SII.
- Task prohibits inventing commercially-real DTE.
- Building this chain inside FA-005 scope = new architecture, explicitly out of scope.
```

Fresh-DB aggravator (verified in database.py DDL):

```
- document_match_v1 has NO CREATE TABLE in DatabaseV4 init (grep: zero matches).
- Fresh empty TEMP_DB would LACK the table → Level 4 queries fail with
  missing-table error (not graceful 0% coverage).
- Baseline-copy TEMP_DB has the table (9,431 rows) but 0 E2E_V1 matches.
- Either way, no safe path to E2E_V1 document coverage exists.
```

---

## FASE 4/6 — E2E_V2 Design (NOT BUILT — blocked)

Financial base preserved from E2E_V1 (net 20800, certified FA-004 R2 PASS).
Treasury addition designed but not created (see FASE 2 above).
Document addition: no safe design exists (see FASE 3).

```
MANUAL_LEDGER_NET: 20800.0 (E2E_V1 certified; treasury row would add -20800 separate group)
MANUAL_TREASURY_VALUE: -20800.0 (derived from mirror equation; never persisted)
MANUAL_DOCUMENT_COVERAGE: UNDEFINED (no match creation path; cannot precompute honestly)
```

---

## Verdict

```
EMPTY_DB_INITIALIZATION: PARTIAL (schema yes; document_match_v1 table NO)
BASELINE_POLLUTION: YES (3,554 ML-June ledger rows + 2 cierre rows in baseline copy)
TREASURY_CONTRACT: PROVEN (real loader + classifier path, value derived)
DOCUMENT_CONTRACT: NO SAFE INGESTION PATH EXISTS
LEVEL_STATUS_VOCABULARY: PASS/ALERTA per level (engine lines 336, 404, 466, 574)
AGGREGATE_STATUS_VOCABULARY: CERTIFICADO/PARCIAL/PENDIENTE/ERROR/FINANCIAL_INTEGRITY_BROKEN (engine lines 94-116)
STATUS: BLOCKED
FIRST_BLOCKER: NO_SAFE_DOCUMENT_MATCH_INGESTION_PATH
  MISSING_CONTRACT: synthetic document-match creation contract
  MISSING_COMPONENT: document_match_v1 writer for synthetic/test data
  MISSING_FIXTURE: no test or fixture populates document_match_v1
ENGINE_FILES_MODIFIED: 0
FA-005: FAIL (unchanged; prior evidence stands)
FA-006_STATUS: BLOCKED (unchanged)
```

E2E_V2 directory NOT created. E2E_V1 preserved untouched.
No expectation was degraded to ALERTA/BROKEN for PASS.

---

## Next Exact Action

Dedicated document-ingestion design task (out of FA-005 scope), options:
(a) certify a synthetic document-match writer component with tests, then
build E2E_V2 treasury+documents on fresh TEMP_DB; or (b) formally scope
FA-005 to engine-behavior verification (levels execute deterministically)
rather than CERTIFICADO parity for a DTE-less dataset. No engine changes needed;
engine behaved correctly in all prior executions.
