# UPLOAD CENTER CONTROLLED UX — EVIDENCE

## Task Info

```
TASK_ID: PFO-UPLOAD-CENTER-CONTROLLED-UX-001
DATE: 2026-10-07
HEAD_BEFORE: ee3bcb3c5728f011e45b5346dc7a92ab88eb656f
BRANCH: main
```

## UI_BEFORE (demonstrated defects, templates/upload_center.html)

```
Single done state conflating validation with persistence ("Subir Todo", "Completado").
Plain FormData POST (dry_run default now, but UI language claimed processing).
No confirmation step. No classification gating. No duplicate state.
Unescaped interpolations (filename, errors, marketplace, period) via innerHTML.
ZIP advertised in UI while backend rejects it.
```

## UI_AFTER (this task, template only)

```
Canonical states: pending → validating → validated|failed → processing → completed|duplicate|failed.
Button 1 "Validar archivos" (pending only) → POST ?dry_run=true, never confirm_write.
validated label "Validado · No se han escrito datos"; never "Completado/Procesado" for dry-run.
Classification rendered strictly from backend response (marketplace/document_type/period); zero hardcoded values.
Button 2 "Procesar archivos validados" disabled unless ≥1 validated; processes validated-only filter.
Confirmation modal lists archivo/marketplace/documento/período + explicit warning text;
  Cancelar sends 0 requests (files stay validated); Confirmar posts dry_run=false&confirm_write=true.
Processing label "Procesando..."; COMPLETED→"Procesado"; FAILED→"Fallido";
  SKIPPED_DUPLICATE→"Ya procesado anteriormente".
Remove deletes full local state (re-add resets to pending/null).
Badge: N pendientes/validados/procesados/fallidos (+ ya procesados).
Results split: Validación section (records N/A) vs Procesamiento section (backend values only).
Multifile: validate pending-all, process validated-only, continue-on-error, no auto-retry.
XSS: central esc() on every external interpolation; event delegation (no inline
  onclick identifiers); verified by structural test.
Extensions aligned: .xlsx/.csv/.xml only (ZIP removed everywhere).
```

## Backend Contract (verified, unmodified)

```
POST /api/v4/ingestion/upload(file, dry_run=True, confirm_write=False) — query params.
No backend change required by this task.
```

## Validation Flow (§25 + §24-no-write)

```
A default validation → request dry_run=true, response DRY_RUN, frontend validated: PASS
B post-validation DB writes → 0 (ledger count unchanged + registry 404): PASS
C process button disabled pre-validation → disabled unless validated>0: PASS
D classification shown == backend response fields, no hardcode: PASS
```

## Write Flow (§26)

```
E confirmation modal visible with file summary after validated + click: PASS (structural)
F cancel → 0 write requests, files stay validated: PASS (structural: closeConfirmModal sends nothing)
G confirmed write sends dry_run=false&confirm_write=true: PASS
H COMPLETED → Procesado: PASS (structural mapping)
I FAILED → Fallido: PASS
J SKIPPED_DUPLICATE → Ya procesado anteriormente: PASS
```

## Multifile / XSS (§27/28)

```
27: validated-only filter enforced in confirmProcess path: PASS
28: external-token interpolation audit — every external value esc()-wrapped: PASS
```

## Regression (§29/30)

```
Backend upload e2e (rewritten contract): 13/13
UI structural: 17/17
Ingestion handlers: 46/46 · docmatch writer: 10/10 · DTE truth: 5/5
XML fixture: 4/4 · E2E_V1: 11/11 · E2E_V2: 8/8
(pre-existing flakes, unrelated: e2e basename collision → separate runs;
conftest TEMP_V8_BASE race → retry passes)
Total: 114 passed.
```

## Non-Contamination

```
PRODUCTION_DB_MODIFIED: FALSE / REAL_RAW_MODIFIED: FALSE
FINANCIAL_CORE_MODIFIED: FALSE / GOLDEN_FILES_MODIFIED: FALSE
Engine touch: none (validator handle-close predates this task).
```

## Readiness (§34)

```
UPLOAD_CENTER_CONTROLLED_UX: PASS
READINESS_DECISION: READY_FOR_CONTROLLED_ROLLOUT (unchanged trajectory)
Open risks retained: CONCURRENT_WRITE_SAFETY NOT_PROVEN, CRASH_SAFETY PARTIAL,
ELECTRONIC_SIGNATURE NOT_IMPLEMENTED, BACKUP now PASS. Never FULL_PRODUCTION_READY.
```

## Next Exact Action

PFO-CONCURRENT-WRITE-SAFETY-001 (per mandated output). No auto-run.
