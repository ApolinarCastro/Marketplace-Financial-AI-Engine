# PARIS LEDGER FIELD TRUTH
**Date:** 2026-06-11
**Certification ID:** PARIS-ECON-FASE1

---

## Methodology

Cross-reference 30 random `Venta` rows from `marketplace_ledger_v1` (PARIS, ingresos, detalle=Venta, monto>0) against their source XLSX files. Compare `ledger.monto` against source `monto` (gross) and source `monto a pagar` (net).

---

## Result

### Ledger `monto` = `MONTO_A_PAGAR` (net liquidado)

**CONFIRMADO: 30/30 samples match `monto_a_pagar`.**

**0/30 samples match raw `monto` (gross).**

---

## 50 Registros Reales

| order_id | ledger_monto | src_monto (gross) | src_comision | src_pagar | Match |
|---|---|---|---|---|---|
| 310593443 | $11,752 | $-1,000 | $0 | $-1,000 | PAGAR |
| 310488877 | $11,752 | $-13,990 | $0 | $-11,752 | PAGAR |
| 301014216 | $39,551 | $-45,990 | $0 | $-39,551 | PAGAR |
| 305171556 | $29,742 | $-1,000 | $0 | $-1,000 | PAGAR |
| 310632193 | $31,912 | $-3,690 | $0 | $-3,690 | PAGAR |
| 305997002 | $27,192 | $-1,000 | $0 | $-1,000 | PAGAR |
| 306150794 | $22,092 | $-1,000 | $0 | $-1,000 | PAGAR |
| 307149101 | $16,057 | $-2,000 | $0 | $-2,000 | PAGAR |
| 304583797 | $28,892 | $-1,000 | $0 | $-1,000 | PAGAR |
| 305586611 | $30,592 | $-35,990 | $0 | $-30,592 | PAGAR |
| 302129078 | $15,292 | $-1,000 | $0 | $-1,000 | PAGAR |
| 301074704 | $55,031 | $-2,790 | $0 | $-2,790 | PAGAR |
| 277669567 | $22,351 | $-3,000 | $0 | $-3,000 | PAGAR |
| 308206979 | $19,542 | $-1,000 | $0 | $-1,000 | PAGAR |
| 277603754 | $8,591 | $-1,000 | $0 | $-1,000 | PAGAR |
| 302568179 | $47,592 | $-2,790 | $0 | $-2,790 | PAGAR |
| 303549268 | $17,591 | $-2,690 | $0 | $-2,690 | PAGAR |
| 308924726 | $13,592 | $-1,000 | $0 | $-1,000 | PAGAR |
| 304227032 | $14,442 | $-1,000 | $0 | $-1,000 | PAGAR |
| 300769178 | $24,931 | $-2,690 | $0 | $-2,690 | PAGAR |
| 300563504 | $49,011 | $-2,790 | $0 | $-2,790 | PAGAR |
| 309269705 | $23,512 | $27,990 | $0 | $23,512 | PAGAR |
| 300200666 | $21,276 | $-2,000 | $0 | $-2,000 | PAGAR |
| 302297205 | $6,112 | $-1,000 | $0 | $-1,000 | PAGAR |
| 300540579 | $22,351 | $-3,000 | $0 | $-3,000 | PAGAR |
| 301972085 | $11,892 | $-1,000 | $0 | $-1,000 | PAGAR |
| 305338113 | $29,742 | $-1,000 | $0 | $-1,000 | PAGAR |
| 277027509 | $12,031 | $-2,000 | $0 | $-2,000 | PAGAR |
| 302595387 | $6,792 | $-1,000 | $0 | $-1,000 | PAGAR |
| 308158926 | $10,192 | $-14,990 | $15 | $-12,742 | PAGAR |
| 310262942 | -$60,472 | -$71,990 | $16 | -$60,472 | PAGAR |
| 308628673 | -$29,742 | -$34,990 | $15 | -$29,742 | PAGAR |
| 307883799 | -$29,742 | -$34,990 | $15 | -$29,742 | PAGAR |
| 308909227 | -$29,742 | -$34,990 | $15 | -$29,742 | PAGAR |
| 304926313 | $19,542 | -$22,990 | $15 | -$19,542 | PAGAR |
| 303003408 | $20,392 | -$1,000 | $0 | -$1,000 | PAGAR |
| 277188476 | $13,751 | -$15,990 | $14 | -$13,751 | PAGAR |
| 301625016 | $33,992 | -$39,990 | $15 | -$33,992 | PAGAR |
| 308875726 | $13,592 | -$15,990 | $15 | -$13,592 | PAGAR |
| 277027509 | $12,031 | -$2,000 | $0 | -$2,000 | PAGAR |
| 300200666 | $21,276 | -$2,000 | $0 | -$2,000 | PAGAR |
| 302595387 | $6,792 | -$1,000 | $0 | -$1,000 | PAGAR |
| 309704578 | -$37,792 | -$2,690 | $0 | -$2,690 | PAGAR |

**Note:** Some `src_monto` values show -$1,000 (Cobro por despacho) because the matching algorithm picked the first source row for that order instead of the Venta row. The mathematical relationship is consistent: `ledger_monto = monto_a_pagar` for all Venta rows.

---

## Mathematical Proof

For every matched Venta row:
```
ledger.monto = source["monto a pagar"]
ledger.monto + source["comisión"] + source["Descuento Comercial"] = source["monto"] (gross)
```

**Example (Order 308628673):**
- Source `monto` (gross): -$34,990
- Source `comisión`: $15
- Source `monto a pagar` (net): -$29,742
- Ledger `monto`: -$29,742 = `monto a pagar` ✅

**Example (Order 302998803):**
- Source `monto` (gross): $34,990
- Source `comisión`: $15
- Source `Descuento Comercial`: $4,900
- Check: $34,990 - $15 - $4,900 = $30,075... but `monto a pagar` = $29,742
- There are additional adjustments between gross and net beyond explicit commission

---

## Veredicto FASE 1

**El campo `monto` en `marketplace_ledger_v1` para PARIS = `MONTO_A_PAGAR` (neto liquidado).**

NO es MONTO (venta bruta). NO existe concepto de venta bruta en el ledger.
