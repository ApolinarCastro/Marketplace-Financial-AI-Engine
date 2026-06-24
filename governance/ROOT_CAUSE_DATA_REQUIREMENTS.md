# E3.0 — Root Cause Data Requirements

**Date:** 2026-06-03  
**Mode:** READ ONLY — specification of what data is needed, no implementation

---

## Data Requirement 1: Product Dimension

### Why needed
Without SKU, brand, and category, no PARIS inventory charge can be attributed to a specific product. This blocks 6 of 11 unanswered questions (54%).

### Required Columns

| Column | Type | Example | Source |
|---|---|---|---|
| `sku` | VARCHAR(50) | "PAR-12345-ABC" | PARIS product catalog |
| `brand` | VARCHAR(100) | "Samsung", "Sony" | Product catalog |
| `category` | VARCHAR(100) | "Electrónica", "Moda" | Product catalog |
| `subcategory` | VARCHAR(100) | "Televisores", "Zapatos" | Product catalog |

### Coverage

| Question Blocked | Area |
|---|---|
| Which SKUs generate retiro stock? | PARIS retiro |
| Which brands generate retiro stock? | PARIS retiro |
| Which categories concentrate RIPLEY penalties? | RIPLEY penalidades |
| Which categories generate retiro stock? | PARIS retiro |
| Which SKUs contribute to aging? | PARIS stock antiguo |
| Which categories age most? | PARIS stock antiguo |

### Integration point
The `marketplace_ledger_v1` currently has no column that references a product. To add this dimension, a `sku` column would need to be added to each row, populated from the source system at the time the transaction is recorded.

**Alternative** (no schema change): A bridge table `transaction_product_map` that maps `id_transaccion` → `sku` for PARIS transactions.

---

## Data Requirement 2: Inventory Movement Data

### Why needed
Without inventory levels and storage duration, PARIS charge timing and amount cannot be correlated with actual inventory events.

### Required Columns

| Column | Type | Example | Source |
|---|---|---|---|
| `sku` | VARCHAR(50) | "PAR-12345-ABC" | PARIS product catalog |
| `snapshot_date` | DATE | "2025-09-30" | PARIS WMS |
| `units_in_stock` | INTEGER | 500 | PARIS WMS |
| `days_in_warehouse` | INTEGER | 45 | PARIS WMS |
| `storage_cost` | DECIMAL(12,2) | 1250.00 | PARIS WMS |

### Coverage

| Question Blocked | Area |
|---|---|
| Why does retiro charge interval vary (2-5 months)? | PARIS retiro |
| Why is February 2026 aging charge 2.3x mean? | PARIS stock antiguo |

### Integration point
Inventory snapshot data is typically maintained in a warehouse management system (WMS), not in the financial ledger. A periodic extract (monthly) would be sufficient to correlate with charge timing.

**Recommended approach:** Monthly inventory snapshot table, indexed by `snapshot_date` and `sku`.

---

## Data Requirement 3: Seller Dimension

### Why needed
Without seller ID, RIPLEY penalty events cannot be attributed to specific sellers. Concentration analysis is impossible.

### Required Columns

| Column | Type | Example | Source |
|---|---|---|---|
| `seller_id` | VARCHAR(50) | "RIP_500346" | RIPLEY order system |
| `seller_name` | VARCHAR(200) | "Comercial XYZ Ltda" | Seller master |
| `seller_tier` | VARCHAR(20) | "Gold", "Silver", "Standard" | Seller master |
| `seller_tenure_months` | INTEGER | 24 | Seller master |

### Coverage

| Question Blocked | Area |
|---|---|
| Which sellers cause cancellations? | RIPLEY penalidades |

### Integration point
The RIPLEY `id_transaccion` format (e.g., `RIP_505930_23282306301-A_descuentoporcancelacion`) likely contains a seller reference. The `505930` segment may be an order or seller ID. This would need to be decoded from the source XLSX files, not inferred.

---

## Data Requirement 4: Adjustment Reason Code

### Why needed
ML Poscobro has 634 entries with a single `detalle` value: "Ajuste Poscobro". They range from $289 to $113,970 with no sub-classification. Without reason codes, every adjustment is a black box.

### Required Columns

| Column | Type | Example | Source |
|---|---|---|---|
| `ajuste_reason_code` | VARCHAR(50) | "PAYMENT_GATEWAY_ERROR" | ML XLSX file |
| `ajuste_subcategory` | VARCHAR(50) | "TIMING_MISMATCH" | ML XLSX file |
| `original_transaction_id` | VARCHAR(100) | "TXN-202501-ABC123" | ML payment system |

### Coverage

| Question Blocked | Area |
|---|---|
| What business reason generates each Poscobro adjustment? | ML Poscobro |

### Integration point
The source XLSX files ("1 enero 2025 - 1 julio 2025.xlsx", etc.) likely contain the reason codes in additional columns not loaded into the ledger. The XLSX file contents would need to be parsed to extract this information.

---

## Data Requirement 5: Process Metadata

### Why needed
The 90% drop in Poscobro volume between December 2025 and January 2026 is unexplained. Without process change documentation or XLSX content, the cause is unknowable.

### Required Columns

| Column | Type | Example | Source |
|---|---|---|---|
| `source_filename` | VARCHAR(200) | Already in id_transaccion | ML XLSX |
| `file_generation_date` | DATE | "2025-07-01" | File metadata |
| `process_batch_id` | VARCHAR(50) | "BATCH-2025-H1" | ML system |
| `total_adjustments_in_file` | INTEGER | 450 | ML XLSX |

### Coverage

| Question Blocked | Area |
|---|---|
| Why did Poscobro volume drop 90% after Dec 2025? | ML Poscobro |

### Integration point
The id_transaccion already contains the filename reference. The file contents (columns, formulas, dates) are what's missing. A one-time audit of the 2 source XLSX files would likely answer this.

---

## Minimum Viable Dataset

### Fastest path to 80% resolution

| Priority | What to Add | Effort | Questions Unblocked | Running Total |
|---|---|---|---|---|
| 1 | Parse 2 XLSX files for reason codes | 1-2 days | G10 (1 question) | 1 |
| 2 | Add SKU to PARIS transactions | 2-3 days | G03, G07 (2 questions) | 3 |
| 3 | Add category (from product master) | 1 day | G02, G05, G08 (3 questions) | 6 |
| 4 | Add seller reference | 2-3 days | G01 (1 question) | 7 |
| 5 | Parse XLSX metadata for process change | 1 day | G11 (1 question) | 8 |
| 6 | Inventory snapshots | 1-2 weeks | G06, G09 (2 questions) | 10 |

**Total effort for 91% resolution (10 of 11 questions): approximately 3-4 weeks.**

### What remains unanswered even with all data:
- G06/G09 (PARIS interval + Feb outlier) require inventory movement data which may not exist historically. If PARIS does not keep inventory snapshots, these questions can never be answered retroactively.

---

## Cost of Not Having This Data

| Without This Data | Consequence |
|---|---|
| Product dimension blind | Cannot target inventory optimization at SKU level — must treat all products equally |
| Category dimension blind | Cannot identify product categories that generate disproportionate cost |
| Seller dimension blind | Cannot identify problematic sellers on RIPLEY |
| Adjustment reason blind | Every Poscobro adjustment is a black box — zero forensic capability |
| Process metadata blind | Cannot explain 90% volume drop — no learning from process change |

### Current operational intelligence capability:

```
                      Without Gaps    With Gaps
RIPLEY penalties        100%            20% (can ID event but not who/category)
PARIS retiro stock      100%            20% (can ID date/amount but not SKU)
PARIS stock antiguo     100%            25% (can ID timing but not product)
ML Poscobro             100%            10% (can ID amount but not reason)
```

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
