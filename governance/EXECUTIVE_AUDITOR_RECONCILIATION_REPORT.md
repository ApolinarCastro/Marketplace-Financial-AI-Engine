# Executive vs Auditor Reconciliation Report

## Status: PASS ✅ (Delta = 0)

## Change Summary

### Before Phase 13 (Violating Single Financial Truth)

| Dashboard | Source | RIPLEY Ingresos | RIPLEY Neto |
|-----------|--------|----------------|-------------|
| Executive (Gerencial) | `cierre_financiero_v1` via `/api/v4/exec/summary` | $1,908,041,379 | $1,673,174,873 |
| Auditor | `marketplace_ledger_v1` via `/api/v4/financial-structure` | $467,621,338 | $434,468,371 |

**Delta:** Different sources, different taxonomies, different numbers. **VIOLATION.**

### After Phase 13 (Single Financial Truth)

| Dashboard | Source | RIPLEY Ingresos | RIPLEY Neto |
|-----------|--------|----------------|-------------|
| Executive (Gerencial) | `marketplace_ledger_v1` + taxonomy | $218,441,218 | $203,217,455 |
| Auditor | `marketplace_ledger_v1` + taxonomy | $218,441,218 | $203,217,455 |

**Delta = $0.** Same endpoint, same taxonomy, same data source. ✅

## What Changed

### 1. Taxonomy Config (`knowledge/taxonomy/ripley_v1.json`)
Created official signal/noise classification for all 32 RIPLEY detalle values.

### 2. API Endpoint (`/api/v4/financial-structure`)
Added `signal_mode` parameter:
- `signal_mode=SIGNAL` — filters to canonical detalle only (new default for both dashboards)
- `signal_mode=ALL` — shows all data (debugging use only)
- `signal_mode=NOISE` — shows only noise data

### 3. Executive Dashboard (`templates/executive_dashboard.html`)
Replaced `/api/v4/exec/summary` (from `cierre_financiero_v1`) with direct calls to `/api/v4/financial-structure?signal_mode=SIGNAL` per marketplace.

### 4. Auditor Dashboard (`templates/dashboard.html`)
Changed default financial-structure query to include `signal_mode=SIGNAL`.

## RIPLEY Canonical vs Full Comparison

| Metric | FULL (ALL) | CANONICAL (SIGNAL) | Reduction |
|--------|-----------|-------------------|-----------|
| Ingresos Brutos | $467,621,338 | $218,441,218 | 53.3% |
| Devoluciones de Venta | -$16,170,071 | -$27,745,348 | — |
| Costos Logísticos & Operacionales | -$6,533,864 | -$7,478,142 | — |
| Comisiones & Comerciales | -$3,930,702 | $26,518,057 | — |
| Ajustes & Retenciones | -$6,518,330 | -$6,518,330 | 0% |
| **Neto** | **$434,468,371** | **$203,217,455** | **53.2%** |

The 53.2% neto reduction is the correction for duplicate/derived concepts previously inflating the P&L.

## Acceptance Criteria

| Criterion | Status |
|-----------|--------|
| Executive and Auditor show same amounts | **PASS** ✅ |
| Delta Executive vs Auditor = 0 | **PASS** ✅ |
| Both consume marketplace_ledger_v1 | **PASS** ✅ |
| Both use same taxonomy | **PASS** ✅ |
| No independent calculations in Executive | **PASS** ✅ |
| No parallel scorecard sources | **PASS** ✅ |

**Date:** 2026-06-17
