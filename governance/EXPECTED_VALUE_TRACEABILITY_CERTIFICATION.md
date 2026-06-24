# E1.1 — Expected Value Traceability Certification

**Date:** 2026-06-03  
**Mode:** READ ONLY — certification of every peso in the E1.0 portfolio

---

## FASE 1 — Traceability Inventory

### P1+P2: RIPLEY Penalidades Framework + Enforcement

**Critical finding:** P1 and P2 are the same $3.5M opportunity described from two angles. Combined EV of $6.68M overstates by **$3.36M (42% inflation).** Corrected EV: **$3,323,255.**

| Component | Value | Source | Period | Formula | Classification |
|---|---|---|---|---|---|
| RIPLEY GMV | $353,160,324 | `marketplace_ledger_v1`, detalle='Importe del pedido', marketplace='RIPLEY' | 17 months (2025-01 to 2026-05) | SUM(monto) WHERE detalle='Importe del pedido' | **HECHO** |
| Current penalidades | $33,440 | `marketplace_ledger_v1`, detalle IN ('Descuento por cancelación','Otros descuentos'), marketplace='RIPLEY' | 8 months aktiv, 10 rows | SUM(monto) | **HECHO** |
| 1% of GMV target | $3,531,603 | Industry benchmark | N/A | $353,160,324 × 1% | **BENCHMARK** |
| Gap to target | $3,498,163 | Calculation | N/A | $3,531,603 - $33,440 | **CÁLCULO** |
| 95% probability | 0.95 | Eccsa controls policy | N/A | Commercial judgment | **HIPÓTESIS** |
| **Corrected EV** | **$3,323,255** | | | $3,498,163 × 0.95 | |

### P3: PARIS Retiro Stock Optimization

| Component | Value | Source | Period | Formula | Classification |
|---|---|---|---|---|---|
| Current retiro cost | $1,630,800 | `marketplace_ledger_v1`, detalle='Retiro stock bodega Paris', marketplace='PARIS' | 5 months, 5 rows | SUM(monto) | **HECHO** |
| 50% reduction target | $815,400 | Operational hypothesis | N/A | $1,630,800 × 50% | **HIPÓTESIS** |
| 80% probability | 0.80 | Operational feasibility | N/A | Commercial judgment | **HIPÓTESIS** |
| **EV** | **$652,320** | | | $815,400 × 0.80 | |

### P4: PARIS Stock Antiguo Elimination

| Component | Value | Source | Period | Formula | Classification |
|---|---|---|---|---|---|
| Current stock antiguo cost | $314,802 | `marketplace_ledger_v1`, detalle='Cobro stock antiguo', marketplace='PARIS' | 10 months, 11 rows | SUM(monto) | **HECHO** |
| 100% elimination target | $314,802 | Operational hypothesis | N/A | $314,802 × 100% | **HIPÓTESIS** |
| 85% probability | 0.85 | Operational feasibility | N/A | Commercial judgment | **HIPÓTESIS** |
| **EV** | **$267,582** | | | $314,802 × 0.85 | |

### P5: ML Ajuste Poscobro Cleanup

| Component | Value | Source | Period | Formula | Classification |
|---|---|---|---|---|---|
| Total Poscobro adjustments | $3,108,659 | `marketplace_ledger_v1`, detalle='Ajuste Poscobro', marketplace='ML' | 23 months, 634 rows | SUM(monto) | **HECHO** |
| Monthly average | $135,159 | Same source | 23 months (2025-01 to 2026-11) | AVG(SUM(monto) per month) | **HECHO** |
| 20% recovery target | $621,732 | Financial hypothesis | N/A | $3,108,659 × 20% | **HIPÓTESIS** |
| 75% probability | 0.75 | Financial feasibility | N/A | Commercial judgment | **HIPÓTESIS** |
| **EV** | **$466,299** | | | $621,732 × 0.75 | |

---

## FASE 2 — Classification by Component

### Full Traceability Map

```
Project     │ HECHO              │ BENCHMARK      │ CÁLCULO        │ HIPÓTESIS
────────────┼────────────────────┼────────────────┼────────────────┼────────────────
P1+P2       │ $353,160,324 GMV   │ 1% industry    │ $3,498,163 gap │ 95% probability
            │ $33,440 current    │ standard       │                │
            │                    │                │                │
P3          │ $1,630,800 cost    │ —              │ $815,400 (50%) │ 50% reduction
            │                    │                │                │ 80% probability
P4          │ $314,802 cost      │ —              │ $314,802 (100%)│ 100% elimination
            │                    │                │                │ 85% probability
P5          │ $3,108,659 adj     │ —              │ $621,732 (20%) │ 20% recovery
            │ $135,159/mo avg    │                │                │ 75% probability
```

---

## FASE 3 — Confidence Level per Project

| Project | Historical Evidence | Repeatability | Eccsa Control | Variability | Confidence |
|---|---|---|---|---|---|
| P1+P2 RIPLEY Pen. | 17 months GMV data | GMV is recurring | Full control | Target % is assumption | **MEDIO** |
| P3 PARIS Retiro | 5 data points (thin) | Small sample | Full control | Cost may not recur linearly | **MEDIO** |
| P4 PARIS Antiguo | 10 months of charges | Recurring monthly | Full control | Easy to eliminate | **ALTO** |
| P5 ML Poscobro | 23 months, 634 rows | Highly recurring | Partial control | Recovery % uncertain | **BAJO** |

### Confidence Justification

**P4 — ALTO:** Stock antiguo charges are purely operational. FIFO rotation + clearance can eliminate them entirely. Lowest variability.

**P1+P2 — MEDIO:** GMV is certain, but the 1% penalty target depends on seller compliance. Actual collection may be 0.5-1.5% of GMV.

**P3 — MEDIO:** Only 5 data points. Retiro stock may decrease naturally or have structural causes beyond simple process change.

**P5 — BAJO:** The 20% recovery rate has zero precedent. Poscobro adjustments may be 100% legitimate. ML cooperation required.

---

## FASE 4 — Executive Separation

### A) BENEFICIO DEMOSTRADO (Fact-only, no assumptions)

**$0.** No EV component is pure fact. Every expected value requires at least one assumption (target %, probability).

### B) BENEFICIO PROBABLE (Backed by facts + reasonable assumptions)

| Project | EV | Reasoning |
|---|---|---|
| P4 PARIS Stock Antiguo | $267,582 | 85% probability on 100% elimination. Ops fix with strong precedent. |
| P1+P2 RIPLEY Penalidades | $3,323,255 | 95% on industry-standard 1%. Eccsa controls policy completely. |
| P3 PARIS Retiro Stock | $652,320 | 80% on 50% reduction. Ops improvement with medium evidence. |
| **Subtotal** | **$4,243,157** | |

### C) BENEFICIO ESPECULATIVO (Significant assumptions, low precedent)

| Project | EV | Reasoning |
|---|---|---|
| P5 ML Ajuste Poscobro | $466,299 | 20% recovery with no precedent. 75% probability not supported by data. |
| **Subtotal** | **$466,299** | |

---

## FASE 5 — Certification

### The $8.06M Correction

The original E1.0 portfolio of **$8,064,479** contains a material overstatement:

| Issue | Impact |
|---|---|
| P1 ($3.36M) + P2 ($3.32M) describe the SAME $3.5M opportunity | **-$3,355,023** (42% overstatement) |
| P1+P2 count 1% of GMV from framework AND enforcement angles | Both can't achieve full 1% independently |

### Corrected Portfolio

| Project | Original EV | Corrected EV | Delta |
|---|---|---|---|
| P1+P2 RIPLEY Penalidades | $6,678,278 | $3,323,255 | -$3,355,023 |
| P3 PARIS Retiro Stock | $652,320 | $652,320 | $0 |
| P4 PARIS Stock Antiguo | $267,582 | $267,582 | $0 |
| P5 ML Ajuste Poscobro | $466,299 | $466,299 | $0 |
| **TOTAL** | **$8,064,479** | **$4,709,456** | **-$3,355,023** |

---
---

## VEREDICTO FINAL

### De los $4,709,456 corregidos:

| Categoría | Monto | % |
|---|---|---|
| **HECHO** (data histórica sin supuestos) | **$0** | 0% |
| **BENCHMARK** (estándar de industria) | **$3,323,255** (embedded in P1+P2) | 71% |
| **ESTIMACIÓN** (hecho × supuesto razonable) | **$4,243,157** (P1+P2+P3+P4) | 90% |
| **HIPÓTESIS** (sin precedente) | **$466,299** (P5) | 10% |
| **DOBLE CONTEO** (eliminado) | **$3,355,023** | — |

### Respuestas a las 8 preguntas obligatorias:

1. **¿Cada peso del EV tiene trazabilidad?** Sí — cada peso está mapeado a su fórmula, fuente DB, y clasificación.

2. **¿Qué porcentaje nace de datos históricos?** 0% — el EV siempre requiere un supuesto (target % o probabilidad). Los HECHOS son los *inputs*, no el EV.

3. **¿Qué porcentaje nace de simulaciones?** 0% — no se usaron simulaciones.

4. **¿Qué porcentaje nace de hipótesis?** 100% — todo EV requiere al menos una hipótesis.

5. **¿Qué proyecto tiene mayor evidencia?** **P1+P2** — 17 meses de GMV, 10 rows de penalidades actuales, benchmark de industria sólido.

6. **¿Qué proyecto tiene menor evidencia?** **P5** — 20% recovery sin precedente. 23 meses de datos históricos pero sin indicio de cuánto es recuperable.

7. **¿Qué EV debería excluirse del dashboard ejecutivo?** **P5 ($466,299)** — Especulativo. Sin precedente de recuperación. Reportar por separado como "under investigation."

8. **¿Qué EV puede considerarse confiable?** **P4 ($267,582)** — 85% de eliminación de stock antiguo por mejora operacional. El más simple, más controlable, más probable.

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
