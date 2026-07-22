# Phase 14B — RIPLEY Financial Truth Certification

## Certification: PASS ✅

## Scope

Phase 14B resolves 3 open observations (OBS_RIPLEY_001–003) from the Phase 14A forensic audit by ensuring that the Signal/Noise taxonomy (`knowledge/taxonomy/ripley_v1.json`) is applied **consistently** across both the Financial Structure endpoint and the Ledger Transaccional click-through.

## Root Cause

The Phase 14A "discrepancies" (OBS_RIPLEY_001–003) were not data errors or filter bugs — they were a **structural inconsistency** between the two frontend data paths:
- **Financial Structure** (`/api/v4/financial-structure?signal_mode=SIGNAL`) correctly filtered by the taxonomy SIGNAL set
- **Ledger click-through** (`/api/v4/ledger`) queried ALL rows, including NOISE entries

This meant clicking a SIGNAL-mode category showed a different total (ALL) than what the category displayed (SIGNAL).

## Fix Applied (3 files)

### 1. `engine/v4/domain/financial_engine.py:284` — `query_ledger()`
Added `signal_mode` parameter. When `signal_mode=SIGNAL` and `marketplace=RIPLEY`, loads `knowledge/taxonomy/ripley_v1.json` and adds `detalle IN (SIGNAL_values...)` to the WHERE clause.

### 2. `api/api.py:55` — `/api/v4/ledger` endpoint
Added `signal_mode` query parameter (default: `"ALL"`) with pass-through to `query_ledger()`.

### 3. `templates/dashboard.html:514` — `buildLedgerUrl()`
Added `&signal_mode=SIGNAL` to all Ledger API calls, so the Auditor dashboard's click-through matches the SIGNAL view.

## Validation Results (AC_01-06)

| # | Criterion | Result |
|---|---|---|
| AC-01 | Ingresos Brutos FS SIGNAL = Ledger SIGNAL | ✅ PASS ($0 delta) |
| AC-02 | Devoluciones de Venta FS SIGNAL = Ledger SIGNAL | ✅ PASS ($0 delta) |
| AC-03 | Costos Logísticos FS SIGNAL = Ledger SIGNAL | ✅ PASS ($0 delta) |
| AC-04 | Comisiones FS SIGNAL = Ledger SIGNAL | ✅ PASS ($0 delta) |
| AC-05 | Ajustes FS SIGNAL = Ledger SIGNAL | ✅ PASS ($0 delta) |
| AC-06 | Liquidación FS SIGNAL = Ledger SIGNAL | ✅ PASS ($0 delta) |
| AC-07 | Sum of categories = Ledger total (conservation) | ✅ PASS |
| AC-08 | Non-RIPLEY marketplaces unaffected | ✅ PASS (ML/PARIS/FALABELLA $0 delta) |

## Regression Impact

- **Tests**: 234/234 PASS (0 regressions, 0 pre-existing failures)
- **DEC-019**: Preserved (include_in_operational_pnl flag)
- **DEC-028**: Taxonomy unchanged
- **DEC-029/030**: Period bug fix preserved

## OBS Resolution

| Observation | Status | Resolution |
|---|---|---|
| OBS_RIPLEY_001 (Devoluciones -$5.4M gap) | ✅ RESOLVED | Ledger now applies SIGNAL filter → returns -$5,983,094 (FS total) |
| OBS_RIPLEY_002 (Costos $536K gap) | ✅ RESOLVED | Ledger now applies SIGNAL filter → returns -$1,226,948 (FS total) |
| OBS_RIPLEY_003 (Comisiones -$5.9M gap) | ✅ RESOLVED | Ledger now applies SIGNAL filter → returns $4,122,807 (FS total) |

## Verdict

**PHASE 14B: PASS** ✅ — RIPLEY Financial Truth certified. The Signal/Noise taxonomy is now consistently applied across all visualization layers (Financial Structure, Ledger click-through, Auditor Dashboard). Single Financial Truth principle maintained.
