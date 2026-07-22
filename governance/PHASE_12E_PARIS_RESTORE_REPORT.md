# Phase 12E — PARIS Financial Structure Restore Report

**Date:** 2026-06-17  
**FIX:** 18, 21, 22  
**Status:** COMPLETED ✅

## Problem

La UI mostraba "Comisiones Marketplace = -3.121.341" mientras el subtotal "Comisiones & Comerciales" mostraba -1.212.640 — inconsistencia subtotal-detalle.

**Root cause:** 
- Phase 12D moved PARIS's `costos_operacionales` into the waterfall's `ccm` slot
- The category card subtotal came from the waterfall (ccm = costos_operacionales)
- But the category details came from the desglose endpoint (which queries `financial_group='costos_comerciales'` — PARIS has none)
- Result: subtotal ≠ sum(details)

## Solution

**FIX-18/22:** Replaced the waterfall-based financial structure with a new endpoint `/api/v4/financial-structure` that queries `marketplace_ledger_v1` directly.

**FIX-21:** Categories are now DYNAMIC — determined by actual `financial_group` values in the ledger, not hardcoded.

## PARIS Financial Structure (Post-Fix)

| Category | Total | Subcategories | Delta |
|----------|-------|---------------|-------|
| Ingresos Brutos | $112,574,966 | Venta, Rebate | $0 |
| Costos Logísticos & Operacionales | -$7,355,536 | Cobro por despacho, Logística inversa, Retiro stock, Cobro stock antiguo | $0 |
| Ajustes & Retenciones | -$32,252,676 | Devolución, Compensación logística, Ajuste Inventario, Cargo, Merma | $0 |
| **Neto** | **$72,966,754** | | **$0** |

PARIS shows 3 categories (no `comisiones` group — correct per DEC-023: 3P marketplace model).

## Verification

- 234/234 tests PASS
- Each category: subtotal = SUM(detalles) — $0 delta
- Neto = SUM(categories) — $0 delta
- 0 frontend calculations (all server-side from ledger)
