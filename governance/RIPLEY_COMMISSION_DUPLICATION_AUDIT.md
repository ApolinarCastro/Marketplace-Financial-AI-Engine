# RIPLEY Commission Deduplication Audit

## Status: NOT DUPLICATED ✅ (0 shared transaction_ids)

## Question

Are `Comisión` and `Comisión de reembolso` counting the same revenue twice?

## Data

| Detalle | Transaction Count | Total Amount | Financial Group |
|---------|-----------------|-------------|-----------------|
| Comisión | 17,928 | $21,526,642 | comisiones |
| Comisión de reembolso | 3,838 | $4,991,415 | comisiones |

## Verification

**Method:** Counted `id_transaccion` values that appear in BOTH `Comisión` and `Comisión de reembolso`.

**Result: 0 shared transaction_ids.**

## Conclusion

`Comisión` and `Comisión de reembolso` apply to completely different sets of transactions:

- **Comisión** = commission revenue on new sales (17,928 unique transactions)
- **Comisión de reembolso** = commission recovery when a sale is refunded (3,838 unique transactions — these are refunded orders where the original commission is reversed)

No double-counting. Both subcategories belong in `comisiones` financial group and are correctly additive.

**Source:** `marketplace_ledger_v1` (YTD 2026, RIPLEY, signal_mode=SIGNAL)
**Date:** 2026-06-17
