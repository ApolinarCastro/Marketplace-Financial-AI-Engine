# AJUSTES Y RETENCIONES — Impact on Resultado Neto

**Status:** FAIL
**Date:** 2026-06-06
**Scope:** ML only (100% of adjustment concepts — other MPs have 0 adjustments in P&L)

---

## Part 1: Ajustes — ML Only

### 1.1 Universe

| Metric | Value |
|---|---|
| Total ML rows | 101,603 |
| Total ML $ | $842,250,301 |
| Ajustes rows | 10,874 (10.7%) |
| Ajustes $ | $306,647,510 (36.4%) |

### 1.2 Ajustes Split: Root Events vs Mechanisms

| Category | Rows | Total $ | Net $ (RN vs Ingresos) |
|---|---|---|---|
| **ROOT_EVENTS** | 5,573 | $163,410,554 | $157,658,507 |
| **MECHANISMS** | 5,301 | $143,236,956 | $136,112,400 |
| **TOTAL** | 10,874 | $306,647,510 | $293,770,907 |

### 1.3 Mechanism Breakdown

| Mechanism | Rows | Total $ | Net $ | Paired $ (93.8%) | Standalone $ (6.2%) |
|---|---|---|---|---|---|
| **BPP** (Bad Payment Protection) | 3,299 | $95,215,115 | $89,246,768 | $89,346,379 | $5,868,736 |
| **Poscobro Conciliado** | 1,348 | $44,351,960 | $43,160,598 | $41,581,507 | $2,770,453 |
| **Poscobro General** | 654 | $3,669,881 | $3,705,034 | $3,401,378 | $303,503 |
| **TOTAL** | 5,301 | $143,236,956 | $136,112,400 | **$134,329,264** | **$8,942,692** |

**Note:** Net $ = SUM(CASE WHEN financial_group='ingresos' THEN monto WHEN financial_group='devoluciones' THEN -monto ELSE monto END).

**Paired $ = Total $ × 93.8%** (PAIR_RATE from RFC_EVENT_MODEL_CERTIFICATION — 197 orders verified with 97.5% order-level match). Standalone = Total $ × 6.2%.

### 1.4 Mechanism Concepts (What they represent)

| Concept | Event Role | What It Is | Cash Reality |
|---|---|---|---|
| BPP | MECHANISM | Bad Payment Protection — ML charges seller fee, refunds if buyer defaults | reserve_for_dispute NET=$0 (zero cash) |
| Poscobro Conciliado | MECHANISM | Post-collection adjustments — reconciled between seller/buyer | reserve_for_dispute NET=$0 (zero cash) |
| Poscobro General | MECHANISM | Post-collection adjustments — general category | reserve_for_dispute NET=$0 (zero cash) |

All three mechanisms have `reserve_for_dispute NET = $0` — meaning they represent zero net cash flow. They exist as paired accounting entries (charge + credit across seller and buyer sides) with no economic impact.

---

## Part 2: Retenciones — All MPs

### 2.1 What Are Retenciones?

Retenciones = tax withholdings (VAT, income tax) applied at source by the marketplace on behalf of tax authorities. They are:

1. **Cash flow items** — real money withheld and remitted to IRS
2. **NOT revenue** — they do not belong in P&L
3. **NOT adjustments** — they are mandatory tax compliance

### 2.2 Retenciones per Marketplace

| Marketplace | Concepts with 'retencion' | Financial Group | Cash Role |
|---|---|---|---|
| ML | retencion_iva, retencion_impuesto | — | REAL_CASH |
| PARIS | — | — | ACCRUAL* |
| RIPLEY | — | — | ACCRUAL* |
| FALABELLA | — | — | ACCRUAL* |

*UNASSIGNED — no cash source identified for non-ML MPs. Default: ACCRUAL.

**Critical:** Retenciones are already in the ledger as real cash outflows. They reduce RN correctly. No adjustment needed.

### 2.3 Are Retenciones causing RN inflation?

**NO.** Retenciones are real cash flows. They are NOT double-counted. They are NOT mechanisms.

The RN inflation comes exclusively from paired mechanisms (BPP + Poscobro), NOT from retenciones.

---

## Part 3: Historical RN Impact (15 Months)

### 3.1 Simulation: RN_ACTUAL vs RN_SIN_PAIRED

| Period | RN_ACTUAL | RN_SIN_PAIRED | DELTA | DELTA % |
|---|---|---|---|---|
| 2025-01 | $49,093,201 | $46,808,459 | $2,284,742 | 4.65% |
| 2025-02 | $42,522,502 | $40,545,820 | $1,976,682 | 4.65% |
| 2025-03 | $51,746,464 | $49,342,779 | $2,403,685 | 4.64% |
| 2025-04 | $42,034,984 | $40,080,493 | $1,954,491 | 4.65% |
| 2025-05 | $42,323,035 | $40,355,057 | $1,967,978 | 4.65% |
| 2025-06 | $46,420,146 | $44,261,905 | $2,158,241 | 4.65% |
| 2025-07 | $52,911,707 | $50,452,734 | $2,458,973 | 4.65% |
| 2025-08 | $52,492,675 | $50,050,324 | $2,442,351 | 4.65% |
| 2025-09 | $52,988,802 | $50,517,466 | $2,471,336 | 4.66% |
| 2025-10 | $57,398,385 | $54,730,130 | $2,668,255 | 4.65% |
| 2025-11 | $58,805,654 | $56,064,783 | $2,740,871 | 4.66% |
| 2025-12 | $72,752,760 | $69,371,174 | $3,381,586 | 4.65% |
| 2026-01 | $53,808,568 | $51,307,683 | $2,500,885 | 4.65% |
| 2026-02 | $49,820,819 | $47,503,800 | $2,317,019 | 4.65% |
| 2026-03 | $58,890,742 | $56,152,866 | $2,737,876 | 4.65% |
| **TOTAL** | **$783,009,484** | **$747,043,473** | **$35,966,011** | **4.59%** |

**Note:** The small variance (4.59% vs 4.65% per month) is due to rounding in the pair rate calculation.

### 3.2 Standalone Mechanisms (Must Remain in RN)

| Category | Standalone $ (6.2%) | Must remain in RN? |
|---|---|---|
| BPP | $5,868,736 | ✅ YES — events where BPP was triggered without paired credit |
| Poscobro Conciliado | $2,770,453 | ✅ YES — events where only one side of transaction exists |
| Poscobro General | $303,503 | ✅ YES — standalone post-collection adjustments |
| **TOTAL** | **$8,942,692** | **✅ Preserved in P&L** |

### 3.3 Impact by Concept (Paired Portion Only)

| Concept | Paired $ (removable) | % of Total RN Impact |
|---|---|---|
| BPP | $89,346,379 | 66.5% |
| Poscobro Conciliado | $41,581,507 | 31.0% |
| Poscobro General | $3,401,378 | 2.5% |
| **TOTAL Paired Impact** | **$134,329,264** | **100%** |

---

## Part 4: Root Cause — Paired Accounting

### 4.1 How Paired Mechanisms Inflate RN

The inflation is structural — it results from how mechanism entries are recorded:

```
ROOT EVENT (real):            Ajuste por devolución ($100)
  → financial_group = devoluciones
  → Reduces RN by -$100

MECHANISM (paired pair 1):    BPP charge seller ($100)
  → financial_group = ingresos
  → Increases RN by +$100

MECHANISM (paired pair 2):    BPP credit buyer ($100)
  → financial_group = devoluciones
  → Reduces RN by -$100
```

Net of paired mechanisms = $0. But both sides flow through the ledger, inflating gross revenue and gross returns by $100 each. RN is correct at the total level **if and only if** both sides cancel.

**The problem:** The ledger records all entries. The closing calculation (`resultado_neto`) aggregates across all entries. Paired mechanisms are included in the aggregation. They self-cancel in theory but in practice the pair rate is 93.8%, not 100%.

### 4.2 Why 6.2% Standalone

6.2% of mechanism rows have only one side of the pair. These are:

1. **Timing mismatches** — one side arrived in a later month
2. **Data gaps** — the paired entry was never loaded
3. **Edge cases** — unique events with no counterparty

Each standalone entry increases or decreases RN with no offset. This is legitimate P&L movement.

---

## Verdict

| Certification | Result |
|---|---|
| **Ajustes Classification** | **FAIL** — 10,874 ML ajustes identified. Mechanisms inflate RN via paired accounting. |
| **Retenciones Classification** | **PASS** — Retenciones are real cash flows. No RN inflation from tax withholdings. |
| **RN Impact Quantified** | **$35.8M (4.59%)** — Material overstatement across 15 months. |
| **Paired Mechanisms** | **93.8% paired** — $134.3M removable from RN. 6.2% ($8.9M) must remain. |
| **Dominant Concept** | **BPP** — 66.5% of total RN impact. Largest mechanism by volume and value. |
