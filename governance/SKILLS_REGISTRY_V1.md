# SKILLS_REGISTRY_V1.md — Certified Skills Registry

**Date:** 2026-06-05  
**Scope:** 7 certified skills for financial governance  
**Status:** BLUEPRINT

---

## Skill 1: `financial-event-causality`

### Objetivo
Certificar que cada transacción financiera tiene un ROOT_EVENT identificable, y que ejecution mechanisms no duplican el impacto económico en Resultado Neto.

### Input
- Ledger rows (id_orden, concepto, monto)
- Classification map (concept → ROOT_EVENT vs MECHANISM)
- Event rule (RFC_EVENT_MODEL_CERTIFICATION)

### Output
- Per-order event_type assignment
- Paired mechanism identification
- Standalone mechanism preservation
- RN impact quantification

### Dependencias
- `RFC_EVENT_MODEL_CERTIFICATION` (PASS)
- `RFC_CASH_CERTIFICATION_BPP_POSCOBRO` (PASS CONDITIONAL)
- Classification engine (upstream)
- Closing engine (downstream — consumes event_type)

### Riesgos
| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| New concept discovered without event assignment | ALTA | Typology must be pre-assigned per marketplace |
| Mechanism paired detection fails (edge case) | MEDIA | Order-level groupby is deterministic — test coverage required |
| Standalone mechanism incorrectly marked as paired | MEDIA | Amount match validation + manual review threshold |
| Rule applied to marketplace without MECHANISM concepts | BAJA | Rule degrades gracefully (all concepts = ROOT_EVENT) |

### Marketplace applicability
| Marketplace | Has MECHANISMS | Certificado |
|-------------|----------------|-------------|
| ML | Sí (BPP, Poscobro) | SÍ |
| PARIS | No | N/A |
| RIPLEY | No | N/A |
| FALABELLA | No | N/A |
| SHOPIFY | No (hypothesis) | PENDIENTE |

---

## Skill 2: `cash-reality-certification`

### Objetivo
Validar que los números del ledger corresponden a caja real. Cada concepto debe tener una fuente de caja externa (Liberaciones, extractos bancarios, etc.) que confirme su valor.

### Input
- Ledger rows (marketplace, concepto, monto, período)
- Cash source file (Liberaciones, bank statement, payment processor report)
- Pairing rules (if applicable)

### Output
- Cash delta per concept: `(ledger_amount - cash_amount) / ledger_amount`
- Cash proxy identification per concept
- Confidence score per marketplace
- Certification verdict (PASS / FAIL / PASS CONDITIONAL)

### Dependencias
- Cash source file availability
- `G6_CASH_REALITY_CERTIFICATION` methodology
- `RFC_CASH_CERTIFICATION_BPP_POSCOBRO` methodology

### Riesgos
| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Cash source unavailable | ALTA | Impossible to certify cash reality — concept remains UNCERTIFIED |
| Cash source incomplete (partial period) | MEDIA | Partial certification with caveat |
| Cash source format changes | MEDIA | Loader spec must be updated |
| Time lag between economic event and cash settlement | BAJA | Define settlement window; accept within threshold |

### Marketplace applicability
| Marketplace | Cash source | Certificado |
|-------------|-------------|-------------|
| ML | Liberaciones (Abril 2025-04) | SÍ (G6, $69.9M neto, 3.9% delta) |
| ML (BPP/Poscobro) | Liberaciones reserve_for_dispute | SÍ (RFC_CASH, NET=$0) |
| PARIS | N/A | NO |
| RIPLEY | N/A | NO |
| SHOPIFY | N/A | PENDIENTE |

---

## Skill 3: `marketplace-reconciliation`

### Objetivo
Conciliar ledger vs source files por marketplace. Verificar que cada fila del ledger tiene un source file correspondiente y viceversa.

### Input
- Source files (XLSX, CSV, XML)
- Ledger rows (id_transaccion, archivo_origen, monto)
- Loader spec

### Output
- Row coverage: `matched_ledger_rows / total_ledger_rows`
- Amount coverage: `matched_amount / total_amount`
- Source-side orphans: rows in source not in ledger
- Bridge table with deltas

### Dependencias
- `FINANCIAL_CHAIN_DESIGN` framework
- `MARKETPLACE_CHARGE_RECONCILIATION_CERTIFICATION` methodology

### Riesgos
| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Source file missing | ALTA | Cannot reconcile — mark as PENDIENTE |
| Source file format changed | MEDIA | Loader spec versioning + file validation |
| Partial period reconciliation | BAJA | Accept with caveat for current month |

---

## Skill 4: `financial-taxonomy`

### Objetivo
Mantener y certificar la taxonomía financiera única: 6 grupos de P&L, asignación de conceptos, sign convention, relaciones jerárquicas.

### Input
- `FINANCIAL_STRUCTURE` dictionary
- `RAW_TO_CLASSIFICATION_MAP`
- New concepts (from source files or marketplace onboarding)

### Output
- Certified concept → financial_group mapping
- Certified sign convention per concept
- Hierarchical KPI definitions
- Impact analysis of taxonomy changes

### Dependencias
- `KPI_DEFINITIONS_V1`
- `SEMANTIC_TRACEABILITY_MATRIX`
- `MARKETPLACE_CONCEPT_MASTER_CERTIFICATION`

### Riesgos
| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Taxonomy change affects historical data | ALTA | Versioned structure; historical closing frozen |
| New concept without financial_group | MEDIA | Default to 'ajustes' until certified |
| Cross-MP concept collision | BAJA | Same canonical name must map to same group |

---

## Skill 5: `pnl-certification`

### Objetivo
Certificar que Resultado Neto es correcto: suma de conceptos regla + exclusión de mechanisms pareados + preservación de standalone.

### Input
- Closed periods (marketplace_cierre_financiero_v1)
- Event model output (per-order event_type)
- Cash cross-check

### Output
- RN per period
- Delta: actual RN vs economic RN (paired mechanisms removed)
- Cash validation per period
- Certification verdict

### Dependencias
- `financial-event-causality` (upstream)
- `cash-reality-certification` (parallel)
- `financial-taxonomy` (upstream)

### Riesgos
| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Closing sums without dedup | ALTA (KNOWN) | This is structural — G6.1 documente d FAIL |
| Mechanism removal affects different periods | MEDIA | Period-by-period certification required |
| Standalone mechanisms incorrectly identified | BAJA | Unlikely (event model certifies this) |

---

## Skill 6: `audit-certification`

### Objetivo
Certificar que cada transacción es auditabile: origen, clasificación, evento, impacto caja, XML evidence.

### Input
- All upstream certifications
- XML coverage report
- Audit trail (marketplace_auditoria_v1)

### Output
- Per-row audit trail: source_file → loader → classification → event_model → closing
- XML coverage score
- Audit readiness score
- Certification verdict

### Dependencias
- All 5 skills above
- `dte_truth_v1` (XML evidence)
- `marketplace_auditoria_v1` (audit alerts)

### Riesgos
| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| XML missing for row | MEDIA | Mark as `SIN_RECURSO_XML` — audit still passes |
| Classification confidence < 1.0 | BAJA | Flag as low-confidence but still auditable |
| Manual correction without trace | ALTA | Require marketplace_correcciones_v1 entry |

---

## Skill 7: `marketplace-onboarding`

### Objetivo
Incorporar un nuevo marketplace o canal ecommerce (Shopify, WooCommerce, etc.) al pipeline financiero certificado.

### Input
- Source files (new marketplace)
- Source format spec
- Concept inventory
- Rate tables (commissions, fees)
- Cash source (if available)

### Output
- Loader spec
- Concept → classification map
- Financial_group assignment per concept
- Event_role assignment per concept
- Cash cross-check (if possible)
- Onboarding certification verdict

### Dependencias
- `financial-taxonomy` (classification map)
- `marketplace-reconciliation` (source matching)
- `cash-reality-certification` (if cash source available)
- `financial-event-causality` (if MECHANISM concepts)

### Riesgos
| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Source format ambiguous | ALTA | Require formal spec from marketplace |
| Unknown concepts without mapping | ALTA | Default to NO_CLASIFICADO; manual review required |
| No cash source available | MEDIA | Certify as ACCRUAL-ONLY with caveat |
| Rate structure fundamentally different | MEDIA | Map to existing financial groups; may require new subgroups |
| MECHANISM pattern discovered late | MEDIA | Recertification after full order-level analysis |

### Onboarding checklist

| Step | What | Skill |
|------|------|-------|
| 1 | Source file inventory | marketplace-onboarding |
| 2 | Loader spec definition | marketplace-onboarding |
| 3 | Test load (subset) | marketplace-onboarding |
| 4 | Concept inventory | marketplace-onboarding |
| 5 | Classification map | financial-taxonomy |
| 6 | Financial_group assignment | financial-taxonomy |
| 7 | Event_role assignment | financial-event-causality |
| 8 | Cash cross-check | cash-reality-certification |
| 9 | Full load + classification | marketplace-onboarding |
| 10 | Closing + RN certification | pnl-certification |
| 11 | Audit certification | audit-certification |
| 12 | API contract validation | pnl-certification |
| 13 | 14/14 regression | all |
| 14 | Onboarding certification | marketplace-onboarding |

---

## Skills Dependency Graph

```
financial-taxonomy
  ├── marketplace-reconciliation
  ├── financial-event-causality
  │     └── cash-reality-certification
  │           └── pnl-certification
  │                 └── audit-certification
  │                       └── marketplace-onboarding
  └───────────────────────────────────────┘
```

All skills depend on `financial-taxonomy` (the classification map is the foundation).
`marketplace-onboarding` depends on ALL upstream skills.
