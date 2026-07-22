# P34.1 — Final Verdict

**Date:** 2026-07-09
**Methodology:** READ-ONLY audit, 689 files analyzed

---

## Q1: ¿Qué conocimiento debe permanecer como código?

Conocimiento que actualmente está en markdown pero debería estar en código ejecutable o configuraciones consumibles:

| Conocimiento | Forma actual | Debe migrar a | Razón | Urgencia |
|---|---|---|---|---|
| `RAW_TO_CLASSIFICATION_MAP` (264 líneas) | Hardcoded Python dict en `marketplace_auditor.py` | Archivo JSON/YAML en `knowledge/taxonomy/` | Cambiar reglas requiere modificar código. Debería ser data-driven. | ALTA |
| `KPI_CATALOG` (6 KPIs) | Hardcoded Python dict en `explainability_engine.py` | Archivo YAML o tabla DB | Las definiciones de KPI deberían ser configurables, no código. | MEDIA |
| `FINANCIAL_STRUCTURE` (9 grupos) | Hardcoded Python dict en `marketplace_auditor.py` | Taxonomía JSON (ya existe) | Ya existe en los taxonomy JSONs — código duplica datos. | MEDIA |

**Evidencia:**
- `engine/v4/marketplace_auditor.py:9-272`: `RAW_TO_CLASSIFICATION_MAP` = 264 líneas de Python
- `engine/v4/marketplace_auditor.py:277-380`: `FINANCIAL_STRUCTURE` = 104 líneas, duplica información en taxonomy JSONs
- `engine/v4/explainability/explainability_engine.py:23-67`: `KPI_CATALOG` = 45 líneas de 6 KPI definitions

**Total: 3 estructuras de datos actualmente en código que deberían ser archivos de conocimiento.**

---

## Q2: ¿Qué conocimiento debe permanecer como Knowledge Base?

Conocimiento que debe permanecer documentado (no código) pero ser consumible por el sistema vía API:

| Conocimiento | Archivos | Debe ser accesible vía | Estado actual |
|---|---|---|---|
| **DEC Registry** | 10 files (5 governance/decisions/ + 5 KnowledgeBase/DEC/) | `GET /api/v4/knowledge/dec` | Parcialmente indexado en knowledge_index.yaml, sin API |
| **RFC Registry** | 7 files (governance/RFC*) | `GET /api/v4/knowledge/rfc` | No existe |
| **Skills Registry** | 3 files (governance/SKILLS_REGISTRY*) | `GET /api/v4/knowledge/skills` | No existe — 0 referencias en código |
| **Core registries** | 3 files (CONCEPT_REGISTRY_V2, EVENT_REGISTRY_V2, CASH_ROLE_REGISTRY_V1) | `GET /api/v4/knowledge/concepts` | Existen como archivos, no indexados |
| **Certifications status** | ~200 cert reports | `GET /api/v4/certify` + KB | Ya existe `/api/v4/certify` (6 claims). Reports markdown son redundantes. |
| **Taxonomías** | 4 JSON files | `GET /api/v4/taxonomy` | Ya consumidos por financial_engine.py pero sin endpoint público |

**Evidencia:**
- `grep -r "knowledge" api/api.py`: solo 1 ruta (`POST /api/v4/knowledge/export`), write-only
- `grep -r "dec" api/api.py --ignore-case`: 0 rutas
- `grep -r "rfc" api/api.py --ignore-case`: 0 rutas
- `grep -r "skill" api/api.py --ignore-case`: 0 rutas

**Total: 6 categorías de conocimiento que deben estar disponibles vía API de solo lectura.**

---

## Q3: ¿Qué conocimiento debe convertirse en Skills?

Skills = capacidades reutilizables que los engines pueden ejecutar.

Actualmente hay 3 skills registries en `governance/` con **cero consumo por código**. Deben consolidarse en un archivo único consumible:

| Skill propuesta | Origen | Engine que la ejecuta | Ya implementada en código |
|---|---|---|---|
| `financial-taxonomy` | SKILLS_REGISTRY_V1.md | financial_engine.py (signal_mode) | **SÍ** — `load_taxonomy_json()` + `_build_signal_filter()` |
| `pnl-certification` | SKILLS_REGISTRY_V1.md | certification_engine.py | **SÍ** — 6 claims, PASS/FAIL |
| `marketplace-reconciliation` | SKILLS_REGISTRY_V1.md | reconciliation_engine.py | **SÍ** — 5 niveles, 66 tests |
| `audit-certification` | SKILLS_REGISTRY_V1.md | marketplace_auditor.py | **SÍ** — `run_audit()`, 22 check types |
| `cash-reality-certification` | SKILLS_REGISTRY_V1.md | reconciliation_engine.py | **PARCIAL** — nivel TESORERIA existe |
| `financial-event-causality` | SKILLS_REGISTRY_V1.md | No existe | **NO** — no hay engine de causalidad |
| `financial-root-cause` | SKILLS_REGISTRY.md | intelligence_engine.py | **SÍ** — anomaly detection |
| `waterfall-validator` | SKILLS_REGISTRY.md | financial_engine.py | **SÍ** — conservation check |
| `regression-detector` | SKILLS_REGISTRY.md | test suite | **SÍ** — 14 regression tests |
| `single-truth-guardian` | SKILLS_REGISTRY.md | certification_gate.py | **SÍ** — 27 tests |

**Evidencia:**
- 6/10 skills ya tienen engine implementado (60%)
- 1/10 tiene implementación parcial
- 1/10 no existe (financial-event-causality)
- 2/10 son tests, no engines runtime

**El Skills Registry documenta lo que YA existe en código pero no hay enlace automático entre la documentación y la implementación.**

---

## Q4: ¿Qué conocimiento debe archivarse?

Conocimiento que ya no aporta valor operativo. 3 categorías:

### Categoría A: Archivar inmediatamente (independiente de KCE) — 144 archivos

| Grupo | Archivos | Peso | Evidencia de nulo valor |
|---|---|---|---|
| Root temp/scratch/output | 85 | ~47.8 MB | Ver P34_REPOSITORY_HYGIENE.md. Log de 43 MB, backups, one-off scripts |
| KnowledgeBase stubs | 25 | ~2 KB | Archivos con solo "Legacy [type] artifact." — cero contenido |
| KnowledgeBase empty templates | 14 | ~7 KB | 8 engine templates + 4 MP templates + 2 index files, todos vacíos |
| Governance DUPLICADO | 6 | ~33 KB | SKILLS_REGISTRY.json = SKILLS_REGISTRY.md, phase12b_raw duplicados |
| Governance OBSOLETO | 14 | ~84 KB | PARIS chain errónea, V1 models invalidados, RECHAZADO |

### Categoría B: Archivar después de absorción por KCE — ~312 archivos

| Grupo | Archivos | Condición |
|---|---|---|
| Certificaciones vigentes (~200) | ~200 | Después de que KCE extraiga PASS/FAIL/delta a knowledge_index.yaml |
| P32 sprint reports (30) | 30 | Después de que KCE indexe resúmenes |
| FCG_REPORTS/ (19) | 19 | Datos ya en certification_engine |
| Phase 12-16F (~50) | 50 | Resúmenes ya en governance/ actual |
| DEC+RFCS (10+7) | 17 | Después de DEC Registry + RFC Registry |

**Total archivable: ~456 archivos (66% del repositorio)**

---

## Q5: ¿Qué componente falta para que el sistema aprenda automáticamente de sus auditorías?

### Componente faltante: KnowledgeConsolidationEngine (KCE)

Actualmente no existe ningún código que convierta hallazgos de auditoría en conocimiento permanente.

**El componente debe tener 5 sub-componentes:**

| Sub-componente | Función | Trigger | Tabla/archivo de entrada | Tabla/archivo de salida |
|---|---|---|---|---|
| **1. AuditScanner** | Escanea `marketplace_auditoria_v1` por nuevos hallazgos | Después de `run_audit()` | marketplace_auditoria_v1 | Entrada KB temporal |
| **2. DecisionParser** | Escanea `governance/*.md` por nuevos DEC-XXX/RFC-XXX | A pedido o cron | governance/*.md | knowledge_index.yaml |
| **3. CertStatusTracker** | Extrae PASS/FAIL status de certification_engine | Después de certify() | certification_engine claims | knowledge_index.yaml |
| **4. KnowledgeIndexer** | Actualiza `knowledge_index.yaml` con nuevas entradas | Después de 1-3 | Entradas KB | knowledge_index.yaml |
| **5. RetentionMarker** | Marca archivos governance/ como HISTORICO cuando su conocimiento es absorbido | Después de 4 | governance/ filenames | governance/ metadata |

### Evidencia de que NO existe:

```
# Consulta 1: ¿Algún código actualiza knowledge_index.yaml?
$ grep -r "knowledge_index" . --include="*.py" | grep -v test | grep -v __pycache__
→ 0 resultados

# Consulta 2: ¿Algún código lee marketplace_auditoria_v1 para crear KB?
$ grep -r "marketplace_auditoria_v1" . --include="*.py"
→ api/api.py: 3 endpoints GET (solo lectura)
→ engine/v4/marketplace_auditor.py: escritura

# Consulta 3: ¿Algún código escribe knowledge_index.yaml?
$ grep -r "yaml.dump\|yaml.safe_dump" . --include="*.py" 
→ 0 resultados (solo yaml.safe_load en tests)

# Consulta 4: ¿Algún código referencia "knowledge" como categoría manejable?
$ grep -r "class Knowledge\|def create_knowledge\|def ingest_knowledge" . --include="*.py"
→ 0 resultados
```

---

## Q6: ¿Cuántos documentos dejarían de ser necesarios una vez implementado KCE?

### Cálculo

| Categoría | Archivos actuales | Después de KCE | Reducción |
|---|---|---|---|
| Certificaciones vigentes | ~200 | ~0 (todo vía cert_engine + KB) | -200 |
| DECs | 10 | 0 (vía DEC Registry API) | -10 |
| RFCs | 7 | 0 (vía RFC Registry API) | -7 |
| Skills registries | 3 | 0 (vía Skills Registry API) | -3 |
| P32 sprint reports | 30 | 0 (vía KB summaries) | -30 |
| FCG_REPORTS/ | 19 | 0 (datos en cert_engine) | -19 |
| Phase 12-16F reports | ~50 | 0 (vía KB summaries) | -50 |
| KnowledgeBase stub/templates | 39 | 0 (eliminar) | -39 |
| Root temp/scratch | 85 | 0 (eliminar) | -85 |
| Root governance reports | 70 | 70 (mover a governance/) | 0 |
| Core governance (VIGENTE) | 286 | ~100 (solo lo no absorbible) | -186 |
| **Total** | **~799** | **~170** | **-629 (79%)** |

### Escenario post-KCE

```
Antes: 799 archivos de conocimiento (541 governance + 110 KnowledgeBase + 70 root + 78 otros)
Después: ~170 archivos (100 governance core + 50 config/JSON + 20 esenciales)
Reducción: 629 archivos (79%)
```

### Lo que permanece después de KCE

1. `governance/decisions/` → 0 files (absorbido por DEC Registry API)
2. `governance/*.md` → ~100 files (solo lo no absorbible: evidencia forense, análisis cualitativos)
3. `KnowledgeBase/` → ~30 files (core registries + taxonomías, servidos vía API)
4. `knowledge_index.yaml` → actualizado automáticamente
5. Root → 22 files (esenciales + código)

### Advertencia

Esta es una estimación basada en el contenido actual. El número exacto depende de:
- Cuántas certificaciones pueden ser completamente reemplazadas por `certification_engine` (6 claims)
- Cuánto análisis cualitativo en governance/ no es reducible a datos estructurados
- La decisión de mantener archivos históricos por razones de auditoría legal

El rango conservador es **400-500 archivos eliminables** (50-63% del total).
