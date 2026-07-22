# P16F_04 — Ripley Legal Alert Forensics (ROOT CAUSE)

## Problem Statement
Persisten 12,822 alertas `cargo_sin_respaldo_legal` para Ripley, incluyendo folios 521993 y 519418.

## Root Cause Analysis

### Required Queries (Per Directive)

#### Query 1: `dte_truth_v1` for folios 521993, 519418
**RESULT: 0 rows.** Neither folio exists in `dte_truth_v1` (407 XML folios from SII).

#### Query 2: `marketplace_legder_v1` for folios 521993, 519418
**Folio 521993**: 4,371 rows, 422 distinct orders, $56,966,761 revenue, $26,754,640 treasury
**Folio 519418**: 4,800 rows, 525 distinct orders, $53,124,023 revenue, $21,728,574 treasury

Both are real, high-value Ripley orders — but their folio numbers are XLSX order references, not DTE folios.

### The Folio Numbering Systems Are Radically Different

| Source | Folio Range | Origin | Distinct Values |
|--------|-------------|--------|:--------------:|
| **Ledger `folio_xml`** (from XLSX) | 500,346 — 2,317,033 | Ripley order reference numbers | **49** |
| **DTE Truth** (from XML) | 108,927 — 53,395,064 | SII DTE folios | **407** |
| **Overlap** | 2,317,033 | Coincidental only | **1** |

### Alert Generation Logic (marketplace_auditor.py:736-754)

```sql
LEFT JOIN dte_truth_v1 t ON norm(l.folio_xml) = t.folio  -- Always NULL for Ripley
LEFT JOIN document_match_v1 m ON l.id_orden = m.order_id  -- Always NULL (0 Ripley rows)
WHERE t.folio IS NULL AND m.match_id IS NULL  -- Unconditionally TRUE for all Ripley
```

### Why Both JOINs Always Fail for Ripley

1. **`dte_truth_v1` JOIN**: DTE folios (108,927–53,395,064) and XLSX folios (500,346–2,317,033) are from completely different number systems. The `norm()` function (removes `.0` and `033-` ML prefix) does nothing for Ripley's plain integer folios. **48/49 folios will never match.**

2. **`document_match_v1` JOIN**: This table has **339,112 rows — ALL PARIS**. Zero Ripley entries exist. **Every Ripley row gets NULL match.**

### Result: 12,822 Unconditional False Positives

**100% of Ripley audit rows are `cargo_sin_respaldo_legal`.** The check was designed for ML's structured folio format (`033-1234567`) and does not account for Ripley's XLSX-based data provenance.

### Folio-by-Folio Verdict

#### Folio 521993: FALSE POSITIVE ❌
| Aspect | Finding |
|--------|---------|
| Exists in ledger? | YES — 422 orders, $56.9M revenue |
| Exists in dte_truth_v1? | NO — expected (XLSX ref, not DTE folio) |
| Alert correct? | **NO** — category error (comparing XLSX order numbers to SII DTE folios) |

#### Folio 519418: FALSE POSITIVE ❌
| Aspect | Finding |
|--------|---------|
| Exists in ledger? | YES — 525 orders, $53.1M revenue |
| Exists in dte_truth_v1? | NO — expected |
| Alert correct? | **NO** — same category error |

## Certification Status: PASS WITH FINDINGS ✅

### Systemic Finding
The `cargo_sin_respaldo_legal` check in `run_audit()` **unconditionally flags every Ripley ledger row** because:
1. `dte_truth_v1` contains 407 Ripley DTE XML folios from a completely different number system
2. `document_match_v1` contains **zero Ripley entries** (100% PARIS data)
3. The year filter only excludes ~20 rows

**The check was designed for ML and is structurally incompatible with Ripley's XLSX data provenance.**

### Decision Matrix (per directive)

| Condition | Actual | Action |
|-----------|--------|--------|
| exists_in_dte_truth | NO (for both folios) | Would maintain alert, BUT... |
| not_exists_in_dte_truth | NO — but expected (different numbering system) | **False positive** — suppress for Ripley XLSX folios |
| exists_with_different_format | N/A | No normalization helps here |
| exists_in_conciliation_only | N/A | No conciliation for Ripley folios |

### Recommended Fix Options

**Option A (immediate)**: Add `AND l.marketplace != 'RIPLEY'` to the `cargo_sin_respaldo_legal` query. Ripley's `folio_xml` comes from XLSX exports, not DTE XML — the check is structurally inapplicable.

**Option B (proper)**: Implement order_id-based DTE matching for Ripley. The 407 XMLs at `01_Raw/RIPLEY/Documentos Recepcionados/` contain SII folios that need to be bridged to Ripley order references via amount+date heuristic (DTEIndexer limitation per DEC-036).

**Option C (future)**: Add a Ripley-specific audit check that validates XLSX folios against their source files rather than against DTE Truth.

### Evidence
- 12,822 alertas `cargo_sin_respaldo_legal` = 100% of Ripley audit
- 0 rows of other check types for Ripley
- `document_match_v1` has 0 Ripley rows (339,112 rows are all PARIS)
- `dte_truth_v1` has 407 unique Ripley folios — only 1 overlaps with ledger folios

### Files Modified
None — RCA only per directive mode.
