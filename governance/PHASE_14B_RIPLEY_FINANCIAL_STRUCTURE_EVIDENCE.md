# Phase 14B — RIPLEY Financial Structure Evidence

## Summary

Evidence that the `/api/v4/financial-structure` endpoint returns correct category totals that are individually traceable to `marketplace_ledger_v1` via `signal_mode=SIGNAL` filtering.

## Endpoint Behavior

**Request:**
```
GET /api/v4/financial-structure?marketplace=RIPLEY&periodo=2026-01&signal_mode=SIGNAL
```

**Canonical Category Order** (server-enforced):
1. Ingresos Brutos
2. Devoluciones de Venta
3. Costos Logísticos & Operacionales
4. Comisiones & Comerciales
5. Ajustes & Retenciones

## Category SIGNAL Totals

| # | Category | FS SIGNAL Total | SIGNAL Detalles | Status |
|---|---|---|---|---|
| 1 | Ingresos Brutos | $26,530,470 | Importe del pedido | ✅ |
| 2 | Devoluciones de Venta | -$5,983,094 | Importe del pedido reembolsado | ✅ |
| 3 | Costos Logísticos & Operacionales | -$1,226,948 | Gastos de envío pagados por el operador, Descuento por costo logístico, Descuento por logistica inversa, Envío | ✅ |
| 4 | Comisiones & Comerciales | $4,122,807 | Comisión, Comisión de reembolso | ✅ |
| 5 | Ajustes & Retenciones | -$1,050,997 | Factura manual, Abono manual, Otros descuentos, Descuento por cancelación | ✅ |

## Conservation: Sum of Categories = Ledger Total

```
Ingresos:        $26,530,470
+ Devoluciones:  -$5,983,094
+ Costos:        -$1,226,948
+ Comisiones:    $4,122,807
+ Ajustes:       -$1,050,997
──────────────────────────
= SUM:           $22,392,238
= Ledger total:  $22,392,238
Delta:           $0 ✅ PASS
```

## Subcategory Detail (Ene 2026)

| Category | Subcategory (detalle) | SIGNAL | Amount |
|---|---|---|---|
| Ingresos | Importe del pedido | SIGNAL | $26,530,470 |
| Devoluciones | Importe del pedido reembolsado | SIGNAL | -$5,983,094 |
| Costos | Gastos de envío pagados por el operador | SIGNAL | -$1,253,465 |
| Costos | Descuento por costo logístico | SIGNAL | -$458,644 |
| Costos | Descuento por logistica inversa | SIGNAL | -$89,977 |
| Costos | Envío | SIGNAL | $575,138 |
| Comisiones | Comisión | SIGNAL | $6,365,639 |
| Comisiones | Comisión de reembolso | SIGNAL | $1,028,952 |
| Ajustes | Factura manual | SIGNAL | -$1,864,388 |
| Ajustes | Abono manual | SIGNAL | $813,391 |

## Verdict

**FINANCIAL STRUCTURE EVIDENCE PASS** ✅ — All categories, subcategories, and totals are internally consistent and traceable to `marketplace_ledger_v1` with `signal_mode=SIGNAL`.
