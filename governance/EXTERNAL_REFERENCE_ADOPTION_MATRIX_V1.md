---
id: EXTERNAL_REFERENCE_ADOPTION_MATRIX_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Domain Specialist & Technical Architect
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - ARCHITECTURE_REGISTRY_V1
  - DATA_CONTRACT_REGISTRY_V1
relacionado_con:
  - DECISION_REGISTRY_V1
  - KNOWLEDGE_OS_SPECIFICATION
---

# MATRIZ DE ADOPCIÓN DE REFERENCIAS EXTERNAS V1

## Propósito
Registrar formalmente la evaluación, impacto y estado de adopción de todas las **Referencias Tecnológicas y Normativas Externas** utilizadas o consideradas para el **Marketplace Financial AI Engine**. Prohíbe la adopción implícita de estándares externos sin trazabilidad probatoria y aprobación de arquitectura.

---

## Matriz Canónica de Referencias Externas

### 1. `REF-001`: Estándar SII DTE Chile (Servicio de Impuestos Internos)
- **reference_id**: `REF-001`
- **nombre**: "Estándar de Documentos Tributarios Electrónicos SII Chile"
- **autor**: Servicio de Impuestos Internos (SII Chile)
- **organizacion**: Gobierno de Chile - SII
- **categoria**: Normativa Tributaria
- **version**: Esquema DTE v1.0 (XML SII)
- **url_oficial**: `https://www.sii.cl/factura_electronica/`
- **proposito**: Definir el formato XML inalterable de Facturas Electrónicas (33), Notas de Crédito (61), Notas de Débito (56) y Guías de Despacho (52).
- **estado**: **ADOPTADA**
- **impacto**: Alto. Requerido para la conciliación tributaria DTE en Etapa 4.
- **componentes_afectados**: `engine/v4/dte_indexer.py`, `stg_dte_sii`
- **contratos_afectados**: `CTR-003` (Normalización → XML)
- **riesgos**: Cambios en esquemas XSD publicados por el SII.
- **beneficios**: Respaldo legal y tributario 100% oficial para operaciones en Chile.
- **evidencia_adopcion**: Indexación exitosa de DTEs Paris ($312.4M).
- **adr_relacionado**: `ADR-005`
- **observaciones**: Estándar mandatorio para facturación electrónica en Chile.

---

### 2. `REF-002`: DuckDB OLAP Database Specification
- **reference_id**: `REF-002`
- **nombre**: "DuckDB In-Process Analytical Database Specification"
- **autor**: DuckDB Foundation / CWI
- **organizacion**: DuckDB Labs
- **categoria**: Persistencia y Base de Datos OLAP
- **version**: v1.5.1
- **url_oficial**: `https://duckdb.org/docs/`
- **proposito**: Motor de base de datos analítico vectorial in-process para consultas OLAP ultrarrápidas y almacenamiento relacional.
- **estado**: **ADOPTADA**
- **impacto**: Crítico Máximo. Base de datos oficial inmutable del sistema.
- **componentes_afectados**: `data/db/meli_financial_v4.db`, `engine/v4/surgical_loader.py`
- **contratos_afectados**: `CTR-002` a `CTR-009`
- **riesgos**: Incompatibilidad en migraciones de versión de DuckDB engine.
- **beneficios**: Ejecución vectorial de alto rendimiento, cero latencia de red, compatibilidad SQL estricta.
- **evidencia_adopcion**: `EVID-DB-001` (DB Hash: `311c78e2b7...`).
- **adr_relacionado**: `ADR-001`
- **observaciones**: Declarada como Única Fuente de Verdad Financiera Corporativa.

---

### 3. `REF-003`: Model Context Protocol (MCP)
- **reference_id**: `REF-003`
- **nombre**: "Model Context Protocol Specification"
- **autor**: Anthropic / Open Source Community
- **organizacion**: Model Context Protocol Initiative
- **categoria**: Arquitectura de Inteligencia Artificial & Agentes
- **version**: v1.0.0
- **url_oficial**: `https://modelcontextprotocol.io/`
- **proposito**: Estándar abierto para exponer herramientas, recursos y prompts a subagentes de IA y sistemas LLM.
- **estado**: **EN_EVALUACIÓN**
- **impacto**: Medio. Reservado para la capa `System Intelligence` en Fase 8.
- **componentes_afectados**: `System Intelligence Layer`, `MCP Adapter`
- **contratos_afectados**: `CTR-011`
- **riesgos**: Cambios de especificación en la incubación del estándar.
- **beneficios**: Interoperabilidad estandarizada para invocación de herramientas por el Copilot.
- **evidencia_adopcion**: Especificación reservada en `SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md`.
- **adr_relacionado**: `ADR-004`
- **observaciones**: Reservado formalmente para implementación en Fase 8.

---

### 4. `REF-004`: Obsidian Markdown & Wikilink Format
- **reference_id**: `REF-004`
- **nombre**: "Obsidian Knowledge Management Specification"
- **autor**: Dynalist Inc.
- **organizacion**: Obsidian
- **categoria**: Gestión de Conocimiento & Markdown
- **version**: v1.5+
- **url_oficial**: `https://obsidian.md/`
- **proposito**: Formato de navegación por enlaces bidireccionales (`[[wikilinks]]`) y YAML frontmatter para bases de conocimiento locales.
- **estado**: **ADOPTADA**
- **impacto**: Alto. Define la interfaz de navegación de `KnowledgeOS`.
- **componentes_afectados**: `KnowledgeOS/`, todos los documentos en `governance/`
- **contratos_afectados**: `CTR-010`
- **riesgos**: Enlaces huérfanos si se modifican nombres de archivos manualmente.
- **bloqueadores**: Ninguno.
- **beneficios**: Navegación gráfica e interconectada del conocimiento canónico.
- **evidencia_adopcion**: `KNOWLEDGE_OS_SPECIFICATION.md`.
- **adr_relacionado**: `ADR-002`
- **observaciones**: Estándar oficial de interfaz para la Capa de Conocimiento.

---

### 5. `REF-005`: SAP BAPI / IDoc Accounting Interface Standard
- **reference_id**: `REF-005`
- **nombre**: "SAP Financial Accounting (FI) BAPI / IDoc Interface Standard"
- **autor**: SAP SE
- **organizacion**: SAP SE
- **categoria**: Integración ERP Corporativo
- **version**: SAP S/4HANA FI v2023+
- **url_oficial**: `https://help.sap.com/`
- **proposito**: Estándar de integración para contabilización de documentos de finanzas (`BAPI_ACC_DOCUMENT_POST`).
- **estado**: **PROPUESTA**
- **impacto**: Alto. Programado para evaluación e integración en Fase 5.
- **componentes_afectados**: `SAP Integration Engine`, `stg_sap_accounting_doc`
- **contratos_afectados**: `CTR-004`
- **riesgos**: Complejidad en mapeos de plan de cuentas corporativo.
- **beneficios**: Conciliación directa contra el libro mayor contable ERP.
- **evidencia_adopcion**: Especificado en `DATA_CONTRACT_REGISTRY_V1.md`.
- **adr_relacionado**: `ADR-005`
- **observaciones**: Programado para implementación en Fase 5.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:EXTERNAL_REFERENCE_ADOPTION_MATRIX_V1` (Tipo: `Matriz_Adopción_Referencias`)
- `Node:REF-001` .. `Node:REF-005` (Tipo: `Referencia_Externa`)

### Execution Graph Nodes
- `ExecNode:VERIFY_EXTERNAL_REF_STATUS` (Process: Auditar estado de adopción y compatibilidad de referencias externas)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: El catálogo de referencias tecnológicas y normativas de terceros.
- **VINCULA**: Estándares externos con los contratos de datos y arquitectura oficial.
- **AFECTA**: [DATA_CONTRACT_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/DATA_CONTRACT_REGISTRY_V1.md).

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[EXTERNAL_REFERENCE_ADOPTION_MATRIX_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/EXTERNAL_REFERENCE_ADOPTION_MATRIX_V1.md`
