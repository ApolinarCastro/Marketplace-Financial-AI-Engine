---
id: END_TO_END_RECONCILIATION_ROADMAP_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Lead Financial Engineer & PMO Lead
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - ARCHITECTURE_REGISTRY_V1
  - DATA_CONTRACT_REGISTRY_V1
  - EVIDENCE_REGISTRY_V1
  - SYSTEM_INTELLIGENCE_SPECIFICATION_V1
relacionado_con:
  - PMO_REGISTRY_V1
  - MATURITY_REGISTRY_V1
  - FINANCIAL_COPILOT_QUESTION_REGISTRY_V1
---

# HOJA DE RUTA OFICIAL DE CONCILIACIÓN INTEGRAL Y COPILOT V1

## Propósito
Establecer la hoja de ruta estratégica y técnica oficial para transformar el **Marketplace Financial AI Engine** en una plataforma de Inteligencia Financiera integral. Define la cadena oficial de 13 etapas desde la ingesta en Marketplace hasta la respuesta certificada del Financial Copilot.

---

## Cadena Oficial de Conciliación Integral (13 Etapas)

```text
Marketplace (Etapa 1) ──> RAW (Etapa 2) ──> Normalización (Etapa 3) ──> XML/DTE (Etapa 4)
        ──> SAP (Etapa 5) ──> Settlement (Etapa 6) ──> Pago (Etapa 7) ──> Banco (Etapa 8)
        ──> Ledger (Etapa 9) ──> Evidence (Etapa 10) ──> Knowledge (Etapa 11)
        ──> System Intelligence (Etapa 12) ──> Financial Copilot (Etapa 13)
```

---

## Especificación Detallada por Etapa (Section 10.3 & 10.4)

### Etapa 1: Marketplace (Fuentes Oficiales)
- **Objetivo**: Conectar y registrar las fuentes de origen por marketplace (Mercado Libre, Falabella, Paris, Ripley).
- **Origen**: APIs públicas / Portales de Seller.
- **Destino**: `01_Raw/<MARKETPLACE>/`.
- **Entradas**: Archivos CSV, XLSX, XML y JSON de transacciones.
- **Salidas**: Archivos descargados con manifiesto de ingesta.
- **Owner**: Marketplace Data Engineer | **Contrato**: `CTR-001`.
- **Validaciones**: Hash SHA-256 no modificado; verificación de headers.
- **Evidencia**: `EVID-RAW-001` .. `004`.
- **Estado Actual**: **VALIDADO** | **Madurez**: Nivel 3 (Validado).
- **Dependencias**: Ninguna | **Bloqueadores**: Inestabilidad de APIs de MP.
- **Preguntas Habilitadas**: Base para Preguntas 1 a 10.

---

### Etapa 2: RAW (Persistencia Inmutable)
- **Objetivo**: Almacenar los archivos fuentes en almacenamiento inmutable respaldado por firmas hash.
- **Origen**: Etapa 1.
- **Destino**: Directorio `01_Raw/` con permisos Read-Only.
- **Entradas**: Archivos en disco.
- **Salidas**: Registro de auditoría con SHA-256 e inmutabilidad verificada.
- **Owner**: Data Infrastructure Specialist | **Contrato**: `CTR-001`.
- **Validaciones**: Prohibición de sobrescritura o edición manual.
- **Evidencia**: Manifiesto de Hashes SHA-256.
- **Estado Actual**: **CERTIFICADO** | **Madurez**: Nivel 4 (Certificado).
- **Preguntas Habilitadas**: Trazabilidad legal para Preguntas 1 a 10.

---

### Etapa 3: Normalización (Staging DuckDB)
- **Objetivo**: Estandarizar estructuras heterogéneas de marketplaces a tablas relacionales DuckDB.
- **Origen**: Etapa 2.
- **Destino**: Tablas de staging (`stg_marketplace_raw`).
- **Entradas**: CSV/XLSX cargados por loaders quirúrgicos.
- **Salidas**: Filas normalizadas en DuckDB con `dayfirst=True` verificado.
- **Owner**: Senior Data Engineer | **Contrato**: `CTR-002`.
- **Validaciones**: `pd.to_datetime(dayfirst=True)`; coerción estricta de tipos.
- **Evidencia**: `EVID-DB-001` (DB Hash `311c78e...`).
- **Estado Actual**: **CERTIFICADO** | **Madurez**: Nivel 4 (Certificado).
- **Preguntas Habilitadas**: Pregunta 1 (Ventas) y Pregunta 2 (Cobros).

---

### Etapa 4: XML / DTE (Documentos Tributarios Electrónicos)
- **Objetivo**: Indexar y conciliar XMLs DTE SII (facturas, notas de crédito) contra ventas de marketplace.
- **Origen**: `01_Raw/XML/` y SII DTEs.
- **Destino**: `engine/v4/dte_indexer.py` & `stg_dte_sii`.
- **Entradas**: Archivos XML SII DTE 33, 43, 52, 61.
- **Salidas**: Cobertura DTE por folio y RUT emisor/receptor.
- **Owner**: DTE & Tax Specialist | **Contrato**: `CTR-003`.
- **Validaciones**: Validez de RUT; `monto_total == neto + iva`.
- **Evidencia**: Reports de Cobertura DTE Paris y Ripley.
- **Estado Actual**: **VALIDADO** | **Madurez**: Nivel 3 (Validado - Cobertura Paris 82.6%).
- **Preguntas Habilitadas**: Pregunta 6 (¿Qué XML/DTE respalda la operación?).

---

### Etapa 5: SAP (Integración ERP Contable)
- **Objetivo**: Relacionar órdenes, facturas, notas de crédito y saldos contables del ERP SAP.
- **Origen**: BAPIs / IDocs / Extracciones SAP.
- **Destino**: `stg_sap_accounting_doc`.
- **Entradas**: Documentos de contabilidad SAP (Sociedad, Ejercicio, Cuenta).
- **Salidas**: Asientos contables conciliados con DTE y Marketplace.
- **Owner**: SAP Integration Specialist | **Contrato**: `CTR-004`.
- **Validaciones**: Partida doble `sum(debe) == sum(haber)`.
- **Evidencia**: Registros SAP auditados.
- **Estado Actual**: **ESPECIFICADO** | **Madurez**: Nivel 1 (Especificado - Fase 5).
- **Preguntas Habilitadas**: Pregunta 7 (¿Qué registro SAP respalda la operación?).

---

### Etapa 6: Settlement (Liquidaciones Marketplace)
- **Objetivo**: Interpretar liquidaciones, comisiones, cargos logísticos, descuentos y abonos.
- **Origen**: Informes de liquidación y abonos.
- **Destino**: `marketplace_liquidaciones_v1`.
- **Entradas**: Movimientos de liquidación por marketplace.
- **Salidas**: Neto liquidado conciliado por período.
- **Owner**: Settlement Specialist | **Contrato**: `CTR-005`.
- **Validaciones**: `neto_liquidado == bruto - comisiones - descuentos + abonos`.
- **Evidencia**: `EVID-RIPLEY-CLASSIF-001` ($206.9M neto).
- **Estado Actual**: **CERTIFICADO** | **Madurez**: Nivel 4 (Certificado - Ripley/ML/Paris/Falabella).
- **Preguntas Habilitadas**: Pregunta 9 (Cargos u ocultos) y Pregunta 3 (¿Qué me pagaron?).

---

### Etapa 7: Pago (Liberaciones y Transferencias)
- **Objetivo**: Identificar órdenes de pago emitidas por marketplaces hacia la empresa.
- **Origen**: Archivos de liberaciones / TEF de marketplaces.
- **Destino**: `stg_pago_origen`.
- **Entradas**: Identificadores de transferencia bancaria y montos.
- **Salidas**: Transacciones de pago conciliadas con liquidaciones.
- **Owner**: Treasury Specialist | **Contrato**: `CTR-006`.
- **Validaciones**: Match 1:1 con `monto_neto_liquidado`.
- **Evidencia**: Liberaciones ML & Ripley conciliadas.
- **Estado Actual**: **VALIDADO** | **Madurez**: Nivel 3 (Validado).
- **Preguntas Habilitadas**: Pregunta 3 (¿Qué me pagaron?) y Pregunta 4 (¿Qué falta por cobrar?).

---

### Etapa 8: Banco (Cartolas y Depósitos Bancarios)
- **Objetivo**: Reconciliar transferencias de marketplace contra cartola bancaria oficial.
- **Origen**: Cartolas bancarias oficiales (Banco de Chile, Santander, BCI).
- **Destino**: `stg_cartola_bancaria`.
- **Entradas**: Movimientos de abono bancario.
- **Salidas**: Depósitos conciliados en la cuenta corriente corporativa.
- **Owner**: Bank Reconciliation Specialist | **Contrato**: `CTR-007`.
- **Validaciones**: Cuadratura de saldos bancarios $0 delta.
- **Evidencia**: Cartolas bancarias conciliadas.
- **Estado Actual**: **ESPECIFICADO** | **Madurez**: Nivel 1 (Especificado - Fase 7).
- **Preguntas Habilitadas**: Pregunta 8 (¿Qué movimiento bancario respalda el pago?).

---

### Etapa 9: Ledger (Consolidación de Verdad Financiera)
- **Objetivo**: Consolidar la verdad financiera corporativa inmutable de doble entrada.
- **Origen**: Etapas 3, 6 y 8.
- **Destino**: `marketplace_ledger_v1` y `marketplace_cierre_financiero_v1`.
- **Entradas**: Transacciones clasificadas en los 96 conceptos canónicos.
- **Salidas**: Cierre financiero de Resultado Neto con paridad $0 delta.
- **Owner**: Single Financial Truth Guardian | **Contrato**: `CTR-008`.
- **Validaciones**: 69/69 períodos sin descalce monetario.
- **Evidencia**: `EVID-DB-001`.
- **Estado Actual**: **PRODUCTIVO** | **Madurez**: Nivel 5 (Productivo).
- **Preguntas Habilitadas**: Pregunta 10 (¿Cuál es el margen financiero real?).

---

### Etapa 10: Evidence (ConstrucciónProbatoria Reproducible)
- **Objetivo**: Construir soporte de auditoría reproducible con metadatos y hashes inmutables.
- **Origen**: Etapa 9 y Harness `validate_fase_1b.py`.
- **Destino**: Archivos en `evidence/fase_1b/`.
- **Entradas**: Registros de cierre y logs de ejecución.
- **Salidas**: `summary.json` y reportes de certificación Nivel 1/2.
- **Owner**: Evidence Guardian | **Contrato**: `CTR-009`.
- **Validaciones**: Presencia obligatoria de `execution_id`, commit y SHA-256.
- **Evidencia**: `EVID-HARNESS-001`.
- **Estado Actual**: **CERTIFICADO** | **Madurez**: Nivel 4 (Certificado).
- **Preguntas Habilitadas**: Explicabilidad para todas las preguntas.

---

### Etapa 11: Knowledge (Transformación en Conocimiento Canónico)
- **Objetivo**: Consolidar la información de auditoría en registros canónicos de KnowledgeOS.
- **Origen**: Etapa 10.
- **Destino**: `KnowledgeOS/01_Canonical/` y `02_Governance/`.
- **Entradas**: Especificaciones en Markdown y registros de gobierno.
- **Salidas**: Estructura de conocimiento navegable e inmutable.
- **Owner**: Knowledge Engineer | **Contrato**: `CTR-010`.
- **Validaciones**: Header Universal normalizado; wikilinks validados.
- **Evidencia**: `KNOWLEDGE_OS_SPECIFICATION.md`.
- **Estado Actual**: **ESPECIFICADO** | **Madurez**: Nivel 1 (Especificado - Fase 2).
- **Preguntas Habilitadas**: Soporte de contexto para System Intelligence.

---

### Etapa 12: System Intelligence (Orquestación Semántica y Grafos)
- **Objetivo**: Resolver preguntas complejas mediante traversal de grafos duales, validación de contratos y RAG.
- **Origen**: Etapas 10 y 11 (Dual Graph Layer).
- **Destino**: System Intelligence Engine.
- **Entradas**: Consultas estructuradas e Intent IDs.
- **Salidas**: Contexto certificado, cita probatoria y score de confianza.
- **Owner**: AI & Copilot Architect | **Contrato**: `CTR-011`.
- **Validaciones**: Hallucination Guard `PASS`; Fallback Handler activo ante evidencia nula.
- **Evidencia**: `SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md`.
- **Estado Actual**: **ESPECIFICADO** | **Madurez**: Nivel 1 (Especificado).
- **Preguntas Habilitadas**: Motor ejecutor para Preguntas 1 a 10.

---

### Etapa 13: Financial Copilot (Interfaz Trazable Certificada)
- **Objetivo**: Presentar respuestas financieras certificadas, explicables y sin alucinaciones al usuario ejecutivo.
- **Origen**: Etapa 12.
- **Destino**: Usuario Final / Dashboard Gerencial.
- **Entradas**: Preguntas del usuario en lenguaje natural.
- **Salidas**: Respuestas Markdown con cifras $0 delta, tablas justificativas y enlaces a evidencias.
- **Owner**: Lead Product TPO | **Contrato**: `CTR-011`.
- **Validaciones**: Cumplimiento de la Regla de Oro del Proyecto.
- **Evidencia**: `FINANCIAL_COPILOT_QUESTION_REGISTRY_V1.md`.
- **Estado Actual**: **ESPECIFICADO** | **Madurez**: Nivel 1 (Especificado - Fase 8).
- **Preguntas Habilitadas**: Respuestas certificadas de las 10 Preguntas Estratégicas.

---

## Mapeo de las 10 Preguntas Financieras Estratégicas (Section 10.5)

| N° | Pregunta Financiera | Etapas Requeridas | Contratos Requeridos | Evidencias Requeridas | Madurez Actual | Criterio de Certificación |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **1** | **¿Qué vendí?** | Etapas 1 a 3, 9, 10, 12, 13 | `CTR-001`, `CTR-002`, `CTR-008` | `EVID-DB-001` | **Nivel 4 (Certificado)** | 69/69 períodos $0 delta en Ventas |
| **2** | **¿Qué me cobraron?** | Etapas 1 a 3, 6, 9, 10, 12, 13 | `CTR-001`, `CTR-002`, `CTR-005` | `EVID-SELLER-REALITY-001` | **Nivel 4 (Certificado)** | Desglose $172.6M ROOT_EVENTS verificado |
| **3** | **¿Qué me pagaron?** | Etapas 1 a 3, 6, 7, 9, 10, 12, 13 | `CTR-005`, `CTR-006`, `CTR-008` | `EVID-RIPLEY-CLASSIF-001` | **Nivel 4 (Certificado)** | 17/17 meses $206.9M neto Ripley conciliado |
| **4** | **¿Qué falta por cobrar?** | Etapas 1 a 7, 9, 10, 12, 13 | `CTR-005`, `CTR-006` | Liquidaciones de Cobro | **Nivel 3 (Validado)** | Saldo pendiente por MP cuadrado contra ledger |
| **5** | **¿Qué devolvieron?** | Etapas 1 a 3, 9, 10, 12, 13 | `CTR-001`, `CTR-002`, `CTR-008` | `EVID-DB-001` | **Nivel 4 (Certificado)** | 69/69 períodos $0 delta en Devoluciones |
| **6** | **¿Qué XML/DTE respalda la op.?** | Etapas 1 a 4, 10, 12, 13 | `CTR-003` | Informes Cobertura DTE | **Nivel 3 (Validado)** | Match folio DTE vs transacción de venta |
| **7** | **¿Qué registro SAP respalda?** | Etapas 1 a 5, 10, 12, 13 | `CTR-004` | Asientos SAP ERP | **Nivel 1 (Especificado)** | Enlace Asiento SAP ↔ Folio DTE |
| **8** | **¿Qué mov. bancario respalda?** | Etapas 1 a 8, 10, 12, 13 | `CTR-007` | Cartola Bancaria Oficial | **Nivel 1 (Especificado)** | Match TEF ↔ Registro Cartola |
| **9** | **¿Qué cargo o desc. está oculto?** | Etapas 1 a 6, 9, 10, 12, 13 | `CTR-002`, `CTR-005` | Desglose Cobros 96 conceptos | **Nivel 4 (Certificado)** | Trazabilidad 100% de abonos y descuentos |
| **10** | **¿Cuál es el margen real?** | Etapas 1 a 13 (Todas) | `CTR-001` a `CTR-011` | Cierre Resultado Neto | **Nivel 4 (Certificado)** | Margen Neto por MP respaldado $0 delta |

---

## Secuencia Maestra Oficial de Fases del Proyecto (Section 10.6)

```text
FASE 0 — Gobierno y Arquitectura (FASE ACTUAL)
        ↓
FASE 1 — Corrección de Deuda Técnica (TD-001 a TD-008)
        ↓
FASE 2 — KnowledgeOS + Dual Graph + Inventario
        ↓
FASE 3 — Contratos de Datos (CTR-001 a CTR-011)
        ↓
FASE 4 — Conciliación XML / DTE (SII DTE Indexer)
        ↓
FASE 5 — Conciliación SAP ERP
        ↓
FASE 6 — Liquidaciones & Pagos Marketplace
        ↓
FASE 7 — Conciliación Bancaria (Cartolas)
        ↓
FASE 8 — Financial Copilot Certificado
```

---

## Escala Oficial de Nivel de Madurez (Section 10.7)

- **Nivel 0 (Idea)**: Concepto en roadmap sin especificación formal.
- **Nivel 1 (Especificado)**: Documentado con Header Universal y Contratos en `governance/`.
- **Nivel 2 (Implementado)**: Código escrito y ejecutable en `engine/` o `api/`.
- **Nivel 3 (Validado)**: Pruebas automatizadas pytest `PASS`.
- **Nivel 4 (Certificado)**: Evidencia reproducible con `execution_id`, SHA-256 y 3 clean runs.
- **Nivel 5 (Productivo)**: Operación congelada en producción sin regresión ($0 delta).

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:END_TO_END_RECONCILIATION_ROADMAP_V1` (Tipo: `Hoja_Ruta_Maestra`)
- `Node:ETAPA_1` .. `Node:ETAPA_13` (Tipo: `Etapa_Conciliacion`)

### Execution Graph Nodes
- `ExecNode:VERIFY_ROADMAP_PROGRESS` (Process: Evaluación del avance real por etapa y nivel de madurez en el PMO)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: El roadmap maestro y la secuencia oficial de desarrollo Fase 0 a Fase 8.
- **VINCULA**: Las 10 Preguntas Financieras Estratégicas con las 13 Etapas de conciliación.
- **AFECTA**: Todos los entregables del proyecto.

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[END_TO_END_RECONCILIATION_ROADMAP_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/END_TO_END_RECONCILIATION_ROADMAP_V1.md`
