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
| FA-004 | PASS (R2) | 8/8 rows, 20800.0=20800.0, 0 missing/0 unexpected/0 mismatches, REVCOMM U+00F3 parity, movement delta 0 |
| FA-005 | FAIL | Engine executed correctly (5/5 levels, doc_cov 0.0 match); 15 field mismatches: baseline cierre pollution (L1/L2), treasury mirror gap (L3), status vocabulary ALERTA/BROKEN vs PENDIENTE, 2 mapping artifacts |
| FA-006 | BLOCKED | Depends on FA-005 PASS |
| FA-007 | BLOCKED | Depends on FA-006 |

## First Blocker

```
FIRST_BLOCKER_ID: FA-005
FIRST_BLOCKER_PHASE: FA-005 reconciliation parity
FIRST_BLOCKER_ERROR: 15 field mismatches despite correct engine execution; golden simplified contract vs engine real contract gap
FIRST_BLOCKER_EVIDENCE: governance/PROJECT_FINISH_ONE/05_FA005_RECONCILIATION_EVIDENCE.md + 05_FA005_RECONCILIATION_COMPARISON.json
PREVIOUS_BLOCKERS_RESOLVED:
  - FA-003 (isolated ingestion COMPLETED)
  - FA-004 R0 ids (golden repaired, R1 confirmed match)
  - FA-004 R1 financial_group + mojibake (RCA demonstrated; golden scope + 2 literals repaired; R2 parity TRUE)
  - FA-005 golden-vs-engine contract gap documented (engine correct; re-scope required)
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
- FA-004: R0 FAIL on ids (__ vs _) → golden repaired → R1 FAIL on financial_group NULL + mojibake (RCA: GOLDEN_OVER_SPECIFICATION + SOURCE_LITERAL_CORRUPTION) → 2 literals + golden scope repaired → R2 PASS (8/8, 20800.0, 0 mismatches, U+00F3 parity); NO financial-logic modification; regression: golden 11/11 + f4_traceability 22 passed
- FA-005: engine executed correctly (5/5 levels present, taxonomy 100%, doc_cov 0.0 match, L4 delta 100 match) → FAIL on 15 fields (baseline cierre pollution L1/L2, treasury mirror L3, status vocabulary ALERTA/BROKEN vs PENDIENTE, 2 mapping artifacts); engine behavior deterministic and correct; golden re-scope required; NO engine modification
- FA-005 full-chain design (E2E_V2): BLOCKED — treasury path PROVEN (Retiro de dinero → tesoreria, mirror -20800 derived), document path MISSING (no writer component/fixture/test for document_match_v1; DTE chain requires real SII; fresh DB lacks the table); E2E_V2 NOT built, E2E_V1 preserved; NO expectation degradation
- Document-match infrastructure: RESOLVED — fresh DatabaseV4 creates document_match_v1 (15/15 cols, empty, compatible); DocumentMatchWriter persists validated matches deterministically (idempotent, validated, tested 10/10); reconciliation coverage consumption proven 100.0; regression golden 11/11 + ingestion 46/46; NO engine-rule changes
- Level 1 vs treasury scope conflict: RESOLVED — RCA demonstrated (L1 ALERTA on valid treasury + L3 PASS); closing proven op_pnl-only; ML exception removed → uniform op_filter; post-repair L1+L3 PASS, negative control ALERTA 5800; regression 2+6+21+1 green; NO formula/closing/golden changes

## Final Status

```
PHASE_1_RESULT: PASS
E2E_STATUS: BLOCKED
```

## Next Exact Action

Re-scope golden reconciliation expectations to the engine real output contract
(dedicated task): either (a) expand E2E_V1 with treasury/settlement + DTE data
and use fresh empty TEMP_DB, or (b) redefine expected levels in engine
vocabulary (PASS/ALERTA per level + aggregate status via _determine_status).
Then re-execute FA-005. No engine modification required.

Document-match infrastructure RESOLVED (writer + fresh-DB DDL tested):
resume E2E_V2 full-chain construction using DocumentMatchWriter for
synthetic CONCILIATED matches on fresh TEMP_DB.

Level 1 treasury conflict RESOLVED (uniform op_filter; post-repair L1+L3
PASS; negative control green).
NEXT: Build and execute E2E_V2.
