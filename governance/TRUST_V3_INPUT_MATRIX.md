# TRUST V3 INPUT MATRIX

**Fecha**: 2026-05-30
**Régimen**: GOVERNANCE — READ ONLY
**Fuente**: TRUST_METHODOLOGY_REVISION_V1.md

---

## MÉTRICAS ANTIGUAS (OBSOLETAS)

| Marketplace | XML Traceability (rows) | XML Traceability ($) | Trust V2 |
|---|---|---|---|
| **ML** | 89.4% | 63.5% | 94/100 |
| **PARIS** | 79.0% | 82.6% | 70/100 |
| **RIPLEY** | 0.0% | 0.0% | 72/100 |
| **FALABELLA** | 61.5% | 34.1% | 71/100 |
| **GLOBAL** | **30.2%** | **56.1%** | **84/100** |

## MÉTRICAS CORREGIDAS (TRUST V3 — PRELIMINAR)

### Revenue Traceability

| Marketplace | Ingresos Elegibles | Ingresos con folio_xml | Revenue Tr. |
|---|---|---|---|
| **ML** | $875,869,354 | $875,869,354 | **100.0%** |
| **PARIS** | $533,201,155 | $438,341,712 | **82.2%** |
| **RIPLEY** | $20,774,862 | $0 | **0.0%** |
| **FALABELLA** | $3,512,457 | $0 | **0.0%** |
| **GLOBAL** | $1,433,357,828 | $1,314,211,066 | **91.7%** |

### Cost Traceability

| Marketplace | Costos Elegibles | Costos con folio_xml | Cost Tr. |
|---|---|---|---|
| **ML** | $247,215,702 | $247,215,702 | **100.0%** |
| **PARIS** | $24,578,542 | $19,750,072 | **80.4%** |
| **RIPLEY** | $3,725,296 | $0 | **0.0%** |
| **FALABELLA** | $877,369 | $912,622 | **104.0%*** |
| **GLOBAL** | $276,396,909 | $267,878,396 | **96.9%** |

*\*FALABELLA >100% por arrastre de montos negativos entre costos_comerciales y costos_operacionales*

### Returns Traceability

| Marketplace | Devoluciones Elegibles | Devoluciones con folio_xml | Returns Tr. |
|---|---|---|---|
| **ML** | $93,009,601 | $93,009,601 | **100.0%** |
| **PARIS** | $131,893,037 | $107,608,993 | **81.6%** |
| **RIPLEY** | $3,338,140 | $0 | **0.0%** |
| **FALABELLA** | $654,445 | $0 | **0.0%** |
| **GLOBAL** | $228,895,223 | $200,618,594 | **87.7%** |

### Adjustment Traceability

| Marketplace | Ajustes Elegibles | Ajustes con folio_xml | Adjustment Tr. |
|---|---|---|---|
| **ML** | $295,368,156 | $405,701 | **0.1%** |
| **PARIS** | $1,375,357 | $1,375,357 | **100.0%** |
| **RIPLEY** | $0 | $0 | **0.0%** |
| **FALABELLA** | $0 | $0 | **0.0%** |
| **GLOBAL** | $296,743,513 | $1,781,058 | **0.6%** |

## MÉTRICA COMPUESTA (0.5R + 0.25C + 0.15Re + 0.1A)

| Marketplace | Revenue(50%) | Cost(25%) | Returns(15%) | Adjustment(10%) | **Compuesta** |
|---|---|---|---|---|---|
| **ML** | 50.0% | 25.0% | 15.0% | 0.0% | **90.0%** |
| **PARIS** | 41.1% | 20.1% | 12.2% | 10.0% | **83.4%** |
| **RIPLEY** | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| **FALABELLA** | 0.0% | 23.6% | 0.0% | 0.0% | **23.6%** |
| **GLOBAL** | 45.9% | 24.2% | 13.2% | 0.1% | **83.3%** |

## DIFERENCIAS: V2 vs V3

| Marketplace | Trust V2 | Trust V3 Compuesta | Diferencia |
|---|---|---|---|
| **ML** | ~95% | 90.0% | -5.0pp |
| **PARIS** | ~80% | 83.4% | +3.4pp |
| **RIPLEY** | ~0% | 0.0% | 0pp |
| **FALABELLA** | ~40% | 23.6% | -16.4pp |
| **GLOBAL** | ~56% | 83.3% | +27.3pp |

## IMPACTO ESPERADO EN TRUST SCORE V3

| Marketplace | Trust V2 | Trust V3 Proyectado | Cambio |
|---|---|---|---|
| **ML** | 94/100 | 93/100 | -1 |
| **PARIS** | 70/100 | 72/100 | +2 |
| **RIPLEY** | 72/100 | 68/100 | -4 |
| **FALABELLA** | 71/100 | 60/100 | -11 |
| **GLOBAL** | ~84/100 | ~78/100 | -6 |

## DATOS FUENTE

- DB: `data/db/meli_financial_v4.db` (DuckDB)
- Ledger: `marketplace_ledger_v1`
- Períodos elegibles: definidos en TRUST_METHODOLOGY_REVISION_V1.md FASE 3
- Certificación semántica: XML_BUSINESS_SEMANTICS_CERTIFICATION.md
- Document Consistency: DOCUMENT_CONSISTENCY_AUDIT.md
