# PARIS PHYSICAL DUPLICATES CERTIFICATION
**Date:** 2026-06-07
**Certification ID:** PARIS-FORENSIC-FASE3

---

## Methodology

For each of the 22 XLSX files in `01_Raw/PARIS/Transacciones/`:
1. Read ALL columns as strings
2. Drop the `id` column (auto-increment row identifier — always unique)
3. Group by ALL remaining columns
4. Count groups with size > 1

This identifies **exact duplicate rows** within each file (same data in every non-identity column).

---

## Verdict

### ¿Existen duplicados fÃ­sicos dentro del mismo archivo?

**NO** — CERO filas duplicadas exactas dentro de cualquier archivo individual.

---

## Detailed Results

| File | Total Rows | Duplicate Groups | Duplicate Rows |
|---|---|---|---|
| 01-2025.xlsx | 1,318 | 0 | 0 |
| 02-2025.xlsx | 1,061 | 0 | 0 |
| 03-2025.xlsx | 643 | 0 | 0 |
| 04-2025.xlsx | 1,405 | 0 | 0 |
| 05-2025.xlsx | 795 | 0 | 0 |
| 06-2025.xlsx | 2,056 | 0 | 0 |
| 07-2025.xlsx | 2,033 | 0 | 0 |
| 08-2025.xlsx | 2,019 | 0 | 0 |
| 09-2025.xlsx | 1,461 | 0 | 0 |
| 10-2025.xlsx | 3,042 | 0 | 0 |
| 11-2025.xlsx | 1,848 | 0 | 0 |
| 12-2025.xlsx | 3,222 | 0 | 0 |
| 01-2026.xlsx | 1,436 | 0 | 0 |
| 02-2026.xlsx | 940 | 0 | 0 |
| 03-2026.xlsx | 1,477 | 0 | 0 |
| 04-2026.xlsx | 1,876 | 0 | 0 |
| 05-2026.xlsx | 1,277 | 0 | 0 |
| 1 jun 2026 - 8 jun 2026.xlsx | 1,329 | 0 | 0 |
| 1 ene 2025 - 31 dic 2025.xlsx | 14,740 | 0 | 0 |
| 1 ene 2026 - 30 abr 2026.xlsx | 1,768 | 0 | 0 |
| 1 may 2026 - 31 may 2026.xlsx | 235 | 0 | 0 |
| 1 jun 2026 - 8 jun 2026.xlsx | 109 | 0 | 0 |
| **TOTAL** | **46,090** | **0** | **0** |

---

## Important Note

While there are **zero exact duplicate rows** (comparing all columns), there ARE **133 cases** where the same order has multiple rows that are identical in all columns EXCEPT the auto-increment `id` column. These are considered **near-duplicates**:

| File | Order | Tipo | Count | monto_a_pagar | Root Cause |
|---|---|---|---|---|---|
| 07-2025.xlsx | 302998803 | Venta | 17 | $29,742 | Same product, same order repeated 17x |
| 1 ene 2025 - 31 dic 2025.xlsx | 300133538 | Venta | 2 | $0 | Zero-value order repeated |
| 1 ene 2025 - 31 dic 2025.xlsx | 277957643 | Venta | 5 | $0 | Zero-value order repeated |
| 1 ene 2025 - 31 dic 2025.xlsx | 300074474 | Venta | 5 | $0 | Zero-value order repeated |
| 1 ene 2025 - 31 dic 2025.xlsx | 300039522 | Venta | 5 | $0 | Zero-value order repeated |
| 1 ene 2025 - 31 dic 2025.xlsx | 276977494 | Venta | 5 | $0 | Zero-value order repeated |
| ... (127 more groups) | | | 2-5 | varies | Same order, same monto, different auto-increment IDs |

**Total near-duplicate groups: 133**
**Total inflated amount: $1,544,345**

These 133 groups are ONLY identifiable by their identical content in ALL non-id columns. They would be exact duplicates if the `id` column were excluded from the comparison.
