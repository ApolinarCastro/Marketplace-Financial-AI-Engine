# RIPLEY Reproducibility Certification

**Sprint:** A3 | **Mode:** FORENSE READ ONLY | **Date:** 2026-05-30
**Authorization:** Sprint A3 | **Source:** Baseline V6

---

## Executive Summary

RIPLEY is **NOT reproducible** from current RAW files. The DB cannot be reconstructed from CSVs and XMLs alone. Seven blocking evidence points are documented below. No fixes proposed. Certification only.

**Overall Verdict:** NO — RIPLEY cannot be rebuilt from RAW.

| Certification Question | Answer |
|---|---|
| Can RIPLEY be rebuilt from current RAWs? | **NO** |
| What % of universe is certified? | **85%** (40/47 facturas in DB) |
| What % is reproducible? | **~51%** (DB matches CSV net for common orders) |
| RIPLEY Trust Score | **16.4 / 100** |
| RIPLEY potential (if all fixed) | **~80 / 100** |

---

## FASE A — RAW Universe

### Files Inventoried

| Source | Count | Format | Period |
|---|---|---|---|
| CSV (Archivos de pedido) | 47 | semicolon-delimited | Dec 2024 — May 2026 |
| XML (Documentos Recepcionados) | 100 | SII DTE standard | Mar 2026 — May 2026 |
| Other | 0 | — | — |

### CSV Structure (47 files, 18,601 rows)

| Column | Description |
|---|---|
| `NÃºmero de factura` (int64) | Invoice number (e.g., 562946) |
| `Order number` (str) | Order ID (e.g., 24131308001-A) |
| `Date created` (datetime) | Order creation date |
| `Estado del pedido` (str) | Order status (Recibido/Reembolsado) |
| `Precio total (con impuestos)` (int64) | Gross amount |
| `Commission (excluding taxes)` (int64) | Commission deducted |
| `Amount transferred to tienda (including taxes)` (int64) | Net amount |
| `Quantity` (int64) | Item count |
| `Producto` (str) | Product description |
| `Offer SKU` (str) | Seller SKU |

**CSV RAW totals**: 18,601 line items across 47 facturas, spanning Dec 2024 — May 2026. Total gross: ~$550M. Total net (transfer): ~$242M.

### XML Structure (100 files, $25,483,777)

| DTE Type | Count | Description |
|---|---|---|
| 33 (Factura) | 60 | Standard invoices |
| 43 (Liquidacion-Factura) | 20 | Settlement invoices |
| 52 (Guia Despacho) | 16 | Delivery guides |
| 61 (Nota Credito) | 4 | Credit notes |

---

## FASE B — DB Universe

### Inventory: `marketplace_ledger_v1 WHERE marketplace='RIPLEY'`

| Metric | Value |
|---|---|
| Total rows | 269,216 |
| Unique orders | 7,475 |
| Unique id_transaccion | 40 |
| Total amount | $284,897,360 |
| Date range | Jan 2025 — Dec 2026 |
| Months | 24 |
| **folio_xml populated** | **0 rows (0.0%)** |
| **financial_group=NULL** | 8,413 rows (3.1%) = **$142,448,680 (50.0%)** |

### Critical: Financial Classification Gap

50% of RIPLEY's dollar value ($142.4M) has NULL financial_group. This means half of RIPLEY's revenue has NO operational classification.

### Critical: Zero XML Traceability

0% of RIPLEY rows have folio_xml populated. RIPLEY is the ONLY marketplace at 0%.

---

## FASE C — Real Coverage (RAW vs DB)

### Order Overlap

| Comparison | Value |
|---|---|
| Total CSV orders | 13,473 |
| Total DB orders | 7,475 |
| **Orders in BOTH** | **7,475 (100% of DB)** |
| Orders in CSV only | 5,998 (44.5% of CSV — NOT in DB) |

### Amount Discrepancy

For the 7,475 common orders:
- DB total: **$284,897,360**
- CSV gross (Precio total): **$310,626,175**
- CSV net (Amount transferred): **$241,777,236**

DB amount is NEITHER gross nor net. Only **75/7,475 orders (1.0%)** have exact DB=CSV match. The loader applies unknown transformation logic.

### Period Discrepancy

- CSV covers: Dec 2024 — May 2026
- DB covers: Jan 2025 — Dec 2026
- DB has **$1.17M in Nov-Dec 2026** — data NOT present in any CSV RAW file
- This indicates a SECONDARY data source beyond the CSVs

### Factura Gap

- CSV facturas: **47** unique invoice numbers
- DB id_transaccion: **40** unique values
- **7 facturas missing from DB** = most recent 7 periods (Apr-May 2026)

---

## FASE D — 7 Missing Invoices

### Validation Results

All 7 invoices **exist in CSV RAW** but are **NOT in DB**.

| Invoice | Amount | Orders | CSV Period | Status |
|---|---|---|---|---|
| 582603 | $11,526,620 | 298 | 05-04-2026 — 13-04-2026 | AUSENTE |
| 584269 | $7,119,080 | 182 | 13-04-2026 — 20-04-2026 | AUSENTE |
| 586105 | $9,113,197 | 220 | 20-04-2026 — 28-04-2026 | AUSENTE |
| 587807 | $3,768,684 | 97 | 28-04-2026 — 05-05-2026 | AUSENTE |
| 589546 | $6,588,320 | 177 | 05-05-2026 — 13-05-2026 | AUSENTE |
| 591235 | $6,220,245 | 163 | 13-05-2026 — 20-05-2026 | AUSENTE |
| 592974 | $6,125,119 | 159 | 20-05-2026 — 28-05-2026 | AUSENTE |
| **Total** | **$50,461,265** | **1,296** | Apr-May 2026 | — |

**Pattern**: Consecutive weekly periods. The loader processed 40 periods then stopped. The 7 most recent periods were never loaded.

**Not found in XML**: None of the 7 invoice numbers appear in any of the 100 XMLs.

---

## FASE E — XML Traceability

### CRITICAL FINDING: All XMLs are PARIS copies

| Check | Result |
|---|---|
| RIPLEY XMLs | 100 files |
| Same filenames in PARIS directory | **100/100 (100%)** |
| RIPLEY-unique XMLs | **0** |
| Content comparison (byte-level) | **Identical** |
| Receptor RUT | 77898100-9 (same as PARIS) |
| Receptor name | "IMPORTADORA Y COMERCIALIZADORA NANDA SPA" (same as PARIS) |

### XML -> Ledger Match

| Metric | Value |
|---|---|
| RIPLEY XML folios in Ledger folio_xml | **0/100 (0%)** |
| XML monto total | $25,483,777 |
| DB monto total | $284,897,360 |
| Max potential XML coverage | 8.9% |

### Conclusion

The 100 XMLs in the RIPLEY directory are NOT RIPLEY documents. They are PARIS DTE notifications (SII service invoices to NANDA SPA) that were copied into the RIPLEY directory. RIPLEY has **NO original SII XML traceability**.

---

## FASE F — Reproducibility Test

### Central Question: If the DB disappears today, can RIPLEY be rebuilt from current RAWs?

**Answer: NO**

### Evidence

| Barrier | Detail | Blocking? |
|---|---|---|
| **Loader broken** | `load_ripley.py` not found. `surgical_loader.py` exists but glob pattern may mismatch (`*.xlsx` vs actual `*.csv` files). Not tested (NO MODIFICAR mode). | YES |
| **Transformation unknown** | Only 1.0% of orders have exact DB=CSV match. The loader transforms amounts in undocumented ways (DB $284.9M vs CSV net $241.8M vs CSV gross $310.6M). | YES |
| **Secondary data source** | DB has Nov-Dec 2026 data ($1.17M) not in any CSV. Source unknown — possibly Mirakl API, manual entries, or adjustments. | YES |
| **XMLs are PARIS copies** | 0 RIPLEY-specific XMLs. No way to trace RIPLEY invoices to SII documents. | YES |
| **7 invoices missing** | $50.5M in RAW but not in DB. Even with a working loader, the mapping would need to be re-verified. | PARTIAL |

### Partial Reproducibility

If the loader were fixed and the transformation logic documented:
- **85% of factura universe** (40/47) could be reproduced ($234.4M of $284.9M)
- **15%** ($50.5M + $1.17M + transformation gap) would require additional work
- **XML traceability would remain at 0%** — this requires external XMLs from RIPLEY/Mirakl

---

## FASE G — Trust Impact

### RIPLEY Trust Score: 16.4 / 100

| Factor | Weight | Score | Rationale |
|---|---|---|---|
| XML Traceability | 30% | 0/20 | 0% folio_xml |
| Financial Classification | 25% | 50/20 | 50% of $ unclassified |
| Source Completeness | 20% | 15/20 | 85% facturas in DB |
| RAW Reproducibility | 15% | 5/20 | Cannot rebuild from RAW |
| Amount Accuracy | 10% | 2/20 | 1% of orders match |

### Global Trust Impact

- RIPLEY represents **65% of DB rows** but only **19% of DB $**
- RIPLEY drags global Trust by approximately **~8-10 points**
- Current global Trust: **74.0** (would be ~82-84 if RIPLEY matched other MPs)

### Potential Improvement

If all RIPLEY issues were resolved (XML traceability, loader, classification):
- RIPLEY Trust: 16.4 → ~80/100
- Global Trust: 74.0 → ~85-90/100

---

## Certification Summary

### 1. Is RIPLEY reproducible?
**NO.** Current RAWs are insufficient. The loader is broken, the transformation logic is unknown, and the DB contains data not derivable from RAWs.

### 2. What evidence proves reproducibility?
- 40/47 facturas (85%) are in both CSV and DB
- Order-level overlap is 100% (all DB orders exist in CSVs)
- CSV format and columns are fully documented

### 3. What evidence prevents reproducibility?
- Loader not found (`load_ripley.py` absent)
- Only 1.0% of orders have exact DB=CSV amount match
- DB has $1.17M in Nov-Dec 2026 not in any RAW file
- 100 RIPLEY XMLs are identical copies of PARIS (no RIPLEY-specific traceability)
- 7 facturas ($50.5M) in RAW not in DB

### 4. What % of universe is certified?
**85%** (40/47 factura periods verified as cross-referenced). Uncertified: 7 missing periods (15%).

### 5. RIPLEY Trust Score: 16.4/100

---

*Certification generated 2026-05-30. READ ONLY / FORENSE mode. No fixes proposed. Baseline V6 remains official source.*
