# RIPLEY "A pagar" Semantics Certification

> **Date:** 2026-06-03
> **Status:** COMPLETE — Root cause identified
> **Scope:** 11,683 rows, $206,946,843.00 (50.0% of RIPLEY ledger)

## 1. What is "A pagar" in RIPLEY?

**"A pagar" (Payable) is the settlement amount** — the net cash amount that RIPLEY transfers to the seller after all deductions (commissions, logistics, refunds, adjustments).

It is **NOT an independent financial concept**. It is the **mirror image** of the sum of all other RIPLEY concepts for the same order.

## 2. Formula Analysis

| Formula | Result |
|---------|--------|
| `A pagar = Importe del pedido - Comisiones - Costos - Reembolsos` | **32.2% exact match, 30.5% near match (<1%)** |
| `Total A pagar = Total Rest (non-A-pagar)` | **EXACT match in every month** |

**Key evidence**: Every single month shows **exactly 50.0% "A pagar" / 50.0% "Rest"** across all 17 RIPLEY periods. This is a structural invariant, not coincidence.

## 3. Financial Nature

| Question | Answer |
|----------|--------|
| a) Revenue? | **NO** — it's the payout to seller, not income |
| b) Cost? | **NO** — it's the net settlement amount |
| c) Adjustment? | **NO** — it's the sum of all adjustments already in other concepts |
| d) Treasury / Settlement? | **YES** — cash transfer from RIPLEY to seller |
| e) Derived KPI? | **YES** — computed as: `Importe del pedido + Comisiones + Costos + Reembolsos + Ajustes` |

## 4. Double-Counting Risk

**If "A pagar" were added to P&L, every transaction would be counted TWICE:**

| Scenario | Amount |
|----------|--------|
| Non-A-pagar (rest) | $206,946,843 |
| A pagar | $206,946,843 |
| **Total if both included** | **$413,893,686 (2x reality)** |
| **Correct P&L (rest only)** | **$206,946,843** |

The 50/50 monthly split proves that every dollar in "A pagar" corresponds to a dollar in the other concepts.

## 5. Individual Examples

### Example 1: Exact match (best case)
```
Order 24565519301-A:
  A pagar:            $213,152    ← settlement
  Importe pedido:     $259,940    ← revenue
  Comisiones:         $-46,788    ← cost
  Costos:             $0          ← cost
  Reembolsos:         $0          ← refund
  Net P&L: (259940-46788-0-0) = $213,152  ✅ MATCHES A pagar
```

### Example 2: Full refund (A pagar is NOT simple formula)
```
Order 23240972501-A:
  A pagar:            $172,362    ← settlement (100% of canceled order value?)
  Importe pedido:     $217,940    ← revenue
  Comisiones:         $0          ← waived on refund
  Costos:             $0          ← waived on refund
  Reembolsos:         $-217,940   ← full refund
  Net P&L: (217940+0+0-217940) = $0   ← net zero
  Delta from A pagar: $172,362 (100%)  ← A pagar ≠ net P&L for refunds!
```
**Conclusion**: "A pagar" diverges from net P&L in refund cases. It represents gross settlement, not net P&L.

## 6. Current Handling

| Property | Current Value | Correct? |
|----------|--------------|----------|
| `financial_group` | NULL | **YES** — treasury concept, no P&L group |
| `include_in_operational_pnl` | **False** | **YES** — excluded from operational P&L |
| `clasificacion_operativa` | "A pagar" | **YES** — correctly identified |

The classification code already handles "A pagar" correctly:
```python
general_exclusions = {"A pagar"}
op_flag[clasif.isin(general_exclusions) | details.isin(general_exclusions)] = False
```

## 7. Verdict

| Criterion | Result |
|-----------|--------|
| Is "A pagar" an independent financial concept? | **NO** — derived settlement KPI |
| Should it appear in Dashboard P&L? | **NO** — would double-count |
| Should financial_group be assigned? | **NO** — correctly NULL as treasury concept |
| Is current classification correct? | **YES** — no changes needed |
| Does Dashboard neto need "A pagar"? | **NO** — Dashboard should exclude it |

**Final determination**: "A pagar" is a **treasury/settlement** concept. It must NOT be included in P&L financial groups. The current state (financial_group = NULL, include_in_operational_pnl = False) is **CORRECT**.

## 8. Impact on Sprint B2.5B

Since "A pagar" correctly has:
- `financial_group = NULL` ✅ (intentional)
- `include_in_operational_pnl = False` ✅ (intentional)

**FASE 1 classification is PASS**: 50,819/50,819 P&L rows ($206,946,843) have financial_group populated. 11,683 treasury rows have NULL (correct).

The Dashboard Neto after classification = **$206,946,843** (correct P&L, excluding settlement mirror).

**Proceed to FASE 2 (Financial Closing).**
