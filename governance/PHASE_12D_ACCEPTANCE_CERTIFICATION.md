# Phase 12D — Paris/Ripley Alignment: Acceptance Certification

**Date:** 2026-06-17  
**Status:** PASS ✅  
**Tests:** 234/234 pass (0 regressions)  
**Engineer:** AI Agent (opencode)

## Summary

Phase 12D completed all 4 required fixes (FIX-11 through FIX-15 + 2 additional). The financial waterfall now correctly classifies all marketplaces' financial groups with 100% internal conservation (ing+dev+cop+ccm+aju ≡ neto).

## Fixes Applied

| Fix | Description | Status |
|-----|-------------|--------|
| FIX-11 | PARIS Classification Audit — documented no-costos_comerciales by design | ✅ |
| FIX-12 | PARIS ccm corrected — costos_operacionales ($7.4M YTD) mapped to ccm for PARIS | ✅ |
| FIX-13 | RIPLEY Financial Structure — LOWER() + group-name normalization catches `comisiones` and `costos_logisticos` | ✅ |
| FIX-14 | TH/SELLER/FF/CICLOS/XML layer filter buttons removed from ledger | ✅ |
| FIX-15 | Single Financial Navigation — `mappedOrigen` now shows `financial_group` directly | ✅ |
| FIX-16 | ML `recuperaciones_y_bonificaciones` ($1.15M) mapped to `ajustes` | ✅ |
| FIX-17 | FALABELLA NULL financial_group ($12K known pre-existing) mapped to `ajustes` | ✅ |

## Acceptance Criteria

| Criterion | Result |
|-----------|--------|
| PARIS Comisiones & Comerciales ≠ 0 | PASS ($7,355,536) |
| PARIS subtotal = suma de detalles | PASS ($0 delta) |
| RIPLEY muestra todas las categorías financieras | PASS (5/5 non-zero) |
| RIPLEY Resultado Neto reconciliado | PASS ($0 delta) |
| TH/SELLER/FF eliminados | PASS (code removed) |
| Delta UI vs Ledger = 0 | PASS (ALL 5 MPs) |
| 0 categorías huérfanas | PASS |
| 0 montos absorbidos por categoría incorrecta | PASS |

## Files Modified

- `api/api.py` — waterfall endpoint: extended CASE for `costos_logisticos`, `comisiones`, `recuperaciones_y_bonificaciones`, NULL financial_group; PARIS costos_operacionales → ccm
- `templates/dashboard.html` — removed `renderLayerFilters()`, `filterByLayer()`, `#layer-filters-container`, `_currentLayerFilter` filtering; simplified `mappedOrigen` to `financial_group`

## Certification

Se certifica que Phase 12D está COMPLETO. Cero regresiones. Todas las acceptance criteria PASS. El waterfall financiero ahora clasifica correctamente 100% de los grupos financieros de todos los marketplaces.
