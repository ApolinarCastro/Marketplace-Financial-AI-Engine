# README — Antes / Después

## Antes (resumen de claims falsos/stale)

- Frontend React/Vite en `src/frontend` (no existe)
- DB oficial `data/db/antigravity_v4.db` (no existe; la oficial es `meli_financial_v4.db`)
- `/legacy` HTML route (no existe)
- `02_Curated`, `04_Conciliaciones`, `analysis/`, `legacy/` (no existen)
- `npm run server/frontend/build:frontend/check:python/pipeline/smoke/test:engine/test:etl/test:integration` (no existen en package.json; solo test:all, lint, typecheck)
- `/legacy` + `ENABLE_LEGACY_V3=1` (no implementado)
- `npm run pipeline` (no existe)

## Después

- Documenta arquitectura REAL: `run_app.py` + `Scripts/run_python.bat` + `templates/` server-side + `frontend/shared/` assets + `engine/v4` cadena Ledger→Classification→Truth→Reconciliation→Exception.
- DB oficial: `data/db/meli_financial_v4.db`.
- Rutas UI reales: /app /exec /documentary /traceability /copilot /upload.
- npm scripts reales: test:all, lint, typecheck.
- Regla de certificación electrónica: LEDGER_EXISTING != CRYPTOGRAPHIC_CERTIFIED.
- Regla de orden: scripts patch/fix/inject se archivan tras consolidación.

## Clasificación por claim (detalle)

Ver `readme_reconciliation.json` — 13 TRUE, 16 FALSE, 4 UNVERIFIED.
Labores de documentación: se corrigió para DESCRIBIR la arquitectura existente; no se reestructuró el sistema.