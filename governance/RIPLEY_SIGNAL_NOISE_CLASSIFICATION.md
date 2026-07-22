# RIPLEY Signal/Noise Classification

## Status: PASS ✅

## Audit-07: Full detalle inventory

Complete query of `marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND COALESCE(include_in_operational_pnl,1)=1`:

| Detalle | Rows | Total ($) | Classification |
|---------|------|-----------|----------------|
| Importe del pedido | 27,300 | $839,601,212 | **SIGNAL** |
| Precio total | 17,928 | $535,283,444 | NOISE |
| Subtotal | 17,928 | $513,257,522 | NOISE |
| Importe del pedido reembolsado | 3,838 | -$112,991,645 | **SIGNAL** |
| Pedidos reembolsados | 2,536 | -$86,498,564 | NOISE |
| Comisiones | 16,179 | -$84,253,262 | NOISE |
| Comisiones sobre pedidos | 11,121 | -$68,113,598 | NOISE |
| Factura manual | 12,326 | -$47,770,671 | **SIGNAL** |
| order_amount | 1,269 | $37,505,936 | NOISE |
| Gastos de envío pagados por el operador | 18,245 | -$39,036,614 | **SIGNAL** |
| Importe del envío del pedido | 10,093 | $19,899,201 | NOISE |
| Comisión | 17,928 | $93,193,394 | **SIGNAL** |
| Envío | 8,152 | $19,137,413 | **SIGNAL** |
| Comisiones sobre pedidos reembolsados | 2,536 | $15,730,070 | NOISE |
| refund_order_amount | 465 | $14,475,092 | NOISE |
| Descuento por costo logístico | 7,049 | -$13,025,554 | **SIGNAL** |
| Comisión de reembolso | 3,838 | $20,648,779 | **SIGNAL** |
| Abono manual | 25 | $7,912,840 | **SIGNAL** |
| commission_fee | 1,269 | $6,750,820 | NOISE |
| refund_commission_fee | 465 | $2,578,071 | NOISE |
| Gastos de envío reembolsados pagados por el operador | 2,118 | $3,696,195 | NOISE |
| Descuento por logistica inversa | 494 | -$1,473,173 | **SIGNAL** |
| Importe del envío del pedido reembolsado | 1,224 | -$1,983,471 | NOISE |
| Descuento por cofinanciamiento logístico (FF) | 132 | $376,600 | NOISE |
| Envío reembolsado | 894 | -$1,712,724 | NOISE |
| Descuento por logística inversa (FF) | 7 | $21,000 | NOISE |
| Descuento por cancelación | 5 | -$28,490 | **SIGNAL** |
| Otros descuentos | 5 | -$4,950 | **SIGNAL** |
| A pagar | — | — | NOISE (treasury) |
| Amount transferred to tienda | — | — | NOISE (treasury) |
| Pago | — | — | NOISE (treasury) |
| transfer_amount | — | — | NOISE (treasury) |

## Audit-08: Classification Rules

Rule applied: a `detalle` is SIGNAL only if it appears in the canonical ingestion rules defined by the directive. All others are NOISE.

**Source:** `knowledge/taxonomy/ripley_v1.json`

**Date:** 2026-06-17
