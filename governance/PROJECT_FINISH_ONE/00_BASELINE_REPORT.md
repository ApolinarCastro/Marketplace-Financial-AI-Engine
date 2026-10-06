# PROJECT FINISH ONE — PHASE 1 BASELINE REPORT

## Task Info

```
TASK_ID: PFO-PHASE1-BASELINE-001
DATE: 2026-10-06
REPOSITORY: https://github.com/ApolinarCastro/Marketplace-Financial-AI-Engine
BRANCH: main
CURRENT_HEAD: aecee2193dc0a4afc2df61aa2c91c1312dd84a99
CODE_BASELINE_SHA: e2ff733e25ede8d8074cbce51aa5bf5f9cbcd3b7
WORKING_TREE: Clean (untracked files are local runtime artifacts covered by .gitignore)
```

## Protocol Status

```
07_PROJECT_EXECUTION_OS_TASKVIEW_ECC: NOT_AVAILABLE
06_ANTI_HALLUCINATION_AND_RESOURCE_GATE: NOT_AVAILABLE
08_DEVIN_EXECUTION_ARCHITECTURE_STANDARD: NOT_AVAILABLE
PROJECT FINISH ONE: ACTIVE
```

## Architecture Found

| Component | Value |
|-----------|-------|
| BACKEND_ENTRYPOINT | `run_app.py` → `api.api:app` (uvicorn, port 3001) |
| FRONTEND_ENTRYPOINT | `templates/dashboard.html` (server-side) |
| START_COMMAND | `START_APP.bat` (Windows) |
| DATABASE_ENGINE | DuckDB |
| DATABASE_PATH | `data/db/meli_financial_v4.db` |
| INGESTION_ENTRYPOINT | `engine/v4/ingestion/` |
| LEDGER_GENERATION_PATH | `engine/v4/` (FinancialEngine) |
| RECONCILIATION_PATH | `engine/v4/reconciliation/` |
| FINANCIAL_CLASSIFICATION_PATH | `engine/v4/classification/` |
| RESULT_CALCULATION_PATH | `engine/v4/` (FinancialEngine) |
| TEST_ENTRYPOINT | `pytest tests/` |

## Database

```
DATABASE_PATH: data/db/meli_financial_v4.db
FILE_EXISTS: TRUE
FILE_SIZE: 58,732,544 bytes (~56 MB)
ENGINE: DuckDB
READ_ONLY_OPEN: PASS
CORE_TABLES_FOUND: 4/4
  - marketplace_ledger_v1: 601,559 rows
  - marketplace_ledger_clasificado_v1: 601,559 rows
  - marketplace_cierre_financiero_v1: 203 rows
  - dte_truth_v1: 667 rows
```

## Golden Dataset Status

```
GOLDEN_DATASET_STATUS: READY
DATASET_ID: E2E_V1
MARKETPLACE: ML
STRUCTURE: tests/golden/e2e_v1/ with input/ and expected/
INPUT_FILES: 1 (ML_Facturacion_E2E_V1.xlsx)
EXPECTED_FILES: 3 (expected_ledger.csv, expected_reconciliation.csv, expected_summary.json)
INTEGRITY_TESTS: 11/11 PASS
SECURITY_GATE: PASS (no production paths, no sensitive data)
RECONCILIATION_EXPECTATION: 5 levels PENDIENTE (document_coverage=0.0, no DTE/XML)
KNOWN_NEXT_BLOCKER: FA-005 cannot reach CERTIFICADO without DTE/XML evidence
```

## FA Status

| FA | Status | Notes |
|----|--------|-------|
| FA-001 | PASS | Application boots: START_APP.bat → uvicorn on 3001 → HTTP 200 on /app and /api/v4/health |
| FA-002 | PASS | DB opens read-only, core tables verified |
| FA-003 | PASS | Isolated ingestion COMPLETED: 8 read, 8 new, 0 errors, TEMP_DB only, no contamination |
| FA-004 | FAIL (R1) | IDs repaired and matching (0 missing/0 unexpected); new classes: financial_group NULL in raw ledger (golden over-spec) + detalle mojibake (encoding path); 0 financial deltas |
| FA-005 | BLOCKED | Depends on FA-004 |
| FA-006 | BLOCKED | Depends on FA-005 |
| FA-007 | BLOCKED | Depends on FA-006 |

## First Blocker

```
FIRST_BLOCKER_ID: FA-004 (R1)
FIRST_BLOCKER_PHASE: FA-004 LEDGER parity re-execution
FIRST_BLOCKER_ERROR: financial_group NULL in raw ledger_v1 (7 rows, golden over-specification) + detalle mojibake (1 row, encoding path issue); IDs now match; 0 financial deltas
FIRST_BLOCKER_EVIDENCE: governance/PROJECT_FINISH_ONE/02_FA004_LEDGER_EVIDENCE_R1.md + 02_FA004_COMPARISON_R1.json (R0 evidence preserved)
PREVIOUS_BLOCKER: FA-004 R0 id_transaccion separator (RESOLVED — golden repaired, IDs match in R1)
KNOWN_NEXT_BLOCKER: FA-005 — Golden Dataset lacks required DTE/XML document evidence for CERTIFICADO
  (Not active until FA-004 passes)
```

## Commands Executed

```bash
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git log --oneline --decorate -10
python tmp_db_check.py
cmd /c START_APP.bat
python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:3001/app', timeout=10)"
python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:3001/api/v4/health', timeout=10)"
python tests/golden/e2e_v1/create_input.py
python -m pytest tests/golden/e2e_v1/test_golden_dataset_integrity.py -v
python tmp_fa003_run.py (isolated FA-003 execution, TEMP_DB only)
```

## Evidence

- DB verified read-only: 39 tables, 4 core tables with 601,559 ledger rows
- Golden Dataset E2E_V1: tests/golden/e2e_v1/ with input/expected structure
  - Input: ML_Facturacion_E2E_V1.xlsx (5 rows, synthetic ML Facturacion)
  - Expected: 8 ledger rows (net 20800.0), 5 reconciliation levels PENDIENTE (doc_coverage=0.0)
  - Integrity tests: 11/11 PASS (incl. README↔CSV consistency check)
  - Security gate: PASS (no production paths, no sensitive data)
  - Reconciliation corrected per _determine_status(): doc 0 < 10 => PENDIENTE
- Architecture: FastAPI backend, DuckDB storage, server-side templates
- FA-001: START_APP.bat executed → uvicorn on port 3001 → HTTP 200 on /app (88,952 bytes) and /api/v4/health (status READY)
- FA-003: isolated ingestion via f3_03 pattern → COMPLETED, exec cb8ee20a, 8 read / 8 new / 0 errors, ledger 8 rows total 20800.0, production DB + real RAW untouched, TEMP_DIR removed
- FA-004: R0 isolated re-ingestion COMPLETED → FAIL on id_transaccion separator only (__ vs _); R1 golden repaired → re-ingestion COMPLETED → FAIL on new classes (financial_group NULL in raw ledger + detalle mojibake); all financial values + movement subtotals exact in both runs; engine ID derivation verified correct; NO engine logic modified
- RCA: BOTH root causes demonstrated — (A) GOLDEN_OVER_SPECIFICATION for financial_group (LEDGER_COLS excludes it, MarketplaceAuditor owns it, f3_03 precedent = 5 fields); (B) SOURCE_LITERAL_CORRUPTION for mojibake (file bytes C3 83 C2 B3, XLSX/calamine/DuckDB all correct, AST confirms); engine + golden repairs scoped as separate tasks

## Final Status

```
PHASE_1_RESULT: PASS
E2E_STATUS: BLOCKED
```

## Next Exact Action

Investigate FA-004 R1 difference classes in a dedicated task:
1. financial_group scope (exclude from raw-ledger parity per f3_03 precedent, or extend FA-004 to classification stage).
2. detalle mojibake in pipeline write/DuckDB path.
Then re-execute FA-004 as R2.
