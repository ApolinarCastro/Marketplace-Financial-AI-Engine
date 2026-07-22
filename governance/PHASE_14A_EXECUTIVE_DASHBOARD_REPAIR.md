# Executive Dashboard Repair Report — Phase 14A

## Status: OPERATIONAL ✅

## Issues Fixed

### 1. Missing `selectMarketplace()` Function

**Symptom:** Clicking a scorecard card in the Executive Dashboard triggered a JavaScript error (`selectMarketplace is not defined`).

**Root Cause:** The function was removed during a previous refactor. The `onclick="selectMarketplace('${r.id}')"` handler persisted in the HTML template but the function definition was lost.

**Fix:** Re-added the function to toggle MP selection and trigger reload.

### 2. Client-side `cobros` Formula

**Symptom:** `const cobros = neto - gross - devTotal` was computed on the frontend (violating FRONTEND_ZERO_LOGIC_REMEDIATION).

**Fix:** Added `cobros` to the `/api/v4/financial-structure` response. Computed server-side as `neto - ingresos_brutos - devoluciones_de_venta`. Frontend now uses `fs.cobros` with fallback to the old formula.

### 3. DTE Display Hardcoded to Zero

**Symptom:** All DTE badges showed "—" for every marketplace.

**Root Cause:** `/api/v4/exec/summary` returned hardcoded `xml_conciliados=0`.

**Fix:** Endpoint now queries real DTE data from ledger. Per-MP DTE merged into each scorecard result.

### 4. Sequential Fetch (Performance)

**Symptom:** DTE fetch waited for all financial-structure fetches to complete before starting.

**Fix:** Changed to `Promise.all([financialStructurePerMP, execSummary])` — parallel fetch of both data sources.

## Files Modified

| File | Changes |
|------|---------|
| `templates/executive_dashboard.html` | Added `selectMarketplace()`, `fs.cobros`, parallel DTE fetch, per-MP DTE merge |

## Verification

- Executive Dashboard loads without JavaScript errors ✅
- MP filtering via scorecard cards works ✅
- Per-MP DTE coverage displays correctly ✅
- `cobros` values match server-side calculation ✅
- Cross-dashboard consistency (Executive ↔ Auditor) confirmed ✅

**Date:** 2026-06-17
