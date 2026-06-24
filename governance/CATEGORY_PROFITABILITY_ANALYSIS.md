# G5.4 — Category Profitability Analysis

**Date:** 2026-06-03  
**Scope:** Analyze profitability by concept category across all 4 marketplaces  
**Method:** Since no vertical/category dimension exists in the ledger, we analyze by concept family and marketplace as pseudo-categories  
**Note:** Without product-level category data (SKU → category mapping), this analysis is at the economic concept level.

---

## I. Category Profitability by Concept Family

### Concept Family: COMMISSIONS

| Marketplace | Gross Commission | Reversals | Net | Effective Rate | Profitability Score |
|---|---|---|---|---|---|
| RIPLEY | $64,158,492 | $15,081,784 | $49,076,708 | 13.9% | ★★★★ (Core revenue) |
| ML | $121,986,523 | $12,595,193 | $109,391,330 | 12.5% | ★★★★ (Core revenue) |
| FALABELLA | $932,359 | $190,709 | $741,650 | 15.9% | ★★★★ (Core revenue) |
| PARIS | Implicit ($48.7M) | N/A | ~$48.7M | ~9.3% | ★★★ (Implicit) |
| **Total** | **$187,077,374** | **$27,867,686** | **$159,209,688** | **Variable** | |

**Verdict:** Commissions are the **primary profit engine** for all 3rd-party marketplaces. They generate the most predictable, high-margin revenue.

### Concept Family: LOGISTICS

| Marketplace | Gross Logistics | Reversals | Net | Margin Character | Profitability Score |
|---|---|---|---|---|---|
| RIPLEY | $31,206,648 | $1,689,874 | $30,875,985 | Pass-through + fee | ★★ (Break-even + fee) |
| ML | $72,769,531 | $6,263,473 | $67,662,878 | Cost to Eccsa | ★ (Cost center) |
| PARIS | $24,578,542 | — | $24,578,542 | Cost to Eccsa | ★ (Cost center) |
| FALABELLA | $956,276 | $572,686 | $383,590 | Cost to Eccsa | ★ (Cost center) |
| **Total** | **$129,510,997** | **$8,526,033** | **$123,500,995** | | |

**Verdict:** Logistics is a **cost center** for most marketplaces. RIPLEY is the exception where it generates a fee margin. For ML, PARIS, and FALABELLA, logistics costs are real third-party expenses.

### Concept Family: ADVERTISING (ML only)

| Ad Type | Amount | % of Total Ads | ROI to Eccsa | Profitability Score |
|---|---|---|---|---|
| Product Ads | $21,681,625 | 45.3% | High — direct conversion | ★★★★★ |
| Display | $19,023,802 | 39.8% | Medium — brand awareness | ★★★★ |
| Brand Ads | $7,066,148 | 14.8% | Medium — brand campaigns | ★★★★ |
| Display programático | $119,586 | 0.3% | Low — experimental | ★★ |
| **Total** | **$47,891,161** | **100.0%** | | |

**Verdict:** Advertising is **high-margin revenue** for ML with near-zero marginal cost. Product Ads are the most profitable format.

### Concept Family: RETURNS

| Marketplace | Return Amount | Return Rate | Cost Character | Profitability Score |
|---|---|---|---|---|
| PARIS | $131,893,037 | 25.1% | Pass-through | ★ (Zero margin) |
| RIPLEY | $82,896,873 | 23.5% | Pass-through | ★ (Zero margin) |
| ML | $93,009,601 | 10.6% | Pass-through | ★ (Zero margin) |
| FALABELLA | $953,554 | 20.5% | Pass-through | ★ (Zero margin) |
| **Total** | **$308,753,065** | **17.6% avg** | | |

**Verdict:** Returns are **zero-margin pass-through** but have a logistics cost that Eccsa may absorb. ML's 10.6% return rate is best-in-class.

### Concept Family: ADJUSTMENTS (ML)

| Type | Amount | Nature | Profitability Score |
|---|---|---|---|
| Buyer Protection (bpp_refunded) | $93,999,912 | Credit to seller | ★★ (Cost — but customer retention) |
| Quality (bigger/smaller/reconciled) | $139,117,050 | Credit for service failures | ★ (Cost — prevention opportunity) |
| Buyer remorse (repentant, dont_want) | $30,173,852 | Credit to buyer via seller | ★ (Cost — inherent to retail) |
| Delivery failures (undelivered) | $13,285,940 | Credit to seller | ★ (Cost — service failure) |
| Other adjustments | $30,029,496 | Misc credits | ★★ |
| **Total** | **$306,606,250** | **35.0% of GMV** | |

**Verdict:** Adjustments are a **massive cost center** for ML that destroys margin. Quality-related adjustments ($139M) are the biggest opportunity for reduction.

---

## II. Category Profitability by Marketplace

| Marketplace | GMV | Revenue | Cost of Revenue | P&L | Margin Type |
|---|---|---|---|---|---|
| RIPLEY | $353.2M | $63.3M (take) | $0 (platform only) | $63.3M | Fee-based |
| PARIS | $532.9M | $532.9M* | $154.8M | $378.1M | Full P&L* |
| ML | $875.8M | $339.4M (gross) | $306.6M (adj.) | $32.8M | Net fee |
| FALABELLA | $4.7M | $1.1M | $0 (platform only) | $1.1M | Fee-based |

*PARIS is 1st party — "revenue" includes product cost.

### Which Categories Fund the Business?

| Rank | Concept Family | Net Contribution | % of Total |
|---|---|---|---|
| 1 | **Comisiones ML** | $109.4M | 23.0% |
| 2 | **Comisiones RIPLEY** | $49.1M | 10.3% |
| 3 | **Publicidad ML** | $47.9M | 10.1% |
| 4 | **Logística RIPLEY** | $14.2M | 3.0% |
| 5 | **Comisiones FALABELLA** | $0.74M | 0.2% |

### Which Categories Destroy Margin?

| Rank | Concept Family | Net Cost | % of GMV | Opportunity |
|---|---|---|---|---|
| 1 | **ML Adjustments** | $306.6M | 35.0% | Largest savings opportunity |
| 2 | **Devoluciones (all MPs)** | $308.8M | 17.5% | Reduce return rate by 5% = $88M |
| 3 | **Logística ML** | $67.7M | 7.7% | Rate negotiation |
| 4 | **Logística PARIS** | $24.6M | 4.6% | Consolidation |
| 5 | **Logística RIPLEY** | $14.2M | 4.0% | Already efficient |

---

## III. The One Number That Matters

**$306,606,250** — ML adjustments.

This single number destroys more margin than any other concept. It is 9.3× the absolute revenue of RIPLEY commissions. Every 1% reduction in ML adjustment rate recovers ~$8.8M.

**Second number: $308,753,065** — Devoluciones across all MPs. Every 1% reduction in return rate recovers ~$17.7M.

### Combined Opportunity

| Initiative | 5% Improvement | 10% Improvement |
|---|---|---|
| Reduce ML adjustment rate | +$15.3M | +$30.7M |
| Reduce return rate | +$15.4M | +$30.9M |
| Renegotiate logistics | +$5.3M | +$10.5M |
| **Total** | **+$36.0M** | **+$72.1M** |

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
