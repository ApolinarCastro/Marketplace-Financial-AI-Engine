# Certificación: RN Operacional (Fuente Operacional Certificada)
**Fecha:** 2026-06-07
**Status:** PASS ✅

---

## Problema resuelto

El dashboard mostraba `resultado_neto` desde `marketplace_cierre_financiero_v1` sin filtro `include_in_operational_pnl`, resultando en RN visible ≠ RN operacional. El cierre incluye rows paired PosCobro (DEC-019, op_pnl=0), inflando el RN en $4.6M/mes ($94.4M total).

## Solución implementada

### API: `/api/v4/exec/waterfall`

**Antes:** Query híbrido — `ingresos, costos_op, costos_com, total_ajustes, resultado_neto` desde `cierre_financiero_v1` (ALL-rows) + `devoluciones` desde `ledger_v1` (op_pnl=1). Universos mixtos, RN inflado.

**Después:** Query unificado desde `marketplace_ledger_v1` con `COALESCE(include_in_operational_pnl, 1) = 1` en TODOS los componentes:

```
Ingresos (op_pnl=1)
+ Devoluciones (op_pnl=1)
+ Costos Operacionales (op_pnl=1)
+ Costos Comerciales (op_pnl=1)
+ Ajustes (op_pnl=1)
= RN Operacional
```

Misma taxonomía oficial (`financial_group`), mismo filtro, misma fuente.

### Frontend: `dashboard.html`

**Línea 728:** `aju` cambió de `currentDesglose.filter(r => r.categoria==='ajustes')` → `window._cierreCertified.aju` (desde waterfall operacional, misma fuente que ing/dev/cop/ccm).

**Línea 868:** Desglose query ahora usa `exclude_non_operational=true` para TODOS los MPs (incluyendo ML). Antes ML tenía excepción (ALL-rows), ahora todo es consistente.

## Verificación

### ML 2026-01 — Comparación

| Componente | Op P&L (op_pnl=1) | Full (ALL-rows) | Delta |
|---|---|---|---|
| Ingresos | $27,646,200.00 | $27,646,200.00 | $0 |
| Devoluciones | -$4,971,696.00 | -$4,971,696.00 | $0 |
| Costos Op | -$2,075,055.00 | -$2,075,055.00 | $0 |
| Costos Com | -$7,954,836.00 | -$7,954,836.00 | $0 |
| Ajustes | $6,843,255.00 | $11,457,254.50 | $4,613,999.50 |
| **RN** | **$19,487,868.00** | **$24,101,867.50** | **$4,613,999.50** |

**Delta = paired PosCobro (3,663 rows, DEC-019).** RN operacional EXCLUYE paired PosCobro. RN full los INCLUYE. Ambos correctos según su universo.

### Dashboard Consistency

- RN visible = RN operacional (op_pnl=1) ✅
- Aju waterfall = Aju breakdown (operacional) ✅
- Visual = Click en ajustes (mismo financial_group='ajustes') ✅
- Single Financial Truth: PASS ($0 delta SFT) ✅

## Entregable

- `api/api.py` — endpoint `/api/v4/exec/waterfall` unificado operacional
- `templates/dashboard.html` — `aju` desde waterfall, desglose operacional para todos los MPs
- `governance/RN_OPERATIONAL_CERTIFICATION.md`
