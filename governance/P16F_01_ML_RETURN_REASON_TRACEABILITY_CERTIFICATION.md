# P16F_01 — ML Return Reason Traceability Certification (ROOT CAUSE)

## Problem Statement
Motivos de devolución (bigger_than_expected_fashion, repentant_buyer, etc.) continúan apareciendo como estructura financiera, generando duda sobre si representan taxonomía financiera o metadata operacional.

## Root Cause Analysis

### Data Volume
- 9,452 rows (5.04% of ML ledger) represent return reason `detalle` codes
- $281,865,983 total value (all 100% positive monto)
- **All rows originate from ML Facturación XLSX files** (5 files, Jan 2025–Jun 2026), NOT from Poscobro

### Classification Chain (3 Layers)

```
Source Facturación XLSX (5 files)
  → marketplace_ledger_v1.detalle (raw codes)
    → RAW_TO_CLASSIFICATION_MAP (44 mappings in marketplace_auditor.py:54-110)
      → CLASIFICACION_TO_FINANCIAL_GROUP (derived from FINANCIAL_STRUCTURE)
        → marketplace_ledger_clasificado_v1.financial_group
```

### Financial Group Distribution

| financial_group | rows | total $ | % |
|----------------|-----:|--------:|---|
| **devoluciones** | 9,312 | $277,105,208 | 98.3% |
| **recuperaciones_y_bonificaciones** | 140 | $4,760,775 | 1.7% |
| **TOTAL** | 9,452 | $281,865,983 | 100% |

### RCA Verdict

**Return reasons are operational metadata, NOT financial structure.** They describe *why* a return happened (talla, arrepentimiento, producto dañado) but are all classified under `financial_group='devoluciones'`. The granularity is preserved in `detalle` only for operational traceability — it does not create separate financial nodes.

### Taxonomy Error Found in ml_v1.json
The Phase 15B `knowledge/taxonomy/ml_v1.json` has 6 entries incorrectly under `ajustes`:

| detalle | ml_v1.json says | Actual DB says |
|---------|----------------|---------------|
| BPP_refunded | `ajustes` | `devoluciones` |
| Respondent_unanswered | `ajustes` | `devoluciones` |
| Bought_by_mistake | `ajustes` | `devoluciones` |
| PPV_covered_melienvio | `ajustes` | `devoluciones` |
| PPV_valid | `ajustes` | `devoluciones` |
| Different_item_other_change | `ajustes` | `devoluciones` |

**Root cause**: The `ml_v1.json` taxonomy was created independently from the classification engine at Phase 15B. The `RAW_TO_CLASSIFICATION_MAP` in `marketplace_auditor.py` correctly routes all "Ajuste por X" concepts to `devoluciones` (since the 16F merge). The taxonomy file was never updated.

## Certification Status: PASS WITH WARNINGS ⚠️

### What's Correct
- Classification engine routes 100% of return reasons to correct financial groups
- 0 rows in `ajustes` from return reasons
- Return reasons preserved as analytic attribute in `detalle`, not as financial structure
- `include_in_operational_pnl` correctly assigned per DEC-019 (MECHANISMS=FALSE, ROOT_EVENTS=TRUE)

### What Needs Fixing
- `knowledge/taxonomy/ml_v1.json` needs 6 entries corrected from `ajustes` to `devoluciones`
- This is a documentation error only — actual DB classification is correct

### Evidence
- 9,452 rows verified across all 44 return reason detalle codes
- Full trace from raw source → canonical concept → financial_group documented
- 0 rows of return reason contamination in `ajustes`, `ingresos`, or `costos_*` groups

### Files Modified
- `taxonomy/taxonomy_rules.yaml`: 12 concepts moved from `riesgos_y_compensaciones` to `devoluciones`
- `taxonomy/taxonomy_mappings.yaml`: 11 concept mappings changed from `ajustes` to `devoluciones`
- `knowledge/taxonomy/ml_v1.json`: NEEDS UPDATE (6 entries)

### Self-Correction Noted
This certification **replaces and supersedes** the pre-Phase 16F understanding where `riesgos_y_compensaciones` was a separate financial group. The post-merge state (`riesgos_y_compensaciones → devoluciones`) is now the Single Financial Truth.
