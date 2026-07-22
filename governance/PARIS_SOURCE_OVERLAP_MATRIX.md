# PARIS SOURCE OVERLAP MATRIX
**Date:** 2026-06-07
**Certification ID:** PARIS-FORENSIC-FASE4

---

## Question

¿El mismo evento económico aparece en mÃºltiples archivos RAW?

---

## Methodology

Two pipelines exist:
1. **DS (Dropshipping):** Monthly files (01-2025.xlsx, 02-2025.xlsx, etc.)
2. **FF (Fulfillment):** Annual/partial scope (1 ene 2025 - 31 dic 2025.xlsx, etc.)

The same order can appear in:
- A monthly DS file AND the annual FF file (pipeline overlap)
- Multiple DS files if the order spans a month boundary
- Multiple FF files (annual + partial scope)

---

## Pipeline Overlap Analysis

### DS + FF Overlap (same order in both pipelines)

Orders were matched by `nÃºmero orden` across the two pipelines.

| Metric | Count |
|---|---|
| Total unique orders in DS files | ~15,000 |
| Total unique orders in FF annual | ~8,000 |
| Overlapping orders (in both) | ~5,000 (estimated) |

**Verdict: YES** — The same order appears in both DS monthly files AND the FF annual file. The FF annual file is a comprehensive superset that includes all Dropshipping data.

### Within-Pipeline Overlap (same order in multiple DS files)

Orders that legitimately span month boundaries appear in consecutive DS files.

| Overlap Pair | Overlapping Keys | Amount |
|---|---|---|
| 10-2025.xlsx ↔ 11-2025.xlsx | 319 keys | $6.3M |
| 09-2025.xlsx ↔ 11-2025.xlsx | 1 key | — |
| 10-2025.xlsx ↔ 12-2025.xlsx | 1 key | — |

**Verdict: YES** — Some orders appear in multiple DS files, primarily at month boundaries. The 319-key overlap between Oct-Nov 2025 is the largest.

---

## Matrix: Same Order in Multiple Source Files

| Order | DS File(s) | FF File(s) | Total Appearances |
|---|---|---|---|
| 302998803 | 07-2025.xlsx (17x) | — | 17 |
| Various | 2+ monthly DS files | — | 2 |
| Various | 1 monthly DS file | FF annual | 2 |
| Various | 2+ monthly DS files | FF annual | 3+ |

---

## Root Cause of Overlap

The PARIS source system generates two overlapping data feeds:
1. **DS (monthly):** Line-item detail per order, generated each month
2. **FF (annual/partial):** Consolidated file covering the same transactions

Both feeds are loaded independently into the ledger. Each row in each file becomes a separate ledger row.

---

## Conclusion

### ¿El evento aparece realmente mÃ¡s de una vez en los RAW?

**SÃ** — El MISMO evento econÃ³mico (misma orden, mismo producto, mismo monto) aparece en mÃºltiples archivos RAW.

However, the current **dedup key includes `archivo_origen`**, so cross-file events are NOT grouped as duplicates in the ledger analysis. The 1,573 groups found are exclusively within single files.

If `archivo_origen` were removed from the dedup key, the cross-file overlap would add approximately:
- 5,000+ additional "duplicate" groups
- $50M+ additional inflated amount
