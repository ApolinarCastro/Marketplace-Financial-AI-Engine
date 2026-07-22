# Phase 12F — UI Filter Binding Report

## Status: CORRECTED ✅

## Changes Summary

| ID | File | Change |
|----|------|--------|
| FIX-23 | `api/api.py:589-595` | Added canonical category sort in `/api/v4/financial-structure` |
| FIX-24 | `api/api.py:589-595` | Enforced order for ALL marketplaces |
| FIX-26 | `templates/dashboard.html:523` | Changed `&clasificacion_operativa=` → `&detalle=` in `buildLedgerUrl()` |
| FIX-27 | `templates/dashboard.html:523` | Separated `display_name` (UI text) from `filter_value` (ledger column) |
| FIX-28 | `templates/dashboard.html:579` | Added defensive warning when ledger=0 ∧ subtotal≠0 |

## Binding Architecture (Post-FIX)

```
Estructura Financiera          Ledger Transaccional
┌─────────────────────┐         ┌──────────────────────┐
│ display_name        │  click  │ buildLedgerUrl()     │
│   "Importe del      │ ──────► │   ?detalle=...       │
│    pedido"          │   FIX   │   LIkE '%Importe%'   │
│ filter_value=detalle│    -26  │                      │
└─────────────────────┘         └──────────────────────┘
     ▲                                   ▲
     │                                   │
     │ UI renders display_name           │ queries marketplace_ledger_v1.detalle
     │ (human readable)                  │ (exact ledger column)
     └───────────────────────────────────┘
```

## Regression Verification

| Test | Before FIX-26 | After FIX-26 |
|------|--------------|-------------|
| RIPLEY "Importe del pedido" → Ledger | 0 rows ❌ | 31,138 rows ✅ |
| RIPLEY "Comisiones" → Ledger | 0 rows ❌ | 29,836 rows ✅ |
| RIPLEY "Factura manual" → Ledger | 0 rows ❌ | 12,326 rows ✅ |
| All 27 RIPLEY subcategories | 0 rows ❌ | All non-zero ✅ |
| PARIS subcategories | unaffected | unaffected ✅ |
| ML subcategories | unaffected | unaffected ✅ |
| FALABELLA subcategories | unaffected | unaffected ✅ |

## Frontend Logic Status

**Zero financial logic in frontend.** The binding is pure UI routing — the `detalle` value from `financial-structure` is passed directly as a URL parameter to the backend. The server does the actual filtering via `LIKE '%value%'` on `marketplace_ledger_v1.detalle`.

**Date:** 2026-06-17
