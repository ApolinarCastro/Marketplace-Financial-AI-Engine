---
id: DECISION_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Chief Architect & Lead Data Engineer
ultima_revision: 2026-07-27
dependencias: [EXECUTION_PLAN_PHASE_0_FOUNDATION_V3]
relacionado_con: [PMO_REGISTRY_V1, ARCHITECTURE_REGISTRY_V1, BASELINE_POST_SURGICAL_FIX]
---

# REGISTRO MAESTRO DE DECISIONES DE ARQUITECTURA (ADR) V1

## Propósito
Consolidar el registro oficial e inmutable de todas las Decisiones de Arquitectura (Architectural Decision Records - ADR) tomadas en el **Marketplace Financial AI Engine**, garantizando la trazabilidad histórica de por qué se adoptó cada diseño y qué alternativas fueron descartadas.

---

## Registro Canónico de ADRs

### ADR ID: `ADR-001`

| Campo | Detalle |
| :--- | :--- |
| **ADR-ID** | `ADR-001` |
| **Fecha** | 2026-05-30 |
| **Problema** | Ambivalencia en la persistencia de datos financieros corporativos entre SQLite (`marketplace.db`) y DuckDB (`meli_financial_v4.db`). |
| **Decisión** | Declarar a `data/db/meli_financial_v4.db` (DuckDB V1.5.1) como la **ÚNICA Fuente de Verdad Financiera Corporativa Inmutable**. |
| **Alternativas Descartadas** | 1. Mantener SQLite como DB operativa (Descartada por limitaciones analíticas OLAP).<br>2. Re-clasificar en runtime (Descartada por pérdida de determinismo e inmutabilidad). |
| **Justificación** | DuckDB ofrece rendimiento OLAP superior, soporte de tipos vectoriales y cumplimiento $0 delta verificado en 69/69 períodos. |
| **Impacto** | Toda consulta de la API, Dashboard y Copilot DEBE consumir exclusivamente `meli_financial_v4.db`. |
| **Estado** | **APROBADO E INMUTABLE** |
| **Referencias** | [AGENTS.md](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/AGENTS.md), `governance/INCIDENT_DB_SURVIVAL_AUDIT.md` |

---

### ADR ID: `ADR-002`

| Campo | Detalle |
| :--- | :--- |
| **ADR-ID** | `ADR-002` |
| **Fecha** | 2026-07-27 |
| **Problema** | Mezclar relaciones conceptuales de documentación con dependencias técnicas de pipelines de ejecución en un solo grafo genérico. |
| **Decisión** | Separar formalmente el modelo en dos grafos complementarios: **Knowledge Graph** (documentos, reglas, decisiones, deuda técnica) y **Execution Graph** (endpoints, pipelines, tests, jobs, ejecuciones). |
| **Alternativas Descartadas** | 1. Grafo único indistinto (Descartada por confusión conceptual y dificultad en trazabilidad).<br>2. Documentación plana sin grafos (Descartada por falta de navegación navegable en Obsidian). |
| **Justificación** | Permite auditorías diferenciadas: impacto de conocimiento vs. fallos en pipelines de ejecución. |
| **Impacto** | Especificación formal en `DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md`. |
| **Estado** | **APROBADO** |
| **Referencias** | `EXECUTION_PLAN_PHASE_0_FOUNDATION_V3` |

---

### ADR ID: `ADR-003`

| Campo | Detalle |
| :--- | :--- |
| **ADR-ID** | `ADR-003` |
| **Fecha** | 2026-07-27 |
| **Problema** | Declarar características como "listas" o "implementadas" sin pruebas automatizadas, evidencias reproducibles o contratos formales. |
| **Decisión** | Promulgar la **Regla de Oro del Proyecto**: Ninguna capacidad se considerará implementada sin Contrato de Datos, Evidencia Registrada, Trazabilidad Completa, Registro Canónico, Pruebas y Certificación Oficial. |
| **Alternativas Descartadas** | 1. Aceptar entregas basadas solo en código escrito (Descartada por violar P37 Product First y FASE 1B-R11). |
| **Justificación** | Garantiza cero regresión y alineación total con los principios de auditoría de TUKE Master Framework. |
| **Impacto** | Criterio supremo de aceptación para todas las tareas del PMO. |
| **Estado** | **APROBADO** |
| **Referencias** | `EXECUTION_PLAN_PHASE_0_FOUNDATION_V3`, `AGENTS.md` |

---

### ADR ID: `ADR-004`

| Campo | Detalle |
| :--- | :--- |
| **ADR-ID** | `ADR-004` |
| **Fecha** | 2026-07-27 |
| **Problema** | Riesgo de que el Financial Copilot consulte directamente documentos no certificados o archivos RAW sin estructurar, produciendo alucinaciones o cifras divergentes. |
| **Decisión** | Crear la capa **System Intelligence** intermedia entre el Dual Graph Layer y el Financial Copilot, prohibiendo consultas directas a documentos RAW sin certificación previa. |
| **Alternativas Descartadas** | 1. Copilot consultando directamente el sistema de archivos (Descartada por riesgo de alucinación).<br>2. Copilot consultando solo SQL plano sin contexto de conocimiento (Descartada por falta de explicabilidad). |
| **Justificación** | Garantiza que toda respuesta del Copilot esté respaldada por cadenas de evidencia auditables $0 delta. |
| **Impacto** | Especificación en `SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md`. |
| **Estado** | **APROBADO** |
| **Referencias** | `EXECUTION_PLAN_PHASE_0_FOUNDATION_V3` |

---

### ADR ID: `ADR-005`

| Campo | Detalle |
| :--- | :--- |
| **ADR-ID** | `ADR-005` |
| **Fecha** | 2026-07-27 |
| **Problema** | Definir la secuencia oficial de desarrollo para las fases subsecuentes del proyecto. |
| **Decisión** | Adoptar formalmente la **Secuencia Maestra de 9 Fases** (Fase 0 a Fase 8) cubriendo desde Gobierno hasta Financial Copilot Certificado. |
| **Alternativas Descartadas** | 1. Desarrollo simultáneo de Copilot e ingestas (Descartada por violar R3 de AGENTS.md: Reparar → Estabilizar → Simplificar → Optimizar → Funcionalidades). |
| **Justificación** | Establece un orden lógico dependiente de contratos de datos, XML, SAP y Banco antes del Copilot. |
| **Impacto** | Determina el roadmap oficial de ejecución de todo el proyecto. |
| **Estado** | **APROBADO** |
| **Referencias** | `EXECUTION_PLAN_PHASE_0_FOUNDATION_V3` |

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:DECISION_REGISTRY_V1` (Tipo: `Registro_Decisiones`)
- `Node:ADR-001` .. `Node:ADR-005` (Tipo: `Decision_Arquitectura`)

### Execution Graph Nodes
- `ExecNode:ENFORCE_ADR_COMPLIANCE` (Process: Verificación automática de cumplimiento de ADRs en pipelines de CI/CD)

---

## Trazabilidad y Relaciones
- **GOBIERNA**: Las decisiones fundamentales de arquitectura y diseño del sistema.
- **AFECTA**: [PMO_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/PMO_REGISTRY_V1.md) y [ARCHITECTURE_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/ARCHITECTURE_REGISTRY_V1.md).
- **CONSOLIDA**: Las justificaciones técnicas de la base congelada y la hoja de ruta futura.

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[DECISION_REGISTRY_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/DECISION_REGISTRY_V1.md`
