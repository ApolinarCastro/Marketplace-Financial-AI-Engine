# P34.1 — Knowledge Consolidation (KCE)

**Date:** 2026-07-09
**Methodology:** READ-ONLY audit, no file modifications

---

## FASE 1 — Auditoría del Conocimiento

### 1.1 Clasificación por destino

| Origen | Archivos | Permanente | Histórico | Temporal | Obsoleto |
|---|---|---|---|---|---|
| `governance/` | 356 | 286 | 50 | 6* | 14 |
| `KnowledgeBase/` | 110 | 88 | 0 | 0 | 22** |
| Root (markdowns) | 70 | 0 | 70 | 0 | 0 |
| `governance/decisions/` | 5 | 5 | 0 | 0 | 0 |
| **Total** | **541** | **379** | **120** | **6** | **36** |

*\* 6 DUPLICADO en governance/ (SKILLS_REGISTRY.json/.md, phase12b_raw.json/.json)
\*\* 2 OBSOLETO + 20 stub files en KnowledgeBase/*

### 1.2 Conocimiento Permanente (379 archivos)

Distribución:

| Categoría | Archivos | Ejemplos |
|---|---|---|
| Certificaciones vigentes | ~200 | RIPLEY_*, PARIS_*, ML_*, POSCOBRO_*, etc. |
| Decisiones arquitectónicas | 5 | DEC-022 a DEC-027 |
| Core registries | 3 | CONCEPT_REGISTRY_V2, EVENT_REGISTRY_V2, CASH_ROLE_REGISTRY_V1 |
| Taxonomías JSON | 4 | ml_v1, ripley_v1, paris_v1, falabella_v1 |
| KPIs y definiciones | ~10 | KPI_DEFINITIONS_V1, TRUST_CERTIFICATION, etc. |
| Modelos financieros MP | 16 | ML_* V1 models, RIPLEY validation reports |
| Análisis operacionales | ~80 | G5.7, E1.0, Phase 12-16F deliverables |
| P32 sprints recientes | 30+ | P32R7, P32R10, P33 deliverables |

### 1.3 Conocimiento Histórico (120 archivos)

70 reports en raíz del proyecto (nunca movidos a governance/) + 50 en governance/:

| Grupo | Count | Característica |
|---|---|---|
| Reports de auditoría en raíz | 70 | P32R4, P32R5, P32R7, P32R8, FINAL_*, FRONTEND_* |
| FCG_REPORTS/ | 19 | Certificaciones de una sola vez, ya cerradas |
| CIERRE_FINANCIERO_* | 3 | Drafts nunca implementados |
| RFC completados | 3 | RFC-001, RFC-PARIS-XML, etc. |
| Sprint completados | 5 | SPRINT_A1, SPRINT_B1, SCORECARD, etc. |

### 1.4 Conocimiento Obsoleto (36 archivos)

| Grupo | Count | Razón |
|---|---|---|
| PARIS duplicate chain | 6 | $21.2M conclusión errónea (DEC-020) |
| PARIS Economic Model V1 | 3 | INVALIDATED por V2 |
| RIPLEY_GROSS_REVENUE_RECHAZADO | 1 | RECHAZADO en título |
| EVENT_REGISTRY_V1 | 1 | Superseded by V2 |
| MARKETPLACE_CHARGE_RECONCILIATION_V1 | 1 | Superseded by V2 |
| KnowledgeBase stub files | 22 | "Legacy [type] artifact" sin contenido |
| KNOWLEDGE_BASE_BLUEPRINT | 1 | Superseded by Phase 12.6 |
| GOVERNANCE_LAYER_V1 | 1 | Superseded by V2 registries |

---

## FASE 2 — Knowledge Learning

### 2.1 ¿Existe un proceso automatizado?

**No.** Evidencia:

| Consulta | Resultado |
|---|---|
| `grep -r "knowledge.*ingest\|auto.*learn\|knowledge.*extract" engine/` | **0 matches** |
| `grep -r "create_knowledge\|store_knowledge\|update_knowledge" .` | **0 matches** |
| `grep -r "SKILLS_REGISTRY" . --include="*.py"` | **0 matches** |
| `grep -r "knowledge_index" . --include="*.py" \| grep -v test` | **0 matches** (solo test_knowledge.py) |
| `grep -r "marketplace_auditoria_v1" . --include="*.py"` | Solo **3 endpoints API** de lectura, 0 escritura → conocimiento |
| `grep -r "CLASIFICACION_TO_FINANCIAL_GROUP" . --include="*.py"` | Solo en `marketplace_auditor.py` para clasificación, no para KB |

### 2.2 Componentes faltantes

El sistema carece de 5 componentes para aprendizaje automático:

1. **KnowledgeExtractor**: Lee `marketplace_auditoria_v1` después de `run_audit()` y extrae hallazgos estructurados
2. **DecisionParser**: Escanea `governance/` por nuevos archivos DEC-XXX/RFC-XXX y extrae título, estado, decisión
3. **KnowledgeIndexer**: Actualiza `knowledge_index.yaml` automáticamente con nuevas entradas
4. **SkillUpdater**: Detecta cuando un nuevo DEC/RFC afecta skills existentes y actualiza SKILLS_REGISTRY
5. **DocumentRetention**: Marca archivos governance/ como HISTÓRICO cuando su conocimiento es absorbido

**Ninguno de estos componentes existe en el código actual.**

---

## FASE 3 — Matriz de Absorción

### 3.1 ¿Qué conocimiento es consumido por código?

| Conocimiento | Consumido por | Cómo |
|---|---|---|
| **Taxonomías JSON** (4 files) | `financial_engine.py` | `load_taxonomy_json()` carga `KnowledgeBase/Marketplace/Taxonomy/*.json` para signal_mode |
| **Clasificación** (hardcoded) | `marketplace_auditor.py` | `RAW_TO_CLASSIFICATION_MAP` (200+ entries, Python dict) |
| **KPI_CATALOG** (hardcoded) | `explainability_engine.py` | 6 KPI definitions hardcoded en Python |
| **DEC-019** (referencia inline) | `financial_engine.py` | Comentario de 1 línea en docstring |
| **DECs varios** (referencia inline) | `marketplace_auditor.py` | 2 comentarios en código |
| **knowledge_index.yaml** | `test_knowledge.py` | Solo tests, no runtime |
| **Resto (~530 archivos)** | **NADA** | Solo lectura humana |

**Conclusión: 4 archivos de conocimiento son consumidos por código (0.7%). 535 archivos (99.3%) son solo para humanos.**

### 3.2 Destinos de absorción

| Destino | Conocimiento que debería absorber | Archivos reemplazables |
|---|---|---|
| **Knowledge Base** | CONCEPT_REGISTRY_V2, EVENT_REGISTRY_V2, CASH_ROLE_REGISTRY_V1 | 3 core registries (ya existen) |
| **DEC Registry** | 10 DECs (5 governance/decisions/ + 5 KnowledgeBase/DEC/) | ~10 archivos |
| **Taxonomías** | 4 JSON + mapa RAW_TO_CLASSIFICATION_MAP | 1 archivo consolidado |
| **Skills Registry** | 3 registros actuales → 1 consolidado | 3 archivos |
| **Lineage** | DEC-019 inline reference → formal knowledge entry | 0 |
| **Explainability** | KPI_CATALOG → knowledge-driven (no hardcoded) | 0 |
| **Certification** | 6 claims + evidence SQL (ya en certification_engine.py) | 0 |

---

## FASE 4 — Dependencias

### 4.1 Cadena actual

```
Markdown (541 archivos, ~2 MB)
    │ 99.3% NO consumido por código
    │
    ▼
Knowledge Base (knowledge_index.yaml, 19 entries)
    │ Solo validado por tests (test_knowledge.py)
    │
    ▼
Engine (7 engines en engine/v4/)
    │ Leen solo DB (no archivos knowledge/)
    │ Excepción: financial_engine.py → taxonomías JSON
    │
    ▼
Backend (api.py, 33 endpoints)
    │ Oroquesta engines, sirve JSON
    │ Ruta /knowledge/export es write-only (→ Obsidian)
    │
    ▼
Frontend (3 templates HTML)
    │ Consume API, zero lógica financiera
    │
    ▼
IA (solo lectura humana via AGENTS.md)
```

### 4.2 Cadena deseada (después de KCE)

```
Markdown (archivos históricos/temporales → archivados)
    │
    ▼
Knowledge Consolidation Engine (NUEVO)
    ├── Lee marketplace_auditoria_v1 automáticamente
    ├── Extrae DEC/RFC de governance/
    ├── Actualiza knowledge_index.yaml
    ├── Actualiza Skills Registry
    └── Marca archivos absorbidos
    │
    ▼
Knowledge Base (API-served, runtime-consumible)
    ├── /api/v4/knowledge (GET — sirve knowledge_index.yaml)
    ├── /api/v4/knowledge/dec (GET — lista DECs)
    ├── /api/v4/knowledge/skills (GET — lista skills)
    └── /api/v4/knowledge/absorbed (GET — archivos absorbidos)
    │
    ▼
Engine → Backend → Frontend → IA (sin cambios en consumidores)
```

### 4.3 Documentos que dejarían de existir después de absorción

400+ archivos podrían ser archivados o eliminados después de que KCE los absorba. Ver FASE 5.

---

## FASE 5 — Candidatos

### 5.1 Archivar (después de absorción por KCE)

Una vez que KCE extraiga el conocimiento de estos archivos y lo almacene en knowledge_index.yaml + API:

| Grupo | Archivos | Conocimiento absorbido |
|---|---|---|
| **DEC governance/decisions/** (5) | 5 | Tabla DEC en KB |
| **DEC KnowledgeBase/DEC/** (5) | 5 | Tabla DEC en KB |
| **Certificaciones vigentes** (~200) | ~200 | Estado de certificación en cert_engine |
| **P32 sprints** (30) | 30 | Resumen en KB |
| **FCG_REPORTS/** (19) | 19 | Resultados en tabla |
| **RFC governance/** (3) | 3 | Estado en KB |
| **Phase 12-16F** (~50) | ~50 | Resumen en KB |

**Subtotal archivar: ~312 archivos**

### 5.2 Consolidar

| Grupo | Archivos actuales | Destino consolidado |
|---|---|---|
| SKILLS_REGISTRY.json + .md + V1.md | 3 | 1 `skills_registry.yaml` consumible |
| RAW_TO_CLASSIFICATION_MAP (hardcoded) | 1 Python (200+ lines) | taxonomy JSON consolidado |
| KPI_CATALOG (hardcoded) | 1 Python (6 KPIs) | knowledge-driven config |
| phase12b_raw.json/.json | 2 | Eliminar tras verificar absorción |

### 5.3 Absorber por KCE

Conocimiento que KCE debe extraer automáticamente:

| Fuente | Destino en KB |
|---|---|
| `marketplace_auditoria_v1` (nuevos hallazgos) | Entrada en knowledge_index.yaml, tipo "audit" |
| Certificaciones (PASS/FAIL/delta) | Estado en tabla cert_status |
| DECs (nuevos en governance/) | Entrada en DEC registry |
| RFCs | Entrada en RFC registry |
| Skills definiciones | Entrada en skills registry |

### 5.4 Eliminar posteriormente

Después de que KCE esté operativo y haya absorbido todo:

| Grupo | Archivos | Condición |
|---|---|---|
| KnowledgeBase stub files | 25 | Sin contenido, eliminables inmediatamente |
| KnowledgeBase empty templates | 14 | Sin contenido, eliminables inmediatamente |
| Root temp/scratch | 85 | Sin valor, eliminables independientemente de KCE |
| Governance DUPLICADO | 6 | Información duplicada |
| Governance OBSOLETO | 14 | Conclusiones invalidadas (histórico) |
| **Subtotal eliminar** | **144** | **~47.9 MB** |

### 5.5 Resumen de candidatos

| Acción | Archivos | Peso | Depende de KCE |
|---|---|---|---|
| **Archivar** | ~312 | ~900 KB | Sí (después de absorción) |
| **Consolidar** | ~7 | ~30 KB | Sí |
| **Absorber** | N/A (proceso) | N/A | Sí (es el proceso) |
| **Eliminar** | 144 | ~47.9 MB | No (independiente) |
| **Conservar** | ~379 | ~500 KB | No |

---

## VALIDACIÓN — Evidencia de ausencia de aprendizaje automático

### V1: knowledge_index.yaml es manual

```
$ grep -r "knowledge_index" . --include="*.py" | grep -v test | grep -v __pycache__
→ 0 resultados
```

Solo `test_knowledge.py` (6 tests) lee `knowledge_index.yaml`. Ningún código runtime lo consume o actualiza.

### V2: Skills Registry no consume auditorías

```
$ grep -r "SKILLS_REGISTRY" . --include="*.py"
→ 0 resultados
```

Tres archivos de skills en governance/ — cero consumo por código.

### V3: Auditorías no son reutilizadas automáticamente

```
$ grep -r "marketplace_auditoria_v1" . --include="*.py"
```

Resultados: solo `api.py` (3 endpoints GET) + `marketplace_auditor.py` (escritura). Cero código que convierta hallazgos en entradas de conocimiento.

### V4: Conocimiento distribuido en cientos de markdown

| Categoría | Archivos |
|---|---|
| governance/*.md | 356 |
| KnowledgeBase/*.md | 110 |
| Raíz del proyecto | 70 |
| **Total** | **541** |

Todos consumidos exclusivamente por humanos. Los engines solo leen DB + 4 taxonomy JSONs.

### V5: La clasificación está hardcodeada, no es knowledge-driven

`RAW_TO_CLASSIFICATION_MAP` en `marketplace_auditor.py` (200+ entries, 264 líneas) es un Python dict. No se carga desde ningún archivo de conocimiento. Para cambiar una regla de clasificación, se debe modificar el código Python, no un documento governance/.
