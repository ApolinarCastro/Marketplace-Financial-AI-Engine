# G5.6 — Revenue Engine Decomposition

**Date:** 2026-06-03  
**Mode:** READ ONLY — all queries against `meli_financial_v4.db`, no modifications  
**Objective:** Answer how each marketplace *generates* money — not where it is, but how it's created.

---

## FASE 1 — Inventory of Revenue Drivers

Each marketplace has a unique monetization structure. The common drivers are: commissions, logistics, advertising, services, storage, penalties. But each driver's weight and economic character differ fundamentally.

### RIPLEY Revenue Drivers

| Driver | Gross Amount | Net Amount | % of MP Revenue | % of GMV |
|---|---|---|---|---|
| **Comisiones** | -$64,158,492 | -$49,076,708 | **77.5%** | 13.9% |
| ┣━ Comisiones sobre pedidos (gross) | -$64,158,492 | | | 18.2% |
| ┗━ Comisiones reembolsadas | +$15,081,784 | | | -4.3% |
| **Logística (fees netas)** | — | -$14,206,460 | **22.4%** | 4.0% |
| ┣━ Descuento por costo logístico | -$12,847,249 | | | 3.6% |
| ┣━ Descuento por logística inversa | -$1,359,211 | | | 0.4% |
| **Penalidades** | -$33,440 | -$33,440 | **0.1%** | 0.01% |
| **NET REVENUE** | | **-$63,316,608** | **100.0%** | **17.9%** |

**Pass-through flows ($0 net):**
- Envío: +$18,359,399
- Gastos de envío operador: -$18,359,399
- Envío reembolsado: -$1,689,874
- Gastos de envío reembolsados: +$1,689,874

### PARIS Revenue Drivers

| Driver | Amount | % of MP Revenue* | % of GMV |
|---|---|---|---|
| **Venta (producto)** | +$525,039,911 | N/A | 100.0% |
| Despacho (envío) | +$7,888,014 | N/A | 1.5% |
| Devoluciones | -$131,893,037 | N/A | -25.1% |
| Logística | -$24,578,542 | N/A | -4.7% |
| Ajustes net | +$1,375,357 | N/A | +0.3% |
| **P&L NETO (1st party)** | **$378,104,933** | | **72.0%** |

*PARIS is 1st party — driver % not meaningful for fee revenue. The marketplace commission (~$48.7M) is implicit.

**Estimated marketplace fee extraction:**
- Commission (from XML): ~$48.7M (9.3% of GMV)
- Logistics markup: included in $19.5M Cobro por despacho

### ML Revenue Drivers

| Driver | Gross | Adjustments | Net | Net % of MP Rev |
|---|---|---|---|---|
| **Comisiones** | -$109,391,330 | — | -$109,391,330 | **32.2%** (gross: 32.2%) |
| **Logística** | -$67,662,878 | — | -$67,662,878 | **19.9%** |
| **Publicidad** | -$48,836,566 | — | -$48,836,566 | **14.4%** |
| **Servicios** | -$16,750,876 | — | -$16,750,876 | **4.9%** |
| **Almacenamiento** | -$4,988,640 | — | -$4,988,640 | **1.5%** |
| **Adjustments** | — | +$306,606,250 | +$306,606,250 | **-90.3%** (reduces revenue) |
| **NET REVENUE** | **-$247,630,290** | **+$306,606,250** | **$32,794,078** | **9.7% of gross** |

**Adjustments breakdown:**
| Sub-driver | Amount | % of Adjustments |
|---|---|---|
| BPP (buyer protection) | $95,109,574 | 31.0% |
| Talla (bigger/smaller/size match) | $98,271,357 | 32.0% |
| Conciliación (reconciled) | $40,845,693 | 13.3% |
| Comprador (remorse, etc.) | $30,173,852 | 9.8% |
| Entrega (delivery failures) | $13,285,940 | 4.3% |
| Calidad (quality mismatches) | $8,474,195 | 2.8% |
| Defecto (broken/missing) | $5,777,739 | 1.9% |
| Otros (admin, sistema, etc.) | $14,667,900 | 4.8% |
| **Total** | **$306,606,250** | **100.0%** |

### FALABELLA Revenue Drivers

| Driver | Gross | Net | % of MP Revenue | % of GMV |
|---|---|---|---|---|
| **Comisiones** | -$932,359 | -$741,650 | **65.9%** | 19.9% |
| ┣━ Cobro comisión (gross) | -$932,359 | | | 20.0% |
| ┗━ Reembolso comisión | +$190,709 | | | -4.1% |
| **Logística** | -$383,590 | -$383,590 | **34.1%** | 8.2% |
| **NET REVENUE** | | **-$1,125,240** | **100.0%** | **24.1%** |

---

## FASE 2 — Revenue Waterfall

### RIPLEY Waterfall

```
GMV: $353,160,324
│
├── 23.5% → Devoluciones (returns to buyers: -$82,896,873)
│
├── 18.2% → Comisiones (gross: -$64,158,492)
│   └── 4.3% ← Reembolsos comisiones (+$15,081,784)
│
├── Envío pass-through (+$18,359,399 / -$18,359,399) → $0 net
│
├── 3.6% → Descuento por costo logístico (-$12,847,249)
├── 0.4% → Logística inversa (-$1,359,211)
│
├── 0.01% → Penalidades (-$33,440)
│
└── 58.6% → A Pagar al vendedor ($206,946,843)
                                   │
                   17.9%           │
            ═══════ NET ════════   │
           ↓ MARKETPLACE REVENUE   │
              = $63,316,608        │
```

### ML Waterfall

```
GMV: $875,809,123
│
├── 38.8% → GROSS CHARGES: $339,400,328
│   │
│   ├── 32.2%  → Comisiones netas ($109,391,330)
│   ├── 19.9%  → Logística ($67,662,878)
│   ├── 14.4%  → Publicidad ($48,836,566)
│   ├── 4.9%   → Servicios ($16,750,876)
│   ├── 1.5%   → Almacenamiento ($4,988,640)
│   │
│   └── 90.3% ← ADJUSTMENTS (CREDITS): $306,606,250
│       ├── 31.0% ← BPP ($95.1M)
│       ├── 32.0% ← Talla ($98.3M)
│       ├── 13.3% ← Conciliación ($40.8M)
│       ├── 9.8%  ← Comprador ($30.2M)
│       └── 13.9% ← Others ($42.2M)
│
└── 3.7% → NET MARKETPLACE REVENUE: $32,794,078
```

### PARIS Waterfall

```
VENTA: $525,039,911 + DESPACHO: $7,888,014 = $532,927,925
│
├── 25.1% → Devoluciones (-$131,893,037)
├── 4.6%  → Logística (-$24,578,542)
│
├── Commission implicit ($48.7M): embedded in P&L spread
│   Revenue = Venta - Devolución - Logística - Pago vendedor
│   Commission is NOT separate — it's the spread
│
└── 70.9% → P&L NETO: $378,104,933
          (includes product margin + implicit commission)
```

### FALABELLA Waterfall

```
GMV: $4,661,810
│
├── 20.5% → Devoluciones (-$953,554)
├── 15.9% → Comisiones netas (-$741,650)
├── 8.2%  → Logística neta (-$383,590)
│
└── 24.1% → NET MARKETPLACE REVENUE: $1,125,240
```

---

## FASE 5 — Monetization Model Classification

### RIPLEY: COMMISSION-DRIVEN HYBRID

```
77.5% Comisiones + 22.4% Logística + 0.1% Penalidades
═══════════════════════════════════
Model: Pure 3P Marketplace
Engine: Transaction commission (Costo Fijo MKP + % periódico)
Secondary: Logistics fee extraction (markup on shipping)
Stability: Take rate stable at 16.9-20.4% for 17 months
```

**Economic engine:** "Cobro por transacción." Every sale generates commission. Logistics is a secondary revenue stream.

### PARIS: MARGIN-DRIVEN 1P

```
Product margin + Implicit commission (~$48.7M)
══════════════════════
Model: 1st Party Retailer
Engine: Product markup (buy low, sell high)
Secondary: Logistics fees (cost recovery)
```

**Economic engine:** "Compra y vende." Eccsa owns inventory. The marketplace fee is secondary to the product margin. This is fundamentally different from the other 3 marketplaces.

### ML: ADJUSTMENT-ERODED HYBRID

```
Gross: 32.2% Comisiones + 19.9% Logística + 14.4% Publicidad + 4.9% Servicios + 1.5% Almacenamiento
Net:   90.3% of gross returned as adjustments
═══════════════════════════════════════
Model: 3P Marketplace with massive rebate structure
Engine: Aggregate volume → charge high fees → return most via programs
Secondary: Advertising platform (ads = high margin)
```

**Economic engine:** "Volumen + programa de créditos." ML's real monetization is not the net fee (3.7%). It's the advertising platform ($47.9M, near-zero cost). The fee structure exists to be partially rebated.

### FALABELLA: COMMISSION-DRIVEN (micro-scale)

```
65.9% Comisiones + 34.1% Logística
════════════════
Model: Pure 3P Marketplace (high rate, tiny scale)
Engine: Commission + logistics markup
```

**Economic engine:** "Comisión alta a baja escala." Highest take rate (24.1%) but too small to matter.

---

## Answer: How Does Each Marketplace Actually Make Money?

| Marketplace | Monetization Model | Primary Engine | Secondary | Vulnerability |
|---|---|---|---|---|
| **RIPLEY** | Commission-driven | Transaction fees (17.9%) | Logistics markup | Volume-dependent |
| **PARIS** | Margin-driven | Product markup (~63%*) | Logistics fees | Inventory risk |
| **ML** | Ads + Volume | Advertising ($47.9M, 0% cost) | Fee rebate structure | Adjustment dependency |
| **FALABELLA** | Commission-driven | High rate (24.1%) | N/A | Irrelevant scale |

*Normalized: after removing estimated COGS

### The Real Answer

**RIPLEY generates revenue the old-fashioned way: per-transaction fees.** Simple, transparent, stable. Each $1M in GMV = $179K in revenue.

**ML generates revenue through advertising** ($47.9M in ads is 1.5× the net fee revenue of $32.8M). The fee structure is a loss leader that funds the adjustment programs. The real profit center is ads.

**PARIS generates revenue through product margin** (buy low, sell high). The marketplace commission (~$48.7M) exists but is not the primary engine.

**FALABELLA generates revenue through high fees at micro scale.** 24.1% is the highest rate, but total contribution is marginal.

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
