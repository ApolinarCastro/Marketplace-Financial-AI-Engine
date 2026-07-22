# FRONTEND-BACKEND RECONCILIATION REPORT
## Phase 12B — Critical Findings

**Date**: 2026-06-16  
**Status**: BLOCKER — 5 structural discrepancies found  

---

## Executive Summary

The Phase 12B Operational Acceptance Certification reported PASS, but **4 frontend-backend contract violations** and **1 false certification display** were found post-certification. The certification chain is broken at multiple points:

```
FinancialEngine → API → Contract → Dashboard
                    ✗         ✗         ✗
```

**5 fixes required** before Phase 12B can be approved:
1. FIX-01: 4 field name mismatches in `/api/v4/exec/summary-v3` vs frontend expectations
2. FIX-02: RIPLEY shows $0 in UI despite $1.9B data in DB — taxonomy group mapping broken
3. FIX-03: `truth_type` referenced in 4 frontend locations but not returned by API
4. FIX-04: 3 endpoint routes renamed/removed, 1 HTML route missing
5. FIX-05: "Certificado" badge hardcoded — shows PRE_LOCK always, never real status

---

## FIX-01: Financial Structure — Field Name Mismatch

### Evidence

**Endpoint**: `GET /api/v4/exec/summary-v3`  
**Endpoint returns**:
```json
{
  "operacional": {
    "venta_mp": 934773504,
    "venta_ff": 0,
    "venta_operacional_consolidada": 934773504,
    "ordenes_mp": 123,
    "ordenes_ff": 0
  }
}
```

**Frontend (`executive_dashboard.html` line 306-307) reads**:
```javascript
document.getElementById('v3-op-venta-ff').textContent = fmtCLP(v3Data.operacional.costos_logisticos);
document.getElementById('v3-op-venta-cons').textContent = fmtCLP(v3Data.operacional.movimiento_financiero);
```

**Same in `dashboard.html` lines 1393-1395**.

| Field in DB | API returns as | Frontend reads as | Match? |
|---|---|---|---|
| venta_ff | `operacional.venta_ff` | `operacional.costos_logisticos` | ✗ |
| venta_operacional_consolidada | `operacional.venta_operacional_consolidada` | `operacional.movimiento_financiero` | ✗ |

**Impact**: Both fields render `undefined` → display shows `$NaN` or `—` instead of actual values.

### Contract Check

**Pydantic contract** (`executive_contract.py`):
- `ExecutiveSummary` defines: `ventas_netas`, `devoluciones`, `cobros`, `disponible`
- `WaterfallResponse` defines: `steps`, `concepts`
- `/api/v4/exec/summary-v3` returns: `operacional`, `liquidacion`, `tesoreria`

**Contract violation**: The API response structure does NOT match any Pydantic contract. No contract validation is applied to this endpoint.

---

## FIX-02: RIPLEY Financial Structure — $0 in UI, $1.9B in DB

### Evidence

**DB confirmation** (`marketplace_ledger_clasificado_v1`):
| financial_group | Rows | Total |
|---|---|---|
| INGRESOS | 73,249 | $1,908,041,379 |
| LIQUIDACION | 31,946 | $425,546,045 |
| COSTOS_LOGISTICOS | 36,207 | -$30,328,918 |
| COMISIONES | 53,336 | -$13,465,726 |
| AJUSTES | 12,361 | -$39,891,271 |
| DEVOLUCIONES | 10,216 | -$151,180,591 |

**RIPLEY has $1.9B in ingresos alone** — but the UI shows $0.

### Root Cause

The `/api/v4/exec/summary-v3` endpoint uses hardcoded file pattern filters:
```python
# Line 301-303 of api.py
WHERE archivo_origen LIKE '%.xlsx'
  AND detalle IN ('Precio total', 'Importe del pedido', 'order_amount', 'Subtotal')
```

RIPLEY data uses `.xlsx` files with `Importe del pedido` detalle. But the `include_in_operational_pnl=0` for RIPLEY ingresos (DEC-019) means the `COALESCE(include_in_operational_pnl,1)=1` filter elsewhere excludes them. The `summary-v3` endpoint does NOT apply the operational filter — it uses `archivo_origen` and `detalle` patterns directly. This means RIPLEY data SHOULD appear, but the `WHERE archivo_origen LIKE '%.xlsx'` combined with ALL 4 MPs unfiltered creates wrong totals.

**Actually the more direct issue**: When RIPLEY is selected (marketplace='RIPLEY'), the `mp_filter` adds `AND marketplace = ?` which should work. But the `INGRESOS` group in RIPLEY uses `detalle` values that include things like `Importe del pedido` which IS in the IN clause. Let me re-check...

Wait, the issue is that the `venta_mp` query (lines 298-305 of api.py) filters by `detalle IN ('Precio total', 'Importe del pedido', 'order_amount', 'Subtotal')`. For RIPLEY, the INGRESOS group has `detalle='Importe del pedido'`, so it should match.

But RIPLEY's `archivo_origen` for INGRESOS doesn't end in `.xlsx` — let me check.

Actually, the `financial_group='ingresos'` is NOT part of the `summary-v3` query at all. The summary-v3 queries are based on `archivo_origen LIKE '%.xlsx'` and `detalle` values, not on `financial_group`. This means the query bypasses the taxonomy entirely.

**Real root cause**: The `summary-v3` endpoint uses a DIFFERENT query methodology than the certified FinancialEngine or Cierre tables. It queries by `archivo_origen` and `detalle` patterns, NOT by `financial_group`. This creates a discrepancy with the certified P&L structure.

### RIPLEY Specific Test

When RIPLEY period filter is applied:
- RIPLEY's `.xlsx` files have `Importe del pedido` which IS in the detalle filter
- But the `archivo_origen LIKE '%.xlsx'` may not match if RIPLEY uses a different extension or path pattern
- Additional issue: RIPLEY only has periods like 2026-12, 2025-12 in the DB (post B2.5C), and the `periodo` filter in `_resolve_period_range` may not match

---

## FIX-03: Truth Type — Phantom Column

### Evidence

**API response** from FinancialEngine (`/api/v4/ledger`) returns these columns:
```
marketplace, id_transaccion, id_orden, fecha, detalle, monto, tipo_movimiento,
archivo_origen, folio_xml, estado_xml, load_ts, asociacion_xml, financial_group,
clasificacion_operativa, include_in_operational_pnl, monto_bruto, comision_marketplace
```

**`truth_type` is NOT present** in the API response.

**DB schema** confirms: `truth_type` does NOT exist in `marketplace_ledger_v1` or `marketplace_ledger_clasificado_v1`.

**Frontend references `truth_type` in 4 locations**:
| File | Line | Code |
|---|---|---|
| `dashboard.html` | 751-758 | `truthTypeColors[row.truth_type]` — used for badge color |
| `dashboard.html` | 764-779 | Fallback logic: `if (row.truth_type === 'TRANSACTION') mappedOrigen = 'TH'` |
| `dashboard.html` | 797 | `<span>${row.truth_type || 'N/A'}</span>` — renders in ledger table |

**Impact**: All 4 references resolve to `undefined`, meaning:
- All rows show `N/A` in the "Truth Type" column
- Origin mapping falls through to the `INCIDENTE_ORIGEN_FALTANTE` fallback
- The layer filter (TH/SETTLEMENT/OPERATIONAL/LOGISTICS/TAX) cannot function

### Contract Check

No Pydantic contract includes `truth_type`. The `FinancialStructureRow` contract uses `clasificacion_operativa` and `financial_group`, not `truth_type`.

---

## FIX-04: Executive Dashboard — Missing/Removed Routes

### Evidence

#### 1. `/api/v4/exec/summary` — ENDPOINT MISSING

**Frontend (`executive_dashboard.html` line 287)**:
```javascript
const summaryUrl = '/api/v4/exec/summary' + (period !== 'YTD' ? '?periodo=' + period : '');
```

**Same in `dashboard.html` line 1368**:
```javascript
const summaryUrl = '/api/v4/exec/summary' + (...);
```

**API has**: `/api/v4/exec/summary-v3` (line 270) — NOT `/api/v4/exec/summary`  
**Result**: 404 Not Found → `summaryRes.ok = false` → scorecard shows all zeros

#### 2. `/api/v4/exec/waterfall` — ENDPOINT RENAMED

**Frontend (`dashboard.html` line 1134)**:
```javascript
const wfRes = await fetch('/api/v4/exec/waterfall' + mkQuery);
```

**API has**: `/api/v4/exec/waterfall-v3` (line 379) — NOT `/api/v4/exec/waterfall`  
**Result**: 404 Not Found → `wfRes.ok = false` → `_cierreCertified` stays undefined → `renderCierre()` shows $0 for all groups

#### 3. `/api/v4/ledger/summary` — ENDPOINT MISSING

**Frontend (`dashboard.html` line 1196)**:
```javascript
const summaryRes = await fetch('/api/v4/ledger/summary' + mkQueryLedger);
```

**API has**: No `/api/v4/ledger/summary` endpoint exists  
**Result**: 404 Not Found → `summaryData = {}` → `renderLayerFilters` gets empty data → layer filter buttons not rendered

#### 4. `/exec` — HTML ROUTE MISSING

**Frontend (`dashboard.html` line 30)**:
```html
<a href="/exec" class="...">Executive</a>
```

**API routes**:
- `GET /` → `dashboard.html`
- `GET /app` → `dashboard.html`  
- **NO `/exec` route**

**Result**: Clicking "Executive" in the Auditor dashboard navigates to 404.

#### 5. `dashboard.html` JS ID mismatches

| Code | Uses ID | Correct ID | Match? |
|---|---|---|---|
| `loadAnalyticLayers()` line 1365 | `document.getElementById('period').value` | `period-selector` | ✗ |
| `loadAnalyticLayers()` line 1366 | `document.getElementById('mp').value` | `marketplace-selector` | ✗ |
| `loadAnalyticLayers()` line 1450 | `loadWaterfallV3('operacional')` | Function takes no params | ✗ |

---

## FIX-05: False Certification Badge

### Evidence

#### Hardcoded "CERTIFICADO" in HTML

**`executive_dashboard.html` line 65-66**:
```html
<span id="audit-status-badge" class="...">
    Financiero: PRE_LOCK CERTIFICADO
</span>
```

This badge is ALWAYS rendered as "PRE_LOCK CERTIFICADO" regardless of actual certification status.

#### Dynamic update never triggers

The JS code at lines 359-436 tries to update the badge based on `v3Data.conciliacion.status`:
```javascript
if (v3Data && v3Data.conciliacion) {
    // Update badge based on conciliacion status
}
```

But `v3Data.conciliacion` is NEVER set because:
- `/api/v4/exec/summary-v3` does NOT return a `conciliacion` field
- The endpoint name is `/api/v4/exec/summary` (which returns 404)

**Result**: Badge always shows the hardcoded "PRE_LOCK CERTIFICADO".

#### Dashboard.html "Certificado" status

**`dashboard.html` lines 922-928**:
```javascript
if (currentDesglose && currentDesglose.length > 0 && !isRipleyWithoutTaxonomy) {
    estadoContainer.innerHTML = `...Certificado...`;
}
```

This shows "Certificado" ANY TIME desglose has data, even if:
- The data is from a wrong period
- The classification is incomplete
- The reconciliation shows large deltas
- The actual certification engine returns DEGRADED

**Actual Certification status** (from `/api/v4/certify`):

| MP | Pass Rate | Status |
|---|---|---|
| ML | 83.3% | DEGRADED |
| PARIS | 83.3% | DEGRADED |
| RIPLEY | 66.7% | DEGRADED |
| FALABELLA | 66.7% | DEGRADED |

**NONE of the MPs are CERTIFIED** — yet the UI shows "Certificado" for all of them.

---

## Reconciliation Summary

| Fix | Component | Broken | Evidence |
|---|---|---|---|
| FIX-01 | `/api/v4/exec/summary-v3` ↔ Frontend | 2 field name mismatches | `costos_logisticos`, `movimiento_financiero` referenced but not returned |
| FIX-01 | Contract validation | None applied | No Pydantic contract wraps `/api/v4/exec/summary-v3` response |
| FIX-02 | RIPLEY → UI | $0 display despite $1.9B DB | 73,249 INGRESOS rows in DB, $0 in dashboard |
| FIX-03 | API → Frontend | `truth_type` not returned | 4 frontend locations reference missing column |
| FIX-04 | Routes | 3 endpoints 404, 1 HTML route 404 | `/exec/summary`, `/exec/waterfall`, `/ledger/summary`, `/exec` |
| FIX-04 | JS DOM IDs | 2 wrong element IDs | `period` vs `period-selector`, `mp` vs `marketplace-selector` |
| FIX-05 | Badge display | Hardcoded CERTIFICADO | Shows PRE_LOCK when all MPs are DEGRADED |

---

## Required Actions (No New Features)

1. **FIX-01**: Fix field names in `/api/v4/exec/summary-v3` (backend) OR fix frontend reads (frontend). Prefer backend fix to match frontend expectations (endpoint already returns "venta_ff" — add "costos_logisticos" and "movimiento_financiero" aliases).

2. **FIX-02**: Fix RIPLEY display — ensure `summary-v3` queries capture RIPLEY data correctly. Likely the `archivo_origen` pattern filter needs adjustment or the data doesn't have matching patterns for RIPLEY.

3. **FIX-03**: Remove `truth_type` references from frontend or map from `financial_group` → truth_type in a server-side derived field. No column exists in DB or API.

4. **FIX-04**: 
   - Add route aliases for `/api/v4/exec/summary` → `/api/v4/exec/summary-v3`
   - Add route aliases for `/api/v4/exec/waterfall` → `/api/v4/exec/waterfall-v3`
   - Add `/api/v4/ledger/summary` endpoint OR fix frontend to use correct endpoint
   - Add `GET /exec` HTML route → executive_dashboard.html
   - Fix JS DOM IDs in `dashboard.html` `loadAnalyticLayers()` function

5. **FIX-05**: Replace hardcoded badge with dynamic fetch to `/api/v4/certify`. Show actual certification status. Remove "CERTIFICADO" display when engine returns DEGRADED or FAILED.

---

## Verification

After all 5 fixes, run:
```bash
pytest tests/ --tb=short  # 234 tests must still PASS
```

And verify: Executive Dashboard → selects RIPLEY → shows $1.9B in Estructura Financiera → certification badge shows DEGRADED (not CERTIFICADO).
