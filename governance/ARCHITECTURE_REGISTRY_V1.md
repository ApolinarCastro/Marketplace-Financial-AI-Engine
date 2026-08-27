---
id: ARCHITECTURE_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Solution Architect & Chief Architect
ultima_revision: 2026-07-27
dependencias: [EXECUTION_PLAN_PHASE_0_FOUNDATION_V3, PMO_REGISTRY_V1, BASELINE_POST_SURGICAL_FIX]
relacionado_con: [DATA_CONTRACT_REGISTRY_V1, DUAL_GRAPH_ARCHITECTURE_MODEL_V1, SYSTEM_INTELLIGENCE_SPECIFICATION_V1]
---

# REGISTRO MAESTRO DE ARQUITECTURA DEL SISTEMA V1

## Propósito
Establecer la especificación oficial de arquitectura por capas del **Marketplace Financial AI Engine**. Define formalmente el mapa de capas, responsabilidades, componentes, contratos de entrada/salida, matriz de dependencias inter-componentes y la reserva de espacio arquitectónico para la evolución de Inteligencia Artificial (System Intelligence / Copilot).

---

## Regla de Gobierno y Aislamiento

> [!IMPORTANT]
> ### PRINCIPIO DE AISLAMIENTO POR CAPAS
> Ninguna capa podrá consumir datos de capas inferiores sin pasar por la interfaz de contrato definida. El Financial Copilot y la capa de Inteligencia jamás consultarán capas RAW o la base de datos sin atravesar la **Knowledge Layer** y la **System Intelligence Layer**.

---

## Definición Formal de Capas Oficiales del Sistema (12 Capas)

### 1. Presentation Layer (Capa de Presentación)
- **Propósito**: Interfaz gráfica de usuario y tableros ejecutivos para interacción humana.
- **Responsabilidades**: Renderizar visualizaciones financieras, dashboards gerenciales (`/exec`), vista auditor (`/app`), formateo monetario CLP, alertas de discrepancia.
- **Componentes**: `templates/dashboard.html`, `templates/executive_dashboard.html`, `static/css/`, `static/js/`.
- **Entradas**: JSON Payloads HTTP GET desde la API Layer.
- **Salidas**: Documentos HTML5, vistas DOM interactivas, exportaciones visuales.
- **Dependencias**: API Layer.
- **Estado de Madurez**: Nivel 3 (Validado).
- **Criticidad**: ALTA.

---

### 2. API Layer (Capa de Servicios REST / API)
- **Propósito**: Exponer servicios de consulta financiera y endpoints con contratos públicos inmutables.
- **Responsabilidades**: Autenticación, rate limiting, validación de schemas de entrada/salida, routing HTTP GET/POST, transformación de respuestas JSON.
- **Componentes**: `api/api.py`, middleware de seguridad, validadores de respuesta HTTP.
- **Entradas**: HTTP Requests desde Presentation Layer o clientes externos.
- **Salidas**: HTTP Responses JSON con headers de seguridad y estado 200/400/500.
- **Dependencias**: Application Layer, Financial Engine.
- **Estado de Madurez**: Nivel 4 (Certificado - 14/14 endpoints inmutables).
- **Criticidad**: CRÍTICA.

---

### 3. Application Layer (Capa de Aplicación y Casos de Uso)
- **Propósito**: Orquestar casos de uso de negocio, flujos de trabajo de ingesta y conciliación.
- **Responsabilidades**: Orquestar tareas de carga, coordinar ejecución de indexadores, orquestar workflows de conciliación.
- **Componentes**: `engine/v4/ingestion/orchestrator.py`, `tools/surgical_migration_orchestrator.py`.
- **Entradas**: Comandos del CLI, triggers de API o eventos programados.
- **Salidas**: Trazas de ejecución, logs de auditoría, llamadas a servicios de dominio.
- **Dependencias**: Domain Layer, Financial Engine.
- **Estado de Madurez**: Nivel 3 (Validado).
- **Criticidad**: ALTA.

---

### 4. Domain Layer (Capa de Dominio y Reglas Negocio)
- **Propósito**: Encapsular entidades de negocio, conceptos financieros canónicos y diccionarios económicos.
- **Responsabilidades**: Definir modelo conceptual de Marketplace (Ventas, Devoluciones, Cobros, Disponible), reglas de clasificación de conceptos.
- **Componentes**: `engine/v4/domain/financial_engine.py`, Economic Dictionary Registry.
- **Entradas**: Estructuras de transacciones de Marketplace y movimientos de liquidación.
- **Salidas**: Entidades de dominio clasificadas y validadas.
- **Dependencias**: Data Layer.
- **Estado de Madurez**: Nivel 4 (Certificado - 96 conceptos mapeados).
- **Criticidad**: CRÍTICA.

---

### 5. Financial Engine (Motor Financiero Core)
- **Propósito**: Ejecutar motores de cálculo, ledger determinista y cierres financieros.
- **Responsabilidades**: Construir `marketplace_ledger_v1`, computar `marketplace_cierre_financiero_v1`, calcular Resultado Neto, verificar paridad $0 delta.
- **Componentes**: `engine/v4/surgical_loader.py`, `engine/v4/surgical_xml_justifier.py`, `engine/v4/dte_indexer.py`.
- **Entradas**: Tablas normalizadas en DuckDB.
- **Salidas**: Registros de ledger clasificados, tablas de cierre mensual.
- **Dependencias**: Data Layer, DuckDB Core.
- **Estado de Madurez**: Nivel 5 (Productivo - 69/69 períodos $0 delta).
- **Criticidad**: CRÍTICA MAXIMA.

---

### 6. Evidence Layer (Capa de Evidencia)
- **Propósito**: Garantizar la trazabilidad legal y documental de cada cifra financiera.
- **Responsabilidades**: Generar resúmenes JSON de auditoría (`summary.json`), almacenar logs con `execution_id`, hashes SHA-256 de archivos fuente.
- **Componentes**: `evidence/`, `evidence/fase_1b/`, `tools/validate_fase_1b.py`.
- **Entradas**: Logs de ejecución del Financial Engine y comprobantes XML/DTE.
- **Salidas**: Archivos de evidencia certificada Nivel 1 y Nivel 2.
- **Dependencias**: Financial Engine, Data Layer.
- **Estado de Madurez**: Nivel 4 (Certificado).
- **Criticidad**: CRÍTICA.

---

### 7. Data Layer (Capa de Datos y Persistencia)
- **Propósito**: Persistir de manera inmutable y determinista todos los datos del sistema.
- **Responsabilidades**: Almacenar base de datos DuckDB oficial, gestionar archivos RAW inmutables, proveer acceso OLAP de alta velocidad.
- **Componentes**: `data/db/meli_financial_v4.db` (DuckDB V1.5.1, SHA256: `311c78e2b7...`), `01_Raw/`.
- **Entradas**: Archivos CSV/XLSX/XML fuente.
- **Salidas**: Tablas relacionales OLAP, vistas de ledger, registros de transacciones.
- **Dependencias**: Sistema de Archivos local.
- **Estado de Madurez**: Nivel 5 (Productivo).
- **Criticidad**: CRÍTICA MAXIMA.

---

### 8. Knowledge Layer (Capa de Conocimiento)
- **Propósito**: Consolidar y estructurar la información documental y conceptual del sistema.
- **Responsabilidades**: Gestionar KnowledgeOS (`00_Inbox` a `99_Quarantine`), mantener registros canónicos, eliminar duplicidad conceptual.
- **Componentes**: `KnowledgeOS/`, `governance/`, `knowledge/`.
- **Entradas**: Documentos Markdown, ADRs, RFCs, especificaciones de arquitectura.
- **Salidas**: Estructura navegable Obsidian, archivos de conocimiento normalizados.
- **Dependencias**: Evidence Layer.
- **Estado de Madurez**: Nivel 1 (Especificado).
- **Criticidad**: ALTA.

---

### 9. Knowledge Graph (Grafo de Conocimiento)
- **Propósito**: Modelar las relaciones conceptuales, normativas y documentales del sistema.
- **Responsabilidades**: Mapear nodos de Documento, Regla, Decisión, Referencia y Deuda Técnica; evaluar impacto de cambios normativos.
- **Componentes**: `DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md` (Vista Knowledge Graph).
- **Entradas**: Metadatos de la Knowledge Layer y registros de gobierno.
- **Salidas**: Estructura de grafo semántico, rutas de impacto documental.
- **Dependencias**: Knowledge Layer.
- **Estado de Madurez**: Nivel 1 (Especificado).
- **Criticidad**: ALTA.

---

### 10. Execution Graph (Grafo de Ejecución)
- **Propósito**: Modelar las relaciones operativas, pipelines de datos y procesos de software.
- **Responsabilidades**: Mapear nodos de Endpoint, Pipeline, Test, Job, Tabla DuckDB, Proceso de Conciliación y Archivo RAW.
- **Componentes**: `DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md` (Vista Execution Graph).
- **Entradas**: Metadatos de API Layer, Financial Engine y Data Layer.
- **Salidas**: Rutas de linaje de datos de ejecución, análisis de fallo en pipelines.
- **Dependencias**: Application Layer, Financial Engine, Data Layer.
- **Estado de Madurez**: Nivel 1 (Especificado).
- **Criticidad**: ALTA.

---

### 11. System Intelligence Layer (Capa de Inteligencia del Sistema)
- **Propósito**: Orquestar capacidades avanzadas de procesamiento semántico, IA y razonamiento sobre el Dual Graph.
- **Responsabilidades**: Generar embeddings, orquestar RAG, ejecutar razonamiento en grafos, administrar memoria de contexto sin tocar RAW no verificado.
- **Componentes (Ubicación Reservada)**: Vector DB Engine, RAG Orchestration Module, Graph Reasoning Engine, MCP Integration.
- **Entradas**: Consultas de Copilot, nodos del Dual Graph, resúmenes de la Knowledge Layer.
- **Salidas**: Contextos certificados, grafos de evidencia explicables, planes de respuesta.
- **Dependencias**: Knowledge Graph, Execution Graph, Evidence Layer.
- **Estado de Madurez**: Nivel 1 (Especificado).
- **Criticidad**: CRÍTICA PARA COPILOT.

---

### 12. Financial Copilot (Capa de Copiloto Financiero)
- **Propósito**: Interfaz conversacional y razonada para respuesta de preguntas financieras corporativas.
- **Responsabilidades**: Responder las 10 Preguntas Financieras Estratégicas respaldadas en evidencia $0 delta con explicabilidad completa.
- **Componentes (Ubicación Reservada)**: Financial Copilot API, Question Resolution Engine.
- **Entradas**: Preguntas en lenguaje natural de usuarios ejecutivos o sistemas externos.
- **Salidas**: Respuestas estructuradas con cifras $0 delta, tablas justificativas y enlaces a evidencias.
- **Dependencias**: System Intelligence Layer.
- **Estado de Madurez**: Nivel 0 (Idea / Especificado).
- **Criticidad**: ALTA.

---

## Matriz de Dependencias e Impacto (Inter-Component Dependency Matrix)

| Componente Origen | Capa | Depende De (Entrada) | Impacta En (Salida) | Criticidad |
| :--- | :--- | :--- | :--- | :--- |
| **Presentation Layer** | Presentation | API Layer | Usuario / Ejecutivo | ALTA |
| **API Layer** | API | Application Layer, Financial Engine | Presentation Layer, Clientes External | CRÍTICA |
| **Application Layer** | Application | Domain Layer, Financial Engine | API Layer | ALTA |
| **Domain Layer** | Domain | Data Layer | Financial Engine | CRÍTICA |
| **Financial Engine** | Financial Engine | Data Layer (DuckDB) | Evidence Layer, API Layer | CRÍTICA MAXIMA |
| **Evidence Layer** | Evidence | Financial Engine, Data Layer | Knowledge Layer | CRÍTICA |
| **Data Layer** | Data | Filesystem (RAW) | Financial Engine, Evidence Layer | CRÍTICA MAXIMA |
| **Knowledge Layer** | Knowledge | Evidence Layer | Knowledge Graph, System Intelligence | ALTA |
| **Knowledge Graph** | Graph | Knowledge Layer | System Intelligence Layer | ALTA |
| **Execution Graph** | Graph | Application, Financial Engine, Data Layer | System Intelligence Layer | ALTA |
| **System Intelligence Layer** | System Intelligence | Knowledge Graph, Execution Graph | Financial Copilot | CRÍTICA |
| **Financial Copilot** | Copilot | System Intelligence Layer | Usuario Final / Sistemas Gerenciales | ALTA |

---

## Reserva de Espacio Arquitectónico para Evolución de IA

La arquitectura reserva formalmente la ubicación de los siguientes módulos dentro de la **System Intelligence Layer**:

1. **Embeddings Engine**: Generación de vectores denso para documentos canónicos y registraciones de gobierno.
2. **RAG Orchestrator**: Recuperación aumentada por generación utilizando únicamente nodos verificados del Knowledge Graph.
3. **Model Context Protocol (MCP)**: Integración de herramientas e interfaces estándar para interacción entre subagentes.
4. **Agentes Especializados**: Spawn de subagentes por dominio (Data Engineer, Financial Auditor, Reconciliation Agent).
5. **Inferencia Local (Ollama)**: Soporte para ejecución local privada de LLMs de tamaño mediano sin salida a la nube.
6. **NVIDIA NIM / Inferencia Cloud**: Conector para microservicios NIM o APIs cloud de alta capacidad.
7. **Motor Semántico & Motor de Grafos**: Evaluador de traversal de grafos para deducción de causas raíz.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:ARCHITECTURE_REGISTRY_V1` (Tipo: `Registro_Arquitectura`)
- `Node:LAYER_PRESENTATION` .. `Node:LAYER_FINANCIAL_COPILOT` (Tipo: `Capa_Sistema`)

### Execution Graph Nodes
- `ExecNode:VERIFY_LAYER_BOUNDARIES` (Process: Auditar cumplimiento de aislamiento entre capas en CI/CD)

---

## Trazabilidad y Relaciones
- **GOBIERNA**: La estructura por capas oficial del proyecto.
- **ORIGINA**: [DATA_CONTRACT_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/DATA_CONTRACT_REGISTRY_V1.md)
- **AFECTA**: Todos los desarrollos de la Fase 1 a la Fase 8.

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[ARCHITECTURE_REGISTRY_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/ARCHITECTURE_REGISTRY_V1.md`
