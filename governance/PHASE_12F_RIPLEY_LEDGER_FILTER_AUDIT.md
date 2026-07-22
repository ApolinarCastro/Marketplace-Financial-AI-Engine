# Phase 12F — RIPLEY Ledger Filter Audit

## Status: PASS ✅

## Root Cause (F12F-02)

RIPLEY subcategories in the UI financial structure were clickable but produced an empty Ledger Transaccional table. This was a **filter parameter mismatch**:

| Layer | Field used | Value example | RIPLEY populated? |
|-------|-----------|--------------|------------------|
| Before FIX-26 | `clasificacion_operativa = ?` (exact match) | `Importe del pedido` | **No** — NULL for RIPLEY |
| After FIX-26 | `detalle LIKE '%value%'` (wildcard) | `Importe del pedido` | **Yes** — populated for all MPs |

**Root cause:** Phase 12E changed the subcategory source from `desglose` (which used `clasificacion_operativa`) to `financial-structure` (which uses `detalle` from `marketplace_ledger_v1`), but `buildLedgerUrl()` at `dashboard.html:523` still passed the value as `clasificacion_operativa` parameter — a column that is NULL for most RIPLEY rows.

### Fix Applied: FIX-26 (dashboard.html:523)

```js
// Before (broken):
url += `&clasificacion_operativa=${encodeURIComponent(activeFinancialFilter.value)}`;
// After (fixed):
url += `&detalle=${encodeURIComponent(activeFinancialFilter.value)}`;
```

## AUDIT-04: RIPLEY detalle registry

All 28 unique `detalle` values in `marketplace_ledger_v1 WHERE marketplace='RIPLEY'` verified — every one exists in the ledger with non-zero row count.

## AUDIT-05/06: Subcategory filter binding

27 subcategories with `subtotal != 0` tested — **ALL 27 return ledger records** via the new `detalle=` parameter.

| Subcategory | Subtotal | Ledger rows | Status |
|------------|---------|------------|--------|
| Importe del pedido | $218.4M | 31,138 | PASS |
| Precio total | $124.6M | 17,928 | PASS |
| Subtotal | $119.7M | 17,928 | PASS |
| Comisiones | -$22.4M | 29,836 | PASS |
| Comisiones sobre pedidos | -$16.9M | 13,657 | PASS |
| Factura manual | -$11.3M | 12,326 | PASS |
| ... (21 more) | ... | ... | ALL PASS |

## FIX-28: Defensive guard (dashboard.html)

Added check in `renderLedger()` — when ledger returns 0 rows but the active subcategory has `subtotal != 0` in financial-structure, a warning banner is displayed with the exact subtotal amount and an explanation.

## Certification

RIPLEY subcategory → ledger filter is repaired for all 27 non-zero subcategories. Every clickable subcategory in the UI returns ledger records. Defensive guard prevents silent empty-state for edge cases.

**Delta: $0. Zero regression.**
**234/234 tests PASS.**

**Date:** 2026-06-17
