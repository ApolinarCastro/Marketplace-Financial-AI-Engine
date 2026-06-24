# AJUSTES & RETENCIONES ROOT CAUSE

**Status:** FAIL
**Date:** 2026-06-06
**Scope:** ML only (0% adjustments in PARIS, RIPLEY, FALABELLA)

---

## Root Cause: Missing `include_in_operational_pnl` Filter in Closing SQL

**The `run_classification()` correctly marks BPP, Poscobro, and other mechanisms as `include_in_operational_pnl = FALSE`. But `run_financial_closing()` NEVER filters by this flag.**

The closing SQL sums ALL classified rows regardless of the flag.

---

## Evidence

### Step 1: Classification correctly identifies mechanisms

In `marketplace_auditor.py:412-437`:
```python
ml_mandatory_exclusions = {
    "reserve_for_dispute", "Mediación", "bpp_refunded", "repentant_buyer",
    "broken_item_fashion", "bigger_than_expected_fashion",
    "smaller_than_expected_fashion", "reconciled", "AJUSTE POSCOBRO",
    "cashback", "cashback_cancel",
    "Reserva para devolución en envío BBP", "Retenciones & Provisiones"
}
op_flag[ml_mask] = ~is_excluded[ml_mask]
```

### Step 2: Flag is correctly set in DB

```
clasificacion_operativa            financial_group  n_rows      total
Ajuste por Talla/Garantía          ajustes            3,309  98,271,357
Ajuste por Compra Protegida (BPP)  ajustes            3,254  93,999,912
Ajuste Poscobro Conciliado         ajustes            1,244  40,845,693
Ajuste por Arrepentimiento         ajustes              537  15,508,764
Ajuste por Producto Dañado/Vacío   ajustes               82   2,526,279
                                                      ─────  ──────────
Total include_in_operational_pnl = FALSE              8,426 251,152,005
```

### Step 3: Closing SQL ignores the flag

In `marketplace_auditor.py:519-528`:
```python
sql = f"""
    SELECT 
        SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ingresos"])}) THEN monto ELSE 0 END) as total_ingresos,
        SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["devoluciones"])}) THEN monto ELSE 0 END) as total_devoluciones,
        SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_operacionales"])}) THEN monto ELSE 0 END) as total_costos_op,
        SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_comerciales"])}) THEN monto ELSE 0 END) as total_costos_com,
        SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ajustes"])}) THEN monto ELSE 0 END) as total_ajustes
    FROM marketplace_ledger_clasificado_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ?
"""
```

**No `AND include_in_operational_pnl = TRUE` anywhere in the query.**

### Step 4: Net RN Impact

| Metric | Value |
|---|---|
| Total mechanisms (all-time) | $143,236,956 |
| Paired rate | 93.8% |
| Paired mechanisms (removable) | $134,329,264 |
| Standalone mechanisms (preserved) | $8,942,692 |
| RN overstatement (15 months) | **$35,966,011 (4.59%)** |

---

## Mechanism Detail

| detalle (raw) | clasificacion_operativa | financial_group | Rows | Gross Total | Net RN Impact |
|---|---|---|---|---|---|
| bpp_refunded | Ajuste por Compra Protegida (BPP) | ajustes | 3,254 | $93,999,912 | $35,966,011 (total) |
| reconciled | Ajuste Poscobro Conciliado | ajustes | 1,244 | $40,845,693 | included above |
| compensated | Ajuste Poscobro Conciliado | ajustes | 104 | $3,545,575 | included above |
| Ajuste Poscobro | Ajuste Poscobro General | ajustes | 634 | $3,108,659 | included above |
| bpp_covered | Ajuste por Compra Protegida (BPP) | ajustes | 37 | $921,722 | included above |
| (others) | Ajuste Poscobro General | ajustes | 28 | $518,069 | included above |

**Note:** The $35.8M net impact on RN is smaller than the gross mechanism total ($143.2M) because paired entries within the same period partially self-cancel. The 6.2% standalone portion ($8.9M) and temporal misalignment of pairs create the net effect.

---

## Retenciones

**Retenciones are NOT the cause.** Zero retenciones exist in the ledger. The concept `Retenciones & Provisiones` is flagged for exclusion but does not currently carry value.

---

## Verdict

| Certification | Result |
|---|---|
| **Ajustes & Retenciones Root Cause** | **FAIL** — `run_financial_closing()` query at `marketplace_auditor.py:519-528` is missing `AND include_in_operational_pnl = TRUE`. All mechanism rows flow unflagged into RN. |
