---
id: KNOWLEDGE_OS_SPECIFICATION
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Knowledge Engineer & Chief Architect
ultima_revision: 2026-07-27
dependencias: [EXECUTION_PLAN_PHASE_0_FOUNDATION_V3, EVIDENCE_REGISTRY_V1, ARCHITECTURE_REGISTRY_V1]
relacionado_con: [DUAL_GRAPH_ARCHITECTURE_MODEL_V1, SYSTEM_INTELLIGENCE_SPECIFICATION_V1, PMO_REGISTRY_V1]
---

# ESPECIFICACIÓN MAESTRA DE KNOWLEDGEOS Y PIPELINE DE CONOCIMIENTO V1

## Propósito
Establecer la estructura oficial, principios de gobernanza, taxonomía en 3 niveles, ciclo de vida documental y reglas de navegación Obsidian para **KnowledgeOS**, la capa de gestión del conocimiento certificado del **Marketplace Financial AI Engine**.

---

## Estructura Oficial de Carpetas KnowledgeOS

```text
KnowledgeOS/
├── 00_Inbox/         # Recepción de documentos crudos, notas y propuestas no clasificadas
├── 01_Canonical/     # Registros canónicos inmutables y fuentes únicas de verdad
├── 02_Governance/    # Planes maestros, ADRs, PMO, contratos de datos y registros de gobierno
├── 03_Evidence/      # Certificaciones de auditoría, resúmenes de tests y evidencias reproducibles
├── 04_Projects/      # Especificaciones de proyectos, sprints y artefactos de desarrollo
├── 05_References/    # Guías externas, estándares de industria, manuales y diccionarios
├── 90_Archive/       # Documentos obsoletos o reemplazados preservados con trazabilidad
└── 99_Quarantine/    # Documentos en observación por contradicciones o falta de evidencia
```

---

## Especificación Detallada por Carpeta (8.1)

### 1. `00_Inbox/` (Entrada y Recepción)
- **Propósito**: Canal de entrada unificado para capturar nuevos documentos, notas de discusión o ideas sin clasificar.
- **Contenido Permitido**: Borradores, notas Markdown, transcripts de sesiones, propuestas de RFC/ADR en revisión.
- **Contenido Prohibido**: Documentos declarados como canónicos o certificaciones oficiales.
- **Responsable**: Knowledge Steward / Inbox Agent.
- **Estado Documental Permitido**: `INBOX`.
- **Criterio de Entrada**: Creación de cualquier nueva nota o documento no validado.
- **Criterio de Salida**: Clasificación exitosa mediante el Pipeline de Conocimiento.
- **Política de Versionado**: No requiere versionado semántico formal en esta etapa.
- **Política de Conservación**: Limpieza periódica tras promover a `01_Canonical`, `02_Governance` o `99_Quarantine`.

---

### 2. `01_Canonical/` (Fuentes Únicas de Verdad)
- **Propósito**: Albergar todos los registros canónicos aprobados que constituyen la Single Source of Truth del proyecto.
- **Contenido Permitido**: Registros de conceptos financieros, Economic Dictionary, lineage canónico, question registries.
- **Contenido Prohibido**: Borradores, notas temporales, evidencias de ejecuciones individuales.
- **Responsable**: Single Financial Truth Guardian.
- **Estado Documental Permitido**: `CANÓNICO`, `CERTIFICADO`.
- **Criterio de Entrada**: Aprobación formal por el PMO y verificación $0 delta.
- **Criterio de Salida**: Reemplazo por una nueva versión canónica (moviéndose la versión anterior a `90_Archive`).
- **Política de Versionado**: Semántico estricto (`v1.0.0`, `v1.1.0`).
- **Política de Conservación**: Inmutable. Conservación permanente.

---

### 3. `02_Governance/` (Gobierno y Dirección)
- **Propósito**: Contener los instrumentos de dirección, control, decisiones de arquitectura y contratos de interfaz.
- **Contenido Permitido**: Master Plan V3, `PMO_REGISTRY_V1.md`, `ARCHITECTURE_REGISTRY_V1.md`, `DATA_CONTRACT_REGISTRY_V1.md`, ADRs, Registros de Deuda Técnica.
- **Contenido Prohibido**: Código fuente, scripts de backend, datos RAW.
- **Responsable**: Chief Architect / PMO Lead.
- **Estado Documental Permitido**: `ESPECIFICADO`, `CANÓNICO`, `CERTIFICADO`.
- **Criterio de Entrada**: Aprobación ejecutiva y asignación en Master Plan.
- **Criterio de Salida**: Desactualización de la gobernanza (con preservación histórica).
- **Política de Versionado**: Versionado semántico obligatorio con Header Universal.
- **Política de Conservación**: Inmutable e histórica.

---

### 4. `03_Evidence/` (Respaldo Probatorio)
- **Propósito**: Almacenar las pruebas físicas y documentales de certificaciones, ejecuciones y auditorías.
- **Contenido Permitido**: `EVIDENCE_REGISTRY_V1.md`, JSON summaries de validación (`summary.json`), reportes de 3 clean runs.
- **Contenido Prohibido**: Opiniones o especificaciones sin respaldo de ejecución.
- **Responsable**: Evidence Guardian / QA Lead.
- **Estado Documental Permitido**: `VALIDADA`, `CERTIFICADA`.
- **Criterio de Entrada**: Generación por harness automatizado con hash SHA-256 e `execution_id`.
- **Criterio de Salida**: Invalidez del test o superación por nueva certificación.
- **Política de Versionado**: Indexación por `execution_id` y timestamp.
- **Política de Conservación**: Inmutable. No eliminación.

---

### 5. `04_Projects/` (Proyectos y Sprints)
- **Propósito**: Documentar el detalle ejecutable de los proyectos y paquetes de trabajo (Work Packages).
- **Contenido Permitido**: Specs de proyectos, backlog de Sprints, planes de captura de valor.
- **Contenido Prohibido**: Registros canónicos globales.
- **Responsable**: Technical Product Owner.
- **Estado Documental Permitido**: `CLASIFICADO`, `INVENTARIADO`, `ANALIZADO`.
- **Criterio de Entrada**: Aprobación de un proyecto en el PMO.
- **Criterio de Salida**: Cierre del proyecto y migración de aprendizajes a `01_Canonical`.
- **Política de Versionado**: Versionado por Sprint / Hito.
- **Política de Conservación**: Conservación post-cierre como registro histórico.

---

### 6. `05_References/` (Referencias Externas y Estándares)
- **Propósito**: Guardar documentación de consulta sobre tecnologías, APIs de terceros y estándares del SII / ERP.
- **Contenido Permitido**: Mapeos de APIs Mercado Libre/Falabella/Paris/Ripley, especificaciones DTE SII, manuales BAPI SAP.
- **Contenido Prohibido**: Documentos propios con datos financieros confidenciales de producción.
- **Responsable**: Domain Specialist.
- **Estado Documental Permitido**: `ANALIZADO`.
- **Criterio de Entrada**: Relevancia directa para contratos de datos o ingestas.
- **Criterio de Salida**: Deprecación de la API o norma externa.
- **Política de Versionado**: Versionado según el emisor externo.
- **Política de Conservación**: Conservación histórica de referencia.

---

### 7. `90_Archive/` (Archivo Histórico)
- **Propósito**: Preservar documentos obsoletos, versiones anteriores reemplazadas o análisis cerrados.
- **Contenido Permitido**: Cualquier documento que haya sido superado por una nueva versión canónica.
- **Contenido Prohibido**: Documentos vigentes o fuentes de verdad activas.
- **Responsable**: Archivist Agent.
- **Estado Documental Permitido**: `ARCHIVADO`, `REEMPLAZADO`.
- **Criterio de Entrada**: Emisión de una versión sucesora en `01_Canonical` o `02_Governance`.
- **Criterio de Salida**: Ninguno (repositorio final).
- **Política de Versionado**: Congelado en la última versión vigente al momento del archivo.
- **Política de Conservación**: Inmutable e indefinida.

---

### 8. `99_Quarantine/` (Cuarentena de Observación)
- **Propósito**: Aislar documentos con contradicciones conceptuales, datos no verificados o deudas probatorias.
- **Contenido Permitido**: Documentos bajo auditoría o en disputa de verdad financiera.
- **Contenido Prohibido**: Documentos certificados o canónicos.
- **Responsable**: Financial Auditor / Debt Reviewer.
- **Estado Documental Permitido**: `CUARENTENA`.
- **Criterio de Entrada**: Detección de divergencia o falta de evidencia probatoria.
- **Criterio de Salida**: Corrección formal y migración a `01_Canonical` / `02_Governance` o descarte a `90_Archive`.
- **Política de Versionado**: Marcado con tag `[CUARENTENA]`.
- **Política de Conservación**: Temporal hasta resolución de auditoría. La cuarentena NO implica eliminación.

---

## Ciclo de Vida Oficial del Conocimiento (8.2)

```text
INBOX (00_Inbox)
  ↓
Clasificación (Identificación de tipo y dominio)
  ↓
Inventario (Catalogación en registro de activos)
  ↓
Análisis (Evaluación de calidad, duplicidad e impacto)
  ↓
Grafo (Mapeo de nodos y aristas en Dual Graph)
  ↓
Canonical (Promoción a 01_Canonical / 02_Governance)
  ↓
Certificación (Asignación de evidencia y hash $0 delta)
  ↓
Obsidian (Integración de enlaces y metadatos)
  ↓
Archivo (Preservación en 90_Archive al ser reemplazado)
```

---

## Separación Obligatoria en 3 Niveles (8.3)

1. **Inventario**: Proceso de identificación que responde a: *¿Qué artefactos existen en el repositorio?* Registrar ruta, tamaño, fecha y SHA-256.
2. **Análisis**: Proceso cualitativo que responde a: *¿Qué validez, vigencia, duplicidad o contradicción tiene cada artefacto?* Determina impacto y dependencias.
3. **Consolidación**: Proceso ejecutivo que responde a: *¿Cuál artefacto es la fuente canónica autorizada?* Promueve el documento a `01_Canonical` o `02_Governance` y archiva versiones competidoras.

---

## Estados Documentales Permitidos (8.4)

| Estado | Descripción | Ubicación Principal |
| :--- | :--- | :--- |
| `INBOX` | Recién ingresado, no evaluado | `00_Inbox/` |
| `CLASIFICADO` | Dominio y tipo identificados | `00_Inbox/` / `04_Projects/` |
| `INVENTARIADO` | Catalogado con hash y ruta | `04_Projects/` / `05_References/` |
| `ANALIZADO` | Evaluado en calidad e impacto | `04_Projects/` / `05_References/` |
| `CANÓNICO` | Fuente única de verdad aprobada | `01_Canonical/` |
| `CERTIFICADO` | Respaldado con evidencia reproducible | `02_Governance/` / `03_Evidence/` |
| `ARCHIVADO` | Obsoleto o histórico preservado | `90_Archive/` |
| `CUARENTENA` | En observación por inconsistencias | `99_Quarantine/` |
| `REEMPLAZADO` | Superado por una versión posterior | `90_Archive/` |

---

## Reglas de Interfaz y Navegación Obsidian (8.5)

1. **Enlaces Internos Estables**: Toda referencia entre documentos debe usar sintaxis Markdown estándar o wikilinks Obsidian con identificadores estables (e.g. `[[ARCHITECTURE_REGISTRY_V1]]` o `[Architecture](file:///path/to/file.md)`).
2. **Metadatos Universales**: Todos los documentos de conocimiento DEBEN llevar el Header Universal normalizado.
3. **Prohibición de Sobrescritura Destructiva**: Prohibido sobrescribir o eliminar archivos originales en Fase 0.
4. **Desacople Estructural**: La validez semántica no depende de la ruta física en disco sino del ID y metadatos del Header.
5. **No Auto-Canonización**: Ningún script o subagente puede auto-promover un documento a `CANÓNICO` sin pasar por el proceso de validación.
6. **Preservación en Cuarentena**: Los archivos en `99_Quarantine/` se preservan intactos para análisis forense.

---

## Integración con Grafos Duales (8.6)

Cada documento en KnowledgeOS se vincula explícitamente a:
- **Knowledge Graph**: Representando decisiones (`ADRs`), deudas técnicas (`TDs`), reglas contables y registros canónicos.
- **Execution Graph**: Vinculando el documento con el código (`engine/`), las pruebas (`tests/`), las tablas DuckDB (`data/db/`) y las preguntas del Copilot.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:KNOWLEDGE_OS_SPECIFICATION` (Tipo: `Especificacion_KnowledgeOS`)
- `Node:INBOX` .. `Node:QUARANTINE` (Tipo: `Carpeta_KnowledgeOS`)

### Execution Graph Nodes
- `ExecNode:VERIFY_KNOWLEDGE_PIPELINE` (Process: Auditar cumplimiento de estados documentales y ciclo de vida en CI/CD)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: El diseño oficial de la Capa de Conocimiento y KnowledgeOS.
- **GOBIERNA**: La organización documental en Obsidian para todas las fases del proyecto.
- **AFECTA**: [EVIDENCE_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/EVIDENCE_REGISTRY_V1.md) y [DUAL_GRAPH_ARCHITECTURE_MODEL_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md).

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[KNOWLEDGE_OS_SPECIFICATION]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/KNOWLEDGE_OS_SPECIFICATION.md`
