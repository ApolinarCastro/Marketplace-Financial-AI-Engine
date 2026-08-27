---
id: KNOWLEDGE_INDEX_MASTER_V1
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: Knowledge Steward & Chief Architect
ultima_revision: 2026-07-27
dependencias:
  - KNOWLEDGE_OS_SPECIFICATION_V1
  - DUAL_GRAPH_ARCHITECTURE_MODEL_V1
relacionado_con:
  - TECHNICAL_DEBT_REGISTRY_V1
  - PMO_REGISTRY_V1
  - EVIDENCE_REGISTRY_V1
  - MATURITY_REGISTRY_V1
---

# ÍNDICE MAESTRO DE KNOWLEDGEOS V1

## Resumen Ejecutivo
Índice canónico de navegación bidireccional de la base de conocimiento estructurada **KnowledgeOS**, conectando documentación de gobierno, contratos de datos, linaje, arquitectura, capacidades, evidencias e índices Obsidian.

---

## 1. Estructura Físico-Lógica de KnowledgeOS

```text
knowledge/
├── 00_Inbox/                # Captura inicial y borradores no clasificados
├── 01_Canonical/            # Conceptos financieros y reglas de negocio canónicas
├── 02_Governance/           # Especificaciones de gobierno, arquitectura y registros
├── 03_Evidence/            # Evidencias probatorias de auditoría y ejecución
├── 04_Projects/            # Planes de ejecución, CAPs y roadmaps de sprint
├── 05_References/          # Referencias externas y estándares de industria
├── 90_Archive/             # Documentos obsoletos o sustituidos
├── 99_Quarantine/          # Alertas de incoherencia o datos no certificados
├── architecture/           # Registro de arquitectura de 12 capas y grafos
├── canonical/              # Glosario canónico de conceptos (96 conceptos)
├── capabilities/           # Registro canónico de capacidades del sistema
├── contracts/              # Registro de contratos de datos CTR-001 a CTR-011
├── copilot/                # Registro de 10 preguntas financieras del Copilot
├── core/                   # Registros de eventos, roles de caja y jerarquías
├── decisions/              # Registro de decisiones de arquitectura (ADRs)
├── dte/                    # Especificaciones de documentos tributarios DTE SII
├── evidence/               # Registros consolidados de evidencias por CAP
├── execution/              # Registros de ejecuciones y harnesses de prueba
├── glossary/               # Diccionario económico y equivalencias de taxonomía
├── governance/             # Documentos de gobierno de proyecto y PMO
├── indexes/                # Índices canónicos y grafos de navegación
├── lineage/                # Linaje canónico LIN-001 a LIN-012 y etapas
├── marketplace/            # Reglas específicas por Marketplace (MELI, Paris, Ripley, Falabella)
├── marketplaces/           # Configuraciones e ingestas por Marketplace
├── maturity/               # Matriz de madurez de capacidades y deudas
├── references/             # Adopción de tecnologías y referencias externas
├── registry/               # Registros maestros y listas de control
├── roadmap/                # Hitos y roadmap de reconciliación end-to-end
├── sap/                    # Especificaciones de integración ERP SAP BAPI/IDoc
└── templates/              # Plantillas estandarizadas para documentos de gobierno
```

---

## 2. Mapa de Navegación Canónica por Dominios

### Gobierno y Dirección
- [[EXECUTION_PLAN_PHASE_0_FOUNDATION_V3]] — Plan Maestro de Ejecución
- [[ARCHITECTURE_REGISTRY_V1]] — Registro de Arquitectura de 12 Capas
- [[PMO_REGISTRY_V1]] — Registro de Paquetes de Trabajo PMO (WP-F1-01 a WP-F1-08)
- [[MATURITY_REGISTRY_V1]] — Matriz de Madurez de Capacidades (Nivel 4 Certificado)
- [[TECHNICAL_DEBT_REGISTRY_V1]] — Registro Maestro de Deuda Técnica (TD-001 a TD-008 CERRADOS)

### Contratos de Datos y Linaje
- [[DATA_CONTRACT_REGISTRY_V1]] — Registro de Contratos CTR-001 a CTR-011
- [[DATA_LINEAGE_REGISTRY_V1]] — Linaje Canónico Origen-Destino (LIN-001 a LIN-012)
- [[LIN-001]] — Linaje Marketplace → RAW
- [[LIN-002]] — Linaje RAW → Staging Normalizado
- [[LIN-008]] — Linaje Financial Closing → DuckDB Ledger
- [[LIN-010]] — Linaje KnowledgeOS Integration
- [[LIN-011]] — Linaje Copilot Query Engine

### Grafos y Sistema Inteligente
- [[DUAL_GRAPH_ARCHITECTURE_MODEL_V1]] — Modelo de Grafos Duales (Knowledge Graph + Execution Graph)
- [[SYSTEM_INTELLIGENCE_SPECIFICATION_V1]] — Especificación del Copilot Financiero e Inteligencia de Sistema
- [[FINANCIAL_COPILOT_QUESTION_REGISTRY_V1]] — Normalización Canónica de las 10 Preguntas Financieras (`Q-001` a `Q-010`)
- [[DUAL_GRAPH_INDEX]] — Índice de Navegación del Grafo Dual Ejecutable

### Evidencias de Ejecución
- [[EVIDENCE_REGISTRY_V1]] — Registro Maestro de Evidencias Probatorias
- [[CAP-TD-001.json]] a [[CAP-TD-008.json]] — Artefactos JSON de ejecución de Fase 1

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:KNOWLEDGE_INDEX_MASTER_V1` (Tipo: `Indice_Maestro_Conocimiento`)
- `Node:KNOWLEDGE_OS_SPEC` (Tipo: `Especificacion_Gobernanza`)

### Execution Graph Nodes
- `ExecNode:INDEX_NAVIGATOR` (Process: Navegación bidireccional Obsidian)
