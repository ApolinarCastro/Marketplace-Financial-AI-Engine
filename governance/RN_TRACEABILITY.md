# RN TRACEABILITY

**Status:** PASS (traceability only)
**Date:** 2026-06-06

---

## Complete RN Flow: Raw File → Ledger → Classification → Closing → Cierre

```
01_Raw/{MP}/*.xlsx
    │
    ▼  surgical_loader.py (lines 104-484)
marketplace_ledger_v1
    │  Columns: detalle, monto, financial_group, include_in_operational_pnl
    │
    ▼  marketplace_auditor.py run_classification() (lines 347-512)
marketplace_ledger_clasificado_v1
    │  Columns: clasificacion_operativa, financial_group, confianza
    │
    ▼  marketplace_auditor.py run_financial_closing() (lines 514-557)
marketplace_cierre_financiero_v1
    │  Columns: resultado_neto, total_ingresos, total_costos_*, total_ajustes
    │
    ▼  API v4 / Dashboard
    resultado_neto
```

---

## Exact SQL: RN Calculation (marketplace_auditor.py:519-528)

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

**Source table:** `marketplace_ledger_clasificado_v1`  
**No filter on:** `include_in_operational_pnl`  
**No filter on:** `confianza_clasificacion`  

Then (line 546):
```python
neto = ing + dev + cop + ccm + aju
```

Where `total_ajustes` in the cierre table is (line 554):
```python
total_ajustes = dev + aju  # compatibility: devoluciones + ajustes
```

---

## FINANCIAL_STRUCTURE Dictionary (marketplace_auditor.py:236-317)

The exact mapping from `clasificacion_operativa` → `financial_group`:

### `ingresos` → total_ingresos
`"Cargo por venta"`, `"Cargo por venta (Venta)"`, `"Venta"`, `"Bonificación"`, `"Rebate"`, `"Compensación comercial"`, `"Importe del pedido"`, `"Pago"`, `"Despacho"`, `"Sale amount"`, `"Gross sales"`, `"Pago por precio del producto"`

### `devoluciones` → total_devoluciones
`"Pedidos reembolsados"`, `"Devolución"`, `"Devolución de venta"`, `"Devolución de dinero"`, `"Descuento por devolución de producto"`

### `costos_operacionales` → total_costos_op
`"Cargo por envíos de Mercado Libre"`, `"Cargo por Mercado Envíos"`, `"Gastos de envío pagados por el operador"`, `"Cobro por despacho"`, `"Logística inversa"`, `"Envío"`, etc.

### `costos_comerciales` → total_costos_com
`"Cargo por venta (Comisión)"`, `"Anulación del cargo por venta"`, `"Comisiones sobre pedidos"`, `"Cobro por comisión por venta"`, `"Cargo por campaña de publicidad"`, etc.

### `ajustes` → total_ajustes
`"Ajuste por Compra Protegida (BPP)"`, `"Ajuste Poscobro Conciliado"`, `"Ajuste Poscobro General"`, `"Ajuste por Talla/Garantía"`, `"Ajuste por Arrepentimiento"`, `"Ajuste por Producto Dañado/Vacío"`, `"Mediación"`, `"cashback"`, `"Reserva para devolución en envío BBP"`, etc.

---

## Propagation: Classification → Ledger (marketplace_auditor.py:467-509)

```sql
UPDATE marketplace_ledger_v1
SET clasificacion_operativa = sub.clasificacion_operativa,
    include_in_operational_pnl = sub.include_in_operational_pnl,
    financial_group = CASE sub.clasificacion_operativa
        WHEN 'Cargo por venta (Venta)' THEN 'ingresos'
        WHEN 'Ajuste por Compra Protegida (BPP)' THEN 'ajustes'
        ...  (one WHEN per concepto)
        ELSE NULL
    END
FROM marketplace_ledger_clasificado_v1 sub
WHERE marketplace_ledger_v1.id_transaccion = sub.id_transaccion
  AND marketplace_ledger_v1.detalle = sub.detalle
```

---

## $35.8M Entry Point

Each dollar of the $35.8M enters RN through this exact path:

```
marketplace_ledger_clasificado_v1.monto
  → SUM(CASE WHEN clasificacion_operativa IN ('Ajuste por Compra Protegida (BPP)', ...) THEN monto ELSE 0 END)
  → total_ajustes
  → neto = ing + dev + cop + ccm + aju
  → marketplace_cierre_financiero_v1.resultado_neto
```

The entries that contribute are those where:
- `clasificacion_operativa` ∈ `FINANCIAL_STRUCTURE["ajustes"]` (lines 292-313)
- `include_in_operational_pnl = FALSE` (but NOT filtered out)
- `marketplace = 'ML'`
- Period 2025-01 to 2026-03

---

## Current DB State (ledger_v1)

| Column | Value for $35.8M concepts |
|---|---|
| `marketplace` | ML |
| `detalle` | bpp_refunded, reconciled, Ajuste Poscobro, compensated, etc. |
| `financial_group` | ajustes |
| `include_in_operational_pnl` | FALSE (but ignored by closing SQL) |
| `clasificacion_operativa` | Ajuste por Compra Protegida (BPP) / Ajuste Poscobro Conciliado / etc. |

---

## Verdict

| Certification | Result |
|---|---|
| **RN Traceability** | **PASS** — Complete trace from raw file → ledger → classification → closing → RN. Single root cause identified: missing `include_in_operational_pnl` filter in `run_financial_closing()`. |
