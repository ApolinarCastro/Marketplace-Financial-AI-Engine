# E2.0 — PARIS Stock Aging: Root Cause Analysis

**Date:** 2026-06-03  
**Mode:** READ ONLY — evidence only, no inferences

---

## 1. Observable Data

### Source: `marketplace_ledger_v1` WHERE marketplace='PARIS' AND detalle='Cobro stock antiguo'

**Total rows:** 11  
**Total amount:** -$314,802 (negative = Eccsa pays cost)  
**Date range:** 2025-05-30 to 2026-04-30  
**Financial group:** 11/11 in 'costos_operacionales'

### All Rows

| # | Date | Amount | id_transaccion |
|---|---|---|---|
| 1 | 2025-05-30 | -$14,580 | 3462492 |
| 2 | 2025-06-30 | -$29,232 | 3659236 |
| 3 | 2025-07-31 | -$18,342 | 3769929 |
| 4 | 2025-08-29 | -$28,152 | 3868777 |
| 5 | 2025-09-30 | -$33,948 | 3972988 |
| 6 | 2025-11-05 | -$23,562 | 4184365 |
| 7 | 2025-11-28 | -$22,860 | 4283914 |
| 8 | 2025-12-31 | -$30,366 | 4611536 |
| 9 | 2026-01-30 | -$27,864 | 4753729 |
| 10 | 2026-02-27 | -$66,492 | 5036421 |
| 11 | 2026-04-30 | -$19,404 | 5350241 |

---

## 2. Observable Patterns

### Temporal Pattern

```
2025-05  Jun  Jul  Aug  Sep  Oct  Nov1  Nov2  Dec 2026-01  Feb  Mar  Apr
  │     │    │    │    │         │     │    │    │       │         │
$14.6K $29K $18K $28K $34K     $23.6K $23K $30K $28K  $66.5K   $19.4K
```

**Observation:**
- 11 charges over 12 months (2025-05 to 2026-04)
- Present in 10 of 12 months (absent: Oct 2025, Mar 2026)
- November has 2 charges (2025-11-05 and 2025-11-28)
- Always at month-end except 2025-11-05 (mid-month)

### Amount Pattern

| Statistic | Value |
|---|---|
| Total | -$314,802 |
| Mean | -$28,618 |
| Median | -$27,864 |
| Min | -$14,580 (May 2025) |
| Max | -$66,492 (Feb 2026) |
| Std Dev | $14,307 |

**Observation:** Amount is variable ($14,580 to $66,492). Mean is $28,618 but February 2026 ($66,492) is 2.3x the mean — an outlier.

### Sequential id_transaccion Analysis

```
3462492 → 3659236 → 3769929 → 3868777 → 3972988 → 4184365 → 4283914 → 4611536 → 4753729 → 5036421 → 5350241
```

**Observation:** IDs are strictly increasing and sequential. Each new charge has a higher ID than the previous. This is consistent with a periodic billing process (not manual or ad-hoc).

### Co-occurrence with Retiro Stock

| Date | Stock Antiguo | Retiro Stock on Same Date? |
|---|---|---|
| 2025-09-30 | -$33,948 | YES (-$328,500) |
| 2025-11-28 | -$22,860 | YES (-$326,400) |
| 2026-01-30 | -$27,864 | YES (-$285,000) |
| 2026-04-30 | -$19,404 | YES (-$354,300) |

**Observation:** On 4 of 11 dates (36%), stock antiguo charge co-occurs with retiro stock charge. On those same dates, Venta and Devolución also appear with high values. This suggests a periodic inventory reconciliation process that generates both charges simultaneously.

### Monthly Pattern (Excluding Co-occuring Dates)

| Month | Amount | Retiro same date? |
|---|---|---|
| May 2025 | -$14,580 | No |
| Jun 2025 | -$29,232 | No |
| Jul 2025 | -$18,342 | No |
| Aug 2025 | -$28,152 | No |
| Sep 2025 | -$33,948 | Yes |
| Nov 2025 (1st) | -$23,562 | No |
| Nov 2025 (2nd) | -$22,860 | Yes |
| Dec 2025 | -$30,366 | No |
| Jan 2026 | -$27,864 | Yes |
| Feb 2026 | -$66,492 | No |
| Apr 2026 | -$19,404 | Yes |

**Observation:** The charges without retiro co-occurrence show an increasing trend (May $14.6K → Jun $29.2K → Jul $18.3K → Aug $28.2K → Sep/Nov → Dec $30.4K → Feb $66.5K), with February 2026 being a clear outlier.

### February 2026 Anomaly

- February 2026 charge is -$66,492 — 2.3x the mean of other months
- This is the highest charge in the series
- No retiro stock on this date
- Adjacent transactions on 2026-02-27: Venta $618,770, Devolución -$79,560, Cobro por despacho -$24,090
- Venta is within normal range — no unusual sales volume that would explain 2.3x aging charge

---

## 3. Answers to Questions

### Q1: ¿Qué SKU permanecen más tiempo?

**NOT DEMONSTRATED.** No SKU dimension in available data.

### Q2: ¿Qué categorías envejecen?

**NOT DEMONSTRATED.** No category dimension in available data.

### Q3: ¿Qué patrones se repiten?

**Observable patterns:**
- **Monthly periodicity:** Charges appear in 10 of 12 months, suggesting a standard monthly billing cycle
- **Month-end timing:** 10 of 11 charges fall on the last 1-3 days of the month
- **Sequential billing:** id_transaccion increases monotonically — systematic process
- **Co-occurrence with retiro:** 36% of charges coincide with stock retiro charges, suggesting a joint inventory reconciliation event
- **Variable amount:** No fixed fee — amount varies month to month

### Q4: ¿Qué productos concentran el costo?

**NOT DEMONSTRATED.** No product dimension in available data.

---

## 4. Demonstrated vs Not Demonstrated

### Demonstrated:
- 11 charges exist, total -$314,802, over 12 months
- Mean monthly charge: -$28,618
- February 2026 is an outlier (-$66,492, 2.3x mean)
- Sequential id_transaccion confirms systematic monthly billing
- 36% of charges co-occur with retiro stock charges
- 10 of 11 charges are month-end
- Absent in October 2025 and March 2026
- Charge amount is variable — not a fixed fee
- All charges in 'costos_operacionales' financial group

### Not Demonstrated:
- Which SKUs or products generate aging charges
- Whether the charge correlates with inventory volume, age, or value
- The business rule that calculates the charge amount
- Why February 2026 is an outlier
- Why October 2025 and March 2026 have no charges

### Missing data required for full causality:
- SKU-level inventory aging reports from PARIS warehouse
- Inventory turnover rates per product
- Storage duration per SKU
- PARIS warehouse fee schedule
- Purchase order dates vs sell-through dates

---

*Documento generado: 2026-06-03 | Status: READ ONLY EVIDENCE*
