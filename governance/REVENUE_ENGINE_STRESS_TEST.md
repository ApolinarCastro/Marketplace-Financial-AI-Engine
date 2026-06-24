# G5.6 — Revenue Engine Stress Test

**Date:** 2026-06-03  
**Mode:** READ ONLY — analysis only, no modifications to DB  
**Method:** Simulated stress on known GMV and revenue drivers at -10%, -20%, -30%

---

## FASE 3 — Stress Test Scenarios

### RIPLEY Stress Test

| Metric | Current | -10% | -20% | -30% |
|---|---|---|---|---|
| GMV | $353,160,324 | $317,844,292 | $282,528,259 | $247,212,227 |
| Commission revenue | -$63,316,608 | -$56,984,947 | -$50,653,286 | -$44,321,626 |
| Logistics revenue | -$14,206,460 | -$12,785,814 | -$11,365,168 | -$9,944,522 |
| Penalties | -$33,440 | -$30,096 | -$26,752 | -$23,408 |
| **NET REVENUE** | **-$77,556,508** | **-$69,800,857** | **-$62,045,206** | **-$54,289,556** |
| Take rate | **17.9%** | **17.9%** | **17.9%** | **17.9%** |

**Interpretation:** RIPLEY's take rate is fixed (not discretionary). Stress = linear. At -30% GMV, revenue drops proportionally. No structural weakness — the model scales linearly with volume.

**Break-even for RIPLEY:** Not applicable — RIPLEY has zero cost of goods sold as a 3P marketplace. Revenue = profit at every GMV level.

### ML Stress Test

| Metric | Current | -10% | -20% | -30% |
|---|---|---|---|---|
| GMV | $875,809,123 | $788,228,211 | $700,647,298 | $613,066,386 |
| Gross charges | $339,400,328 | $305,460,295 | $271,520,262 | $237,580,230 |
| Adjustments (-90.3%) | $306,606,250 | $275,945,625 | $245,285,000 | $214,624,375 |
| **NET REVENUE** | **$32,794,078** | **$29,514,670** | **$26,235,262** | **$22,955,855** |

**Dual stress — adjustment ratio scenarios:**

| Scenario | Net Revenue (-10% GMV) | % Change |
|---|---|---|
| Current: 90.3% adj ratio, -10% GMV | $29,514,670 | -10.0% |
| Worsened: 93% adj ratio, -10% GMV | $22,695,769 | -30.8% |
| Improved: 80% adj ratio, -10% GMV | $61,092,059 | +86.3% |

**Interpretation:** ML's net revenue is extremely sensitive to the adjustment ratio. A 3-point change in adjustment ratio (90.3% → 93%) effectively creates a -30.8% revenue impact — 3× the GMV impact. The business has a structural vulnerability: fee erosion via adjustment programs.

**Break-even adjustment ratio for ML:**
- At current GMV: adjustments cannot exceed 100% of gross charges (currently 90.3%)
- At 100% adjustment ratio: net = $0
- At 90.3%: net = $32.8M (3.7% take rate)
- Safety margin: only 9.7% of gross charges before $0

### PARIS Stress Test

| Metric | Current | -10% | -20% | -30% |
|---|---|---|---|---|
| Venta | $525,039,911 | $472,535,920 | $420,031,929 | $367,527,938 |
| Despacho | $7,888,014 | $7,099,213 | $6,310,411 | $5,521,610 |
| Returns (-25.1%) | -$131,893,037 | -$118,703,733 | -$105,514,430 | -$92,325,126 |
| Logistics (-4.6%) | -$24,578,542 | -$22,120,688 | -$19,662,834 | -$17,204,979 |
| **P&L NETO** | **$378,104,933** | **$340,294,440** | **$302,483,946** | **$264,673,453** |
| % of sales | **70.9%** | **70.9%** | **70.9%** | **70.9%** |

**Interpretation:** PARIS's return and logistics ratios are proportional to sales. No non-linear stress. However, COGS is invisible — if product margin is thin, revenue drop could become a loss.

**Break-even for PARIS:**
- P&L Neto = Venta - Returns - Logistics - (product cost)
- Product cost NOT in DB — cannot compute true break-even
- Surface-level break-even: impossible (revenue always < cost visibility)

### FALABELLA Stress Test

| Metric | Current | -10% | -20% | -30% |
|---|---|---|---|---|
| GMV | $4,661,810 | $4,195,629 | $3,729,448 | $3,263,267 |
| Net revenue | -$1,125,240 | -$1,012,716 | -$900,192 | -$787,668 |
| Take rate | **24.1%** | **24.1%** | **24.1%** | **24.1%** |

**Interpretation:** Linear scaling. At $3.3M GMV, revenue drops to $0.79M. At FALABELLA's scale, the stress is immaterial — total impact at -30% is only $337,572 lost revenue.

---

## FASE 4 — Risk Heatmap

| Marketplace | Linear Stress | Non-linear Risk | Break-even Visibility | Resilience Score |
|---|---|---|---|---|
| **RIPLEY** | ✓ Linear | None | Unlimited (0 COGS) | **95/100** |
| **PARIS** | ✓ Linear | COGS invisible | Unknown | **50/100** |
| **ML** | ✗ Non-linear | Adjustment ratio risk | 9.7% margin | **30/100** |
| **FALABELLA** | ✓ Linear | Irrelevant scale | Unlimited (3P) | **90/100** |

**Key finding:** ML's net revenue is 3× more sensitive to the adjustment ratio than to GMV changes. This is the single largest financial vulnerability in the marketplace portfolio.

---

## Summary

| Metric | RIPLEY | PARIS | ML | FALABELLA |
|---|---|---|---|---|
| -10% GMV impact | -$6.33M | -$37.81M | -$3.28M | -$0.11M |
| -30% GMV impact | -$19.0M | -$113.4M | -$9.8M | -$0.34M |
| Non-linear risk | None | COGS hidden | Adj ratio (3×) | None |
| Recovery levers | None needed | COGS optimization | Reduce adj ratio | Grow scale |

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
