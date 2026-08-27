---
id: DUAL_GRAPH_INDEX_V1
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: Graph Architect & Chief System Architect
ultima_revision: 2026-07-27
dependencias:
  - DUAL_GRAPH_ARCHITECTURE_MODEL_V1
  - SYSTEM_INTELLIGENCE_SPECIFICATION_V1
relacionado_con:
  - KNOWLEDGE_CANONICAL_REGISTRY_V1
  - CAPABILITY_REGISTRY_V1
  - DATA_LINEAGE_REGISTRY_V1
  - FINANCIAL_COPILOT_QUESTION_REGISTRY_V1
---

# ÍNDICE DEL GRAFO DUAL DE CONOCIMIENTO Y EJECUCIÓN (DUAL GRAPH)

## Resumen Ejecutivo
Representación navegable determinista y ejecutable del **Grafo Dual** (`Knowledge Graph` + `Execution Graph`), implementada por `engine/v4/knowledge/dual_graph.py`. Permite trazabilidad end-to-end de 11 pasos entre documentación canónica, contratos de datos, capacidades, evidencias, preguntas estratégicas del Copilot y pipelines de ejecución.

---

## 1. Nodos Registrados del Knowledge Graph (KG)

| ID Nodo | Tipo Nodo | Propietario | Estado | Ruta / Referencia Obsidian |
| :--- | :--- | :--- | :--- | :--- |
| `DOC-001` | Documento | PMO Lead | CERTIFICADO | [[EXECUTION_PLAN_PHASE_0_FOUNDATION_V3]] |
| `DOC-002` | Documento | Chief Architect | CERTIFICADO | [[ARCHITECTURE_REGISTRY_V1]] |
| `DOC-003` | Documento | Data Architect | CERTIFICADO | [[DATA_CONTRACT_REGISTRY_V1]] |
| `DOC-004` | Documento | Evidence Guardian | CERTIFICADO | [[EVIDENCE_REGISTRY_V1]] |
| `DOC-005` | Documento | Knowledge Eng | CERTIFICADO | [[KNOWLEDGE_OS_SPECIFICATION]] |
| `DOC-006` | Documento | Graph Architect | CERTIFICADO | [[DUAL_GRAPH_ARCHITECTURE_MODEL_V1]] |
| `DOC-007` | Documento | AI Architect | CERTIFICADO | [[SYSTEM_INTELLIGENCE_SPECIFICATION_V1]] |
| `DOC-008` | Documento | PMO Lead | CERTIFICADO | [[PMO_REGISTRY_V1]] |
| `DOC-009` | Documento | QA Manager | CERTIFICADO | [[MATURITY_REGISTRY_V1]] |
| `DOC-010` | Documento | Technical Debt Lead | CERTIFICADO | [[TECHNICAL_DEBT_REGISTRY_V1]] |
| `CTR-001` .. `CTR-011` | Contrato_Datos | Data Architect | CERTIFICADO | [[DATA_CONTRACT_REGISTRY_V1]] |
| `CAP-TD-001` .. `CAP-TD-007` | Capacidad | Product Owner | CERTIFICADO | [[CAPABILITY_REGISTRY_V1]] |
| `EVID-TD-001` .. `EVID-TD-007` | Evidencia | Evidence Guardian | CERTIFICADO | [[EVIDENCE_REGISTRY_V1]] |
| `LIN-001` .. `LIN-012` | Linaje | Senior Data Engineer | CERTIFICADO | [[DATA_LINEAGE_REGISTRY_V1]] |
| `Q-001` .. `Q-010` | Pregunta_Financiera | Copilot Architect | CERTIFICADO | [[FINANCIAL_COPILOT_QUESTION_REGISTRY_V1]] |
| `TD-001` .. `TD-007` | Deuda_Técnica | Technical Debt Lead | RESUELTO | [[TECHNICAL_DEBT_REGISTRY_V1]] |

---

## 2. Nodos Registrados del Execution Graph (EG)

| ID ExecNode | Tipo ExecNode | Componente / Archivo | Método / Path | Estado |
| :--- | :--- | :--- | :--- | :--- |
| `EXEC_API_COPILOT` | Endpoint | `api/api.py` | `GET /api/v4/copilot/ask` | CERTIFICADO |
| `EXEC_COPILOT_ENGINE` | Handler | `engine/v4/copilot/copilot_engine.py` | `CopilotEngine.ask()` | CERTIFICADO |
| `EXEC_FINANCIAL_ENGINE` | Servicio | `engine/v4/domain/financial_engine.py` | `FinancialEngine` | CERTIFICADO |
| `EXEC_SURGICAL_LOADER` | Pipeline | `engine/v4/surgical_loader.py` | `SurgicalLoader` | CERTIFICADO |
| `EXEC_DUCKDB_MAIN` | Tabla_DuckDB | `data/db/meli_financial_v4.db` | `marketplace_ledger_v1` | CERTIFICADO |
| `EXEC_VALIDATE_HARNESS` | Harness | `tools/validate_fase_1b.py` | `validate_fase_1b.py` | CERTIFICADO |
| `EXEC_DUAL_GRAPH_ENGINE` | Servicio | `engine/v4/knowledge/dual_graph.py` | `DualGraphRegistry` | CERTIFICADO |
| `EXEC_PYTEST_SUITE` | Prueba_Integración | `tests/` | `pytest tests/` | CERTIFICADO |

---

## 3. Matriz de Puentes Cruzados entre Grafos (Cross-Graph Bridges)

- `Q-001` .. `Q-010` --(RESPONDIDA_POR)--> `EXEC_API_COPILOT` --(IMPLEMENTADA_POR)--> `EXEC_COPILOT_ENGINE`
- `EXEC_COPILOT_ENGINE` --(USA)--> `EXEC_FINANCIAL_ENGINE` --(CONSUME)--> `EXEC_DUCKDB_MAIN`
- `EXEC_DUCKDB_MAIN` --(CUMPLE)--> `CTR-008` --(EVIDENCIADA_POR)--> `EVID-TD-005` --(CERTIFICA)--> `CAP-TD-005`
- `TD-001` .. `TD-007` --(RESUELVE)--> `CAP-TD-001` .. `CAP-TD-007`
- `CAP-TD-007` --(PRODUCE)--> `EVID-TD-007` --(CERTIFICA)--> `EXEC_DUAL_GRAPH_ENGINE`

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:DUAL_GRAPH_INDEX_V1` (Tipo: `Indice_Grafo_Dual`)
- `Node:DUAL_GRAPH_ENGINE` (Tipo: `Modulo_Ejecutable`)

### Execution Graph Nodes
- `ExecNode:DUAL_GRAPH_TESTS` (Prueba_Integracion: `tests/test_dual_graph.py`)
