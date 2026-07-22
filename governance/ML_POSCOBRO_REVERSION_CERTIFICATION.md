# ML PosCobro Reversion Certification

**Directive:** P16F_01  
**Date:** 2026-06-19  
**Status:** CERTIFIED ✅

## Problem

PosCobro fashion return reasons (bigger_than_expected_fashion, etc.) appeared as a separate `Riesgos_y_Compensaciones` financial group in Financial Structure, Waterfall, and Executive Dashboard — a regression from Phase 16C.

## Root Cause

`riesgos_y_compensaciones` (5,833 operational rows, $175.9M) was not present in `DISPLAY_NAMES` in `api/api.py:544`. The fallback `get_cat_display()` returned `"Riesgos Y Compensaciones"` as a standalone category at sort position 99 (after canonical groups). The waterfall `aju` CASE also excluded it, breaking conservation (`ing+dev+cop+ccm+aju ≠ neto`).

## Fix Applied

Three changes in `api/api.py`:

| # | File | Line | Change | Rationale |
|---|------|------|--------|-----------|
| 1 | `api/api.py` | 553 | `'riesgos_y_compensaciones': 'Devoluciones de Venta'` | PosCobro fashion reasons are DEVTYPES of returns; merge into Devoluciones |
| 2 | `api/api.py` | 758 | `LOWER(financial_group) IN ('devoluciones', 'riesgos_y_compensaciones')` | Waterfall dev CASE now includes riesgos |
| 3 | `api/api.py` | 761 | Removed `'riesgos_y_compensaciones'` from aju CASE | No longer counted in Ajustes |

## Economic Justification

Each `riesgos_y_compensaciones` detalle (e.g., `different_color_or_size_fashion`, `repentant_buyer`) describes the REASON for a return. These are **analytical subtypes of Devoluciones**, not standalone adjustments. They belong under Devoluciones in the financial hierarchy:

```
Devoluciones de Venta
├── Importe del pedido reembolsado  (operational return amount)
├── bigger_than_expected_fashion     (PosCobro reason — analytical)
├── repentant_buyer                  (PosCobro reason — analytical)
├── different_color_or_size_fashion  (PosCobro reason — analytical)
└── ... (31 more reasons)
```

## Verification

| Check | Result |
|-------|--------|
| No separate `Riesgos` category in Financial Structure | PASS ✅ |
| 8+ fashion details found under Devoluciones subcategories | PASS ✅ |
| 0 fashion details under Ajustes | PASS ✅ |
| ML waterfall conservation $0 delta | PASS ✅ |
| RIPLEY waterfall conservation $0 delta | PASS ✅ |
| ALL waterfall conservation $0 delta | PASS ✅ |
| 265/265 tests pass | PASS ✅ |
| Certification gate (27 tests) | PASS ✅ |

## Delta

**$0** — Single Financial Truth preserved. No P&L amounts changed, only display grouping.
