# UI ↔ Ledger Reconciliation Report — Phase 14A

## Status: PASS ✅ (Delta = 0 at all levels)

## Validation Matrix (YTD 2026, signal_mode=SIGNAL)

| Level | Validation | FALABELLA | ML | PARIS | RIPLEY |
|-------|-----------|-----------|-----|-------|--------|
| **Category = Subcategory** | FS category total = sum of subcategories | $0 ✅ | $0 ✅ | $0 ✅ | $0 ✅ |
| **Subcategory = Ledger** | Exact detalle match | $0 ✅ | $0 ✅ | $0 ✅ | $0 ✅ |
| **Category click → Ledger** | financial_group filter returns correct rows | $0 ✅ | $0 ✅ | $0 ✅ | $0 ✅ |
| **Subcategory click → Ledger** | detalle filter returns correct rows | $0 ✅ | $0 ✅ | $0 ✅ | $0 ✅ |
| **Neto = Categories** | Server-side sum | $0 ✅ | $0 ✅ | $0 ✅ | $0 ✅ |

## Bugs Fixed

### 1. Case-sensitive financial_group (RIPLEY)
**Impact:** All RIPLEY category clicks returned 0 ledger rows  
**Fix:** `LOWER(financial_group) = LOWER(?)` in `query_ledger()`  
**Pre-fix:** 0 rows for `financial_group='ingresos'`  
**Post-fix:** 17,533 rows ($467.6M)

### 2. Merged financial_group (ML)
**Impact:** "Ajustes & Retenciones" category click returned 0 rows  
**Fix:** Comma-separated `financial_group` → `LOWER(financial_group) IN (values)`  
**Pre-fix:** 0 rows for `'ajustes, recuperaciones_y_bonificaciones'`  
**Post-fix:** 104 rows ($1.15M)

### 3. Substring collision (ALL MPs)
**Impact:** Subcategory clicks returned wrong totals due to LIKE substring matches  
**Fix:** `LOWER(detalle) = LOWER(?)` — exact match instead of `LIKE '%value%'`  
**Example:** "Importe del pedido" no longer matches "Importe del pedido reembolsado"  
**Pre-fix:** $190.7M (contaminated)  
**Post-fix:** $218.4M (correct)

## Certification

Every category click returns exactly the same data as the sum of its subcategories.
Every subcategory click returns exactly the same total as the financial-structure value.
Delta = 0 at all levels for all 4 marketplaces.

**Source of Truth:** `marketplace_ledger_v1` via `/api/v4/financial-structure` and `/api/v4/ledger`
**Date:** 2026-06-17
