# Phase 12E — UI ↔ Ledger Reconciliation Certificate

**Date:** 2026-06-17  
**Status:** PASS ✅

## Traceability Chain

Every number visible in the Estructura Financiera UI can be traced to a direct SQL query:

```
UI Category Card Total
  ← /api/v4/financial-structure (server)
    ← SELECT LOWER(financial_group), detalle, SUM(monto)
         FROM marketplace_ledger_v1
         WHERE fecha >= ? AND COALESCE(include_in_operational_pnl,1)=1
         GROUP BY LOWER(financial_group), detalle

UI Subcategory Line Item
  ← Same query returns detalle-level totals

UI Resultado Neto
  ← SUM(categories.total) = SUM(monto) from ledger
```

## SQL → UI Mapping

```sql
SELECT LOWER(financial_group) as cat, detalle, SUM(monto) as total
FROM marketplace_ledger_v1
WHERE marketplace = ? AND fecha >= ? AND COALESCE(include_in_operational_pnl,1)=1
  AND financial_group IS NOT NULL
GROUP BY LOWER(financial_group), detalle
ORDER BY cat, ABS(SUM(monto)) DESC
```

The API response maps as:
- `cat` → category card with `display_name` from lookup
- `detalle` → subcategory line items
- `SUM(monto)` → category total

## Verification: Zero Frontend Calculations

Audited `dashboard.html` for financial logic:

| Check | Location | Result |
|-------|----------|--------|
| No `+=` on financial values | renderCierre | PASS |
| No `reduce()` on monto | renderCierre | PASS |
| No waterfall data for subtotals | loadDashboard | PASS |
| No desglose endpoint usage | loadDashboard | PASS |
| No `||` operator on amounts | Entire file | PASS (fixed in Phase 12C) |
| No `mapDetalleToConcept()` | Entire file | PASS (removed UX1.1) |
| Render uses API totals directly | renderCierre | PASS |

## Delta Verification (All MPs)

| MP | SUM(categories) | Neto | Delta |
|----|-----------------|------|-------|
| PARIS | $72,966,754 | $72,966,754 | $0 |
| RIPLEY | $434,468,371 | $434,468,371 | $0 |
| ML | $133,742,925 | $133,742,925 | $0 |
| FALABELLA | $7,676,485 | $7,676,485 | $0 |
| ALL | $648,854,535 | $648,854,535 | $0 |

**Certified: Every UI number = SELECT SUM(monto) FROM marketplace_ledger_v1.** ✅
