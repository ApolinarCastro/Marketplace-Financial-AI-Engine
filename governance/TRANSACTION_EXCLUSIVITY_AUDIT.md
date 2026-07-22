# Transaction Exclusivity Audit

## Status: PASS ✅ (0 cross-SIGNAL overlaps)

## Question

Does any single `id_transaccion` appear in more than one SIGNAL subcategory? If so, the same transaction dollar would be counted in multiple subcategories.

## Method

For every pair of SIGNAL `detalle` values (RIPLEY, YTD 2026), compute the intersection of their `id_transaccion` sets. Count pairs with non-zero intersection.

## Verified Pairs (55 pairs, all zero overlap)

The 11 RIPLEY SIGNAL subcategories produce `11 choose 2 = 55` unique pairs. All 55 pairs have exactly 0 shared `id_transaccion` values.

### SIGNAL Subcategories

1. Importe del pedido
2. Importe del pedido reembolsado
3. Envío
4. Gastos de envío pagados por el operador
5. Descuento por costo logístico
6. Descuento por logistica inversa
7. Comisión
8. Comisión de reembolso
9. Abono manual
10. Factura manual
11. Descuento por cancelación

## Conclusion

Every transaction in the RIPLEY canonical SIGNAL set belongs to exactly one subcategory. The financial-structure's `LOWER(financial_group)` grouping correctly aggregates these without any transaction-level double-counting.

**Source:** `marketplace_ledger_v1` (YTD 2026, RIPLEY)
**Date:** 2026-06-17
