# E2.0 — PARIS Retiro Stock: Root Cause Analysis

**Date:** 2026-06-03  
**Mode:** READ ONLY — evidence only, no inferences

---

## 1. Observable Data

### Source: `marketplace_ledger_v1` WHERE marketplace='PARIS' AND detalle='Retiro stock bodega Paris'

**Total rows:** 5  
**Total amount:** -$1,630,800 (negative = Eccsa pays cost)  
**Date range:** 2025-04-29 to 2026-04-30  
**Financial group:** 5/5 in 'costos_operacionales'

### All Rows

| # | Date | Amount | id_transaccion |
|---|---|---|---|
| 1 | 2025-04-29 | -$336,600 | 3339187 |
| 2 | 2025-09-30 | -$328,500 | 3972908 |
| 3 | 2025-11-28 | -$326,400 | 4283852 |
| 4 | 2026-01-30 | -$285,000 | 4753797 |
| 5 | 2026-04-30 | -$354,300 | 5350256 |

---

## 2. Observable Patterns

### Temporal Pattern

| Charge | Date | Days since previous | Day of month |
|---|---|---|---|
| 1 | 2025-04-29 | — | 29th (end of month) |
| 2 | 2025-09-30 | 154 days (5 months) | 30th (end of month) |
| 3 | 2025-11-28 | 59 days (2 months) | 28th (end of month) |
| 4 | 2026-01-30 | 63 days (2 months) | 30th (end of month) |
| 5 | 2026-04-30 | 90 days (3 months) | 30th (end of month) |

**Observation:** Not monthly. Frequency varies: 2, 3, or 5 months between charges. Always on the last business day of the month (29th, 28th, or 30th).

### Amount Pattern

| Charge | Amount |
|---|---|
| 1 | -$336,600 |
| 2 | -$328,500 |
| 3 | -$326,400 |
| 4 | -$285,000 |
| 5 | -$354,300 |

**Observation:** Amounts are similar but not identical: $285K to $354K range. Mean: $326,160. Standard deviation: ~$25,000. Coefficient of variation: 7.7% — relatively stable.

### Adjacent Transactions

On each retiro date, normal PARIS operations occur:

| Date | Venta (total) | Devolución | Other notable items |
|---|---|---|---|
| 2025-04-29 | $1,203,604 | -$77,980 | Logística inversa -$8,070 |
| 2025-09-30 | $874,730 | -$296,940 | Cobro stock antiguo: -$33,948 (same day) |
| 2025-11-28 | $5,058,884 | -$124,950 | Cobro stock antiguo: -$22,860 (same day) |
| 2026-01-30 | $517,810 | -$381,440 | Cobro stock antiguo: -$27,864 (same day) |
| 2026-04-30 | $696,780 | -$175,950 | Cobro stock antiguo: -$19,404 (same day) |

**Critical observation:** On 4 out of 5 retiro dates (Sep, Nov, Jan, Apr), "Cobro stock antiguo" also occurs. This establishes a relationship: **stock retiro and stock aging charges co-occur on the same dates.**

### id_transaccion Pattern

IDs: 3339187, 3972908, 4283852, 4753797, 5350256

**Observation:** Sequential integers. Not linked to specific products or orders. Appears to be a systematic billing reference, not an order-specific identifier.

---

## 3. Answers to Questions

### Q1: ¿Qué SKU generan retiro?

**NOT DEMONSTRATED.** The `marketplace_ledger_v1` schema does not contain SKU columns. Each row is a flat amount with no product-level breakdown.

### Q2: ¿Qué marcas generan retiro?

**NOT DEMONSTRATED.** No brand dimension in available data.

### Q3: ¿Qué categorías generan retiro?

**NOT DEMONSTRATED.** No category dimension in available data.

### Q4: ¿Qué porcentaje se repite?

**Repetition analysis:**
- 5 charges over a 12-month period (2025-04 to 2026-04)
- Average interval: 3.0 months between charges
- Minimum interval: 2 months
- Maximum interval: 5 months
- Charges appear recurrently but not with fixed periodicity

**Pattern hypothesis (based on observable data only):**
- The charge may be triggered by an inventory threshold or a periodic audit
- Always at month end
- Amount relatively stable ($285K-$354K range)

### Q5: ¿Existe concentración?

**NOT DEMONSTRATED.** 5 data points is insufficient to establish concentration. The average charge is $326,160 with moderate variation (CV=7.7%).

---

## 4. Demonstrated vs Not Demonstrated

### Demonstrated:
- 5 retiro stock charges exist in the DB, total -$1,630,800
- All charges occur at month-end dates (28th-30th)
- Charges are periodic (every 2-5 months), not monthly
- All in 'costos_operacionales' financial group
- Retiro stock and stock antiguo charges co-occur on 4 of 5 dates
- Amounts are stable ($285K-$354K), suggesting a formulaic calculation
- id_transaccion is sequential numeric, not product-specific

### Not Demonstrated:
- Which SKUs, brands, or categories cause the retiro
- Why 2025-04-29 and 2025-09-30 have 5 months apart vs 2 months thereafter
- Whether retiros are caused by over-ordering, slow sell-through, or seasonal returns
- Whether the charge is a fixed fee or proportional to inventory volume
- The formula or business rule that determines the charge amount

### Missing data required for full causality:
- SKU-level inventory movement data
- Purchase orders and reorder decision records
- Sell-through rates per SKU
- Warehouse storage duration per SKU
- Inventory aging reports from PARIS

---

*Documento generado: 2026-06-03 | Status: READ ONLY EVIDENCE*
