---
id: EXTERNAL_REFERENCE_ADOPTION_MATRIX_V2
version: 2.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: Chief Architect & Technology Evaluator
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - SYSTEM_INTELLIGENCE_SPECIFICATION_V1
  - DUAL_GRAPH_ARCHITECTURE_MODEL_V1
---

# MATRIZ DE ADOPCIÓN DE REFERENCIAS Y EXPERIENCIAS EXTERNAS V2

## Propósito
Evaluación formal y gobernada de arquitecturas, tecnologías y marcos conceptuales externos considerados para su incorporación o integración con el **Marketplace Financial AI Engine**.

---

## 1. Clasificación Oficial de Referencias Externas

```text
====================================================================================================
TECNOLOGÍA / EXPERIENCIA EXTERNA    DECISIÓN OFICIAL     REGLA DE APLICACIÓN Y JUSTIFICACIÓN
====================================================================================================
Escalafy LLM ES                      REFERENCIAR          Concepto de promps estructurados en español.
                                                          PROHIBIDO como router primario o calculador.
----------------------------------------------------------------------------------------------------
CEcommerce                           ADAPTAR              Estructura de taxonomías de e-commerce y atribución
                                                          de órdenes. Adaptado a la capa DuckDB Staging.
----------------------------------------------------------------------------------------------------
DuckDB V1.5.1                        ADOPTAR              Motor analítico in-memory oficial ($0 delta).
----------------------------------------------------------------------------------------------------
FastAPI + Pydantic v2                ADOPTAR              Capa API backend oficial con contratos estrictos.
----------------------------------------------------------------------------------------------------
Obsidian Markdown Wikilinks          ADOPTAR              Estructura de navegación documental de KnowledgeOS.
----------------------------------------------------------------------------------------------------
Neo4j / GraphDB                      RECHAZAR             No se requiere BD de grafos externa. DualGraph
                                                          implementado en Python determinista puro.
====================================================================================================
```

---

## 2. Criterios de Evaluación y Clasificación

- **ADOPTAR**: Integrado oficialmente en la pila del proyecto sin alteraciones conceptuales.
- **ADAPTAR**: Modificado internamente para alineación estricta con las reglas de Single Financial Truth.
- **REFERENCIAR**: Utilizado como material de consulta o benchmark sin dependencia de código.
- **RECHAZAR**: Descartado formalmente por vulnerar restricciones de arquitectura (e.g. BDs de grafos pesadas o LLM no determinista).
- **POSPONER**: Evaluado para posibles fases avanzadas (Fase 5 o posterior).

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:EXTERNAL_REFERENCE_ADOPTION_MATRIX_V2` (Tipo: `Matriz_Adopcion_Tecnologica`)

### Execution Graph Nodes
- `ExecNode:TECH_EVALUATOR` (Process: Evaluación continua de compatibilidad técnica)
