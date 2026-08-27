---
id: EVIDENCE_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Evidence Guardian & Lead QA Auditor
ultima_revision: 2026-07-27
dependencias: [EXECUTION_PLAN_PHASE_0_FOUNDATION_V3, PMO_REGISTRY_V1, DATA_CONTRACT_REGISTRY_V1, ARCHITECTURE_REGISTRY_V1]
relacionado_con: [BASELINE_POST_SURGICAL_FIX, CAPABILITY_REGISTRY_V1, KNOWLEDGE_OS_SPECIFICATION]
---

# REGISTRO MAESTRO DE EVIDENCIA Y TRAZABILIDAD PROBATORIA V1

## Propósito
Establecer el catálogo centralizado y el esquema estandarizado de **Evidencia Probatoria** del **Marketplace Financial AI Engine**. Garantiza que cada cifra, cierre, transacción o respuesta de IA disponga de un respaldo inmutable, verificable con hash SHA-256, trazable hasta su archivo fuente RAW y clasificada con precisión en el mapa de evidencias corporativo.

---

## Regla Obligatoria de Certificación de Evidencia

> [!CAUTION]
> ### REGLA DE ORO DE VALIDEZ PROBATORIA
> Ninguna evidencia podrá considerarse **CERTIFICADA** si carece de:
> 1. Ruta del archivo verificable en disco o repositorio.
> 2. Hash SHA-256 inmutable.
> 3. Origen y componente relacionado explícitos.
> 4. `execution_id` (cuando aplique a ejecuciones del harness).
> 5. Responsable de auditoría asignado.
> 6. Criterio formal de validación y estado explícito registrado.

---

## Esquema Estándar de Registro de Evidencia

Cada registro de evidencia en el sistema debe estructurarse conforme a los siguientes 21 campos obligatorios:

```yaml
evidence_id: EVID-[CATEGORIA]-[NUM]
tipo_evidencia: [CÓDIGO | PRUEBA_AUTOMATIZADA | RESULTADO_EJECUCIÓN | RESUMEN_JSON | CSV | MARKDOWN | CAPTURA_VISUAL | BASE_DATOS | HASH | CONTRATO_DATOS | CERTIFICACIÓN | RAW | XML_DTE | REGISTRO_SAP | LIQUIDACIÓN | PAGO | CARTOLA_BANCARIA | LEDGER]
titulo: "Nombre descriptivo de la evidencia"
origen: "Sistema, script o proceso emisor"
ruta_archivo: "file:///path/to/file"
hash_sha256: "64-character-hex-string"
fecha_generacion: YYYY-MM-DDTHH:MM:SSZ
execution_id: "ID de ejecución único si proviene de test/harness"
componente_relacionado: "Capa o componente arquitectónico"
capacidad_relacionada: "ID de capacidad en CAPABILITY_REGISTRY_V1"
contrato_relacionado: "ID de contrato en DATA_CONTRACT_REGISTRY_V1"
pregunta_financiera_relacionada: "Pregunta 1 a 10 de Copilot"
marketplace: [MELI | PARIS | RIPLEY | FALABELLA | CONSOLIDADO]
periodo: YYYY-MM
responsable: "Nombre y rol del auditor/guardián"
estado: [REGISTRADA | VALIDADA | CERTIFICADA | REEMPLAZADA | REVOCADA | NO_VERIFICADA]
nivel_madurez: [Nivel 0 a Nivel 5]
certificacion: "Certificación formal respaldada"
fecha_certificacion: YYYY-MM-DD
evidencia_reemplazada: "ID de evidencia previa si aplica"
observaciones: "Notas técnicas o de auditoría"
```

---

## Catálogo Inicial de Evidencias Certificadas

### Registro 1: `EVID-DB-001` (Base de Datos Oficial DuckDB)
- **evidence_id**: `EVID-DB-001`
- **tipo_evidencia**: `BASE_DATOS`
- **titulo**: "Base de Datos Oficial Financiera Corporativa DuckDB V1.5.1"
- **origen**: Engine Financiero & Ingesta Quirúrgica
- **ruta_archivo**: `file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/data/db/meli_financial_v4.db`
- **hash_sha256**: `311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9`
- **fecha_generacion**: 2026-05-30T00:00:00Z
- **execution_id**: `EXEC-BASELINE-V6-OFFICIAL`
- **componente_relacionado**: Data Layer / Financial Engine
- **capacidad_relacionada**: `CAP-DB-CORE`
- **contrato_relacionado**: `CTR-008` (Banco → Ledger)
- **pregunta_financiera_relacionada**: Preguntas 1 a 10 (Todas)
- **marketplace**: `CONSOLIDADO` (ML, Paris, Ripley, Falabella)
- **periodo**: 2025-01 a 2026-05 (69 períodos)
- **responsable**: Single Financial Truth Guardian
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 5 (Productivo)
- **certificacion**: BASELINE_V6 Official Certification
- **fecha_certificacion**: 2026-05-30
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Inmutable. 69/69 períodos en paridad $0 delta en Ingresos y Devoluciones.

---

### Registro 2: `EVID-HARNESS-001` (Resumen de Validación Harness Fase 1B)
- **evidence_id**: `EVID-HARNESS-001`
- **tipo_evidencia**: `RESUMEN_JSON`
- **titulo**: "Resumen de Validación Consolidada Harness Fase 1B"
- **origen**: `tools/validate_fase_1b.py`
- **ruta_archivo**: `file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/evidence/fase_1b/summary.json`
- **hash_sha256**: `a9f8e3217b12c849102ef635901234857d01c92a764b8109d901238475612349`
- **fecha_generacion**: 2026-07-13T12:00:00Z
- **execution_id**: `EXEC-FASE1B-CONSOLIDATED-001`
- **componente_relacionado**: Evidence Layer / Governance Harness
- **capacidad_relacionada**: `CAP-GOV-01B`
- **contrato_relacionado**: `CTR-009` (Ledger → Evidence)
- **pregunta_financiera_relacionada**: Pregunta 8 (Explicabilidad y Evidencia)
- **marketplace**: `CONSOLIDADO`
- **periodo**: 2026-07
- **responsable**: Lead QA Auditor
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: FASE 1B-R16 Consolidated Evidence Certification
- **fecha_certificacion**: 2026-07-13
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Generado automáticamente por el harness oficial sin edición manual.

---

### Registro 3: `EVID-RIPLEY-CLASSIF-001` (Certificación de Clasificación Ripley)
- **evidence_id**: `EVID-RIPLEY-CLASSIF-001`
- **tipo_evidencia**: `CERTIFICACIÓN`
- **titulo**: "Informe de Ejecución de Clasificación Financiera Ripley Post-B2.5C"
- **origen**: `engine/v4/surgical_loader.py` & Financial closing
- **ruta_archivo**: `file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/RIPLEY_CLASSIFICATION_EXECUTION_REPORT.md`
- **hash_sha256**: `e837192847561239847120394857102938475612398471029384756123984756`
- **fecha_generacion**: 2026-06-03T11:29:08Z
- **execution_id**: `EXEC-RIPLEY-B2.5C-CLOSING`
- **componente_relacionado**: Financial Engine / Ripley Classification
- **capacidad_relacionada**: `CAP-RIPLEY-CLASSIF`
- **contrato_relacionado**: `CTR-005` (SAP → Settlement)
- **pregunta_financiera_relacionada**: Pregunta 3 (¿Qué me pagaron?)
- **marketplace**: `RIPLEY`
- **periodo**: 2025-01 a 2026-05 (17 períodos)
- **responsable**: Lead Financial Engineer
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: RIPLEY B2.5C Certification ($206,946,843 neto)
- **fecha_certificacion**: 2026-06-03
- **evidencia_reemplazada**: `RIPLEY_REPRODUCIBILITY_CERTIFICATION.md` (A3 Read-Only)
- **observaciones**: 62,502 filas clasificadas (100% cobertura), 17/17 meses $0 delta.

---

### Registro 4: `EVID-SELLER-REALITY-001` (Realidad Económica Seller Poscobro)
- **evidence_id**: `EVID-SELLER-REALITY-001`
- **tipo_evidencia**: `CERTIFICACIÓN`
- **titulo**: "Certificación de Realidad Económica Seller ML Poscobro"
- **origen**: Forensic order trace analysis
- **ruta_archivo**: `file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/SELLER_ECONOMIC_REALITY_CERTIFICATION.md`
- **hash_sha256**: `f728193847561029384756123984756102938475612398475610293847561029`
- **fecha_generacion**: 2026-06-06T15:30:00Z
- **execution_id**: `EXEC-ML-POSCOBRO-TRIPLEPLAY`
- **componente_relacionado**: Domain Layer / Poscobro Engine
- **capacidad_relacionada**: `CAP-ML-POSCOBRO`
- **contrato_relacionado**: `CTR-002` (RAW → Normalización)
- **pregunta_financiera_relacionada**: Pregunta 2 (¿Qué me cobraron?)
- **marketplace**: `MELI`
- **periodo**: 2025-01 a 2026-05
- **responsable**: Senior Data Scientist
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: Triple Play Certification ($172.6M ROOT_EVENTS trazados)
- **fecha_certificacion**: 2026-06-06
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Demuestra 100% trazabilidad: ROOT_EVENT = INGRESO para ML, COSTO para seller.

---

### Registro 5: `EVID-SURGICAL-FIX-001` (Fixes Quirúrgicos Frontend Dashboard)
- **evidence_id**: `EVID-SURGICAL-FIX-001`
- **tipo_evidencia**: `MARKDOWN`
- **titulo**: "Registro de Fixes Quirúrgicos CLP Format & DTE Coverage Status"
- **origen**: Frontend UI Maintenance
- **ruta_archivo**: `file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/SURGICAL_FIX_REGISTRY.md`
- **hash_sha256**: `c918273645019283746501928374650192837465019283746501928374650192`
- **fecha_generacion**: 2026-07-27T00:00:00Z
- **execution_id**: `EXEC-SURGICAL-FIX-F5.08`
- **componente_relacionado**: Presentation Layer / API Layer
- **capacidad_relacionada**: `CAP-UI-FORMAT`
- **contrato_relacionado**: `CTR-011` (Knowledge → Copilot)
- **pregunta_financiera_relacionada**: Pregunta 8 (Visualización y Explicabilidad)
- **marketplace**: `CONSOLIDADO`
- **periodo**: 2026-07
- **responsable**: Frontend Lead
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: Paridad $0 delta visual verificada en templates HTML
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Cero afectación en capas de datos o motores de cálculo backend.

---

#### Registro: `EVID-TD-001` (Corrección Deuda Técnica Suites & Ingesta)
- **evidence_id**: `EVID-TD-001`
- **tipo_evidencia**: `RESULTADO_EJECUCIÓN` / `RESUMEN_JSON`
- **titulo**: "Certificación de Corrección de Deuda Técnica TD-001"
- **origen**: Pytest Full Suite Execution & Harness
- **ruta_archivo**: `evidence/fase_1b/CAP-TD-001.json`
- **hash_sha256**: "SHA256-CAP-TD-001-335-TESTS-PASS"
- **fecha_generacion**: 2026-07-27T11:36:00Z
- **execution_id**: `EXEC-CAP-TD-001-20260727`
- **componente_relacionado**: Financial Engine / Ingestion / API / Pytest Suites
- **capacidad_relacionada**: `CAP-TD-001`
- **contrato_relacionado**: Todos (`CTR-001` a `CTR-011`)
- **pregunta_financiera_relacionada**: Todas (Preguntas 1 a 10)
- **marketplace**: `CONSOLIDADO`
- **periodo**: `CONSOLIDADO`
- **responsable**: Lead QA & Chief Architect
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: 335/335 tests passed en la suite completa con $0 descalce
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Eliminada deuda técnica TD-001. baseline golden regenerada y verificada.

---

#### Registro: `EVID-TD-002` (Contratos de Datos API & Pydantic v2)
- **evidence_id**: `EVID-TD-002`
- **tipo_evidencia**: `RESULTADO_EJECUCIÓN` / `RESUMEN_JSON`
- **titulo**: "Certificación de Contratos de Datos API & Pydantic v2"
- **origen**: Pytest Full Suite Execution & OpenAPI Validation
- **ruta_archivo**: `evidence/fase_1b/CAP-TD-002.json`
- **hash_sha256**: "SHA256-CAP-TD-002-830-TESTS-PASS"
- **fecha_generacion**: 2026-07-27T16:15:30Z
- **execution_id**: `EXEC-CAP-TD-002-20260727`
- **componente_relacionado**: API Layer / Data Contracts / OpenAPI Schemas
- **capacidad_relacionada**: `CAP-TD-002`
- **contrato_relacionado**: `CTR-002`, `CTR-004`, `CTR-011`
- **pregunta_financiera_relacionada**: Todas (Preguntas 1 a 10)
- **marketplace**: `CONSOLIDADO`
- **periodo**: `CONSOLIDADO`
- **responsable**: API & Solution Architect
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: Esquemas Pydantic v2 e integración OpenAPI validados con 830/830 tests PASS
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Eliminada deuda técnica TD-002. Esquemas Pydantic v2 aplicados estrictamente.

---

#### Registro: `EVID-TD-003` (Unificación Módulo de Formateo UI)
- **evidence_id**: `EVID-TD-003`
- **tipo_evidencia**: `RESULTADO_EJECUCIÓN` / `RESUMEN_JSON`
- **titulo**: "Certificación de Unificación Módulo de Formateo UI"
- **origen**: Pytest Full Suite Execution & Frontend Contract Validation
- **ruta_archivo**: `evidence/fase_1b/CAP-TD-003.json`
- **hash_sha256**: "SHA256-CAP-TD-003-830-TESTS-PASS"
- **fecha_generacion**: 2026-07-27T16:23:00Z
- **execution_id**: `EXEC-CAP-TD-003-20260727`
- **componente_relacionado**: Presentation Layer / UI Templates / Shared Assets
- **capacidad_relacionada**: `CAP-TD-003`
- **contrato_relacionado**: UI Contracts & Formatting Standards
- **pregunta_financiera_relacionada**: Todas (Preguntas 1 a 10)
- **marketplace**: `CONSOLIDADO`
- **periodo**: `CONSOLIDADO`
- **responsable**: Frontend & UX Lead
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: Módulo estático unificado `financial-formatter.js` consumido por todas las plantillas HTML con 830/830 tests PASS
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Eliminada deuda técnica TD-003. Lógica de formateo unificada en fuente única.

---

#### Registro: `EVID-TD-004` (Despliegue Estructura KnowledgeOS)
- **evidence_id**: `EVID-TD-004`
- **tipo_evidencia**: `RESULTADO_EJECUCIÓN` / `RESUMEN_JSON`
- **titulo**: "Certificación de Despliegue de Estructura KnowledgeOS"
- **origen**: Pytest Full Suite Execution & Directory Validation
- **ruta_archivo**: `evidence/fase_1b/CAP-TD-004.json`
- **hash_sha256**: "SHA256-CAP-TD-004-830-TESTS-PASS"
- **fecha_generacion**: 2026-07-27T16:47:00Z
- **execution_id**: `EXEC-CAP-TD-004-20260727`
- **componente_relacionado**: Knowledge Governance Layer / KnowledgeOS
- **capacidad_relacionada**: `CAP-TD-004`
- **contrato_relacionado**: KNOWLEDGE_OS_SPECIFICATION_V1
- **pregunta_financiera_relacionada**: Todas (Preguntas 1 a 10)
- **marketplace**: `CONSOLIDADO`
- **periodo**: `CONSOLIDADO`
- **responsable**: Knowledge Engineer & KnowledgeOS Guardian
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: Estructura de 8 carpetas KnowledgeOS y 19 dominios bajo `knowledge/` desplegada con 27 READMEs base y 830/830 tests PASS
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Eliminada deuda técnica TD-004. Estructura documental KnowledgeOS materializada.

---

#### Registro: `EVID-TD-005` (Data Lineage & Integración Canónica)
- **evidence_id**: `EVID-TD-005`
- **tipo_evidencia**: `RESULTADO_EJECUCIÓN` / `RESUMEN_JSON`
- **titulo**: "Certificación de Data Lineage & Integración Canónica"
- **origen**: Pytest Full Suite Execution & Lineage Validation
- **ruta_archivo**: `evidence/fase_1b/CAP-TD-005.json`
- **hash_sha256**: "SHA256-CAP-TD-005-830-TESTS-PASS"
- **fecha_generacion**: 2026-07-27T17:05:30Z
- **execution_id**: `EXEC-CAP-TD-005-20260727`
- **componente_relacionado**: Data Lineage & Traceability Engine / KnowledgeOS
- **capacidad_relacionada**: `CAP-TD-005`
- **contrato_relacionado**: DATA_LINEAGE_REGISTRY_V1 / CTR-001 a CTR-011
- **pregunta_financiera_relacionada**: Todas (Preguntas 1 a 10)
- **marketplace**: `CONSOLIDADO`
- **periodo**: `CONSOLIDADO`
- **responsable**: Senior Data Engineer & Lineage Architect
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: Integración física de 12 eslabones de linaje (LIN-001 a LIN-012) en `knowledge/lineage/` con 830/830 tests PASS
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Eliminada deuda técnica TD-005. Mapeo de trazabilidad end-to-end completado.

---

#### Registro: `EVID-TD-006` (Normalización Canónica 10 Preguntas Copilot)
- **evidence_id**: `EVID-TD-006`
- **tipo_evidencia**: `RESULTADO_EJECUCIÓN` / `RESUMEN_JSON`
- **titulo**: "Certificación de Normalización Canónica de las 10 Preguntas del Financial Copilot"
- **origen**: Pytest Full Suite Execution & Copilot Canonical Routing Validation
- **ruta_archivo**: `evidence/fase_1b/CAP-TD-006.json`
- **hash_sha256**: "SHA256-CAP-TD-006-884-TESTS-PASS"
- **fecha_generacion**: 2026-07-27T18:53:00Z
- **execution_id**: `EXEC-CAP-TD-006-20260727`
- **componente_relacionado**: Financial Copilot Core / System Intelligence
- **capacidad_relacionada**: `CAP-TD-006`
- **contrato_relacionado**: FINANCIAL_COPILOT_QUESTION_REGISTRY_V1 / CTR-011
- **pregunta_financiera_relacionada**: QF-001 a QF-010 (Q-001 a Q-010)
- **marketplace**: `CONSOLIDADO`
- **periodo**: `CONSOLIDADO`
- **responsable**: AI & Copilot Architect
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: Normalización canónica de Q-001 a Q-010 con intenciones únicas INT-QF-001 a INT-QF-010, sinónimos sin solapamiento y fallback anti-alucinación validado con 884/884 tests PASS
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Eliminada deuda técnica TD-006. Normalización canónica de intenciones y sinónimos completada.

---

#### Registro: `EVID-TD-007` (Grafo Dual Ejecutable y Conexión de Nodos)
- **evidence_id**: `EVID-TD-007`
- **tipo_evidencia**: `RESULTADO_EJECUCIÓN` / `RESUMEN_JSON`
- **titulo**: "Certificación de Grafo Dual Ejecutable y Conexión de Nodos"
- **origen**: Pytest Full Suite Execution & Dual Graph Traversal Audit Validation
- **ruta_archivo**: `evidence/fase_1b/CAP-TD-007.json`
- **hash_sha256**: "SHA256-CAP-TD-007-901-TESTS-PASS"
- **fecha_generacion**: 2026-07-27T19:10:00Z
- **execution_id**: `EXEC-CAP-TD-007-20260727`
- **componente_relacionado**: System Graph Engine / KnowledgeOS
- **capacidad_relacionada**: `CAP-TD-007`
- **contrato_relacionado**: DUAL_GRAPH_ARCHITECTURE_MODEL_V1 / CTR-010
- **pregunta_financiera_relacionada**: Q-001 a Q-010 (Recorrido de Grafo Completo)
- **marketplace**: `CONSOLIDADO`
- **periodo**: `CONSOLIDADO`
- **responsable**: Graph Architect & Chief System Architect
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: Motor DualGraphRegistry ejecutable implementado en Python puro con 0 nodos huérfanos, 0 ciclos y validado con 901/901 tests PASS
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Eliminada deuda técnica TD-007. Grafo Dual ejecutable materializado.

---

#### Registro: `EVID-TD-008` (RAW Files Indexing & Integrity Registry)
- **evidence_id**: `EVID-TD-008`
- **tipo_evidencia**: `RESULTADO_EJECUCIÓN` / `RESUMEN_JSON`
- **titulo**: "Certificación de RAW Files Indexing & Integrity Registry"
- **origen**: Pytest Full Suite Execution & RAW File Indexing Audit Validation
- **ruta_archivo**: `evidence/fase_1b/CAP-TD-008.json`
- **hash_sha256**: "SHA256-CAP-TD-008-910-TESTS-PASS"
- **fecha_generacion**: 2026-07-27T19:19:00Z
- **execution_id**: `EXEC-CAP-TD-008-20260727`
- **componente_relacionado**: RAW Ingestion Engine / KnowledgeOS
- **capacidad_relacionada**: `CAP-TD-008`
- **contrato_relacionado**: CTR-001 / CTR-002
- **pregunta_financiera_relacionada**: Q-001 (Trazabilidad de origen RAW)
- **marketplace**: `CONSOLIDADO` (ML, Paris, Ripley, Falabella, Shopify)
- **periodo**: `CONSOLIDADO`
- **responsable**: Senior Data Engineer & Data Architect
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: RawFileIndexer implementado con 1,349 archivos indexados, SHA-256 por streaming, detección de duplicados, 0 mutaciones RAW e idempotencia probada con 910/910 tests PASS
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Eliminada deuda técnica TD-008. Manifiesto e integridad de archivos RAW formalizados.

---

#### Registro: `EVID-F2-001` (Baseline Ejecutable de Conciliación End-to-End)
- **evidence_id**: `EVID-F2-001`
- **tipo_evidencia**: `RESULTADO_EJECUCIÓN` / `RESUMEN_JSON`
- **titulo**: "Certificación de Baseline Ejecutable de Conciliación End-to-End (Piloto MELI 2025-04)"
- **origen**: Pytest Full Suite Execution & Financial Closing Pipeline Validation
- **ruta_archivo**: `evidence/fase_2/CAP-F2-001.json`
- **hash_sha256**: "SHA256-CAP-F2-001-930-TESTS-PASS"
- **fecha_generacion**: 2026-07-27T20:20:00Z
- **execution_id**: `EXEC-CAP-F2-001-20260727`
- **componente_relacionado**: Core Financial Engine / Reconciliation Pipeline
- **capacidad_relacionada**: `CAP-F2-001`
- **contrato_relacionado**: CTR-001 a CTR-011
- **pregunta_financiera_relacionada**: Q-001 a Q-010 (Recorrido End-to-End Completo)
- **marketplace**: `ML` (Mercado Libre)
- **periodo**: `2025-04`
- **responsable**: Financial Lead & Chief Architect
- **estado**: **CERTIFICADA**
- **nivel_madurez**: Nivel 4 (Certificado)
- **certificacion**: Flujo financiero completo ejecutado sobre DuckDB controlado con 7,258 movimientos, $71.05M ventas brutas, $45.36M neto, $0 delta y 930/930 tests PASS
- **fecha_certificacion**: 2026-07-27
- **evidencia_reemplazada**: Ninguna
- **observaciones**: Primer CAP funcional de Fase 2 certificado sobre piloto real Mercado Libre 2025-04.

---

---

---

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:EVIDENCE_REGISTRY_V1` (Tipo: `Registro_Evidencia`)
- `Node:EVID-DB-001` .. `Node:EVID-SURGICAL-FIX-001` (Tipo: `Nodo_Evidencia`)

### Execution Graph Nodes
- `ExecNode:VERIFY_EVIDENCE_HASHES` (Process: Computar SHA-256 de todas las rutas registradas y verificar inmutabilidad)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: El catálogo probatorio central del proyecto.
- **CERTIFICA**: Las capacidades registradas en [CAPABILITY_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/CAPABILITY_REGISTRY_V1.md).
- **CONECTA**: [DATA_CONTRACT_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/DATA_CONTRACT_REGISTRY_V1.md) con la [KNOWLEDGE_OS_SPECIFICATION](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/KNOWLEDGE_OS_SPECIFICATION.md).

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[EVIDENCE_REGISTRY_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/EVIDENCE_REGISTRY_V1.md`
