# Phase 14B — RIPLEY Ledger Transactional Evidence

## Summary

Evidence that the `/api/v4/ledger` endpoint with `signal_mode=SIGNAL` returns exactly the same rows as the Financial Structure (FS) endpoint, ensuring click-through consistency.

## Evidence A: FS + Ledger SIGNAL Category Totals (Ene 2026)

Every FS category matches the Ledger SIGNAL query at $0 delta:

| Category | FS SIGNAL | Ledger SIGNAL | Delta | Status |
|---|---|---|---|---|
| Ingresos Brutos | $26,530,470 (1059 rows) | $26,530,470 (1059 rows) | $0 | ✅ |
| Devoluciones de Venta | -$5,983,094 (250 rows) | -$5,983,094 (250 rows) | $0 | ✅ |
| Costos Logísticos | -$1,226,948 (1302 rows) | -$1,226,948 (1302 rows) | $0 | ✅ |
| Comisiones | $4,122,807 (879 rows) | $4,122,807 (879 rows) | $0 | ✅ |
| Ajustes | -$1,050,997 (548 rows) | -$1,050,997 (548 rows) | $0 | ✅ |
| Liquidación | $0 (0 rows) | $0 (0 rows) | $0 | ✅ |

## Evidence B: YTD SIGNAL Consistency

YTD (2026) SIGNAL totals confirm the pattern across all available data:

| Category | YTD SIGNAL | YTD ALL | NOISE Delta |
|---|---|---|---|
| Ingresos Brutos | $839,601,212 (27,300 rows) | $1,908,041,379 (73,249 rows) | $1,068,440,167 |
| Devoluciones de Venta | -$112,991,645 (3,838 rows) | -$151,172,371 (10,206 rows) | -$38,180,726 |
| Costos Logísticos | -$34,397,928 (33,940 rows) | -$30,337,138 (36,217 rows) | $4,060,790 |
| Comisiones | $113,842,173 (21,766 rows) | -$13,465,726 (53,336 rows) | -$127,307,899 |
| Ajustes | -$39,891,271 (12,361 rows) | -$39,891,271 (12,361 rows) | $0 |
| Liquidación | $0 (0 rows) | $0 (0 rows) | $0 |

## Evidence C: Non-RIPLEY Isolation

`signal_mode=SIGNAL` has no effect on non-RIPLEY marketplaces — confirms correct isolation:

| Marketplace | SIGNAL | ALL | Delta | Status |
|---|---|---|---|---|
| ML | $12,730,978 | $12,730,978 | $0 | ✅ PASS |
| PARIS | $5,464,333 | $5,464,333 | $0 | ✅ PASS |
| FALABELLA | $0 | $0 | $0 | ✅ PASS |

## Evidence D: Devoluciones Click-Through Detail

When a user clicks "Devoluciones de Venta" in SIGNAL mode, the Ledger returns:
- **SIGNAL**: 250 rows, -$5,983,094, 1 detalle: `Importe del pedido reembolsado`
- **ALL** (pre-fix): 583 rows, -$3,666,853, 6 detalles: `Envío reembolsado`, `Importe del envío del pedido reembolsado`, `Importe del pedido reembolsado`, `Pedidos reembolsados`, `order_amount`, `refund_order_amount`

## Evidence E: Single Order Trace

Order `RIP_TH_99184_importedelpedidoreembolsado`:
- SIGNAL: 1 row, -$22,990, detalle=`Importe del pedido reembolsado` [SIGNAL]
- ALL: 1 row, -$22,990, detalle=`Importe del pedido reembolsado` [SIGNAL] (same — this order only has SIGNAL rows)

## Verdict

**LEDGER EVIDENCE PASS** ✅ — All click-through paths now maintain $0 delta against Financial Structure in SIGNAL mode.
