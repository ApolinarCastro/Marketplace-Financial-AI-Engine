# P16F_03 — DTE Coverage Reconstruction (ROOT CAUSE)

## Problem Statement
Marketplace individual muestra cobertura DTE en cero mientras Executive dashboard muestra datos válidos para el mismo marketplace.

## Root Cause Analysis

### Endpoint Architecture — Two Divergent Queries

| Aspect | `/api/v4/exec/summary` (Auditor Dashboard) | `/api/v4/financial-structure` (Executive Dashboard) |
|--------|-------------------------------------------|-----------------------------------------------------|
| **DTE denominator** | ALL ledger rows (`WHERE fecha >= ?`) | Operational P&L only (`WHERE COALESCE(include_in_operational_pnl,1)=1`) |
| **Error handling** | None (exception propagates) | Silent try/except → returns `{}` |
| **Case sensitivity** | Uses `LOWER(marketplace)` | Uses `LOWER(marketplace)` |
| **null folio handling** | `IS NOT NULL` only | `IS NOT NULL AND != 'None'` |

### PRIMARY Root Cause: Operational PNL Filter Divergence

| Marketplace | exec/summary (no op_pnl filter) | financial-structure (with op_pnl filter) | Delta |
|------------|--------------------------------|------------------------------------------|-------|
| **ML** | 51.5% (21,669/42,108) | **94.2%** (21,669/23,009) | +42.7pp |
| **RIPLEY** | 93.4% (51,443/55,051) | **84.6%** (11,443/13,524) | -8.8pp |
| **PARIS** | 61.2% (10,268/16,782) | 61.2% (10,268/16,782) | 0pp |
| **FALABELLA** | 42.9% (1,118/2,609) | 42.9% (1,118/2,609) | 0pp |

After DEC-019 (paired mechanism removal), **19,099 ML rows** and **41,527 RIPLEY rows** were flagged `include_in_operational_pnl=0`. The `exec/summary` endpoint still counts ALL rows in the denominator, producing artificially LOW coverage.

The Executive dashboard uses `financial-structure` (with filter), so it shows 94.2% for ML. The Auditor dashboard uses `exec/summary` (no filter), so it shows 51.5%.

### SECONDARY Cause: Silent Failure in financial-structure

```python
# api/api.py lines 692-722
try:
    dte_query = ...
    dte = {mp: {...} for mp in marketplaces}
except Exception:
    dte = {}  # ← Silent failure returns empty dict
```

If the DTE query fails for any reason, the frontend receives `dte_coverage: {}`, and the fallback renders as `cobertura: 0`.

### TERTIARY Cause: Genuine Data Gaps

Geniune 0% coverage periods exist:
- PARIS 2026-06: 0/2,302 rows have folio_xml (0%) — no XML files ingested for Junio
- FALABELLA 2026-06: 0/678 rows have folio_xml (0%) — no XML files ingested
- FALABELLA 2026-01/02: 0 rows in ledger (0%) — no data for these periods

### Actual DTE Coverage (Operational P&L, YTD 2026)

| Marketplace | With folio_xml | Total (op_pnl) | Coverage |
|------------|:-------------:|:--------------:|:--------:|
| **ML** | 21,669 | 23,009 | **94.2%** |
| **RIPLEY** | 11,443 | 13,524 | **84.6%** |
| **PARIS** | 10,268 | 16,782 | **61.2%** |
| **FALABELLA** | 1,118 | 2,609 | **42.9%** |
| **TOTAL** | 44,498 | 55,924 | **79.6%** |

## Certification Status: FAIL ❌ (pending fix)

### Findings
1. **Both endpoints must use the same filter**: Either both include `COALESCE(include_in_operational_pnl,1)=1` or both omit it
2. **Remove silent try/except** in `financial-structure` DTE query — add logging instead
3. **Remove dead code**: The `exec/summary` route is marked `# LEGACY` at api.py:415 — it should be unified with `financial-structure`
4. **PARIS/FALABELLA coverage below 95%** — requires order_id-based DTE matching (DTEIndexer heuristic limitation, DEC-036)

### Evidence
- SQL queries from both endpoints extracted and compared
- Row counts verified against DB: 21,669 ML folio_xml rows confirmed
- 661 unique DTE folios in `dte_truth_v1` verified

### Files Modified
None — RCA only per directive mode.

### Recommended Fix
1. Add `COALESCE(include_in_operational_pnl,1)=1` to `exec/summary` DTE query
2. Remove silent `except Exception: dte = {}` in `financial-structure`
3. Add `AND folio_xml != 'None' AND folio_xml != ''` to both queries
4. Return `cobertura: null` (not 0) for periods with no data
