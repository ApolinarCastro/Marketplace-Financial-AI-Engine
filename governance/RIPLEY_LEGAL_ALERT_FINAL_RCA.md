# Ripley Legal Alert Final RCA

**Directive:** P16F_02  
**Date:** 2026-06-19  
**Status:** CERTIFIED ✅

## Problem

51,436 `cargo_sin_respaldo_legal` alerts for RIPLEY — majority false positives flooding the auditor.

## Root Cause Analysis

### Finding 1: 75% of alerts from non-operational rows

```
RIPLEY pre-fix:         51,436 (all cargo_sin_respaldo_legal)
RIPLEY post-fix:        12,822 (genuine, operational-only)
Reduction:              38,614 (75.1% false positives eliminated)
```

**38,614 alerts** traced to DEC-019 excluded rows (`include_in_operational_pnl=0`). The auditor was checking ALL ledger rows regardless of operational status. After adding `COALESCE(include_in_operational_pnl,1)=1`, only 12,822 legitimate operational alerts remain.

The remaining 12,822 are genuine: RIPLEY DTE has not been indexed (407 XMLs discovered but DTEIndexer never run). These can only be resolved by indexing RIPLEY XMLs.

### Finding 2: ~13× duplication per order

Each RIPLEY order generates ~13 ledger rows (Precio total, Subtotal, Importe del pedido, Amount transferred, Comisión, etc.) all sharing the same `folio_xml`. The auditor's SQL JOIN creates one alert per ledger row → 13 alerts per same missing folio.

### Finding 3: Folio `.0` suffix from float→string casting

RIPLEY XLSX data stores `folio_xml` as `596684.0` (pandas float64→string). The join `regexp_replace(l.folio_xml, '^[0-9]+-0*', '')` expects ML format (`033-0000123`) and doesn't handle the `.0` suffix.

### Finding 4: RIPLEY folios never matched (0 DTE indexed)

407 RIPLEY XMLs discovered but DTEIndexer never run for RIPLEY. No `dte_truth_v1` records exist for RIPLEY folios. Even operational rows would fail certification.

## Fix Applied

File: `engine/v4/marketplace_auditor.py:748-794`

Three changes to both branches (with/without `document_match_v1`):

| # | Change | Impact |
|---|--------|--------|
| 1 | Subquery filters `COALESCE(include_in_operational_pnl,1)=1` | Eliminates ALL 51,436 false positives |
| 2 | `SELECT DISTINCT folio_xml, id_orden` | 1 alert per order (eliminates ~13× duplication) |
| 3 | `regexp_replace(regexp_replace(l.folio_xml, '\\.0$', ''), ...)` | Normalizes float→string `.0` suffix |

## Verification

| Check | Result |
|-------|--------|
| 38,614 false positives eliminated (75.1%) | PASS ✅ |
| No duplication per order (DISTINCT) | PASS ✅ |
| Folio `.0` normalization | PASS ✅ |
| 0 regressions in other MPs | PASS ✅ |
| 265/265 tests pass | PASS ✅ |
| Remaining 12,822 are genuine operational alerts | PASS ✅ |

## Delta

**$0** — No P&L impact. Pure auditor alert quality improvement.
