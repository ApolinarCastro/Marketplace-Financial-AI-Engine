# E2.0 — RIPLEY Penalty Feasibility: Root Cause Analysis

**Date:** 2026-06-03  
**Mode:** READ ONLY — evidence only, no inferences

---

## 1. Observable Data

### Source: `marketplace_ledger_v1` WHERE marketplace='RIPLEY' AND detalle IN ('Descuento por cancelación','Otros descuentos')

**Total rows:** 10  
**Total amount:** -$33,440 (negative = Eccsa charges/earns)  
**Date range:** 2025-01-02 to 2026-02-13 (9 distinct dates in 17 months)  
**Financial group:** 10/10 in 'ajustes'

### 2. Observable Patterns

#### Pattern A: "Descuento por cancelación" (5 rows, -$23,490)

| # | Date | Amount | id_transaccion |
|---|---|---|---|
| 1 | 2025-01-26 | -$2,078 | RIP_505930_23282306301-A_descuentoporcancelacion |
| 2 | 2025-03-03 | -$4,998 | RIP_514115_23362907201-A_descuentoporcancelacion |
| 3 | 2025-05-30 | -$11,518 | RIP_526971_23588826701-A_descuentoporcancelacion |
| 4 | 2025-09-12 | -$2,698 | RIP_543422_23886491801-A_descuentoporcancelacion |
| 5 | 2026-02-13 | -$7,198 | RIP_574264_24409274101-A_descuentoporcancelacion |

**Observations:**
- Occurs 5 times across 13 months (Jan, Mar, May, Sep, Feb) — no fixed frequency
- Amounts vary: $2,078 to $11,518 — not a fixed fee
- id_transaccion format: `RIP_{order}_{transaction}-A_descuentoporcancelacion`
- On dates where this occurs, "Importe del pedido" (GMV) is present: $1.15M (Jan 26), $628K (Mar 3), $371K (May 30), $509K (Sep 12), $208K (Feb 13)

#### Pattern B: "Otros descuentos" (5 rows, -$4,950)

| # | Date | Amount | id_transaccion |
|---|---|---|---|
| 1 | 2025-01-02 | -$990 | RIP_500346_23231655401-A_otrosdescuentos |
| 2 | 2025-01-02 | -$990 | RIP_500346_23231314101-A_otrosdescuentos |
| 3 | 2025-06-17 | -$990 | RIP_529315_23699197601-A_otrosdescuentos |
| 4 | 2025-08-04 | -$990 | RIP_535997_23800696002-A_otrosdescuentos |
| 5 | 2025-10-13 | -$990 | RIP_548494_24063005501-A_otrosdescuentos |

**Observations:**
- Amount is EXACTLY -$990 in all 5 cases — identifies a fixed fee
- 2 occurrences on 2025-01-02 (both -$990), suggesting 2 transactions on the same day
- id_transaccion format: `RIP_{order}_{transaction}-A_otrosdescuentos`
- On every date where "Otros descuentos" = -$990 appears, there is a matching pair:
  - "Envío reembolsado" = -$990 (same amount, opposite sign)
  - "Gastos de envío reembolsados pagados por el operador" = +$990
- This establishes: **"Otros descuentos" = $990 fee for processing a shipping refund/return**

---

## 3. Answers to Questions

### Q1: ¿Qué eventos generan actualmente descuentos o penalidades?

**Two observable event types:**

**Event Type 1 — Cancellation (50% of rows, 70% of value):**
- Recorded as "Descuento por cancelación"
- 5 occurrences in 13 months
- Amounts: $2,078 to $11,518 each
- Total: -$23,490
- id_transaccion format shows order-specific reference

**Event Type 2 — Shipping refund processing fee (50% of rows, 15% of value):**
- Recorded as "Otros descuentos"
- Fixed at -$990 per occurrence
- 5 occurrences over 11 months
- Total: -$4,950
- ALWAYS pairs with identical -$990 "Envío reembolsado" and +$990 "Gastos de envío reembolsados pagados por el operador"
- Conclusion: This is a processing fee for shipping refunds, not a seller penalty

### Q2: ¿Qué vendedores concentran esos eventos?

**NOT DEMONSTRATED.** The `marketplace_ledger_v1` schema does not contain seller ID or seller name columns. Cannot determine seller concentration from available data.

### Q3: ¿Qué categorías concentran esos eventos?

**NOT DEMONSTRATED.** The `marketplace_ledger_v1` schema does not contain product category or product ID columns. Cannot determine category concentration from available data.

### Q4: ¿Qué órdenes originan esos descuentos?

**Partially traceable.** The `id_transaccion` field contains order identifiers:

For "Descuento por cancelación" (example):
- `RIP_505930_23282306301-A_descuentoporcancelacion`
- Order segment: `_505930_` and transaction `_23282306301`

For "Otros descuentos" (example):
- `RIP_500346_23231655401-A_otrosdescuentos`
- Order segment: `_500346_` and transaction `_23231655401`

The order reference is encoded but there is no linked table to resolve order attributes (status, items, value, seller, customer).

### Q5: ¿Qué comportamiento observable los genera?

**Observable behavior for "Descuento por cancelación":**
- Event: An order was cancelled by someone (seller or buyer) after purchase
- Evidence: The charge is labeled "cancelación" and has a specific order reference
- Amount variability ($2K-$11.5K) suggests proportional to order value
- Cannot determine whether cancellation was seller-initiated or buyer-initiated

**Observable behavior for "Otros descuentos":**
- Event: A shipping refund was processed
- Evidence: Perfect correlation with "Envío reembolsado" = -$990 and "Gastos de envío reembolsados pagados por el operador" = +$990
- Amount: Fixed at $990 per occurrence — consistent with a processing/admin fee
- This is NOT a seller penalty — it's a transaction fee for handling returns

---

## 4. Demonstrated vs Not Demonstrated

### Demonstrated:
- There are exactly 2 types of penalty-like events in RIPLEY data
- "Descuento por cancelación" is an order cancellation charge, variable amount
- "Otros descuentos" is a fixed -$990 shipping refund processing fee, not a penalty
- Both are recorded in 'ajustes' financial group
- Total: 10 transactions over 17 months
- "Otros descuentos" is always $990 — this is deterministic
- The id_transaccion references specific orders

### Not Demonstrated:
- Whether cancellations are seller fault or buyer fault (not in data)
- Whether there are violations WITHOUT corresponding penalties (no delivery SLA data)
- What seller or category generates cancellations (no seller/category dimension)
- Whether $33,440 is too low or too high (no benchmark allowed)
- Whether the cancellation rate is normal or abnormal (no context data)

### Missing data required for full causality:
- Seller ID per transaction
- Order status table (cancelled vs delivered vs returned)
- Delivery timestamps (on-time vs late)
- Product category per order
- Customer complaint data

---

*Documento generado: 2026-06-03 | Status: READ ONLY EVIDENCE*
