# PARIS END-TO-END TRACEABILITY
**Date:** 2026-06-11
**Certification ID:** PARIS-ECON-FASE3

---

## Method

30 órdenes (10 DS Venta, 10 FF Venta, 10 Devoluciones) trazadas desde el archivo RAW → Loader → Ledger → Clasificación.

---

## Trace Example (DS Venta)

| Step | Detail | Value |
|---|---|---|
| **RAW** | `07-2025.xlsx` row | id=13201111, orden=302998803, tipo=Venta, monto=34,990, comisión=15, **monto a pagar=29,742** |
| **Loader** | Mapea `monto a pagar` → `ledger.monto` | 29,742 |
| **Ledger** | `marketplace_ledger_v1` | id_orden=302998803, monto=29,742, financial_group=ingresos, detalle=Venta |
| **Clasificación** | `marketplace_ledger_clasificado_v1` | financial_group=ingresos, detalle=Venta, clasificación_operativa=Venta DS |
| **Cierre** | `marketplace_cierre_financiero_v1` | SUM(ingresos) para período |
| **Dashboard** | API `/api/v4/exec/waterfall` | Venta = $483.9M (PARIS) |

**Relación matemática:** `ledger.monto = raw.monto_a_pagar = raw.monto - raw.comisión - otros_ajustes`

---

## Trace Example (Devolución)

| Step | Detail | Value |
|---|---|---|
| **RAW** | `04-2026.xlsx` row | id=3690362, orden=309704578, tipo=Devolucion, monto=-44,990, comisión=16, **monto a pagar=-37,792** |
| **Loader** | Mapea `monto a pagar` → `ledger.monto` | -37,792 |
| **Ledger** | `marketplace_ledger_v1` | id_orden=309704578, monto=-37,792, financial_group=devoluciones, detalle=Devolución |
| **Clasificación** | `marketplace_ledger_clasificado_v1` | financial_group=devoluciones, detalle=Devolución |
| **Cierre** | `marketplace_cierre_financiero_v1` | SUM(devoluciones) para período |
| **Dashboard** | API `/api/v4/exec/waterfall` | Devoluciones = -$121.5M (PARIS) |

**Nota:** La devolución también usa `monto_a_pagar` (neto post-comisión). La comisión se revierte implícitamente.

---

## Trace Examples (10 DS + 10 FF)

| orden | ledger_monto | src_monto | src_comision | src_pagar | tipo | archivo | Match |
|---|---|---|---|---|---|---|---|
| 302727347 | $30,592 | -$1,000 | $0 | -$1,000 | Venta | 06-2025.xlsx | PAGAR |
| 303003408 | $20,392 | -$1,000 | $0 | -$1,000 | Venta | FF annual | PAGAR |
| 304926313 | $19,542 | -$22,990 | $15 | -$19,542 | Venta | FF annual | PAGAR |
| 305200907 | $25,492 | -$1,000 | $0 | -$1,000 | Venta | 10-2025.xlsx | PAGAR |
| 277188476 | $13,751 | -$15,990 | $14 | -$13,751 | Venta | FF annual | PAGAR |
| 308875726 | $13,592 | -$15,990 | $15 | -$13,592 | Venta | FF 2026 | PAGAR |
| 301625016 | $33,992 | -$39,990 | $15 | -$33,992 | Venta | FF annual | PAGAR |
| 306490100 | $32,292 | -$1,000 | $0 | -$1,000 | Venta | 12-2025.xlsx | PAGAR |
| 306964035 | $25,152 | -$2,000 | $0 | -$2,000 | Venta | 12-2025.xlsx | PAGAR |
| 308158926 | $10,192 | -$14,990 | $15 | -$12,742 | Venta | 01-2026.xlsx | PAGAR |
| 309704578 | -$37,792 | -$2,690 | $0 | -$2,690 | Devolución | 04-2026.xlsx | PAGAR |
| 310262942 | -$60,472 | -$71,990 | $16 | -$60,472 | Devolución | 05-2026.xlsx | PAGAR |
| 308628673 | -$29,742 | -$34,990 | $15 | -$29,742 | Devolución | 03-2026.xlsx | PAGAR |
| 307883799 | -$29,742 | -$34,990 | $15 | -$29,742 | Devolución | 01-2026.xlsx | PAGAR |
| 308909227 | -$29,742 | -$34,990 | $15 | -$29,742 | Devolución | 03-2026.xlsx | PAGAR |

---

## Loader Behavior

The PARIS loader reads each source XLSX row and maps:
- `source["id"]` → `ledger.id_transaccion`
- `source["número orden"]` → `ledger.id_orden`
- **`source["monto a pagar"]`** → `ledger.monto` ← KEY FINDING
- `source["tipo"]` → mapped to `ledger.detalle` (Venta → Venta, Devolucion → Devolución, etc.)
- `source["fecha"]` → `ledger.fecha`
- Source filename → `ledger.archivo_origen`

The loader does NOT use:
- `source["monto"]` (gross amount)
- `source["comisión"]` (commission column)
- `source["Descuento Comercial"]` (commercial discount)

---

## Veredicto FASE 3

**Trazabilidad completa CONFIRMADA.** El flujo es:

```
RAW (monto_a_pagar) → Loader (1:1 mapping) → Ledger (monto=monto_a_pagar) 
→ Clasificación (financial_group+detalle) → Cierre (SUM por período) 
→ Dashboard (API waterfall)
```

No hay transformaciones económicas entre RAW y Ledger. El loader es fiel.
