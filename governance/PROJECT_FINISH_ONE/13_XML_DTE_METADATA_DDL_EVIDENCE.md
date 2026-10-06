# PFO XML/DTE METADATA + CERTIFIED DDL — EVIDENCE

## Task Info

```
TASK_ID: PFO-XML-DTE-METADATA-DDL-001
DATE: 2026-10-06
HEAD_BEFORE: 05ccd8748afb6a084a649fd12d3913601ab79b82
BRANCH: main
```

Resolves: DTE_TRUTH_INGESTION_METADATA_GAP + FRESH_DB_MISSING_DTE_CERTIFIED_MATCH_TABLE.
No matching formulas, tolerances, signatures, or golden values touched.

---

## Root Causes (from PFO-XML-DTE-E2E-001 execution)

```
ROOT_CAUSE_METADATA: DTEMatcher.load_dtes() INSERT listed 7 columns only;
  marketplace + tipo_dte stayed NULL while DTELedgerMatcher requires
  dte_truth_v1 WHERE marketplace='ML'. XML parse itself was correct.
ROOT_CAUSE_DDL: dte_certified_match_v1 absent from DatabaseV4 fresh schema
  (MISSING_TABLE on fresh DB); only _ensure_schema() created it on demand.
```

## DTE_MATCHER_BEFORE → AFTER

File: `engine/v4/dte_matcher.py` (only file with logic change).

Before: `__init__(self)` → singleton DB, hardcoded ROOT glob, no TipoDTE
read, 7-column INSERT, global `DELETE FROM dte_truth_v1`.

After:
- `__init__(self, db=None, marketplace="ML", root=None)` — injectable DB,
  explicit marketplace (default ML preserves historic single-market behavior),
  overridable scan root (tests redirect without touching 01_Raw/).
- TipoDTE extracted from `IdDoc/TipoDTE` (null-safe when absent).
- Row carries `tipo_dte` + `marketplace`.
- INSERT persists all 9 columns.
- DELETE scoped: `WHERE marketplace = ?` (baseline holds RIPLEY 407 +
  PARIS 62 + FALABELLA 6 rows — global wipe would destroy them; no evidence
  the global DELETE was deliberate, so scoped refresh is the safe contract).

```
DTEMATCHER_MARKETPLACE_PARAMETER: YES (default "ML")
DTEMATCHER_ROOT_INJECTION: YES (Path(root) or project ROOT)
TIPO_DTE_EXTRACTED: YES (IdDoc/TipoDTE, null-safe)
MARKETPLACE_PERSISTED: YES
DELETE_SCOPE: marketplace-scoped (global DELETE removed with justification)
CROSS_MARKETPLACE_PRESERVATION: PROVEN (PARIS row survives ML load)
```

## Fresh DDL (database.py, additive only)

```sql
CREATE TABLE IF NOT EXISTS dte_certified_match_v1 (marketplace VARCHAR,
id_transaccion VARCHAR, folio_xml VARCHAR, dte_folio VARCHAR, dte_monto DOUBLE,
dte_fecha DATE, emisor_nombre VARCHAR, emisor_rut VARCHAR, tipo_dte VARCHAR,
match_rule VARCHAR, match_status VARCHAR, match_source VARCHAR,
execution_id VARCHAR, PRIMARY KEY (marketplace, id_transaccion))
```

Byte-identical column contract to `DTELedgerMatcher._ensure_schema()`.
`_ensure_schema()` re-run over the DDL table: idempotent, 0 rows, no error
→ MATCHER_SCHEMA_COMPATIBILITY = PASS.

## Test Results (tests/test_dte_truth_ingestion.py, tmp_path-isolated)

```
FRESH_DB_TEST: PASS (dte_truth_v1 + dte_certified_match_v1 + document_match_v1
  exist, all 0 rows; certified columns exact 13/13)
INSERT_TEST (tipo_dte + marketplace): PASS
  folio=90000001, tipo_dte=33, marketplace=ML, neto=4789, iva=911,
  total=5700, rut=76000000-0
DUPLICATE/ISOLATION (PARIS preserved): PASS
ML_DTE_VISIBLE_TO_MATCHER: PASS (WHERE marketplace='ML' returns the row)
SCHEMA_COMPATIBILITY: PASS
TEST_RESULTS: 5/5 PASS
```

## Regression

```
New DTE tests: 5/5 · fresh-DB exec-id: 3/3 · docmatch writer: 10/10
E2E_V1 golden: 11/11 · E2E_V2 golden: 8/8 · xml fixture: 4/4
dte_traceability: 17 passed + 1 skipped · xml_dte_certification: 2/2
Note: e2e_v1/e2e_v2 integrity files share a basename (no __init__.py);
  run in separate pytest invocations (pre-existing collection quirk).
```

## Non-Contamination

```
PRODUCTION_DB_MODIFIED: FALSE (tmp_path DBs only; singleton rebound + reset)
REAL_RAW_MODIFIED: FALSE (fixture copied to tmp_path only)
```

## Boundaries (unchanged)

```
XML_DTE_E2E_STATUS: FAIL (unchanged until steps 6-12 re-execution)
ELECTRONIC_SIGNATURE_CERTIFICATION: NOT_IMPLEMENTED (degraded-PASS bypass
  + unwired validator remain an independent follow-up)
FA-005: PASS (unchanged) / FA-006: READY (unchanged)
```

## Next Exact Action

Re-execute PFO-XML-DTE-E2E-001 steps 6-12 (ingestion metadata now present;
certified table exists fresh). Then signature-hardening track.
