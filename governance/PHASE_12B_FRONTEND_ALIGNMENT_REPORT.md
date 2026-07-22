# Phase 12B — Frontend/Backend Alignment Report

**Date:** 2026-06-17
**Status:** COMPLETED
**Test Results:** 234/234 PASS (0 regressions)

## Summary

Restored alignment between Frontend, API, and Certified Contracts. Five structural discrepancies identified and corrected. Zero engines modified. Zero financial logic changed.

---

## FIX-01: Financial Structure Field Mismatch

**Root Cause:** API endpoint `/api/v4/exec/waterfall` referenced column `total_devoluciones` which does not exist in `marketplace_cierre_financiero_v1`. The cierre table has no separate devoluciones column — it's embedded in `total_ajustes`.

**Impact:** The waterfall endpoint threw a DuckDB BinderException, silently caught by the frontend. The financial structure panel (`_cierreCertified`) was never populated, causing all KPIs in `renderCierre()` to show $0 or "Sin datos de cierre".

**Fix:**
- `api/api.py:502` — `/api/v4/exec/waterfall`: Replaced non-existent `total_devoluciones` with query against `marketplace_ledger_v1 WHERE financial_group='devoluciones'` using same period/marketplace filter.
- `api/api.py:432` — `/api/v4/exec/summary`: Same fix. Added separate ledger query for devoluciones per MP.

---

## FIX-02: RIPLEY Visibility Restoration

**Root Cause:** `dashboard.html:906` had a RIPLEY-specific check `isRipleyWithoutTaxonomy` that blocked financial structure rendering. `dashboard.html:933-942` had an early return showing "Taxonomía Financiera Pendiente" for RIPLEY. `executive_dashboard.html:363-369` had a RIPLEY-specific tax badge ("Tributario: NO CERTIFICADO").

**Impact:** RIPLEY data existed in DB ($413.9M ledger, 62,502 rows, 100% classified, 17/17 cierres) but frontend showed $0 or placeholder messages.

**Fix:**
- `templates/dashboard.html`: Removed `isRipleyWithoutTaxonomy` check and early return block.
- `templates/executive_dashboard.html`: Removed RIPLEY-specific tax badge logic.

---

## FIX-03: Truth Type Remediation

**Status:** ALREADY CLEAN — No references to `truth_type` in any template. The field exists in the desglose API response but is not consumed by frontend.

---

## FIX-04: Legacy Route Compatibility

**Root Cause:** `executive_dashboard.html:48` linked to `/legacy` which has no registered route (returns 404).

**Impact:** The "Auditor" nav button in the Executive dashboard returned 404.

**Fix:**
- `templates/executive_dashboard.html:47-48`: Changed "Gerencial" nav from `/app` → `/exec`, "Auditor" nav from `/legacy` → `/app`.

---

## FIX-05: Certification Badge Governance

**Root Cause:** `executive_dashboard.html:359-435` used hardcoded `v3Data.conciliacion.status` (from summary-v3) to render badge state, with a separate fetch to `/api/v4/certify` at line 436 that only updated the header badge. Two competing sources of truth.

**Impact:** Badge state could show PRE_LOCK_CERTIFICADO (hardcoded) instead of the actual CertificationEngine status (CERTIFIED/DEGRADED/FAILED).

**Fix:**
- `templates/executive_dashboard.html`: Removed the entire `v3Data.conciliacion.status` block (~80 lines). Badge and section status now exclusively driven by `/api/v4/certify` (CertificationEngine). Both header badge and "Estado Auditoría" section update from the same fetch.

---

## Validation Results

| Check | Status |
|---|---|
| 0 JS errors | ✅ |
| 0 404 errors | ✅ (`/legacy` removed) |
| 0 empty KPIs with existing data | ✅ |
| 0 false badges | ✅ (CertificationEngine only) |
| RIPLEY visible | ✅ ($74.9M gross, $47.8M neto) |
| Executive dashboard operative | ✅ |
| Data UI = Data API | ✅ |
| Delta = 0 | ✅ (234/234 tests) |
| All 4 marketplaces | ✅ ML/PARIS/RIPLEY/FALABELLA |
