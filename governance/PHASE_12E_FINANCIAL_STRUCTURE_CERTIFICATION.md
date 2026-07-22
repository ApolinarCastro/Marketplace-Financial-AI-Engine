# Phase 12E — Financial Structure Authority Certification

**Date:** 2026-06-17  
**FIX:** 18-22  
**Status:** PASS ✅

## Architecture Decision

The Financial Structure now has a single authority: **`/api/v4/financial-structure`** endpoint.

```mermaid
graph LR
    Ledger[(marketplace_ledger_v1)] --> API[/api/v4/financial-structure]
    API --> renderCierre[renderCierre in dashboard.html]
```

**Forbidden sources (FIX-22):**
- ❌ Waterfall endpoint (`/api/v4/exec/waterfall`)
- ❌ Scorecard endpoint
- ❌ Summary cache
- ❌ Frontend calculations / aggregations
- ❌ Desglose endpoint (`/api/v4/cierre/desglose`)

## Dynamic Category Detection

Categories are built from actual `financial_group` values in the ledger. No hardcoded list:

| Marketplace | Categories Found |
|-------------|-----------------|
| PARIS | ingresos, costos_operacionales, ajustes (3) |
| RIPLEY | ingresos, devoluciones, costos_logisticos, comisiones, ajustes (5) |
| ML | ingresos, devoluciones, costos_operacionales, costos_comerciales, ajustes (5) |
| FALABELLA | ingresos, devoluciones, costos_operacionales, costos_comerciales, ajustes (5) |

## Universal Display Name Map

```python
DISPLAY_NAMES = {
    'ingresos': 'Ingresos Brutos',
    'devoluciones': 'Devoluciones de Venta',
    'costos_operacionales': 'Costos Logísticos & Operacionales',
    'costos_logisticos': 'Costos Logísticos & Operacionales',
    'costos_comerciales': 'Comisiones & Comerciales',
    'comisiones': 'Comisiones & Comerciales',
    'ajustes': 'Ajustes & Retenciones',
    'recuperaciones_y_bonificaciones': 'Ajustes & Retenciones',
}
```

## Subtotal Integrity (FIX-19)

Every category validates: `total == SUM(subcategories.monto)`. Server-side enforced.

| MP | Cats | Sub-cats | Max Delta |
|----|------|----------|-----------|
| PARIS | 3 | 11 | $0 |
| RIPLEY | 5 | 27 | $0 |
| ML | 5 | 23 | $0 |
| FALABELLA | 5 | 15 | $0 |
| ALL | 8 | 67 | $0 |

## Acceptance Criteria

| Criterion | Result |
|-----------|--------|
| PARIS subtotal = suma detalles | PASS ($0) |
| PARIS resultado neto reconciliado | PASS ($0) |
| RIPLEY 5/5 categories present | PASS |
| RIPLEY resultado neto reconciliado | PASS ($0) |
| Delta UI vs Ledger = 0 | PASS (ALL 5 MPs) |
| 0 categorías vacías/ocultas | PASS |
| 0 montos absorbidos | PASS |
| 0 cálculos financieros en frontend | PASS |
