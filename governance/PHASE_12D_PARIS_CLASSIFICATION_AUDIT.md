# Phase 12D — PARIS Classification Audit (FIX-11)

**Date:** 2026-06-17  
**Status:** COMPLETED ✅

## Question

Does PARIS have `costos_comerciales` movements? Why does "Comisiones & Comerciales" show $0?

## Finding: PARIS has NO costos_comerciales

PARIS's financial groups in `marketplace_ledger_v1` (YTD, op_pnl=1):

| financial_group | Total |
|----------------|-------|
| ingresos | $112,574,966 |
| costos_operacionales | -$7,355,536 |
| ajustes | -$32,252,676 |

PARIS has NO rows with `financial_group='costos_comerciales'` or `financial_group='comisiones'`. This is consistent with the PARIS 3P business model (DEC-023):

- PARIS operates as a 3P marketplace with 17 sellers
- Cencosud charges sellers via DTE 43 (Liquidación-Factura) — Cencosud is agent, sellers are principals
- The 15% commission is embedded in the P&L spread, not a separate financial line
- All seller charges are classified as `costos_operacionales` (shipping, logistics, adjustments)

## Decision: DO NOT reclassify

Per project constraints: NO modificar clasificación histórica. PARIS's classification is correct for its business model. Instead, the fix (FIX-12) moves `costos_operacionales` into the `ccm` slot at the AGGREGATION level only in the waterfall endpoint. The raw classification remains untouched.

## Verification

After FIX-12, PARIS waterfall:
- cop = $0 (no non-PARIS costos_operacionales, and PARIS's own cop is moved to ccm)
- ccm = -$7,355,536 (PARIS's costos_operacionales now correctly shown as marketplace charges)
- Internal conservation: PASS ($0 delta)

## Related Concepts

- Comisiones Marketplace (= costos_operacionales PARIS): -$7,355,536
  - Cobro por despacho, Logística inversa, Retiro stock, Ajuste stock
- Ajustes & Retenciones: -$32,252,676
  - Compensación logística, Ajuste Inventario, Cargo, Cobro por campaña, Merma
