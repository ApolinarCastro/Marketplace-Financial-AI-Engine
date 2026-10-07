# UPLOAD + CONFIG GUARD HARDENING — EVIDENCE

## Task Info

```
TASK_ID: PFO-UPLOAD-CONFIG-GUARD-001
DATE: 2026-10-07
HEAD_BEFORE: 9f3a420a7f6ad53441608d46acc1a8f2f061fc17
BRANCH: main
```

## Before (demonstrated defects, api/api.py)

```
1. Writer opened on DatabaseV4.get() singleton default (production path).
2. Hardcoded marketplace="ML", document_type="facturacion", period="2026-01".
3. registry.update_status(..., "COMPLETED") BEFORE real processing.
4. Direct SurgicalLoader.load_file() call, bypassing orchestrator stages.
5. Fixed stages_completed list (all 6, unexecuted).
6. Registry GET fallback: fake test.csv/COMPLETED for unknown ids.
7. Registry LIST fallback: fake execution_id "test" on error.
8. No TEST/CONTROLLED/PRODUCTION distinction anywhere.
```

## After

```
RUNTIME_MODE_GUARD: engine/v4/config_guard.py (new, minimal).
  MF_RUNTIME_MODE ∈ {TEST, CONTROLLED, PRODUCTION}, default TEST (fail-closed).
  authorize_db_write(target, confirmed): unconfirmed → WRITE_NOT_CONFIRMED;
  TEST + production path → PRODUCTION_WRITE_BLOCKED_IN_TEST; else AUTHORIZED.
  Production erkannt by resolved-path equality with DatabaseV4.DB_PATH.
DEFAULT_RUNTIME_MODE: TEST / DEFAULT_UPLOAD_BEHAVIOR: non-writing dry run.
DRY_RUN_DEFAULT: true → DETECT+VALIDATE+CLASSIFY via the same component
  classes the orchestrator uses (FileDetector, IntegrityValidator,
  MarketplaceClassifier); PERSIST/CERTIFY/KNOWLEDGE never run; staged file
  removed; status DRY_RUN (validation issues → FAILED, never COMPLETED).
WRITE_CONFIRMATION_REQUIRED: dry_run=false demands confirm_write=true,
  else HTTP 409 WRITE_NOT_CONFIRMED with zero DB writes.
PRODUCTION_DB_PATH_GUARD: TEST mode blocks confirmed writes whose target
  resolves to the production DB (HTTP 403 PRODUCTION_WRITE_BLOCKED_IN_TEST).
REAL_ORCHESTRATOR_USED: confirmed writes run IngestionOrchestrator
  (async endpoint, full stages); direct loader call removed.
  Response fields come from the real record (marketplace/document_type/period
  from classifier; stages from record.details).
HARDCODED_MARKETPLACE_REMOVED: yes / HARDCODED_PERIOD_REMOVED: yes.
PREMATURE_COMPLETED_REMOVED: yes (no update_status before pipeline).
FAKE_REGISTRY_GET_REMOVED: yes → 404 EXECUTION_NOT_FOUND (+ ensure_schema
  so fresh DBs answer honestly instead of 500ing).
FAKE_REGISTRY_LIST_REMOVED: yes → 500 Registry unavailable (generic).
UPLOAD CLEANUP: staged file removed after DRY_RUN/FAILED/COMPLETED/rejection
  (verified UPLOAD_TEMP_ARTIFACTS_LEFT = 0 in tests).
```

Resource fix required by mandated cleanup (§14): IntegrityValidator._check_xlsx
held `pd.ExcelFile` open (Windows lock blocked staged-file deletion; proven by
isolation probe). Added try/finally close — resource hygiene only, zero
financial/classifier/reconciliation logic touched.

## Tests (tests/test_upload_center_e2e.py rewritten, 13/13 PASS)

```
A default → DRY_RUN, 0 ledger writes, registry 404 for dry-run id: PASS
B dry_run=false w/o confirm → 409 WRITE_NOT_CONFIRMED, 0 writes: PASS
C CONTROLLED + temp DB + confirm → real orchestrator, classifier-sourced
  fields, core-4 stages, COMPLETED (real record status), 8 ledger rows: PASS
D TEST + forced-production target + confirm → 403, 0 writes: PASS
E classification == live classifier output (no hardcode): PASS
F invalid input → FAILED, never COMPLETED, PERSIST absent: PASS
G unknown execution → 404 EXECUTION_NOT_FOUND: PASS
H forced registry error → 500 generic, no fake: PASS
+ page served, invalid extension 400, no-file 400, cleanup empty,
  real registry record round-trip: PASS
```

Old assertions encoding the bugs (hardcoded ML/COMPLETED/stages, direct
loader call, file persistence, fake registry) replaced with corrected-contract
assertions; each change traceable to task §5–§14.

## Regression

```
Upload (rewritten): 13/13 · ingestion handlers: 46/46 · docmatch writer: 10/10
DTE truth: 5/5 · xml fixture: 4/4 · E2E_V1: 11/11 · E2E_V2: 8/8
(pre-existing flakes noted: e2e basename collision → run separately;
conftest TEMP_V8_BASE race → retry passes; unrelated to this change)
```

## Matrix (re-audit §25: CONFIG_ISOLATION only)

```
DEFAULT_UPLOAD_IS_NON_WRITING: TRUE
WRITE_REQUIRES_EXPLICIT_CONFIRMATION: TRUE
PRODUCTION_DB_PATH_GUARDED: TRUE (TEST mode; resolved-path equality)
REAL_ORCHESTRATOR_USED: TRUE
NO_HARDCODED_CLASSIFICATION: TRUE
NO_PREMATURE_COMPLETED: TRUE
NO_FAKE_REGISTRY_RESPONSES: TRUE
PRODUCTION_DB_MODIFIED: FALSE / REAL_RAW_MODIFIED: FALSE
PRODUCTION_CONFIG_ISOLATION: PASS
```

Unchanged open risks (recorded, not re-audited): BACKUP/RESTORE MISSING,
CONCURRENT_WRITE_SAFETY NOT_PROVEN, crash atomicity PARTIAL,
ELECTRONIC_SIGNATURE NOT_IMPLEMENTED.

## Readiness Re-evaluation (§26)

```
CONFIG_ISOLATION was the sole §23 minimum missing.
CONFIG_ISOLATION: PARTIAL → PASS.
READINESS_DECISION: READY_FOR_CONTROLLED_ROLLOUT (controlled/supervised use;
  never FULL_PRODUCTION_READY while open risks above persist).
```

## Files

```
MODIFIED: api/api.py (3 endpoints), engine/v4/ingestion/handlers/integrity_validator.py
  (handle close only), tests/test_upload_center_e2e.py (corrected contract)
NEW: engine/v4/config_guard.py,
  governance/PRODUCTION_ROLLOUT/01_UPLOAD_CONFIG_GUARD_EVIDENCE.md,
  governance/PRODUCTION_ROLLOUT/01_UPLOAD_CONFIG_GUARD_MATRIX.json
FINANCIAL_CORE_MODIFIED: NO / GOLDEN_FILES_MODIFIED: NO
Frontend note (out of scope): upload_center.html posts plain FormData → now
receives DRY_RUN by default; UI must opt into dry_run=false + confirm_write
explicitly (follow-up, not in allowed files).
```

## Next Exact Action

Controlled rollout may proceed under supervision with the documented open
risks. Suggested order: backup procedure first, then concurrency policy.
