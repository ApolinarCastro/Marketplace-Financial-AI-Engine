---
id: DATA_LINEAGE_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Senior Data Engineer & Data Architect
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - ARCHITECTURE_REGISTRY_V1
  - DATA_CONTRACT_REGISTRY_V1
  - EVIDENCE_REGISTRY_V1
relacionado_con:
  - END_TO_END_RECONCILIATION_ROADMAP_V1
  - KNOWLEDGE_CANONICAL_REGISTRY_V1
  - FINANCIAL_COPILOT_QUESTION_REGISTRY_V1
---

# REGISTRO MAESTRO DE LINEAJE DE DATOS (DATA LINEAGE) V1

## Propósito
Establecer la especificación formal del **Lineaje de Datos (Data Lineage)** para la cadena completa de 13 etapas del **Marketplace Financial AI Engine**. Garantiza la trazabilidad inmutable desde los archivos fuente RAW descargados de los marketplaces hasta la respuesta emitida por el Financial Copilot.

---

## Cadena Oficial de Lineaje de Datos (13 Etapas)

```text
Marketplace (1) ──LIN-001──> RAW (2) ──LIN-002──> Normalización (3) ──LIN-003──> XML/DTE (4)
        ──LIN-004──> SAP (5) ──LIN-005──> Settlement (6) ──LIN-006──> Pago (7)
        ──LIN-007──> Banco (8) ──LIN-008──> Ledger (9) ──LIN-009──> Evidence (10)
        ──LIN-010──> Knowledge (11) ──LIN-011──> System Intelligence (12) ──LIN-012──> Copilot (13)
```

---

## Esquema Estándar por Eslabón de Lineaje (12 Transformaciones)

### Eslabón 1: `LIN-001` (Marketplace → RAW)
- **lineage_id**: `LIN-001`
- **origen**: Portales / APIs de Marketplace (MELI, Paris, Ripley, Falabella)
- **destino**: `01_Raw/<MARKETPLACE>/`
- **transformacion**: Ingesta directa sin alteración de bytes.
- **contrato**: `CTR-001` (Marketplace → RAW)
- **evidencia**: Manifiesto de Hashes SHA-256
- **owner**: Marketplace Data Engineer | **componente**: Downloader Module
- **entradas**: Archivos descargados por HTTP/SFTP.
- **salidas**: Archivos `.csv`, `.xlsx`, `.xml` inmutables en disco.
- **validaciones**: Verificación de extensión y firma SHA-256.
- **riesgos**: Cambios inesperados en formatos de descarga de MP.
- **bloqueadores**: Inestabilidad de APIs de MP.
- **madurez**: Nivel 4 (Certificado) | **certificacion**: CERTIFICADO
- **observaciones**: Mantiene intacto el archivo original.

---

### Eslabón 2: `LIN-002` (RAW → Normalización)
- **lineage_id**: `LIN-002`
- **origen**: `01_Raw/`
- **destino**: Staging DuckDB (`stg_marketplace_raw`)
- **transformacion**: Parsing CSV/XLSX, estandarización de columnas, parseo de fechas con `dayfirst=True`.
- **contrato**: `CTR-002` (RAW → Normalización)
- **evidencia**: `EVID-DB-001` (DB Hash: `311c78e2b7...`)
- **owner**: Senior Data Engineer | **componente**: `engine/v4/surgical_loader.py`
- **entradas**: Archivos RAW en disco.
- **salidas**: Filas estructuradas en DuckDB.
- **validaciones**: Parsing estricto de fechas; coerción de tipos numéricos.
- **riesgos**: Swap de mes/día si se omite `dayfirst=True`.
- **bloqueadores**: Ninguno.
- **madurez**: Nivel 5 (Productivo) | **certificacion**: CERTIFICADO
- **observaciones**: Corregido quirúrgicamente en FASE 2.5C.

---

### Eslabón 3: `LIN-003` (Normalización → XML/DTE)
- **lineage_id**: `LIN-003`
- **origen**: Staging DuckDB (`stg_marketplace_raw`) y DTEs SII (`01_Raw/XML/`)
- **destino**: `stg_dte_sii` y Matcher DTE
- **transformacion**: Carga y parseo de XMLs SII DTE 33/43/52/61 y matching por folio/RUT.
- **contrato**: `CTR-003` (Normalización → XML)
- **evidencia**: Reports de Cobertura DTE Paris y Ripley.
- **owner**: DTE Specialist | **componente**: `engine/v4/dte_indexer.py`
- **entradas**: XMLs SII y transacciones de venta normalizadas.
- **salidas**: Folio DTE cruzado con transacción de venta.
- **validaciones**: `monto_total == neto + iva`; RUT válido.
- **riesgos**: XMLs no recepcionados o folios no coincidentes.
- **bloqueadores**: Tareas de indexación DTE pendientes.
- **madurez**: Nivel 3 (Validado) | **certificacion**: VALIDADO
- **observaciones**: Cobertura Paris 82.6% ($312.4M).

---

### Eslabón 4: `LIN-004` (XML/DTE → SAP ERP)
- **lineage_id**: `LIN-004`
- **origen**: Matcher DTE SII (`stg_dte_sii`)
- **destino**: `stg_sap_accounting_doc`
- **transformacion**: Mapeo de documentos tributarios a asientos contables SAP (Sociedad, Ejercicio, Cuentas).
- **contrato**: `CTR-004` (XML → SAP)
- **evidencia**: Registros SAP auditados.
- **owner**: SAP Integration Specialist | **componente**: SAP Module (Especificado)
- **entradas**: Folios DTE y partidas tributarias.
- **salidas**: Asientos contables SAP en staging.
- **validaciones**: Partida doble `sum(debe) == sum(haber)`.
- **riesgos**: Mapeo de plan de cuentas desactualizado.
- **bloqueadores**: Programado para Fase 5.
- **madurez**: Nivel 1 (Especificado) | **certificacion**: ESPECIFICADO
- **observaciones**: Especificación formal entregada en Fase 0.

---

### Eslabón 5: `LIN-005` (SAP → Settlement Marketplace)
- **lineage_id**: `LIN-005`
- **origen**: `stg_sap_accounting_doc` y Staging MP
- **destino**: `marketplace_liquidaciones_v1`
- **transformacion**: Clasificación de conceptos de liquidación en los 96 conceptos del Economic Dictionary.
- **contrato**: `CTR-005` (SAP → Settlement)
- **evidencia**: `EVID-RIPLEY-CLASSIF-001` ($206.9M neto)
- **owner**: Settlement Specialist | **componente**: `engine/v4/surgical_loader.py`
- **entradas**: Transacciones y cargos de liquidación MP.
- **salidas**: Registros de liquidación clasificados por período.
- **validaciones**: `neto_liquidado == bruto - comisiones - descuentos + abonos`.
- **riesgos**: Conceptos de cobro no clasificados en Economic Dictionary.
- **bloqueadores**: Ninguno.
- **madurez**: Nivel 4 (Certificado) | **certificacion**: CERTIFICADO
- **observaciones**: 100% de cobertura en Ripley (62,502 filas).

---

### Eslabón 6: `LIN-006` (Settlement → Pago)
- **lineage_id**: `LIN-006`
- **origen**: `marketplace_liquidaciones_v1`
- **destino**: `stg_pago_origen`
- **transformacion**: Mapeo de informes de pago/liberaciones enviadas por MP contra liquidaciones.
- **contrato**: `CTR-006` (Settlement → Pago)
- **evidencia**: Liberaciones ML & Ripley.
- **owner**: Treasury Specialist | **componente**: Treasury Module
- **entradas**: Montos transferidos e IDs de pago.
- **salidas**: Registro de pagos emparejados con liquidación.
- **validaciones**: Match 1:1 con `monto_neto_liquidado`.
- **riesgos**: Pagos consolidados que agrupan múltiples liquidaciones.
- **bloqueadores**: Ninguno.
- **madurez**: Nivel 3 (Validado) | **certificacion**: VALIDADO
- **observaciones**: Liberaciones ML conciliadas en G6.

---

### Eslabón 7: `LIN-007` (Pago → Banco)
- **lineage_id**: `LIN-007`
- **origen**: `stg_pago_origen`
- **destino**: `stg_cartola_bancaria`
- **transformacion**: Conciliación de referencias bancarias de pago contra abonos en la cartola oficial.
- **contrato**: `CTR-007` (Pago → Banco)
- **evidencia**: Cartolas Bancarias Oficiales.
- **owner**: Bank Reconciliation Specialist | **componente**: Bank Module (Especificado)
- **entradas**: TEFs de MP y extractos de cartola bancaria.
- **salidas**: Movimientos bancarios concilidados con $0 descalce.
- **validaciones**: Match por referencia bancaria, monto exacto y fecha.
- **riesgos**: Comisiones bancarias o cargos de transferencia no registrados.
- **bloqueadores**: Programado para Fase 7.
- **madurez**: Nivel 1 (Especificado) | **certificacion**: ESPECIFICADO
- **observaciones**: Especificación formal en Fase 0.

---

### Eslabón 8: `LIN-008` (Banco → Ledger Financiero)
- **lineage_id**: `LIN-008`
- **origen**: `stg_cartola_bancaria` y Staging Normalizado
- **destino**: `marketplace_ledger_v1` & `marketplace_cierre_financiero_v1`
- **transformacion**: Construcción del ledger de doble entrada y cómputo de Resultado Neto mensual.
- **contrato**: `CTR-008` (Banco → Ledger)
- **evidencia**: `EVID-DB-001`
- **owner**: Single Financial Truth Guardian | **componente**: `engine/v4/domain/financial_engine.py`
- **entradas**: Transacciones clasificadas y abonos bancarios.
- **salidas**: Cierre financiero de Resultado Neto inmutable.
- **validaciones**: 69/69 períodos sin descalce monetario.
- **riesgos**: Modificación accidental de reglas de cierre.
- **bloqueadores**: Ninguno.
- **madurez**: Nivel 5 (Productivo) | **certificacion**: CERTIFICADO
- **observaciones**: Fuente Única de Verdad Financiera Corporativa.

---

### Eslabón 9: `LIN-009` (Ledger → Evidence Layer)
- **lineage_id**: `LIN-009`
- **origen**: `marketplace_ledger_v1` & DuckDB DB
- **destino**: `evidence/fase_1b/` (`summary.json`, `C1.json` .. `C4.json`)
- **transformacion**: Extracción de metadatos de auditoría, cómputo de hashes SHA-256 e `execution_id`.
- **contrato**: `CTR-009` (Ledger → Evidence)
- **evidencia**: `EVID-HARNESS-001`
- **owner**: Evidence Guardian | **componente**: `tools/validate_fase_1b.py`
- **entradas**: Resultados del cierre y ejecuciones de suite.
- **salidas**: Resúmenes JSON de evidencia reproducibles.
- **validaciones**: Generación automática sin intervención manual.
- **riesgos**: Invalidez por cambios no commiteados en Git.
- **bloqueadores**: Ninguno.
- **madurez**: Nivel 4 (Certificado) | **certificacion**: CERTIFICADO
- **observaciones**: Arnés de validación oficial.

---

### Eslabón 10: `LIN-010` (Evidence → Knowledge Layer)
- **lineage_id**: `LIN-010`
- **origen**: Evidencias JSON & Specs Governance
- **destino**: `KnowledgeOS/01_Canonical/` & `02_Governance/`
- **transformacion**: Indexación de evidencias en registros canónicos de conocimiento con Header Universal.
- **contrato**: `CTR-010` (Evidence → Knowledge)
- **evidencia**: `KNOWLEDGE_OS_SPECIFICATION.md`
- **owner**: Knowledge Engineer | **componente**: KnowledgeOS Pipeline
- **entradas**: Archivos de evidencia y metadatos de auditoría.
- **salidas**: Documentos de conocimiento canónico navegables en Obsidian.
- **validaciones**: Presencia de Header Universal e IDs estables.
- **riesgos**: Desacople entre metadatos documental y archivos en disco.
- **bloqueadores**: Programado para Fase 2.
- **madurez**: Nivel 4 (Certificado) | **certificacion**: CERTIFICADO
- **observaciones**: Materializado en `knowledge/lineage/` en Fase 1 (CAP-TD-005).

---

### Eslabón 11: `LIN-011` (Knowledge → System Intelligence)
- **lineage_id**: `LIN-011`
- **origen**: KnowledgeOS & Dual Graph Layer
- **destino**: System Intelligence Engine
- **transformacion**: Traversal de grafos duales, resolución de contratos, generación de contextos RAG.
- **contrato**: `CTR-011` (Knowledge → Copilot)
- **evidencia**: `SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md`
- **owner**: AI & Copilot Architect | **componente**: System Intelligence Layer
- **entradas**: Consultas interpretadas e Intent IDs.
- **salidas**: Contexto certificado respaldado en evidencia $0 delta.
- **validaciones**: Hallucination Guard `PASS`; Fallback Handler activo si falta evidencia.
- **riesgos**: Consulta a fuentes no certificadas.
- **bloqueadores**: Desarrollo programado para Fase 8.
- **madurez**: Nivel 1 (Especificado) | **certificacion**: ESPECIFICADO
- **observaciones**: Especificación formal entregada en Task 4.

---

### Eslabón 12: `LIN-012` (System Intelligence → Financial Copilot)
- **lineage_id**: `LIN-012`
- **origen**: System Intelligence Engine
- **destino**: Financial Copilot API / Interface Usuario
- **transformacion**: Formateo de respuesta final explicable en Markdown con citas bidireccionales y métricas.
- **contrato**: `CTR-011` (Knowledge → Copilot)
- **evidencia**: `FINANCIAL_COPILOT_QUESTION_REGISTRY_V1.md`
- **owner**: Lead Product TPO | **componente**: Financial Copilot Interface
- **entradas**: Contexto certificado y métricas de confianza.
- **salidas**: Respuestas explicables $0 delta para las 10 Preguntas Estratégicas.
- **validaciones**: Cumplimiento de la Regla de Oro del Proyecto.
- **riesgos**: Presentación engañosa o sin citas probatorias.
- **bloqueadores**: Programado para Fase 8.
- **madurez**: Nivel 1 (Especificado) | **certificacion**: ESPECIFICADO
- **observaciones**: Interfaz final del usuario corporativo.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:DATA_LINEAGE_REGISTRY_V1` (Tipo: `Registro_Lineaje_Datos`)
- `Node:LIN-001` .. `Node:LIN-012` (Tipo: `Eslabon_Lineaje`)

### Execution Graph Nodes
- `ExecNode:VERIFY_LINEAGE_INTEGRITY` (Process: Auditar completitud de 12 eslabones sin saltos de contrato en CI/CD)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: El lineaje oficial ininterrumpido desde RAW hasta el Financial Copilot.
- **GARANTIZA**: Que no exista ninguna transformación sin un contrato de datos asociado (`CTR-001` a `CTR-011`).
- **AFECTA**: [END_TO_END_RECONCILIATION_ROADMAP_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/END_TO_END_RECONCILIATION_ROADMAP_V1.md).

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[DATA_LINEAGE_REGISTRY_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/DATA_LINEAGE_REGISTRY_V1.md`
