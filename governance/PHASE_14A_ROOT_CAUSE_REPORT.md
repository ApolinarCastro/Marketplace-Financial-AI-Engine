# Root Cause Report — Phase 14A

## Status: ALL RESOLVED ✅

## OBS_UI_01: Ingresos Brutos shows monto but ledger returns 0

**Root Cause:** RIPLEY stores `financial_group` in UPPERCASE (`'INGRESOS'`, `'DEVOLUCIONES'`). The `query_ledger()` function used `financial_group = ?` (exact case match). The frontend `buildLedgerUrl()` passed lowercase `'ingresos'` from `cat.financial_group` (which comes from `LOWER(financial_group)` in the financial-structure SQL). Exact match failed → 0 rows.

**Fix:** Changed `query_ledger()` to use `LOWER(financial_group) = LOWER(?)` — case-insensitive matching.

**Evidence:** Pre-fix: 0 rows with `financial_group='ingresos'`. Post-fix: 17,533 rows ($467.6M), matching uppercase query.

## OBS_UI_02: Category click ≠ subcategory sum

**Two separate root causes:**

### 2a: ML merged financial_group
**Root Cause:** When multiple financial_group values map to the same display_name (e.g., `ajustes + recuperaciones_y_bonificaciones` → "Ajustes & Retenciones"), the financial-structure endpoint concatenates them: `financial_group = 'ajustes, recuperaciones_y_bonificaciones'`. `buildLedgerUrl()` passed this merged string as a single filter value. `query_ledger` did `financial_group = 'ajustes, recuperaciones_y_bonificaciones'` which matched NO rows.

**Fix:** Updated `query_ledger()` to detect comma-separated financial_group values, split them, and use `LOWER(financial_group) IN (...)`.

**Evidence:** Pre-fix: 0 rows. Post-fix: 104 rows ($1.15M).

### 2b: Substring collision with LIKE
**Root Cause:** `query_ledger` used `detalle LIKE '%value%'` for subcategory filtering. "Importe del pedido" matches BOTH "Importe del pedido" AND "Importe del pedido REEMBOLSADO" (devoluciones). The devoluciones rows ($-27.7M) were incorrectly included, reducing the total from $218.4M to $190.7M.

**Fix:** Changed to `LOWER(detalle) = LOWER(?)` — exact match instead of LIKE.

**Evidence:** Pre-fix: Importe del pedido = $190.7M (includes devoluciones). Post-fix: $218.4M (exact match).

## OBS_UI_03: Total Seleccionado vs category mismatch

**Root Cause:** Direct consequence of OBS_UI_01 and OBS_UI_02 — the grid defaults to the sum of all returned ledger rows, which was $0 when category filter failed, or wrong values when LIKE collisions occurred.

**Fix:** Resolved by fixing OBS_UI_01 and OBS_UI_02.

## OBS_UI_04: Executive Dashboard degraded

**Three root causes:**

### 4a: Missing `selectMarketplace()` function
**Root Cause:** The `selectMarketplace()` function was removed during a previous refactor. Clicking a scorecard card triggered `onclick="selectMarketplace('ML')"` → JavaScript error.

**Fix:** Re-added the function:
```javascript
function selectMarketplace(mpId) {
    const globalMp = document.getElementById('exec-mp');
    if (globalMp.value === mpId) { globalMp.value = ''; }
    else { globalMp.value = mpId; }
    onFilterChange();
}
```

### 4b: Client-side cobros formula
**Root Cause:** `const cobros = neto - gross - devTotal` was computed on the frontend.

**Fix:** Added `cobros` field server-side in `/api/v4/financial-structure` response. Frontend now uses `fs.cobros` with fallback `|| (neto - gross - devTotal)`.

### 4c: DTE returned hardcoded zeros
**Root Cause:** `/api/v4/exec/summary` had `"documentary": {"xml_conciliados": 0, ...}` hardcoded.

**Fix:** Added real DTE queries per MP from `marketplace_ledger_v1` using `folio_xml IS NOT NULL` to count conciliated documents.

## OBS_UI_05: DTE coverage broken

**Root Cause:** The `/api/v4/exec/summary` legacy endpoint had hardcoded zero values for all documentary metrics. The executive dashboard consumed this endpoint for DTE display.

**Fix:** Computed real DTE metrics per MP from `marketplace_ledger_v1`:
- `xml_conciliados`: COUNT where `folio_xml IS NOT NULL`
- `xml_pendientes`: total - conciliados
- `total_dte`: total rows
- `cobertura`: conciliados / total * 100

**Current coverage:** ML 51.5%, RIPLEY 90.9%, FALABELLA 0%, PARIS 0% (FALABELLA/PARIS have no XML ingestion pipeline active).

## Files Modified

| File | Change |
|------|--------|
| `engine/v4/domain/financial_engine.py` | `financial_group` → case-insensitive + merged IN; `detalle` → exact match |
| `api/api.py` | DTE computation in `/api/v4/exec/summary`; `cobros` in `/api/v4/financial-structure` |
| `templates/executive_dashboard.html` | `selectMarketplace()`, `fs.cobros`, parallel DTE + FS fetch |
