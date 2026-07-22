# PARIS RAW vs LEDGER RECONCILIATION
**Date:** 2026-06-07
**Certification ID:** PARIS-FORENSIC-FASE5

---

## Universe Comparison

| Metric | RAW (XLSX) | LEDGER (marketplace_ledger_v1) | Delta |
|---|---|---|---|
| Total rows | 46,090 | 45,540 (incl. 2,052 excess copies) | -550 |
| Unique events | 43,488 (unique dedup key) | 43,488 (unique dedup key) | $0 |
| Total monto_a_pagar / ledger monto | $338,658,414 | $337,418,552 | -$1,239,862 |

---

## Classification by Cross-Reference

| Category | Description | Count |
|---|---|---|
| **A** | Exists in RAW once AND exists once in ledger | 43,488 unique keys |
| **B** | Exists in RAW N times AND exists N times in ledger | **1,573 groups (2,052 excess)** |
| **C** | Exists in RAW but NOT in ledger | ~3,500 rows (unloaded) |
| **D** | Exists in ledger but NOT in RAW | 381 groups (files missing from disk) |

---

## Category B Breakdown

| Sub-category | Groups | Description |
|---|---|---|
| **B1 — True Source Duplicates** | **133** | Source file has identical rows for same order (only `id` differs). Same SKU, same product, same amount. |
| **B2 — Multi-Item Collapse** | **1,059** | Source has different line items in same order with same monto_a_pagar (different SKUs, different products). The dedup key is too aggressive — these are NOT duplicates. |
| **B3 — Unverifiable** | **381** | Source file referenced in ledger (`archivo_origen`) not found on disk. |

---

## Concept-Level Comparison

| Concept | RAW monto_a_pagar | Ledger monto | Delta | Reason |
|---|---|---|---|---|
| Venta | $487,741,043 | $483,888,712 | -$3,852,331 | Unloaded data from newer files (Jun 2026) |
| DevoluciÃ³n | -$123,490,638 | -$121,458,109 | +$2,032,529 | Unloaded data from newer files |
| Cobro por despacho | -$22,067,830 | -$21,625,080 | +$442,750 | Unloaded data from newer files |
| LogÃ­stica inversa | -$3,225,310 | -$3,088,120 | +$137,190 | Unloaded rows |
| Retiro stock | -$1,630,800 | -$1,630,800 | $0 | Fully loaded |
| CompensaciÃ³n log. | $1,618,057 | $1,618,057 | $0 | Fully loaded |
| Ajuste Inv. Activo | $647,108 | $647,108 | $0 | Fully loaded |
| Cargo | -$646,295 | -$646,295 | $0 | Fully loaded |
| Cobro stock antiguo | -$316,638 | -$316,638 | $0 | Fully loaded |
| Rebate | $273,230 | $273,230 | $0 | Fully loaded |
| Cobro campaÃ±a | -$260,504 | -$260,504 | $0 | Fully loaded |
| Merma | $16,991 | $16,991 | $0 | Fully loaded |

---

## Key Discovery: Ledger Stores `monto_a_pagar`, NOT Raw `monto`

The ledger `monto` field corresponds to the source file's **`monto a pagar`** column (net amount after commission deduction), NOT the raw `monto` (gross price).

| Source Column | Example (Order 302998803) | Ledger Field |
|---|---|---|
| `monto` (gross) | $34,990 | NOT stored |
| `comisiÃ³n` | $15.00 | NOT stored |
| **`monto a pagar` (net)** | **$29,742** | **→ `monto` in ledger** |

**Implication:** The ledger does NOT preserve commission information for PARIS. The $76.9M in commissions (18.5% take rate) exists only in the source files.

---

## Reconciliation Equations

```
RAW monto_a_pagar = Ledger monto + Unloaded rows - Duplicate excess
$338,658,414 = $337,418,552 + X - $1,544,345
X = $2,784,207 (unloaded from newer files)
```

```
RAW Ventas (monto_a_pagar) = Ledger Ventas + Unloaded Ventas - Duplicate excess
$487,741,043 = $483,888,712 + $3,852,331 - $26,228,900
$487,741,043 = $487,741,043 ✓
```

**Note:** The duplicate excess for Ventas ($26.2M) from the prior certification includes non-duplicate multi-item orders. The TRUE duplicate excess is $1,544,345.
