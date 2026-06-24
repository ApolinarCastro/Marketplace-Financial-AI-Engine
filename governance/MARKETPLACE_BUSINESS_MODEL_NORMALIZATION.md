# G5.5A — Marketplace Business Model Normalization

**Date:** 2026-06-03  
**Objective:** Certify that all economic comparisons between marketplaces use equivalent metrics  
**Problem:** The current data mixes 1st-party, 3rd-party, and hybrid business models in a single ledger. Direct comparison of "profitability" is economically invalid.  
**Solution:** A normalized economic framework.

---

## I. The Three Business Models

### Model 1: First-Party (1P) — PARIS

```
┌─────────────────────────────────────────────────────┐
│                    ECCSA                             │
│  ┌──────────────────────────────────────┐            │
│  │  PARIS Marketplace                    │            │
│  │  • Eccsa is the SELLER               │            │
│  │  • Eccsa owns inventory              │            │
│  │  • Eccsa sets prices                 │            │
│  │  • Eccsa takes full revenue          │            │
│  │  • Eccsa bears COGS (not in ledger)  │            │
│  └──────────────────────────────────────┘            │
│                                                      │
│  Ledger records: Full transaction flow               │
│  "Profit" = Venta - Devolución - Costos              │
│  BUT: COGS is NOT recorded — ledger looks inflated   │
└─────────────────────────────────────────────────────┘
```

**Accounting identity:** `Venta($525M) - Devolución($132M) - Logística($25M) + Ajustes($2M) = $378M P&L`  
**Reality:** The $378M includes product markup. Actual marketplace margin is lower.

### Model 2: Third-Party (3P) — RIPLEY, FALABELLA

```
┌─────────────────────────────────────────────────────────┐
│  BUYER ──$353M──→ ECCSA ──$207M──→ SELLER               │
│                    (RIPLEY)                              │
│                      │                                   │
│                      ├── $63M → Commissions + Fees       │
│                      ├── $83M → Returns to buyers        │
│                      └── $0   → Pass-through logistics   │
│                                                          │
│  Ledger records: Seller's perspective                   │
│  "A Pagar" = Net settlement to seller                    │
│  Marketplace revenue = GMV - A Pagar - Returns           │
└─────────────────────────────────────────────────────────┘
```

**Accounting identity:** `Importe($353M) + Envío($18M) - Devoluciones($83M) - Comisiones($49M) - Logística($31M) ± Ajustes($0) = A Pagar($207M)`  
**Marketplace revenue:** `Comisiones + Logística fees + Penalidades = $63M`

### Model 3: Hybrid with Adjustments — ML

```
┌────────────────────────────────────────────────────────┐
│  BUYER ──$876M──→ MERCADO LIBRE ──$??M──→ SELLER       │
│                    (ML)                                 │
│                      │                                  │
│                      ├── $339M → Gross charges          │
│                      │   (commissions, logistics, ads)  │
│                      ├── $307M ← Adjustments (BPP, etc.)│
│                      ├── $ 33M → Net marketplace revenue│
│                      └── $843M → Seller net (ledger)    │
│                                                         │
│  Ledger records: Partial seller perspective             │
│  NO "A Pagar" — settlement is external                  │
│  Adjustments = 90.3% of gross charges returned          │
└────────────────────────────────────────────────────────┘
```

**Accounting identity:** `Venta($876M) - Devoluciones($93M) - Comisiones($109M) - Logística($67M) - Ads($48M) - Otros($22M) + Ajustes($307M) = $842M`  
**Net marketplace revenue:** `Gross charges($339M) - Adjustments($307M) = $33M`

---

## II. Normalized Economic Framework

### Metric: GMV (Gross Merchandise Value)

| Marketplace | GMV Definition | Value | Comparable? |
|---|---|---|---|
| RIPLEY | Importe del pedido | $353,160,324 | **YES** — product sales |
| PARIS | Venta | $525,039,911 | **YES** — product sales, same concept |
| ML | Cargo por venta (Venta) | $875,809,123 | **YES** — product sales |
| FALABELLA | Pago por precio del producto | $4,661,810 | **YES** — product sales |

**GMV IS comparable across all 4 marketplaces.** It represents the total value of products transacted.

**Total platform GMV: $1,758,671,168**

### Metric: Net Marketplace Revenue (NMR)

| Marketplace | Revenue Definition | Value | Includes |
|---|---|---|---|
| RIPLEY | Sum of charges to sellers (comisiones + logística fees + penalidades) | $63,316,608 | Pure marketplace fees |
| PARIS | Commission only (estimated from XML, NOT from ledger) | ~$48,722,169 | Commission implicit in P&L spread |
| ML | Gross charges minus adjustments | $32,794,078 | Net after $306.6M adjustments |
| FALABELLA | Sum of charges (comisiones + logística fees) | $1,125,240 | Pure marketplace fees |

**NMR is NOT directly comparable** because:
- PARIS figure is estimated (XML), not from ledger
- ML is net of adjustments; gross is $339M (11× higher)
- RIPLEY and FALABELLA are "gross" (no significant adjustments)

### Metric: "Profit" — NOT Comparable Across Models

| Marketplace | Ledger "Profit" | What it actually means | Comparable? |
|---|---|---|---|
| RIPLEY | $206,946,843 (P&L Neto) | This is the seller's profit, not Eccsa's | **NO** — other MP |
| PARIS | $378,104,933 (P&L Neto) | Full P&L including product margin | **NO** — 1P vs 3P |
| ML | $842,250,301 (P&L Neto) | Seller's ledger balance, not profit | **NO** — other MP |
| FALABELLA | $2,583,016 (P&L Neto) | Seller's perspective, not Eccsa's | **NO** — same issue |

**The ledger's "P&L Neto" is the seller's view, NOT the marketplace operator's profit.** Comparing these numbers across marketplaces is economically invalid.

### Metric: A Pagar (Settlement to Seller)

| Marketplace | Value | Comparable? |
|---|---|---|
| RIPLEY | $206,946,843 | **YES** — explicit in ledger |
| PARIS | $0 | **NO** — 1P model (no external seller) |
| ML | $0 | **NO** — not recorded in this ledger |
| FALABELLA | $0 | **NO** — not recorded in this ledger |

**A Pagar is ONLY comparable for RIPLEY.** Other marketplaces don't record seller settlement in this DB.

---

## III. Normalized Metrics Table

### What IS Comparable

| Metric | RIPLEY | PARIS | ML | FALABELLA | Unit |
|---|---|---|---|---|---|
| **GMV** | $353.2M | $525.0M | $875.8M | $4.7M | $ |
| **Transactions (rows)** | 62,502 | 42,487 | 101,603 | 1,008 | count |
| **Avg ticket per row** | $5,655 | $8,899 | $15,998 | $2,562 | $ |
| **Return rate (% of GMV)** | 23.5% | 25.1% | 10.6% | 20.5% | % |
| **Total marketplace charges** | $63.3M | ~$48.7M* | $339.4M (gross) | $1.1M | $ |
| **Take rate (charges/GMV)** | 17.9% | ~9.3%* | 38.8% (gross) | 24.1% | % |

*PARIS commission estimated from XML, not ledger

### What is NOT Comparable (without normalization)

| Metric | RIPLEY | PARIS | ML | FALABELLA | Why not comparable |
|---|---|---|---|---|---|
| P&L Neto (ledger) | $206.9M | $378.1M | $842.3M | $2.6M | Different perspectives (seller vs operator) |
| A Pagar | $206.9M | $0 | $0 | $0 | Only RIPLEY records settlement |
| Adjustments | $0.03M | $0.04M | $306.6M | $0.001M | ML has unique program structure |
| Logística costs | $31.2M | $24.6M | $72.8M | $0.7M | Different levels of marketplace vs self-managed |

---

## IV. Normalization Methodology

### Step 1: Classify Each Marketplace

| MP | Type | Economic Perspective |
|---|---|---|
| RIPLEY | **3P Pure** | Earner of fees |
| PARIS | **1P Pure** | Earner of product margin + platform margin |
| ML | **3P with Adjustments** | Earner of fees, net of credits |
| FALABELLA | **3P Pure** | Earner of fees |

### Step 2: Use GMV as Universal Denominator

All percentage comparisons must use GMV as the base, not ledger totals or P&L numbers.

### Step 3: Separate 1P from 3P for Margin Analysis

- **3P comparison group:** RIPLEY, ML, FALABELLA
- **1P standalone:** PARIS
- **Cross-group comparison:** GMV, return rates, avg ticket ONLY

### Step 4: Adjust ML Gross vs Net

ML has two valid metrics:
- **Gross take rate (38.8%):** What Eccsa CHARGES before adjustments
- **Net take rate (3.7%):** What Eccsa KEEPS after adjustments

Both are valid but must be labelled clearly.

### Step 5: Normalize PARIS Commission

For PARIS, extract the marketplace commission from the implicit P&L spread. Use XML evidence ($48.7M) as the estimate.

---

## V. The Five Invalid Comparisons (Do Not Do)

| Invalid Comparison | Why |
|---|---|
| "PARIS is 4× more profitable than RIPLEY" | PARIS includes product margin; RIPLEY is pure fee |
| "ML has 96% P&L margin" | That's the seller's ledger balance, not Eccsa's profit |
| "FALABELLA take rate (24%) is better than ML (4%)" | ML net is after $307M adjustments; gross is 39% |
| "RIPLEY A Pagar ($207M) = seller profit" | A Pagar is cash flow, not profit — seller still has COGS |
| "Total platform profit = sum of ledgers ($1.6B)" | Ledger totals are NOT profit — they include amounts owed to sellers |

---

## VI. Correct Comparison Table

| Metric | RIPLEY (3P) | PARIS (1P) | ML (3P adj.) | FALABELLA (3P) |
|---|---|---|---|---|
| Business model | Pure 3P | Pure 1P | 3P + adjustments | Pure 3P |
| GMV | $353.2M | $525.0M | $875.8M | $4.7M |
| Gross marketplace revenue | $63.3M | *~$48.7M (est.)* | $339.4M | $1.1M |
| Adjustments | -$0.03M | $0 | -$306.6M | $0 |
| Net marketplace revenue | $63.3M | *~$48.7M (est.)* | $32.8M | $1.1M |
| Gross take rate | 17.9% | ~9.3% | 38.8% | 24.1% |
| Net take rate | 17.9% | ~9.3% | 3.7% | 24.1% |
| Return rate | 23.5% | 25.1% | 10.6% | 20.5% |
| Comparable group | **3P Group** | **Standalone** | **3P Group** | **3P Group** |

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
