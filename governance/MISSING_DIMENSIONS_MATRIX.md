# E3.0 — Missing Dimensions Matrix

**Date:** 2026-06-03  
**Mode:** READ ONLY — dimension mapping, no implementation

---

## Matrix: Missing Dimensions × Unanswered Questions

| Dimension | G01 | G02 | G03 | G04 | G05 | G06 | G07 | G08 | G09 | G10 | G11 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Product (SKU)** | | | ✓ | ✓ | | | ✓ | | | | | **3** |
| **Product (Brand)** | | | | ✓ | | | | | | | | **1** |
| **Category** | | ✓ | | | ✓ | | | ✓ | | | | **3** |
| **Seller** | ✓ | | | | | | | | | | | **1** |
| **Inventory level** | | | | | | ✓ | | | ✓ | | | **2** |
| **Adjustment reason** | | | | | | | | | | ✓ | | **1** |
| **Process metadata** | | | | | | | | | | | ✓ | **1** |

### Legend

| G01 | G02 | G03 |
|---|---|---|
| RIPLEY: which sellers? | RIPLEY: which categories? | PARIS retiro: which SKUs? |

| G04 | G05 | G06 |
|---|---|---|
| PARIS retiro: which brands? | PARIS retiro: which categories? | PARIS retiro: why interval varies? |

| G07 | G08 | G09 |
|---|---|---|
| PARIS antiguo: which SKUs? | PARIS antiguo: which categories? | PARIS antiguo: why Feb outlier? |

| G10 | G11 |
|---|---|
| ML Poscobro: business reason? | ML Poscobro: why 90% drop? |

---

## Current Ledger Schema vs Required Schema

### What `marketplace_ledger_v1` Currently Has

| Column | Type | Purpose |
|---|---|---|
| marketplace | VARCHAR | Which MP |
| detalle | VARCHAR | Concept (e.g., "Retiro stock bodega Paris") |
| monto | DECIMAL | Amount |
| fecha | DATE | Transaction date |
| financial_group | VARCHAR | Accounting group |
| id_transaccion | VARCHAR | Transaction reference |

### What Is Missing (for root cause analysis)

| Missing Column | Current Workaround | Why Workaround Fails |
|---|---|---|
| `sku` | Not available | Cannot identify which product caused a charge |
| `category` | Not available | Cannot group charges by business line |
| `seller_id` | Not available | Cannot identify seller responsible for events |
| `reason_code` | Not available | Cannot subclassify "Ajuste Poscobro" |
| `order_id` (original) | Only adjustment ID | Cannot link adjustment to original transaction |
| `inventory_level` | Not available | Cannot correlate charge amount with stock position |

---

## Impact Assessment

### If Product Dimension (SKU + Brand) Were Available

| Question | Current State | With Product Dimension |
|---|---|---|
| G03: Which SKUs generate retiro? | BLIND | Know exact SKUs driving cost |
| G04: Which brands? | BLIND | Know brand concentration of retiros |
| G07: Which SKUs age? | BLIND | Know which products accumulate aging cost |
| **Action enabled** | Guesswork | Target specific SKUs for inventory optimization |

### If Category Dimension Were Available

| Question | Current State | With Category Dimension |
|---|---|---|
| G02: Which categories concentrate penalties? | BLIND | Know which product types cause RIPLEY penalties |
| G05: Which categories generate retiro? | BLIND | Know which product categories drive PARIS retiro cost |
| G08: Which categories age most? | BLIND | Know which categories accumulate aging charges |
| **Action enabled** | Blind portfolio | Prioritized category-level inventory management |

### If Inventory Movement Data Were Available

| Question | Current State | With Inventory Data |
|---|---|---|
| G06: Why interval varies? | BLIND | Correlate charge timing with stock-out events |
| G09: Why Feb outlier? | BLIND | Identify if stock spike or aging event caused it |
| **Action enabled** | Unexplained timing | Predictable inventory planning |

---

## Dimensionality Cost-Benefit

| Dimension | Questions Unblocked | % of 11 | Implementation Difficulty |
|---|---|---|---|
| Product (SKU) | 3 | 27% | Medium — requires PARIS product catalog integration |
| Category | 3 | 27% | Low — derived from SKU or product master |
| Inventory level | 2 | 18% | High — requires periodic inventory snapshots from PARIS WMS |
| Seller | 1 | 9% | Medium — requires RIPLEY seller master |
| Adjustment reason | 1 | 9% | Low — requires ML to provide reason codes in XLSX |
| Process metadata | 1 | 9% | Low — requires saving XLSX content vs just reference |

### Cumulative Resolution by Adding Dimensions

```
Questions Resolved
│
10  ┤                          ┌── 10 (Seller + Reason + Metadata)
9   ┤                    ┌─────┤
8   ┤              ┌─────┤     │
7   ┤              │     │     │
6   ┤        ┌─────┤     │     │
5   ┤        │     │     │     │
4   ┤  ┌─────┤     │     │     │
3   ┤  │     │     │     │     │
2   ┤  │     │     │     │     │
1   ┤  │     │     │     │     │
0   ──┴──┴──┴──┴──┴──┴──┴──┴──┴──
        SKU  Cat  Inv  Sell Reas Meta
        27%  54%  73%  82%  91%  100%

SKU = Product dimension (SKU + brand)
Cat = Category dimension
Inv = Inventory movement data
Sell = Seller dimension
Reas = Adjustment reason code
Meta = Process metadata
```

---

## Conclusion

**Without 3 core dimensions (product, category, inventory), 73% of root cause questions cannot be answered.**

The `marketplace_ledger_v1` is optimized for financial reporting, not operational analysis. Adding 4-5 columns would enable:
- SKU-level cost attribution (PARIS)
- Category-level concentration analysis (all MPs)
- Seller-level penalty tracking (RIPLEY)
- Reason-based adjustment classification (ML)

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
