# Phase 12D — Single Financial Navigation Certificate (FIX-14/15)

**Date:** 2026-06-17  
**Status:** PASS ✅

## Removed Layer Filter Buttons

The following layer filter buttons have been removed from `templates/dashboard.html`:

| Button | Type | Removed |
|--------|------|---------|
| TH | CAPA TRANSACTION | ✅ |
| CICLOS | CAPA SETTLEMENT | ✅ |
| SELLER | CAPA OPERATIONAL | ✅ |
| FF | CAPA LOGISTICS | ✅ |
| XML | CAPA TAX | ✅ |

## Removed Code

- `renderLayerFilters()` function — was rendering 5 layer filter buttons
- `filterByLayer()` function — was setting `_currentLayerFilter` and re-rendering
- `#layer-filters-container` HTML div — container for the buttons
- `_currentLayerFilter` filtering in `renderLedger()` — was filtering ledger by `origen_capa`

## Simplified `mappedOrigen`

Before (incorrect mapping):
```
costos_operacionales → 'FF'
costos_comerciales → 'Comisiones'
tesoreria → 'TH'
liquidacion → 'CICLOS'
ingresos → 'Seller'
devoluciones → 'XML'
ajustes → 'Ajustes'
comisiones → 'Comisiones'
```

After (direct financial_group display):
```
row.financial_group → displayed directly
```

## Navigation Architecture

The financial structure now uses a clean Category→Subcategory→Ledger navigation:

1. **Category** (click on any financial category card in Estructura Financiera)
2. **Subcategory** (click on any detail row within a category)
3. **Ledger** (filtered by selected category/subcategory)

No duplicate navigation paths. No layer overlay. Single source of truth from `financial_group`.

## Verification

- 234/234 tests PASS
- All navigation still works via `selectFinancialFilter('category', ...)` and `selectFinancialFilter('subgroup', ...)`
- Ledger still displays correctly with `financial_group` as the source column
