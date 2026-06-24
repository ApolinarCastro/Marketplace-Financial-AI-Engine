# E3.0 — Operational Data Gap Certification

**Date:** 2026-06-03  
**Mode:** READ ONLY — gap identification, no schema changes

---

## FASE 1 — All Unanswered Questions from E2.0

E2.0 analyzed 19 causality questions across 4 areas. 11 (58%) could not be demonstrated due to missing operational data. This document identifies exactly what data is missing.

### Area: RIPLEY Penalidades (2 questions not demonstrated)

| # | Question | Why unanswered |
|---|---|---|
| G01 | Which sellers cause cancellations that generate "Descuento por cancelación"? | No seller ID in ledger |
| G02 | Which product categories concentrate cancellation events? | No category dimension in ledger |

### Area: PARIS Retiro Stock (4 questions not demonstrated)

| # | Question | Why unanswered |
|---|---|---|
| G03 | Which SKUs generate retiro stock charges? | No SKU dimension in ledger |
| G04 | Which brands generate retiro stock charges? | No brand dimension in ledger |
| G05 | Which product categories generate retiro stock charges? | No category dimension in ledger |
| G06 | What causes the 2-5 month interval variation between charges? | No inventory movement data to correlate charge timing with stock levels |

### Area: PARIS Stock Antiguo (3 questions not demonstrated)

| # | Question | Why unanswered |
|---|---|---|
| G07 | Which SKUs contribute to aging inventory charges? | No SKU dimension in ledger |
| G08 | Which product categories age most? | No category dimension in ledger |
| G09 | Why is February 2026 an outlier (2.3x mean charge)? | No inventory level data to verify stock spike or aging event |

### Area: ML Ajuste Poscobro (2 questions not demonstrated)

| # | Question | Why unanswered |
|---|---|---|
| G10 | What is the business reason for each Poscobro adjustment? | No reason code/category in ledger |
| G11 | Why did Poscobro volume drop 90% after December 2025? | No process change metadata or XLSX content data |

---

## FASE 2 — Missing Data per Question

| ID | Question | Missing Data Field | Probable Source System |
|---|---|---|---|
| G01 | Which sellers cause cancellations? | `seller_id` | RIPLEY order management |
| G02 | Which categories concentrate penalties? | `category_id` or `category_name` | Product catalog |
| G03 | Which SKUs generate retiro stock? | `sku` | PARIS inventory system |
| G04 | Which brands generate retiro stock? | `brand` | Product catalog |
| G05 | Which categories generate retiro stock? | `category_id` | Product catalog |
| G06 | Why interval varies 2-5 months? | `inventory_level` (per SKU, per date) | PARIS inventory system |
| G07 | Which SKUs contribute to aging? | `sku` | PARIS inventory system |
| G08 | Which categories age most? | `category_id` | Product catalog |
| G09 | Why Feb 2026 is outlier? | `inventory_age` (days in storage per SKU) | PARIS warehouse management |
| G10 | Business reason for Poscobro? | `ajuste_reason_code` | ML reconciliation system |
| G11 | Why 90% Poscobro drop? | `process_change_log` or XLSX file content | ML operations / file archive |

---

## FASE 3 — Gap Matrix

| Dimension | Questions Blocked | Areas Affected | Data Not in Ledger |
|---|---|---|---|
| **Product (SKU)** | G03, G04, G07 = 3 | PARIS retiro, PARIS antiguo | SKU, brand, category |
| **Category** | G02, G05, G08 = 3 | RIPLEY, PARIS retiro, PARIS antiguo | category_id |
| **Seller/Vendor** | G01 = 1 | RIPLEY | seller_id |
| **Inventory level** | G06, G09 = 2 | PARIS retiro, PARIS antiguo | stock level per SKU, storage duration |
| **Adjustment reason** | G10 = 1 | ML Poscobro | reason code / subcategory |
| **Process metadata** | G11 = 1 | ML Poscobro | change log, file contents |

### Dimension Frequency

| Missing Dimension | Questions Blocked | Frequency |
|---|---|---|
| Product (SKU/brand) | 3 | ★★★ |
| Category | 3 | ★★★ |
| Inventory movement | 2 | ★★ |
| Seller | 1 | ★ |
| Reason code | 1 | ★ |
| Process metadata | 1 | ★ |

---

## FASE 4 — Classification

### CRÍTICO (blocks root cause for 3+ questions)

| Dimension | Questions | Impact |
|---|---|---|
| **Product dimension** | G03, G04, G07 | Without SKU and brand, PARIS inventory charges are blind — no way to identify which products generate cost |
| **Category dimension** | G02, G05, G08 | Without category, no cross-MP pattern detection. All three areas depend on this |

### IMPORTANTE (blocks root cause for 2 questions)

| Dimension | Questions | Impact |
|---|---|---|
| **Inventory movement data** | G06, G09 | Without inventory levels and storage duration, PARIS charge timing and amount variation is unexplainable |

### DESEABLE (blocks root cause for 1 question)

| Dimension | Questions | Impact |
|---|---|---|
| **Seller dimension** | G01 | RIPLEY penalty concentration analysis |
| **Adjustment reason code** | G10 | ML Poscobro forensic classification |
| **Process metadata** | G11 | Poscobro regime change explanation |

---

## FASE 5 — Minimal Dataset to Answer 80% of Unanswered Questions

### Current state:
11 questions unanswered (58%)

### With Product + Category dimensions:
- Unblocks: G02, G03, G04, G05, G07, G08 = **6 questions**
- Remaining: G01, G06, G09, G10, G11 = **5 questions**
- **Resolution rate: 54%** (6 of 11)

### With Product + Category + Inventory movement:
- Unblocks: G02, G03, G04, G05, G06, G07, G08, G09 = **8 questions**
- Remaining: G01, G10, G11 = **3 questions**
- **Resolution rate: 73%** (8 of 11)

### With Product + Category + Inventory + Seller:
- Unblocks: G01, G02, G03, G04, G05, G06, G07, G08, G09 = **9 questions**
- Remaining: G10, G11 = **2 questions**
- **Resolution rate: 82%** (9 of 11)

### Minimal dataset required for 80% resolution:

| Table | Columns Needed | Source | Priority |
|---|---|---|---|
| `product_master` | `sku`, `brand`, `category_id`, `category_name` | Product catalog | CRÍTICO |
| `inventory_snapshot` | `sku`, `storage_date`, `quantity`, `days_in_warehouse` | PARIS WMS | IMPORTANTE |
| `seller_master` | `seller_id`, `seller_name`, `seller_tier` | RIPLEY system | DESEABLE |

**These 3 tables with 9 columns would enable answering 82% of unanswered questions.**

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
