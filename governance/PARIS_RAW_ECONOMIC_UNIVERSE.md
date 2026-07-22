# PARIS RAW ECONOMIC UNIVERSE
**Date:** 2026-06-07
**Source:** Raw XLSX files only. No ledger queries.

---

## Economic Universe by Concept (from RAW monto_a_pagar)

| Concept | RAW monto_a_pagar |
|---|---|
| **Venta** | **$487,741,043** |
| DevoluciÃ³n | -$123,490,638 |
| Cobro por despacho | -$22,067,830 |
| LogÃ­stica inversa | -$3,225,310 |
| Retiro stock bodega Paris | -$1,630,800 |
| CompensaciÃ³n logÃ­stica | $1,618,057 |
| Ajuste Inventario Activo | $647,108 |
| Cargo | -$646,295 |
| Cobro stock antiguo | -$316,638 |
| Rebate | $273,230 |
| Cobro por campaÃ±a | -$260,504 |
| Merma | $16,991 |
| Despacho | $0 |
| **TOTAL NETO** | **$338,658,414** |

---

## Financial Groups (mapped from concepts)

| Financial Group | RAW monto_a_pagar |
|---|---|
| **Ingresos** (Venta + Rebate + Despacho) | **$488,014,273** |
| **Devoluciones** | **-$123,490,638** |
| **Costos Operacionales** (Cobro despacho + Log inversa + Retiro stock + Cobro stock antiguo) | **-$27,240,578** |
| **Ajustes** (CompensaciÃ³n log + Ajuste Inventario + Cargo + CampaÃ±a + Merma) | **$1,375,357** |
| **Resultado Neto** | **$338,658,414** |

---

## Year-Over-Year Comparison

| Period | RAW monto_a_pagar (Ventas) |
|---|---|
| 2025 Total | $366,023,406 |
| 2026 (Jan-May) | $121,717,617 |
| 2026 (Jun partial) | $18,076,842 |

*Note: 2026 Jun data is partial (1-8 Jun).*

---

## Key Observations

1. **Commission Rate:** RAW monto (gross) = $415.6M vs RAW monto_a_pagar (net) = $338.7M. Implicit commission = $76.9M (18.5% take rate).

2. **Negative FF file:** `1 may 2026 - 31 may 2026.xlsx` (FF) has negative monto (-$790,116). This file contains primarily devoluciones/credits. Its scope is partial.

3. **Despacho concept:** Exists in RAW (with $0 monto) but represents shipping/logistics events, not financial transactions.

4. **Date range anomalies:** Some DS files contain dates outside their nominal month (e.g., 04-2025.xlsx has dates back to 2024-01-09). This suggests data from prior periods is included.

5. **File scope overlap:** Both DS and FF pipelines cover the same transaction universe. DS is monthly, FF is annual/partial.
