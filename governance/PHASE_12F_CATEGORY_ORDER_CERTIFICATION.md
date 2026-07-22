# Phase 12F — Category Order Certification

## Status: PASS ✅

## Fix Applied: FIX-23/24 (2026-06-17)

**File:** `api/api.py:589-595`

**Change:** Added `CANONICAL_ORDER` sort after the merge step in `/api/v4/financial-structure`:

```python
CANONICAL_ORDER = [
    "Ingresos Brutos",
    "Devoluciones de Venta",
    "Costos Logísticos & Operacionales",
    "Comisiones & Comerciales",
    "Ajustes & Retenciones",
]
order_map = {name: i for i, name in enumerate(CANONICAL_ORDER)}
cats_list.sort(key=lambda c: order_map.get(c['display_name'], 99))
```

## Result (all 5 views)

| View | Position 1 | Position 2 | Position 3 | Position 4 | Position 5 |
|------|-----------|-----------|-----------|-----------|-----------|
| PARIS | Ingresos Brutos | Costos Logísticos & Operacionales | Ajustes & Retenciones | — | — |
| RIPLEY | Ingresos Brutos | Devoluciones de Venta | Costos Logísticos & Operacionales | Comisiones & Comerciales | Ajustes & Retenciones |
| ALL | Ingresos Brutos | Devoluciones de Venta | Costos Logísticos & Operacionales | Comisiones & Comerciales | Ajustes & Retenciones |
| ML | Ingresos Brutos | Devoluciones de Venta | Costos Logísticos & Operacionales | Comisiones & Comerciales | Ajustes & Retenciones |
| FALABELLA | Ingresos Brutos | Devoluciones de Venta | Costos Logísticos & Operacionales | Comisiones & Comerciales | Ajustes & Retenciones |

**Ordering: 5/5 PASS** — Ingresos Brutos always first, canonical order preserved.

## Certification

The category ordering for all marketplace views now follows the canonical financial hierarchy:
1. Ingresos Brutos
2. Devoluciones de Venta
3. Costos Logísticos & Operacionales
4. Comisiones & Comerciales
5. Ajustes & Retenciones

No marketplace displays categories in a different order regardless of SQL `LOWER()` or merge sequence.

**Delta: $0. Zero regression.**

**Certified by:** FIX-23/24 automated enforcement
**Date:** 2026-06-17
