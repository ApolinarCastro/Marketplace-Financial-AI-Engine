# Phase 15B — Signal Taxonomy Certification

**Date**: 2026-06-18
**Status**: CERTIFIED ✅
**Directory**: `knowledge/taxonomy/`

## Taxonomy Files

| File | Marketplace | Detalles | SIGNAL | NOISE | Canonical Groups |
|---|---|---|---|---|---|
| `ripley_v1.json` | RIPLEY | 32 | 12 (37.5%) | 20 (62.5%) | 6 (ing, dev, cos_log, com, liq, aju) |
| `ml_v1.json` | ML | 71 | 70 (98.6%) | 1 (1.4%) | 7 (ing, dev, cos_op, cos_com, aju, rec, tes) |
| `paris_v1.json` | PARIS | 15 | 14 (93.3%) | 1 (6.7%) | 4 (ing, cos_op, dev/aju, aju) |
| `falabella_v1.json` | FALABELLA | 16 | 15 (93.8%) | 1 (6.2%) | 5 (ing, dev, cos_op, cos_com, aju) |

## Validation Gates
| Check | Status |
|---|---|
| No orphan detalles without classification | ✅ 0/134 orphans |
| Every financial_group has a canonical_group | ✅ 0 uncovered groups |
| Canonical groups in canonical order | ✅ ing→dev→costs→com→aju (+ treasury) |
| Case-insensitive matching | ✅ LOWER() in all comparisons |

## Key Classification Decisions

### RIPLEY (Phase 13)
- **12 SIGNAL**: Importe del pedido, Importe del pedido reembolsado, Comisión, Comisión de reembolso, Gastos de envío pagados por el operador, Descuento por costo logístico, Descuento por logistica inversa, Envío, Factura manual, Abono manual, Otros descuentos, Descuento por cancelación
- **20 NOISE**: Duplicados estructurales (Precio total, Subtotal, Comisiones, etc.) + tesorería (A pagar, Pago, etc.)

### ML (Phase 15B)
- **70 SIGNAL**: All operating P&L entries — ingresos, devoluciones, costos operacionales, costos comerciales, ajustes (57 BPP/Poscobro reasons), recuperaciones y bonificaciones
- **1 NOISE**: `Retiro de dinero` — treasury, not P&L
- ML has far fewer duplicates than RIPLEY because ML's raw data comes from Facturación (accounting records), not from multiple report columns

### PARIS (Phase 15B)
- **14 SIGNAL**: Venta, Rebate, Devolución, Cobro por despacho, Logística inversa, Retiro stock bodega Paris, Cobro stock antiguo, Pago de envío comprador, Reversa de pago de envío comprador, Compensación logística, Ajuste inventario activo, Cargo, Cobro por campaña, Merma
- **1 NOISE**: `Despacho` ($0 monto — no financial impact)

### FALABELLA (Phase 15B)
- **15 SIGNAL**: Pago por precio del producto, Descuento por devolución de producto, Cobro por comisión por venta, Reembolso por comisión por venta, Cobro por cofinanciamiento logístico, Reembolso por Promo envío falabella.com, Cobro Promo envío falabella.com, Reversa de pago de envío comprador, Pago de envío comprador, Cobro por logística inversa, Pago por envío directo, Corrección de cobro por envío directo, Corrección de pago envio directo, Pago de aporte promocionales a cliente, Descuento por aportes promocionales a clientes
- **1 NOISE**: `Cobro por comisión por cancelación` — orphan without financial_group classification ($12,099, known since FALABELLA $12K delta)

## Runtime Equivalence (test_taxonomy_equivalence.py)
All 12 taxonomy equivalence tests PASS: identical classification results, $0 monetary delta, operational P&L equivalence for all 4 MPs.
