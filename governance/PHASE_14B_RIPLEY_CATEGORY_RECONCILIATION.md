# Phase 14B — RIPLEY Category Reconciliation: FS SIGNAL vs Ledger SIGNAL

## Validation Criteria (AC_01-06)

Every category in the Financial Structure (FS) dashboard must match the Ledger Transaccional query when both use `signal_mode=SIGNAL`. The delta must be $0.

## Methodology

1. Query `/api/v4/financial-structure?marketplace=RIPLEY&periodo=2026-01&signal_mode=SIGNAL` → get FS category totals
2. Query `marketplace_ledger_v1` by `financial_group` with `signal_mode=SIGNAL` → get Ledger SIGNAL totals
3. Compare: `delta = FS_total - Ledger_SIGNAL_total`

## Results — RIPLEY Ene 2026

| # | Category | FS SIGNAL | Ledger SIGNAL | Delta | Status |
|---|---|---|---|---|---|
| 1 | Ingresos Brutos | $26,530,470 | $26,530,470 | $0 | ✅ PASS |
| 2 | Devoluciones de Venta | -$5,983,094 | -$5,983,094 | $0 | ✅ PASS |
| 3 | Costos Logísticos & Operacionales | -$1,226,948 | -$1,226,948 | $0 | ✅ PASS |
| 4 | Comisiones & Comerciales | $4,122,807 | $4,122,807 | $0 | ✅ PASS |
| 5 | Ajustes & Retenciones | -$1,050,997 | -$1,050,997 | $0 | ✅ PASS |
| 6 | Liquidación | $0 | $0 | $0 | ✅ PASS |

## Difference from Ledger ALL

The delta between FS SIGNAL and Ledger ALL (unfiltered) is **intentional** — it represents NOISE entries excluded by the taxonomy:

| Category | FS SIGNAL | Ledger ALL | NOISE Delta | NOISE Rows |
|---|---|---|---|---|
| Ingresos | $26,530,470 | $61,788,496 | **+$35,258,026** | Precio total, Subtotal, Importe del envío del pedido |
| Devoluciones | -$5,983,094 | -$3,666,853 | **+$2,316,241** | order_amount, Pedidos reembolsados, refund_order_amount, Envío reembolsado, Importe del envío del pedido reembolsado |
| Costos Logísticos | -$1,226,948 | -$1,173,143 | **+$53,805** | Gastos de envío reembolsados pagados por el operador |
| Comisiones | $4,122,807 | $758,627 | **-$3,364,180** | Comisiones, Comisiones sobre pedidos, commission_fee, etc. |
| Ajustes | -$1,050,997 | -$1,050,997 | **$0** | (no NOISE in this group) |

## Conservation Check

```
Sum of 5 categories (SIGNAL): $22,392,238
Ledger total (SIGNAL):        $22,392,238
Conservation:                 ✅ PASS
```

## Verdict

**ALL 6 CATEGORIES PASS** ✅ — FS SIGNAL = Ledger SIGNAL with $0 delta for every financial group. The NOISE delta documented above is by design (taxonomy exclusions), not a reconciliation error.
