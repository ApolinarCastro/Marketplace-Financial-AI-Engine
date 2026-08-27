---
id: KNOWLEDGE_CANONICAL_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Single Financial Truth Guardian & Knowledge Engineer
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - ARCHITECTURE_REGISTRY_V1
  - DATA_CONTRACT_REGISTRY_V1
  - EVIDENCE_REGISTRY_V1
  - KNOWLEDGE_OS_SPECIFICATION
relacionado_con:
  - PMO_REGISTRY_V1
  - CAPABILITY_REGISTRY_V1
  - FINANCIAL_COPILOT_QUESTION_REGISTRY_V1
---

# REGISTRO CANÓNICO DE CONOCIMIENTO FINANCIERO Y TÉCNICO V1

## Propósito
Establecer la **Fuente Única de Verdad (Single Source of Truth)** para todos los conceptos financieros, técnicos, arquitectónicos, documentales, de gobierno y de auditoría del **Marketplace Financial AI Engine**. Elimina la duplicidad conceptual y garantiza que cada término disponga de un identificador canónico inmutable.

---

## Esquema Estándar de Registro Canónico (22 Atributos)

```yaml
canonical_id: CAN-[CATEGORIA]-[NUM]
nombre: "Nombre oficial del concepto canónico"
definicion_oficial: "Definición conceptual unificada e inmutable"
categoria: [FINANCIERO | TÉCNICO | ARQUITECTÓNICO | DOCUMENTAL | GOBIERNO | AUDITORÍA]
subcategoria: "Subclasificación específica"
descripcion: "Explicación detallada del concepto y alcance"
owner: "Rol responsable de mantener la verdad canónica"
fuente_oficial: "Documento o artefacto oficial que origina el concepto"
contrato_relacionado: "ID del contrato de datos (CTR-001 a CTR-011)"
evidencia_relacionada: "ID de evidencia registrada (EVID-...)"
capability_relacionada: "ID de la capacidad en CAPABILITY_REGISTRY_V1"
pregunta_financiera_relacionada: "ID de la pregunta estratégica 1 a 10"
arquitectura_relacionada: "Capa de la arquitectura de 12 capas"
data_lineage_relacionado: "Eslabón del data lineage de 13 etapas"
marketplace_relacionado: [MELI | PARIS | RIPLEY | FALABELLA | CONSOLIDADO]
version: "1.0.0"
estado: [ESPECIFICADO | CANÓNICO | CERTIFICADO]
madurez: [Nivel 0 a Nivel 5]
fecha_creacion: YYYY-MM-DD
ultima_revision: YYYY-MM-DD
politica_reemplazo: "Regla de deprecación y archivo histórico"
observaciones: "Notas técnicas o normativas"
```

---

## Catálogo de Conceptos Canónicos Oficiales

### 1. Conceptos Financieros

#### `CAN-FIN-001`: Ventas Brutas Marketplace
- **canonical_id**: `CAN-FIN-001`
- **nombre**: "Ventas Brutas Marketplace"
- **definicion_oficial**: "Suma total de los ingresos generados por la venta de productos en plataformas marketplace antes de comisiones, devoluciones o cargos logísticos."
- **categoria**: `FINANCIERO` | **subcategoria**: `Ingresos`
- **descripcion**: "Consolidador del valor bruto facturado a compradores en Mercado Libre, Paris, Ripley y Falabella."
- **owner**: Single Financial Truth Guardian
- **fuente_oficial**: `marketplace_ledger_v1.financial_group = 'ingresos'`
- **contrato_relacionado**: `CTR-002`, `CTR-008`
- **evidencia_relacionada**: `EVID-DB-001`
- **capability_relacionada**: `CAP-LEDGER-V1`
- **pregunta_financiera_relacionada**: Pregunta 1 (¿Qué vendí?)
- **arquitectura_relacionada**: Domain Layer / Financial Engine
- **data_lineage_relacionado**: Normalización (Etapa 3) → Ledger (Etapa 9)
- **marketplace_relacionado**: `CONSOLIDADO`
- **version**: `1.0.0` | **estado**: `CANÓNICO` | **madurez**: Nivel 5 (Productivo)
- **fecha_creacion**: 2026-05-30 | **ultima_revision**: 2026-07-27
- **politica_reemplazo**: Modificación requiere RFC aprobado. Cero delta obligatorio.
- **observaciones**: CERTIFICADO 69/69 períodos $0 delta.

#### `CAN-FIN-002`: Devoluciones y Notas de Crédito
- **canonical_id**: `CAN-FIN-002`
- **nombre**: "Devoluciones y Notas de Crédito"
- **definicion_oficial**: "Monto total de reversiones de venta por anulaciones, devoluciones de producto o reclamos procesados por los marketplaces."
- **categoria**: `FINANCIERO` | **subcategoria**: `Devoluciones`
- **descripcion**: "Deducción directa de los ingresos brutos registrada en la línea de devoluciones oficial del ledger."
- **owner**: Single Financial Truth Guardian
- **fuente_oficial**: `marketplace_ledger_v1.financial_group = 'devoluciones'`
- **contrato_relacionado**: `CTR-002`, `CTR-008`
- **evidencia_relacionada**: `EVID-DB-001`
- **capability_relacionada**: `CAP-LEDGER-V1`
- **pregunta_financiera_relacionada**: Pregunta 5 (¿Qué devoluciones existen?)
- **arquitectura_relacionada**: Domain Layer / Financial Engine
- **data_lineage_relacionado**: Normalización (Etapa 3) → Ledger (Etapa 9)
- **marketplace_relacionado**: `CONSOLIDADO`
- **version**: `1.0.0` | **estado**: `CANÓNICO` | **madurez**: Nivel 5 (Productivo)
- **fecha_creacion**: 2026-05-30 | **ultima_revision**: 2026-07-27
- **politica_reemplazo**: Modificación requiere RFC aprobado.
- **observaciones**: CERTIFICADO 69/69 períodos $0 delta.

#### `CAN-FIN-003`: Cobros y Deducciones Operacionales
- **canonical_id**: `CAN-FIN-003`
- **nombre**: "Cobros y Deducciones Operacionales"
- **definicion_oficial**: "Conjunto de cargos retenidos por los marketplaces por concepto de comisiones de venta, costo logístico, servicios, publicidad, fulfillment y penalidades."
- **categoria**: `FINANCIERO` | **subcategoria**: `Cobros`
- **descripcion**: "Desglose de los 96 conceptos económicos clasificados en el Economic Dictionary."
- **owner**: Financial Data Engineer
- **fuente_oficial**: `marketplace_ledger_v1.financial_group = 'cobros'`
- **contrato_relacionado**: `CTR-002`, `CTR-005`, `CTR-008`
- **evidencia_relacionada**: `EVID-SELLER-REALITY-001`
- **capability_relacionada**: `CAP-ML-POSCOBRO`
- **pregunta_financiera_relacionada**: Pregunta 2 y Pregunta 9
- **arquitectura_relacionada**: Domain Layer / Financial Engine
- **data_lineage_relacionado**: Settlement (Etapa 6) → Ledger (Etapa 9)
- **marketplace_relacionado**: `CONSOLIDADO`
- **version**: `1.0.0` | **estado**: `CANÓNICO` | **madurez**: Nivel 4 (Certificado)
- **fecha_creacion**: 2026-06-06 | **ultima_revision**: 2026-07-27
- **politica_reemplazo**: Requerido match 100% con ROOT_EVENTS de seller.
- **observaciones**: Trazabilidad completa $172.6M ROOT_EVENTS.

#### `CAN-FIN-004`: Resultado Neto (Disponible Liquidado)
- **canonical_id**: `CAN-FIN-004`
- **nombre**: "Resultado Neto / Disponible Liquidado"
- **definicion_oficial**: "Flujo neto disponible resultado de restar de las Ventas Brutas las Devoluciones y los Cobros Operacionales totales."
- **categoria**: `FINANCIERO` | **subcategoria**: `Cierre_Financiero`
- **descripcion**: "Cifra final de resultado corporativo registrada en el cierre financiero oficial."
- **owner**: Single Financial Truth Guardian
- **fuente_oficial**: `marketplace_cierre_financiero_v1.resultado_neto`
- **contrato_relacionado**: `CTR-005`, `CTR-008`
- **evidencia_relacionada**: `EVID-DB-001`, `EVID-RIPLEY-CLASSIF-001`
- **capability_relacionada**: `CAP-CIERRE-V1`
- **pregunta_financiera_relacionada**: Pregunta 3, Pregunta 10
- **arquitectura_relacionada**: Financial Engine (Motor Core)
- **data_lineage_relacionado**: Ledger (Etapa 9) → Evidence (Etapa 10)
- **marketplace_relacionado**: `CONSOLIDADO`
- **version**: `1.0.0` | **estado**: `CANÓNICO` | **madurez**: Nivel 5 (Productivo)
- **fecha_creacion**: 2026-05-30 | **ultima_revision**: 2026-07-27
- **politica_reemplazo**: Invariable. Certificado Paris/Ripley $0 delta.
- **observaciones**: Cierre oficial inmutable.

---

### 2. Conceptos Técnicos y Arquitectónicos

#### `CAN-TEC-001`: Single Source of Truth (SSOT)
- **canonical_id**: `CAN-TEC-001`
- **nombre**: "Single Source of Truth Financiera"
- **definicion_oficial**: "Principio arquitectónico que declara a `Marketplace Financial` (`meli_financial_v4.db`) como la única base de datos oficial inmutable para cifras financieras corporativas."
- **categoria**: `ARQUITECTÓNICO` | **subcategoria**: `Persistencia`
- **descripcion**: "Invalida cualquier reporte o visualización externa que contradiga los saldos de la base DuckDB oficial."
- **owner**: Chief Architect
- **fuente_oficial**: `ADR-001` en `DECISION_REGISTRY_V1.md`
- **contrato_relacionado**: `CTR-008`
- **evidencia_relacionada**: `EVID-DB-001`
- **capability_relacionada**: `CAP-DB-CORE`
- **pregunta_financiera_relacionada**: Todas (1 a 10)
- **arquitectura_relacionada**: Data Layer
- **data_lineage_relacionado**: Ledger (Etapa 9)
- **marketplace_relacionado**: `CONSOLIDADO`
- **version**: `1.0.0` | **estado**: `CANÓNICO` | **madurez**: Nivel 5 (Productivo)
- **fecha_creacion**: 2026-05-30 | **ultima_revision**: 2026-07-27
- **politica_reemplazo**: Inviolable.
- **observaciones**: SHA-256 DB: `311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9`.

#### `CAN-TEC-002`: Modelo de Grafos Duales
- **canonical_id**: `CAN-TEC-002`
- **nombre**: "Modelo de Grafos Duales (Knowledge + Execution)"
- **definicion_oficial**: "Arquitectura de representación basada en dos grafos interconectados pero desacoplados: uno para el conocimiento y gobierno (Knowledge Graph) y otro para la ejecución y pipelines (Execution Graph)."
- **categoria**: `ARQUITECTÓNICO` | **subcategoria**: `Grafos`
- **descripcion**: "Permite análisis de impacto, detección de SPOF y auditorías automatizadas sin mezclar código con especificaciones."
- **owner**: Graph Architect
- **fuente_oficial**: `DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md`
- **contrato_relacionado**: `CTR-010`, `CTR-011`
- **evidencia_relacionada**: `DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md`
- **capability_relacionada**: `CAP-DUAL-GRAPH`
- **pregunta_financiera_relacionada**: Preguntas 1 a 10
- **arquitectura_relacionada**: Knowledge Graph / Execution Graph
- **data_lineage_relacionado**: System Intelligence (Etapa 12)
- **marketplace_relacionado**: `CONSOLIDADO`
- **version**: `1.0.0` | **estado**: `ESPECIFICADO` | **madurez**: Nivel 1 (Especificado)
- **fecha_creacion**: 2026-07-27 | **ultima_revision**: 2026-07-27
- **politica_reemplazo**: Evolución aditiva de tipos de nodos y relaciones.
- **observaciones**: Especificación formal de 24 nodos KG y 26 nodos EG.

---

### 3. Conceptos de Gobierno y Auditoría

#### `CAN-GOB-001`: La Regla de Oro del Proyecto
- **canonical_id**: `CAN-GOB-001`
- **nombre**: "Regla de Oro de Implementación y Certificación"
- **definicion_oficial**: "Norma suprema de gobierno que prohíbe considerar implementada o certificada cualquier capacidad que carezca de Contrato de Datos, Evidencia Registrada, Trazabilidad Completa, Registro Canónico, Pruebas Automatizadas y Certificación Oficial."
- **categoria**: `GOBIERNO` | **subcategoria**: `Normativa`
- **descripcion**: "Estándar innegociable de aceptación para todos los paquetes de trabajo del proyecto."
- **owner**: PMO Lead
- **fuente_oficial**: `EXECUTION_PLAN_PHASE_0_FOUNDATION_V3.md`
- **contrato_relacionado**: Todos (`CTR-001` a `CTR-011`)
- **evidencia_relacionada**: `EVIDENCE_REGISTRY_V1.md`
- **capability_relacionada**: Todas las capacidades
- **pregunta_financiera_relacionada**: Todas las preguntas
- **arquitectura_relacionada**: Todas las capas
- **data_lineage_relacionado**: Todas las etapas (1 a 13)
- **marketplace_relacionado**: `CONSOLIDADO`
- **version**: `1.0.0` | **estado**: `CANÓNICO` | **madurez**: Nivel 5 (Productivo)
- **fecha_creacion**: 2026-07-27 | **ultima_revision**: 2026-07-27
- **politica_reemplazo**: Inmutable. Regla rectora del Master Plan.
- **observaciones**: Aplicación obligatoria en todas las tareas del PMO.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:KNOWLEDGE_CANONICAL_REGISTRY_V1` (Tipo: `Registro_Canónico_Maestro`)
- `Node:CAN-FIN-001` .. `Node:CAN-GOB-001` (Tipo: `Concepto_Canónico`)

### Execution Graph Nodes
- `ExecNode:VERIFY_CANONICAL_CONSISTENCY` (Process: Auditar ausencia de conceptos duplicados o no catalogados)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: El diccionario canónico unificado de verdades del proyecto.
- **GOBIERNA**: La terminología utilizada en contratos, evidencias, UI y Copilot.
- **AFECTA**: [FINANCIAL_COPILOT_QUESTION_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/FINANCIAL_COPILOT_QUESTION_REGISTRY_V1.md).

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[KNOWLEDGE_CANONICAL_REGISTRY_V1]]
- Mapeo de navegación: `KnowledgeOS/01_Canonical/KNOWLEDGE_CANONICAL_REGISTRY_V1.md`
