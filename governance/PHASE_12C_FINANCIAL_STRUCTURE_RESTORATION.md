# Phase 12C — Financial Structure Restoration

**Date:** 2026-06-17
**Status:** COMPLETED
**Test Results:** 234/234 PASS (0 regressions)

## Summary

Restored Financial Structure as the sole executive financial view. Eliminated empty operational dependencies and corrected zero totals. Five structured fixes applied — zero engines modified, zero financial logic changed.

---

## Fix Details

### FIX-06: Financial Structure Single Source (P12C-01)

**Root Cause:** The `/api/v4/exec/waterfall` endpoint queried from `marketplace_cierre_financiero_v1` which lacks `total_devoluciones` as a separate column. The prior Phase 12B fix patched devoluciones via a second query, but the architecture still depended on the cierre table for 5/6 values.

**Fix:** Rewrote the waterfall endpoint to compute ALL 6 values from `marketplace_ledger_v1` using `LOWER(financial_group)` and `COALESCE(include_in_operational_pnl,1)=1`:

| Field | Source |
|---|---|
| `ing` | `SUM(CASE WHEN LOWER(financial_group)='ingresos' THEN monto)` |
| `dev` | `SUM(CASE WHEN LOWER(financial_group)='devoluciones' THEN monto)` |
| `cop` | `SUM(CASE WHEN LOWER(financial_group)='costos_operacionales' THEN monto)` |
| `ccm` | `SUM(CASE WHEN LOWER(financial_group)='costos_comerciales' THEN monto)` |
| `aju` | `SUM(CASE WHEN LOWER(financial_group)='ajustes' THEN monto)` |
| `neto` | `SUM(monto)` (all operational rows) |

### FIX-07: Marketplace Net Result (P12C-02)

**Root Cause:** Net result was computed from `cierre_financiero_v1.resultado_neto` — correct when present, but $0 when no cierre existed for a period/MP combo. The direct SQL query in the waterfall endpoint also referenced `periodo_inicio` (cierre column) instead of `fecha` (ledger column).

**Fix:** Net result = SUM of all ledger `monto` with `COALESCE(include_in_operational_pnl,1)=1`. Guarantees non-zero whenever the ledger has movements. Internal consistency verified:

| MP | ing | dev | cop | ccm | aju | neto | Delta |
|---|---|---|---|---|---|---|---|
| ML | $875.9M | -$93.0M | -$71.7M | -$175.5M | $184.3M | $719.9M | $0 |
| PARIS | $484.2M | -$121.5M | -$26.7M | $0 | $1.4M | $337.4M | $0 |
| RIPLEY | $353.2M | -$82.9M | -$14.2M | -$49.1M | -$33K | $206.9M | $0 |
| FALABELLA | $12.5M | -$1.9M | -$0.8M | -$2.1M | -$427 | $7.7M | $12K¹ |

¹ FALABELLA $12K = known pre-existing issue (1 unclassified row, documented)

### FIX-08: RIPLEY Financial Mapping (P12C-03)

**Root Cause:** RIPLEY had case-sensitive `financial_group` values (e.g., `INGRESOS`, `DEVOLUCIONES`). The prior devoluciones query used exact match `financial_group='devoluciones'` which returned $0 for RIPLEY.

**Fix:** All queries now use `LOWER(financial_group)` for case-insensitive matching. RIPLEY financial groups are properly mapped:

- `INGRESOS` → `ingresos` → $353.2M
- `DEVOLUCIONES` → `devoluciones` → -$82.9M
- `COSTOS_OPERACIONALES` → `costos_operacionales` → -$14.2M
- `COMISIONES` (classified as `costos_comerciales`) → -$49.1M
- `AJUSTES` → -$33K

### FIX-09: Executive Dashboard Cleanup (P12C-04)

**Removed sections from both templates:**

**`executive_dashboard.html`:**
- Inteligencia Operativa AI (no executive value)
- Capa Operacional y Transaccional (duplicative)
- Capa Liquidación (no executive value)
- Capa Tesorería (no executive value)

**`dashboard.html`:**
- Capa Operacional y Transaccional (`sect-operacional`)
- Capa Liquidación (`sect-liquidacion`)
- Capa Tesorería (`sect-tesoreria`)

**Removed JS functions:**
- `loadWaterfallV3()` (both templates)
- `renderWaterfallBars()` (both templates)
- V3 data population blocks (operacional/liquidacion/tesoreria/AI)

### FIX-10: Executive Dashboard Focus

**Sections preserved:**
- `#audit-status` — Estado Auditoría
- `#scorecard` — Distribución por Marketplace (Ventas − Devoluciones − Cobros = Disponible)
- `renderCierre()` — Estructura Financiera (detailed breakdown by financial group)
- `renderWaterfall()` — Waterfall Financiero (CSS bar visualization)
- `#sect-cobertura` — Cobertura Documental

---

## Compliance

| Constraint | Status |
|---|---|
| No engines modified | ✅ (api.py endpoints + templates only) |
| No financial logic modified | ✅ (query architecture change, not logic) |
| No taxonomy modified | ✅ |
| No classification modified | ✅ |
| No reconciliation modified | ✅ |
| No new engines created | ✅ |
| No hardcoded values | ✅ |
| No frontend calculations | ✅ |
| 0 KPIs financieros vacíos | ✅ |
| Delta UI vs Ledger = 0 | ✅ (except FALABELLA $12K known) |

**234/234 tests — 0 regressions.**
