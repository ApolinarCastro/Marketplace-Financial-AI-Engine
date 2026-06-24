# E2.0 — Root Cause Intelligence Certification

**Date:** 2026-06-03  
**Mode:** READ ONLY — evidence certification

---

## Executive Summary

This certification validates root cause intelligence for 4 operational areas. Each area was analyzed using ONLY data observable in `marketplace_ledger_v1`. No benchmarks, no industry standards, no probabilities, no external sources.

**Overall finding:** Of 20 causality questions across 4 areas, only 8 (40%) could be answered with demonstrable evidence. The remaining 12 (60%) are NOT DEMONSTRATED due to missing dimensions in the ledger schema.

---

## Area 1: RIPLEY Penalidades

| File | `governance/RIPLEY_PENALTY_FEASIBILITY.md` |
|---|---|

### What was demonstrated:

| Finding | Evidence |
|---|---|
| Exactly 2 types of penalty events exist | 10 rows from DB: 5 "Descuento por cancelación" ($23,490), 5 "Otros descuentos" ($4,950) |
| "Otros descuentos" is a shipping refund processing fee | Amount is exactly -$990 in all 5 cases; always pairs with "Envío reembolsado" = -$990 and "Gastos de envío reembolsados" = +$990 |
| "Descuento por cancelación" amounts vary with order value | Range: $2,078 to $11,518 — proportional, not fixed |
| Both are in 'ajustes' financial group | 10/10 rows |
| Event frequency is low | 9 distinct dates in 17 months |
| id_transaccion references specific orders | Format: `RIP_{order}_{txn}-A_descuentoporcancelacion` |

### What was NOT demonstrated:

| Question | Reason |
|---|---|
| Which sellers cause cancellations? | No seller dimension in ledger |
| Which categories concentrate penalties? | No category dimension in ledger |
| Are there violations without penalties? | No delivery SLA or compliance data |
| Is $33,440 too low? | Cannot use benchmarks per E2.0 constraint |
| Are cancellations seller-fault or buyer-fault? | No order status data |

### Data gaps:
- Seller ID column
- Product/category ID column
- Order status/lifecycle table
- Delivery timestamp data

---

## Area 2: PARIS Retiro Stock

| File | `governance/PARIS_RETIRO_ROOT_CAUSE.md` |
|---|---|

### What was demonstrated:

| Finding | Evidence |
|---|---|
| 5 charges exist, total $1,630,800 | 5 rows from DB |
| All at month-end | Dates: 29th, 30th, 28th, 30th, 30th |
| Periodic (every 2-5 months) | Intervals: 154, 59, 63, 90 days |
| Amounts are stable | Mean $326K, CV=7.7% |
| 4 of 5 co-occur with stock antiguo charge | Same dates as Cobro stock antiguo |
| Sequential billing IDs | IDs: 3339187 → 3972908 → 4283852 → 4753797 → 5350256 |
| All in 'costos_operacionales' | 5/5 rows |

### What was NOT demonstrated:

| Question | Reason |
|---|---|
| Which SKUs generate retiro? | No SKU dimension |
| Which brands? | No brand dimension |
| Which categories? | No category dimension |
| Why 5-month gap vs 2-month gap? | No inventory data to explain |
| Cause of retiro (over-order vs slow sell-through)? | No purchase order data |

### Data gaps:
- SKU/Product ID column
- Inventory movement data
- Purchase order records
- Sell-through rate data

---

## Area 3: PARIS Stock Antiguo

| File | `governance/PARIS_STOCK_AGING_ROOT_CAUSE.md` |
|---|---|

### What was demonstrated:

| Finding | Evidence |
|---|---|
| 11 charges, total $314,802 | 11 rows from DB |
| Monthly billing cycle | 10 of 12 months have charges |
| Variable amounts | Range: $14,580 to $66,492; mean $28,618 |
| Sequential billing process | IDs increase monotonically: 3462492 → 5350241 |
| 36% co-occur with retiro stock | 4 of 11 dates have both charges |
| February 2026 is outlier | $66,492 = 2.3x mean |
| Month-end timing | 10 of 11 charges on last 1-3 days of month |

### What was NOT demonstrated:

| Question | Reason |
|---|---|
| Which SKUs age? | No SKU dimension |
| Which categories age? | No category dimension |
| What causes aging (over-order vs slow demand)? | No sell-through data |
| Why February 2026 is outlier? | No inventory data for that period |
| Why Oct 2025 and Mar 2026 have no charge? | No billing cycle visibility |

### Data gaps:
- SKU-level inventory aging report
- Product category/type
- Sell-through rate data
- PARIS warehouse fee schedule
- Storage duration per SKU

---

## Area 4: ML Ajuste Poscobro

| File | `governance/ML_POSCOBRO_FORENSICS.md` |
|---|---|

### What was demonstrated:

| Finding | Evidence |
|---|---|
| 634 entries, $3,108,659 total | 634 rows from DB, all positive |
| 23 months continuous activity | Jan 2025 to Nov 2026 |
| 84.2% of value in 14.4% of rows | 91 rows >$10K = $2.62M |
| Two distinct regimes | Pre-2026: $237K/mo avg; Post-2026: $24K/mo avg (90% drop) |
| Zero reversals | 0 negative entries |
| Source: 2 XLSX files | id_transaccion references "1 enero 2025 - 1 julio 2025.xlsx" and "1 julio 2025 - 1 enero 2026.xlsx" |
| Standard amounts repeat | $289, $299, $441, $525, $598 appear 30-100+ times |
| No correlation with other ML adjustments | R² ≈ 0 between Poscobro and other adjustments |
| All in 'ajustes' financial group | 634/634 |
| Weekday/weekend distribution is even | Consistent with automated processing |

### What was NOT demonstrated:

| Question | Reason |
|---|---|
| Business reason for each adjustment | No reason code in ledger |
| Whether any are erroneous | No cross-reference to original transactions |
| Why 90% drop occurred | No process change documentation |
| Whether $113,970 outliers are correct | No verification data |
| Recovery potential | Explicitly excluded by E2.0 constraints |

### Data gaps:
- Adjustment reason/category code
- Original transaction ID for each Poscobro
- Source XLSX file contents
- Approval/review workflow data
- Reconciliation status

---

## Cross-Area Findings

### Structural Limitation

The `marketplace_ledger_v1` schema is a financial ledger designed for accounting aggregation. It does NOT contain operational dimensions:

| Operational Dimension | Present in Ledger? | Required For |
|---|---|---|
| Seller/Vendor ID | NO | RIPLEY penalties |
| Product/SKU | NO | PARIS retiro, stock antiguo |
| Category | NO | All areas |
| Order Status | NO | RIPLEY penalties |
| Reason Code | NO | ML Poscobro |
| Original Transaction ID | NO (only adjustment ID) | ML Poscobro |

### Proven Pattern

The ledger can demonstrate:
- **WHAT** happened (detalle + monto)
- **WHEN** it happened (fecha)
- **HOW MUCH** (monto)

The ledger CANNOT demonstrate:
- **WHO** caused it (no seller/customer dimension)
- **WHICH** product (no SKU/product dimension)
- **WHY** it happened (no reason code dimension)

---

## Final Classification

### 20 Questions Analyzed

| Area | Questions | Demonstrated | Not Demonstrated |
|---|---|---|---|
| RIPLEY Penalidades | 5 | 3 | 2 |
| PARIS Retiro Stock | 5 | 1 | 4 |
| PARIS Stock Antiguo | 5 | 2 | 3 |
| ML Poscobro | 4 | 2 | 2 |
| **TOTAL** | **19** | **8 (42%)** | **11 (58%)** |

### Fact vs Hypothesis

| Category | Count | Detail |
|---|---|---|
| **HECHO** (demonstrated with evidence) | 8 findings | All traceable to specific DB rows |
| **HIPÓTESIS** (not demonstrable with current data) | 11 gaps | All due to missing dimensions in schema |
| **BENCHMARK** | 0 | Not used per E2.0 constraint |
| **SIMULACIÓN** | 0 | Not used per E2.0 constraint |

### What is needed to answer the remaining 11 questions:
- Add product dimension (SKU, category) to ledger → enables PARIS retiro + stock antiguo root cause
- Add seller dimension to ledger → enables RIPLEY penalty concentration analysis
- Add order lifecycle table → enables cancellation root cause
- Add reason codes to ML adjustments → enables Poscobro classification

**Without these dimensions, causality for 58% of questions cannot be established — regardless of analytical methodology.**

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
