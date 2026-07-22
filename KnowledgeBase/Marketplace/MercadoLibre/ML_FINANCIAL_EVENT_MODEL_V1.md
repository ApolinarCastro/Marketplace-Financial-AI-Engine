# ML_FINANCIAL_EVENT_MODEL_V1 — Certified Financial Event Model

**CERTIFICADO 006**
**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Fuente oficial:** RFC_EVENT_MODEL_CERTIFICATION, RFC_CASH_CERTIFICATION_BPP_POSCOBRO, RFC_EVENT_RULE_LOCATION

---

## Definiciones Fundamentales

```
ROOT_EVENT  =  Evento económico real con impacto en caja
MECHANISM   =  Ejecución operacional que refleja un ROOT_EVENT existente

Si ROOT_EVENT + MECHANISM representan el mismo caso:
  → Resultado Neto considera SOLO ROOT_EVENT
  → MECHANISM queda disponible solo para trazabilidad y auditoría
```

## ML Concepts Certified

### ROOT_EVENTS (14 concepts, preserve in Resultado Neto)

| Concept | Cash Evidence | Standalone % |
|---------|--------------|-------------|
| Talla/Garantía | Mediación ($10.5M) | 15.2% |
| Arrepentimiento | Mediación | 10.4% |
| Producto Dañado/Vacío | REAL_CASH | 22.5% |
| Diferencia Publicación | REAL_CASH | 14.2% |
| Item Faltante | REAL_CASH | 40.0% |
| Falta de Stock | REAL_CASH | 0.0% |
| Retraso en Entrega | REAL_CASH | 10.4% |
| Cambio de Dirección | REAL_CASH | 0.0% |
| Falla en Entrega | REAL_CASH | 9.4% |
| Disputa no Respondida | REAL_CASH | 10.5% |
| Abono manual | REAL_CASH | 0.0% |
| Mediación | REAL_CASH | — |
| Cancelación de la mediación | REAL_CASH | — |
| cashback / cashback_cancel | ACCRUAL | — |

### EXECUTION MECHANISMS (3 concepts, exclude when paired)

| Concept | Cash Evidence | Paired % | Standalone % |
|---------|--------------|----------|-------------|
| BPP | MIRROR_ZERO (NET=$0) | 96.9% | 3.1% ($2.8M) |
| Poscobro Conciliado | MIRROR_ZERO (NET=$0) | 92.0% | 8.0% ($3.5M) |
| Poscobro General | MIRROR_ZERO | 21.7% | 78.3% ($2.4M) |

## Certified Pairs

| Díada | Orders | Exact Matches | Cash Proxy |
|-------|--------|--------------|------------|
| Talla + BPP | 1,902 | 1,751 ($52.4M) | Mediación |
| Talla + Poscobro Conciliado | 746 | 637 ($22.3M) | Mediación |
| Arrepentimiento + Poscobro Conciliado | 342 | 297 ($10.1M) | Mediación |
| Arrepentimiento + Poscobro General | 12 | 11 ($0.4M) | Mediación |

## Financial Impact

| Métrica | Valor |
|---------|-------|
| RN actual (all-time ML) | $842,250,300.65 |
| Paired mechanisms | $11,879,141.79 (1.41% of RN) |
| Standalone mechanisms preserved | $137,911,973.00 (16.37% of RN) |
| **Cash impact** | **$0** |

## Rule Location

La regla debe vivir en una **nueva capa conceptual de evento económico** (Opción D), entre clasificación y cierre:

```
Loader → Ledger → Clasificación → Clasificado → EventModel → Cierre → API
```

## Certificaciones Asociadas

| Documento | Relación |
|-----------|----------|
| `governance/RFC_EVENT_MODEL_CERTIFICATION.md` | Event model (PASS) |
| `governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md` | Cash certification (PASS CONDITIONAL) |
| `governance/RFC_EVENT_RULE_LOCATION.md` | Arquitectura (Opción D) |
| `governance/G6_1_RESULTADO_NETO_EVENTS_VS_RECORDS.md` | FAIL: Events vs Records |
| `governance/RFC_POSCOBRO_CAUSALITY_FINAL.md` | Lifecycle reconstruction |

## Aplicación a otros marketplaces

Marketplaces SIN mechanism cascade → todos los conceptos son ROOT_EVENT.
Marketplaces CON mechanism cascade → aplicar mismo patrón (detectar pares por id_orden).
