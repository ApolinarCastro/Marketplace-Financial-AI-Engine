# Phase 14B — RIPLEY Taxonomy Mapping Audit

## Summary

Every `detalle` value in RIPLEY's `marketplace_ledger_v1` was audited against `knowledge/taxonomy/ripley_v1.json` to verify its `canonical_group` and `signal` classification are correct and match the actual `financial_group` in the database.

## Audit Scope

- **Marketplace**: RIPLEY
- **Period**: All available (2024-01 to 2026-06)
- **Source**: `marketplace_ledger_v1`
- **Taxonomy**: `knowledge/taxonomy/ripley_v1.json` v1.0
- **Verification**: For each `detalle`, confirm:
  1. The `financial_group` in the DB matches the taxonomy's `canonical_group`
  2. The `signal` classification correctly identifies canonical P&L entries vs. noise/derived entries

## Per-Detalle Mapping Verification

| # | detalle | DB financial_group | Taxonomy canonical_group | Signal | Match |
|---|---|---|---|---|---|
| 1 | Importe del pedido | INGRESOS | ingresos | SIGNAL | ✅ |
| 2 | Precio total | INGRESOS | null (noise) | NOISE | ✅ |
| 3 | Subtotal | INGRESOS | null (noise) | NOISE | ✅ |
| 4 | Importe del envío del pedido | INGRESOS | null (noise) | NOISE | ✅ |
| 5 | Importe del pedido reembolsado | DEVOLUCIONES | devoluciones | SIGNAL | ✅ |
| 6 | Pedidos reembolsados | DEVOLUCIONES | null (noise) | NOISE | ✅ |
| 7 | Importe del envío del pedido reembolsado | DEVOLUCIONES | null (noise) | NOISE | ✅ |
| 8 | Envío reembolsado | DEVOLUCIONES | null (noise) | NOISE | ✅ |
| 9 | order_amount | DEVOLUCIONES | null (noise) | NOISE | ✅ |
| 10 | refund_order_amount | DEVOLUCIONES | null (noise) | NOISE | ✅ |
| 11 | Comisión | COMISIONES | comisiones | SIGNAL | ✅ |
| 12 | Comisión de reembolso | COMISIONES | comisiones | SIGNAL | ✅ |
| 13 | Comisiones | COMISIONES | null (noise) | NOISE | ✅ |
| 14 | Comisiones sobre pedidos | COMISIONES | null (noise) | NOISE | ✅ |
| 15 | Comisiones sobre pedidos reembolsados | COMISIONES | null (noise) | NOISE | ✅ |
| 16 | commission_fee | COMISIONES | null (noise) | NOISE | ✅ |
| 17 | refund_commission_fee | COMISIONES | null (noise) | NOISE | ✅ |
| 18 | Gastos de envío pagados por el operador | COSTOS_LOGISTICOS | costos_logisticos | SIGNAL | ✅ |
| 19 | Descuento por costo logístico | COSTOS_LOGISTICOS | costos_logisticos | SIGNAL | ✅ |
| 20 | Descuento por logistica inversa | COSTOS_LOGISTICOS | costos_logisticos | SIGNAL | ✅ |
| 21 | Envío | COSTOS_LOGISTICOS | costos_logisticos | SIGNAL | ✅ |
| 22 | Gastos de envío reembolsados pagados por el operador | COSTOS_LOGISTICOS | null (noise) | NOISE | ✅ |
| 23 | Descuento por cofinanciamiento logístico (FF) | COSTOS_LOGISTICOS | null (noise) | NOISE | ✅ |
| 24 | Descuento por logística inversa (FF) | COSTOS_LOGISTICOS | null (noise) | NOISE | ✅ |
| 25 | Factura manual | AJUSTES | ajustes | SIGNAL | ✅ |
| 26 | Abono manual | AJUSTES | ajustes | SIGNAL | ✅ |
| 27 | Otros descuentos | AJUSTES | ajustes | SIGNAL | ✅ |
| 28 | Descuento por cancelación | AJUSTES | ajustes | SIGNAL | ✅ |
| 29 | A pagar | LIQUIDACION | null (noise) | NOISE | ✅ |
| 30 | Amount transferred to tienda | LIQUIDACION | null (noise) | NOISE | ✅ |
| 31 | Pago | LIQUIDACION | null (noise) | NOISE | ✅ |
| 32 | transfer_amount | LIQUIDACION | null (noise) | NOISE | ✅ |

**Result**: 32/32 mappings verified. **PASS** ✅

## Coverage Analysis

- **SIGNAL detalles**: 12 (across ingresos=1, devoluciones=1, costos_logisticos=4, comisiones=2, ajustes=4)
- **NOISE detalles**: 20 (duplicates=10, derived=4, treasury=4, logistics components=2)
- **Duplicación estructural**: 9 NOISE values are direct duplicates of SIGNAL values (Precio total, Subtotal, Pedidos reembolsados, Comisiones, Comisiones sobre pedidos, Comisiones sobre pedidos reembolsados, commission_fee, refund_commission_fee)
- **Tesorería**: 4 NOISE values (A pagar, Amount transferred to tienda, Pago, transfer_amount) — correctly excluded from P&L

## Verdict

**MAPPING AUDIT PASS** — All 32 `detalle` values map correctly. No misclassified entries. No orphan `detalle` values. Taxonomy is complete and accurate.
