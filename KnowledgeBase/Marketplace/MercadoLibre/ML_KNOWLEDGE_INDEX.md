# ML_KNOWLEDGE_INDEX — Certified Knowledge Index: Mercado Libre

**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Primer marketplace certificado que alimenta el CORE**

---

## Knowledge Files

| File | Cert | Propósito |
|------|------|-----------|
| `ML_GOLDEN_REPORTS_V1.md` | 001 | Jerarquía oficial de fuentes (Nivel A→D) |
| `ML_CONCILIATION_DOMAIN_MODEL_V1.md` | 002 | Separación de dominios (OPERATIONAL / FISCAL / CASH) |
| `ML_TRANSACTION_LIFECYCLE_V1.md` | 003 | Ciclo de vida completo VENTA→CAJA |
| `ML_TRACEABILITY_MODEL_V1.md` | 004 | Jerarquía de llaves y niveles de trazabilidad |
| `ML_CASH_REALITY_MODEL_V1.md` | 005 | Verdades de caja, cash proxies, delta certificado |
| `ML_FINANCIAL_EVENT_MODEL_V1.md` | 006 | ROOT_EVENT vs MECHANISM, regla, impacto |
| `ML_POSTCOBRO_RULES_V1.md` | 007 | Reglas de pipeline postventa |
| `ML_FULL_RULES_V1.md` | 008 | Reglas de conciliación Full |
| `ML_FACTURATION_MODEL_V1.md` | — | Modelo de facturación y clasificación |

---

## Knowledge Graph: ML

```
ML_FACTURATION_MODEL
  │
  ├──→ ML_GOLDEN_REPORTS (Jerarquía de fuentes)
  │       │
  │       ├──→ ML_TRANSACTION_LIFECYCLE (VENTA → CAJA)
  │       │       │
  │       │       ├──→ ML_TRACEABILITY_MODEL (Llaves y niveles)
  │       │       │
  │       │       └──→ ML_FINANCIAL_EVENT_MODEL (ROOT_EVENT vs MECHANISM)
  │       │               │
  │       │               └──→ ML_POSTCOBRO_RULES (Pipeline postventa)
  │       │
  │       └──→ ML_CASH_REALITY_MODEL (Cash proxies y deltas)
  │
  └──→ ML_CONCILIATION_DOMAIN_MODEL (Dominios: OP / FISCAL / CASH)
          │
          └──→ ML_FULL_RULES (Logística fulfillment)
```

---

## Certificaciones Asociadas (14 governance documents)

| Governance Doc | Knowledge File |
|----------------|----------------|
| `RFC_EVENT_MODEL_CERTIFICATION.md` | `ML_FINANCIAL_EVENT_MODEL_V1.md` |
| `RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md` | `ML_CASH_REALITY_MODEL_V1.md` + `ML_POSTCOBRO_RULES_V1.md` |
| `RFC_POSCOBRO_CAUSALITY_FINAL.md` | `ML_POSTCOBRO_RULES_V1.md` + `ML_TRANSACTION_LIFECYCLE_V1.md` |
| `RFC_EVENT_RULE_LOCATION.md` | `ML_FINANCIAL_EVENT_MODEL_V1.md` |
| `G6_CASH_REALITY_CERTIFICATION.md` | `ML_CASH_REALITY_MODEL_V1.md` |
| `G6_1_RESULTADO_NETO_EVENTS_VS_RECORDS.md` | `ML_FINANCIAL_EVENT_MODEL_V1.md` |
| `SEMANTIC_TRACEABILITY_MATRIX.md` | `ML_TRACEABILITY_MODEL_V1.md` |
| `MARKETPLACE_CONCEPT_MASTER_CERTIFICATION.md` | `ML_FACTURATION_MODEL_V1.md` |
| `MARKETPLACE_CHARGE_RECONCILIATION_V2.md` | `ML_CONCILIATION_DOMAIN_MODEL_V1.md` |
| `MARKETPLACE_ECONOMIC_TRUTH_CERTIFICATION.md` | `ML_CONCILIATION_DOMAIN_MODEL_V1.md` |
| `MARKETPLACE_MONEY_FLOW_TRUTH.md` | `ML_CASH_REALITY_MODEL_V1.md` |
| `REVENUE_ENGINE_DECOMPOSITION.md` | `ML_FACTURATION_MODEL_V1.md` |
| `ML_POSCOBRO_FORENSICS.md` | `ML_POSTCOBRO_RULES_V1.md` |
| `MARKETPLACE_WATERFALL_CERTIFICATION.md` | `ML_CONCILIATION_DOMAIN_MODEL_V1.md` |

---

## Métricas de Conocimiento ML

| Métrica | Valor |
|---------|-------|
| Knowledge files | 10 |
| Governance docs referenciados | 14 |
| Conceptos certificados | 14 ROOT_EVENT + 3 MECHANISM + 11 otros |
| Pairs certificados | 4 díadas |
| Cash proxies identificados | 2 (Mediación, reserve_for_dispute) |
| Dominios separados | 3 (OPERATIONAL, FISCAL, CASH) |
| Niveles de fuente | 4 (A→D) |
| Niveles de trazabilidad | 4 (Source→XML→Cash→Event) |

---

## Preparación para Shopify y Falabella

ML es el primer marketplace certificado. Su conocimiento alimenta el CORE:

| Core File | ML Knowledge Source |
|-----------|-------------------|
| `knowledge/core/EVENT_MODEL_CORE_V1.md` | `ML_FINANCIAL_EVENT_MODEL_V1.md` |
| `knowledge/core/CASH_REALITY_CORE_V1.md` | `ML_CASH_REALITY_MODEL_V1.md` |
| `knowledge/core/TRACEABILITY_CORE_V1.md` | `ML_TRACEABILITY_MODEL_V1.md` |
| `knowledge/core/FINANCIAL_GOVERNANCE_CORE_V1.md` | All ML knowledge files |
