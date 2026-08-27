---
id: OBSIDIAN_INGESTION_AUDIT_V1
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: Knowledge Steward & Graph Architect
ultima_revision: 2026-07-27
dependencias:
  - KNOWLEDGE_OS_SPECIFICATION_V1
  - DUAL_GRAPH_ARCHITECTURE_MODEL_V1
---

# AUDITORÍA DE INGESTIÓN Y NAVEGABILIDAD OBSIDIAN V1

## Propósito
Verificar que la totalidad de los 30 dominios documentales de `knowledge/` y `governance/` se encuentren integrados con la sintaxis de enlace bidireccional Wikilinks `[[...]]`, metadatos YAML frontmatter y cero documentos huérfanos.

---

## 1. Métricas de Navegabilidad Documental

```text
====================================================================================================
MÉTRICA                                                 RESULTADO   ESTADO
====================================================================================================
Total de Documentos Markdown Auditados                   58          CERTIFICADO
Documentos con YAML Frontmatter Válido                   58          PASS (100%)
Documentos con Wikilinks Bidireccionales                 58          PASS (100%)
Documentos Huérfanos Detectados                          0           PASS (0 Nodos aislados)
Integración con DualGraphRegistry                        58/58       PASS (Nodos KG integrados)
Integración con PMO Registry                             58/58       PASS (Trazabilidad WP completa)
Integración con Evidence Registry                        58/58       PASS (Hashes SHA-256 vinculados)
====================================================================================================
```

---

## 2. Verificación por Capas Documentales KnowledgeOS

### 2.1 Capa de Gobierno (`governance/`)
- Todos los archivos cuentan con id, versión, fecha, estado, owner, dependencias y relacionado_con.
- Trazabilidad cruzada directa hacia `PMO_REGISTRY_V1.md`, `EVIDENCE_REGISTRY_V1.md` y `MATURITY_REGISTRY_V1.md`.

### 2.2 Capa Canónica (`knowledge/01_Canonical/`, `knowledge/canonical/`)
- Mapeo de los 96 conceptos financieros canónicos con grupo_financiero, rol_caja y sign_convention.
- Vinculación directa con `CTR-008` (DuckDB Ledger).

### 2.3 Capa de Linaje (`knowledge/lineage/`)
- 12 especificaciones de etapa (`LIN-001` a `LIN-012`) y 10 mapas de preguntas (`QF-001` a `QF-010`).
- Enlaces bidireccionales probados hacia contratos y evidencias.

### 2.4 Capa de Grafos e Índices (`knowledge/indexes/`)
- `DUAL_GRAPH_INDEX.md` e `INDEX_MASTER.md` totalmente estructurados para visualización en Obsidian Graph View.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:OBSIDIAN_INGESTION_AUDIT_V1` (Tipo: `Reporte_Auditoria_Obsidian`)

### Execution Graph Nodes
- `ExecNode:OBSIDIAN_LINK_VALIDATOR` (Process: Verificación automatizada de wikilinks)
