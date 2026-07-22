# Ledger Subcategory Reconciliation Report

## Status: PASS ✅

## Verification Method

For every subcategory in the financial-structure response (all 4 MPs, signal_mode=SIGNAL):
1. Extract the `detalle` value
2. Query `marketplace_ledger_v1` with exact `detalle = ?` match and YTD filter
3. Compare SUM(monto) with the subcategory total from financial-structure
4. Verify delta = 0

## Results

### FALABELLA — All 5 subcategories PASS
### ML — All 17 subcategories PASS
### PARIS — All 6 subcategories PASS
### RIPLEY — All 11 SIGNAL subcategories PASS

## Subcategory Detail (RIPLEY SIGNAL)

| Subcategory | Cat Total | Ledger SUM | Delta |
|------------|-----------|------------|-------|
| Importe del pedido | $218,441,218 | $218,441,218 | $0 |
| Importe del pedido reembolsado | -$27,745,348 | -$27,745,348 | $0 |
| Envío | $4,365,041 | $4,365,041 | $0 |
| Gastos de envío pagados por el operador | -$9,282,241 | -$9,282,241 | $0 |
| Descuento por costo logístico | -$1,865,167 | -$1,865,167 | $0 |
| Descuento por logistica inversa | -$695,775 | -$695,775 | $0 |
| Comisión | $21,526,642 | $21,526,642 | $0 |
| Comisión de reembolso | $4,991,415 | $4,991,415 | $0 |
| Abono manual | $4,793,840 | $4,793,840 | $0 |
| Factura manual | -$11,304,972 | -$11,304,972 | $0 |
| Descuento por cancelación | -$7,198 | -$7,198 | $0 |

## Certification

All 39 subcategories across 4 marketplaces reconcile with $0 delta against the source ledger.

**Source:** `marketplace_ledger_v1`
**Date:** 2026-06-17
