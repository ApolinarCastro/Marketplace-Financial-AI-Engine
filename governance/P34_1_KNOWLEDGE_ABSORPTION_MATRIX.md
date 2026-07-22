# P34.1 — Knowledge Absorption Matrix

**Date:** 2026-07-09
**Rule:** Knowledge debe fluir desde archivos Markdown → sistema consumible por código

---

## Matrix Structure

Cada fila indica:
- **Fuente**: archivo(s) markdown origen
- **Destino**: componente que debe absorber el conocimiento
- **Estado**: YA_ABSORBIDO / NO_ABSORBIDO / PARCIAL
- **Evidencia**: prueba de que existe o no existe la absorción
- **Archivos reemplazables**: cuántos archivos markdown dejarían de ser necesarios

---

## 1. Knowledge Base (knowledge_index.yaml)

| Fuente | Destino | Estado | Evidencia | Reemplazables |
|---|---|---|---|---|
| DEC-022 a DEC-027 (5 files) | knowledge_index.yaml | **PARCIAL** | Indexados (presentes) pero sin código que los sirva | 5 |
| DEC-001 a DEC-003, DEC-009, DEC-019 | knowledge_index.yaml | **YA_ABSORBIDO** | Presentes en index | 5 |
| CERT-PLATFORM-V1 (governance/) | knowledge_index.yaml | **YA_ABSORBIDO** | Presente en index | 1 |
| AUDIT-ML-2026-06 | knowledge_index.yaml | **YA_ABSORBIDO** | Presente en index | 1 |
| AUDIT-DATA-FRESHNESS | knowledge_index.yaml | **YA_ABSORBIDO** | Presente en index | 1 |
| TAXONOMY-INGRESOS/DEVOLUCIONES/AJUSTES | knowledge_index.yaml | **YA_ABSORBIDO** | Presente en index | 3 |
| CONCEPT_REGISTRY_V2 (KnowledgeBase/) | knowledge_index.yaml | **NO_ABSORBIDO** | No hay entrada en index | 1 |
| EVENT_REGISTRY_V2 (KnowledgeBase/) | knowledge_index.yaml | **NO_ABSORBIDO** | No hay entrada en index | 1 |
| CASH_ROLE_REGISTRY_V1 (KnowledgeBase/) | knowledge_index.yaml | **NO_ABSORBIDO** | No hay entrada en index | 1 |
| 4 taxonomy JSONs | knowledge_index.yaml | **NO_ABSORBIDO** | No hay entradas para taxonomías | 4 |
| 10 ML V1 model files | knowledge_index.yaml | **NO_ABSORBIDO** | No hay entradas | 10 |
| **Subtotal** | | | | **32** |

---

## 2. DEC Registry

| Fuente | Destino | Estado | Evidencia | Reemplazables |
|---|---|---|---|---|
| governance/decisions/DEC-022.md | DEC Registry | **PARCIAL** | En knowledge_index.yaml pero sin API/endpoint | 1 |
| governance/decisions/DEC-024.md | DEC Registry | **PARCIAL** | En knowledge_index.yaml pero sin API/endpoint | 1 |
| governance/decisions/DEC-025.md | DEC Registry | **PARCIAL** | En knowledge_index.yaml pero sin API/endpoint | 1 |
| governance/decisions/DEC-026.md | DEC Registry | **PARCIAL** | En knowledge_index.yaml pero sin API/endpoint | 1 |
| governance/decisions/DEC-027.md | DEC Registry | **PARCIAL** | En knowledge_index.yaml pero sin API/endpoint | 1 |
| KnowledgeBase/DEC/DEC-014.md | DEC Registry | **NO_ABSORBIDO** | Stub file (<100B, sin contenido real) | 1 |
| KnowledgeBase/DEC/DEC-015.md | DEC Registry | **NO_ABSORBIDO** | Stub file | 1 |
| KnowledgeBase/DEC/DEC-016.md | DEC Registry | **NO_ABSORBIDO** | Stub file | 1 |
| KnowledgeBase/DEC/DEC-019.md | DEC Registry | **NO_ABSORBIDO** | Stub file | 1 |
| KnowledgeBase/DEC/DEC-071.md | DEC Registry | **NO_ABSORBIDO** | Tiene contenido real, no indexado | 1 |
| **Subtotal** | | | | **10** |

---

## 3. RFC Registry

| Fuente | Destino | Estado | Evidencia | Reemplazables |
|---|---|---|---|---|
| governance/RFC-001-RIPLEY-*.md | RFC Registry | **NO_ABSORBIDO** | No existe RFC registry en código | 2 |
| governance/RFC-PARIS-XML-*.md | RFC Registry | **NO_ABSORBIDO** | No existe RFC registry | 1 |
| governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md | RFC Registry | **NO_ABSORBIDO** | No existe RFC registry | 1 |
| governance/RFC_EVENT_MODEL_CERTIFICATION.md | RFC Registry | **NO_ABSORBIDO** | No existe RFC registry | 1 |
| governance/RFC_FINANCIAL_STRUCTURE_REDESIGN.md | RFC Registry | **NO_ABSORBIDO** | No existe RFC registry | 1 |
| governance/RFC_POSCOBRO_CAUSALITY_FINAL.md | RFC Registry | **NO_ABSORBIDO** | No existe RFC registry | 1 |
| **Subtotal** | | | | **7** |

---

## 4. Skills Registry

| Fuente | Destino | Estado | Evidencia | Reemplazables |
|---|---|---|---|---|
| governance/SKILLS_REGISTRY_V1.md | Skills Registry | **NO_ABSORBIDO** | `grep -r "SKILLS_REGISTRY" . --include="*.py"` = 0 | 1 |
| governance/SKILLS_REGISTRY.md | Skills Registry | **NO_ABSORBIDO** | Idem | 1 |
| governance/SKILLS_REGISTRY.json | Skills Registry | **NO_ABSORBIDO** | Idem | 1 |
| **Subtotal** | | | | **3** |

---

## 5. Taxonomías (ya parcialmente absorbidas)

| Fuente | Destino | Estado | Evidencia | Reemplazables |
|---|---|---|---|---|
| KnowledgeBase/Marketplace/Taxonomy/ml_v1.json | financial_engine.py | **YA_ABSORBIDO** | `load_taxonomy_json()` en línea 373 | 0 (es el archivo) |
| KnowledgeBase/Marketplace/Taxonomy/ripley_v1.json | financial_engine.py | **YA_ABSORBIDO** | `load_taxonomy_json()` + `_build_signal_filter()` | 0 (es el archivo) |
| KnowledgeBase/Marketplace/Taxonomy/paris_v1.json | financial_engine.py | **YA_ABSORBIDO** | `load_taxonomy_json()` en línea 373 | 0 |
| KnowledgeBase/Marketplace/Taxonomy/falabella_v1.json | financial_engine.py | **YA_ABSORBIDO** | `load_taxonomy_json()` en línea 373 | 0 |
| RAW_TO_CLASSIFICATION_MAP (hardcoded) | Taxonomy consolidada | **NO_ABSORBIDO** | 264 líneas Python, debería ser JSON/YAML | 1 (el propio .py) |
| **Subtotal** | | | | **1** |

---

## 6. Lineage

| Fuente | Destino | Estado | Evidencia | Reemplazables |
|---|---|---|---|---|
| DEC-019 (conocimiento) | LineageEngine pnl_flag | **YA_ABSORBIDO** | `include_in_operational_pnl` en queries | 0 |
| DEC-022 (Financial Engine Authority) | LineageEngine | **YA_ABSORBIDO** | Usa FinancialEngine (no directo a DB) | 0 |
| **Subtotal** | | | | **0** |

---

## 7. Explainability

| Fuente | Destino | Estado | Evidencia | Reemplazables |
|---|---|---|---|---|
| KPI_DEFINITIONS_V1.md | ExplainabilityEngine | **PARCIAL** | `KPI_CATALOG` hardcoded (mismo contenido, distinto formato) | 1 |
| CONCEPT_REGISTRY_V2.md | ExplainabilityEngine | **NO_ABSORBIDO** | No referencia el registro de conceptos | 0 |
| **Subtotal** | | | | **1** |

---

## 8. Certification Engine

| Fuente | Destino | Estado | Evidencia | Reemplazables |
|---|---|---|---|---|
| trust score definitions | CertificationEngine | **YA_ABSORBIDO** | 6 claims con evidence SQL | 0 |
| KPI definitions | CertificationEngine | **YA_ABSORBIDO** | reconciliation/ingresos/devoluciones/etc | 0 |
| **Subtotal** | | | | **0** |

---

## 9. Hallazgos de auditoría (proceso automático faltante)

| Fuente | Destino | Estado | Evidencia | Reemplazables |
|---|---|---|---|---|
| marketplace_auditoria_v1 | knowledge_index.yaml (auto) | **NO_EXISTE** | Cero código que lea auditoría y cree KB entries | ~46 cert reports |
| pipeline_log | knowledge_index.yaml (auto) | **NO_EXISTE** | Cero código | ~20 reports |
| run_audit() output | Skills Registry (auto) | **NO_EXISTE** | Cero código | ~3 skills registries |
| **Subtotal** | | | | **~69** |

---

## Resumen de absorción

| Destino | YA_ABSORBIDO | PARCIAL | NO_ABSORBIDO | Reemplazables |
|---|---|---|---|---|
| Knowledge Base (index) | 8 | 1 | 4 | 32 |
| DEC Registry | 0 | 5 | 5 | 10 |
| RFC Registry | 0 | 0 | 6 | 7 |
| Skills Registry | 0 | 0 | 3 | 3 |
| Taxonomías | 4 | 0 | 1 | 1 |
| Lineage | 2 | 0 | 0 | 0 |
| Explainability | 0 | 1 | 1 | 1 |
| Certification | 2 | 0 | 0 | 0 |
| Auto audit → KB | 0 | 0 | 1 | 69 |
| **Total** | **16** | **7** | **21** | **123** |

### Significado

- **16 conocimientos ya absorbidos**: funcionan sin archivos markdown
- **7 parcialmente absorbidos**: existen en index pero sin API/endpoint
- **21 no absorbidos**: existen solo como markdown, no consumibles por código
- **123 archivos reemplazables** después de absorción completa

---

## Knowledge Sources vs Consumers (matriz completa)

```
                    │ KB     │ DEC    │ RFC    │ Skills │ Tax    │ Lineage │ Explain │ Cert
────────────────────┼────────┼────────┼────────┼────────┼────────┼─────────┼─────────┼─────
governance/*.md     │ MANUAL │ ✗      │ ✗      │ ✗      │ ✗      │ ✗       │ ✗       │ ✗
governance/decisions│ MANUAL │ ✗      │ -      │ -      │ -      │ inline  │ -       │ -
KnowledgeBase/      │ MANUAL │ ✗      │ ✗      │ ✗      │ ✓ JSON │ ✗       │ ✗       │ ✗
knowledge_index.yaml│ -      │ -      │ -      │ -      │ -      │ -       │ -       │ -  
marketplace_auditor │ ✗      │ ✗      │ ✗      │ ✗      │ ✗      │ ✗       │ ✗       │ ✗
API endpoints       │ ✗      │ ✗      │ ✗      │ ✗      │ ✓      │ ✓       │ ✓       │ ✓
```

**Leyenda:**
- `✓` = consumido automáticamente por código
- `MANUAL` = solo lectura humana del YAML
- `inline` = referencia en comentario de código
- `✗` = no consumido

**Conclusión: solo 4 taxonomy JSONs y los engines internos son automáticamente consumidos. El 99% del conocimiento es documentación muerta para el sistema.**
