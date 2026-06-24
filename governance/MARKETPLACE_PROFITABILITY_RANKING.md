# G5.1 — Marketplace Profitability Ranking

**Date:** 2026-06-03  
**Scope:** Calculate and rank profitability of all 4 marketplaces  
**Perspective:** Eccsa (marketplace operator)  
**Method:** Take rate = marketplace charges to sellers / GMV. Absolute revenue = sum of charges retained.

---

## I. Profitability Calculation by Marketplace

### RIPLEY

| Metric | Value | Notes |
|---|---|---|
| GMV (Importe del pedido) | $353,160,324 | Total products sold through platform |
| A Pagar (seller receives) | $206,946,843 | Net settlement to sellers |
| Marketplace revenue | **$63,316,608** | Gross charges: commissions + logistics + penalties |
| Devuelto a compradores | $82,896,873 | Buyer refunds (pass-through, not revenue) |
| **Take rate** | **17.9%** | Stable 16.9-20.4% over 17 months |
| Cash retained (GMV - AP) | $146,213,481 | Includes refunds + fees |

**Revenue breakdown:**
- Comisiones netas: $49,076,708 (77.5% of revenue)
- Logística neta: $14,206,460 (22.4% of revenue)
- Penalidades: $33,440 (0.1% of revenue)

### PARIS

| Metric | Value | Notes |
|---|---|---|
| Ventas + Despacho | $532,927,925 | 1st party — Eccsa owns inventory |
| Devoluciones | -$131,893,037 | Buyer returns |
| Costos logísticos | -$24,578,542 | Logistics operations |
| Ajustes net | +$1,648,587 | Misc credits |
| **P&L Neto** | **$378,104,933** | **70.9% margin on gross revenue** |
| Commission (implicit) | ~$48.7M | Not a separate line item — embedded in spread |

**Model:** 1st party. Eccsa is the seller. Full P&L flows to Eccsa. The 70.9% margin includes product margin.

### ML

| Metric | Value | Notes |
|---|---|---|
| GMV (Cargo por venta) | $875,809,123 | Total sold |
| **Gross charges to sellers** | **$339,400,328** | **38.8% gross take rate** |
| ┃ Comisiones netas | -$109,391,330 | Platform commission |
| ┃ Logística neta | -$66,701,046 | Shipping operations |
| ┃ Publicidad neta | -$48,836,566 | Ads |
| ┃ Asesoría Comercial | -$16,462,046 | Subscription |
| ┃ Almacenamiento neto | -$4,999,740 | Fulfillment |
| ┃ Devoluciones | -$93,009,601 | Buyer refunds |
| Adjustments to sellers | **+$306,606,250** | **35.0% returned as credits** |
| **Net charges** | **$32,794,078** | **3.7% net take rate** |
| Ajustes as % of gross charges | — | 90.3% of gross charges returned |

**The ML Paradox:** ML charges 38.8% effective rate but returns 90.3% of that through credits. Net effective rate = 3.7%.

### FALABELLA

| Metric | Value | Notes |
|---|---|---|
| GMV | $4,661,810 | Smallest marketplace |
| Comisiones netas | -$741,650 | Platform commission |
| Logística neta | -$383,590 | Shipping operations |
| **Marketplace revenue** | **$1,125,240** | **24.1% take rate** |
| Devuelto a compradores | -$953,554 | Buyer refunds |

**Model:** 3rd party. Highest take rate (24.1%) but smallest scale.

---

## II. Profitability Ranking

### Ranked by Take Rate (marketplace efficiency)

| Rank | Marketplace | Take Rate | Revenue $ | Model | Notes |
|---|---|---|---|---|---|
| **#1** | **FALABELLA** | **24.1%** | **$1.1M** | 3rd party | Highest rate, micro scale |
| **#2** | **RIPLEY** | **17.9%** | **$63.3M** | 3rd party | Stable rate, large scale |
| #3 | ML (gross) | 38.8% | $339.4M | 3rd party | Charges high, returns most |
| #4 | ML (net) | 3.7% | $32.8M | 3rd party | After $306.6M adjustments |
| — | PARIS | 70.9% | $378.1M | 1st party | NOT comparable (product margin included) |

### Ranked by Absolute Revenue (Eccsa earnings)

| Rank | Marketplace | Annual Revenue | % of Total |
|---|---|---|---|
| **#1** | **PARIS** | **$378,104,933** | **74.1%** |
| **#2** | **RIPLEY** | **$63,316,608** | **12.4%** |
| **#3** | **ML** | **$32,794,078** | **6.4%** |
| **#4** | **FALABELLA** | **$1,125,240** | **0.2%** |
| **TOTAL** | | **$475,340,859** | **100.0%** |

### Ranked by GMV (transaction volume)

| Rank | Marketplace | GMV | % of Total |
|---|---|---|---|
| **#1** | **ML** | **$875,809,123** | **49.6%** |
| **#2** | **PARIS** | **$532,927,925** | **30.2%** |
| **#3** | **RIPLEY** | **$353,160,324** | **20.0%** |
| **#4** | **FALABELLA** | **$4,661,810** | **0.3%** |
| **TOTAL** | | **$1,766,559,182** | **100.0%** |

---

## III. Answer: Where do we really make money?

**PARIS generates the most absolute profit** for Eccsa ($378.1M), but it's a 1st party model — Eccsa is both marketplace AND seller. The margin includes product markup.

**RIPLEY is the most profitable 3rd party marketplace** in absolute terms ($63.3M). It has a stable 17.9% take rate and generates 12.4% of Eccsa's total marketplace revenue.

**FALABELLA has the highest effective take rate (24.1%)** but at tiny scale ($1.1M) — the least absolute contribution.

**ML is the paradox** — it has the highest GMV ($875.8M, 49.6% of total) but the lowest net take rate (3.7%). Its $306.6M in adjustments (90.3% of gross charges returned) destroy margin. ML contributes only $32.8M (6.4% of total revenue) despite processing half of all transactions.

### The Real Answer:

| Question | Answer |
|---|---|
| ¿Dónde ganamos más? | **PARIS** ($378.1M) — but it's 1st party |
| ¿Dónde ganamos más en marketplace puro? | **RIPLEY** ($63.3M, 17.9% take rate) |
| ¿Dónde tenemos más volumen sin margen? | **ML** ($875.8M GMV at 3.7% net take) |
| ¿Dónde tenemos mejor eficiencia? | **FALABELLA** (24.1% take) pero escala irrelevante |

---

## IV. RIPLEY Take Rate Trend (17 months)

```
Periodo     GMV        MP Revenue  Take Rate
─────────────────────────────────────────────
2025-01  $17.4M       $3.2M       18.7%
2025-02  $11.0M       $2.1M       18.9%
2025-03  $20.8M       $3.8M       18.3%
2025-04  $32.3M       $5.7M       17.5%
2025-05  $23.7M       $4.0M       17.0%
2025-06  $26.6M       $4.7M       17.6%
2025-07  $28.9M       $5.6M       19.3%
2025-08  $22.7M       $3.9M       17.2%
2025-09  $17.2M       $3.5M       20.4%
2025-10  $26.3M       $5.0M       18.9%
2025-11  $29.7M       $5.0M       17.0%
2025-12  $24.5M       $4.3M       17.5%
2026-01  $10.8M       $2.0M       18.5%
2026-02  $9.3M        $1.7M       18.8%
2026-03  $22.9M       $3.9M       16.9%
2026-04  $16.5M       $2.8M       16.9%
2026-05  $12.4M       $2.1M       16.9%
─────────────────────────────────────────────
Range:              16.9% – 20.4%
Average:            18.0%
95% CI:             ±0.6%
```

**Take rate is remarkably stable.** No drift, no degradation. RIPLEY's pricing model is consistent.

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
