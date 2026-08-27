---
id: DATA_CONTRACT_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Data Architect & Financial Data Engineer
ultima_revision: 2026-07-27
dependencias: [EXECUTION_PLAN_PHASE_0_FOUNDATION_V3, ARCHITECTURE_REGISTRY_V1]
relacionado_con: [PMO_REGISTRY_V1, DUAL_GRAPH_ARCHITECTURE_MODEL_V1, EVIDENCE_REGISTRY_V1]
---

# REGISTRO MAESTRO DE CONTRATOS DE DATOS V1

## Propósito
Establecer la especificación formal e inmutable de los **Contratos de Datos (Data Contracts)** para las 11 interfaces que conforman la cadena completa de conciliación financiera del **Marketplace Financial AI Engine**. Garantiza compatibilidad hacia atrás, integridad referencial y cero ambigüedad en el flujo de información desde archivos fuente hasta el Financial Copilot.

---

## Cadena de Contratos Financieros End-to-End

```
Marketplace (CTR-001) → RAW (CTR-002) → Normalización (CTR-003) → XML (CTR-004) → SAP 
(CTR-005) → Settlement (CTR-006) → Pago (CTR-007) → Banco (CTR-008) → Ledger 
(CTR-009) → Evidence (CTR-010) → Knowledge (CTR-011) → Copilot
```

---

## Registro Canónico de Contratos de Datos (11 Contratos)

### Contrato 1: `CTR-001` (Marketplace → RAW)
- **ID**: `CTR-001`
- **Origen**: Portales / APIs de Marketplace (Mercado Libre, Falabella, Paris, Ripley).
- **Destino**: Directorio inmutable `01_Raw/<MARKETPLACE>/`.
- **Campos Obligatorios**: `fecha_ingesta`, `nombre_archivo_original`, `contenido_bytes`, `marketplace_id`, `hash_sha256_origen`.
- **Campos Opcionales**: `metadata_peticion_http`, `folio_descarga`.
- **Reglas de Validación**: Inmutabilidad absoluta tras escritura; hash SHA-256 no modificable; extensión válida (`.csv`, `.xlsx`, `.xml`, `.json`).
- **Owner**: Marketplace Data Engineer.
- **Versión**: `1.0.0`
- **Política de Cambios**: Aditiva estricta. Nunca sobrescribir ni modificar archivos RAW existentes.
- **Compatibilidad Hacia Atrás**: 100% Garantizada por conservación de RAW original.
- **Estado de Certificación**: **CERTIFICADO**

---

### Contrato 2: `CTR-002` (RAW → Normalización)
- **ID**: `CTR-002`
- **Origen**: Directorio `01_Raw/`.
- **Destino**: Tablas de staging en DuckDB (`stg_marketplace_raw`).
- **Campos Obligatorios**: `raw_id`, `marketplace`, `fecha_evento`, `monto_original`, `concepto_raw`, `orden_id`.
- **Campos Opcionales**: `sku`, `comercio_id`, `retencion_monto`.
- **Reglas de Validación**: `fecha_evento` parseada obligatoriamente con `dayfirst=True`; `monto_original` numérico no nulo; `raw_id` único por fila.
- **Owner**: Senior Data Engineer.
- **Versión**: `1.0.0`
- **Política de Cambios**: Versionado de parsers por marketplace. No alterar columnas preexistentes.
- **Compatibilidad Hacia Atrás**: Mapeos legacy conservados en `surgical_loader.py`.
- **Estado de Certificación**: **CERTIFICADO**

---

### Contrato 3: `CTR-003` (Normalización → XML / DTE)
- **ID**: `CTR-003`
- **Origen**: Tablas de staging normalizadas y archivos DTE SII (`01_Raw/XML/`).
- **Destino**: `engine/v4/xml_matcher.py` y tabla `stg_dte_sii`.
- **Campos Obligatorios**: `folio_dte`, `tipo_dte` (33/43/52/61), `rut_emisor`, `rut_receptor`, `monto_neto`, `monto_iva`, `monto_total`, `fecha_emision`.
- **Campos Opcionales**: `razon_social`, `timbre_xml`, `track_id_sii`.
- **Reglas de Validación**: `monto_total == monto_neto + monto_iva`; RUTs válidos con digito verificador; `folio_dte` único por tipo_dte.
- **Owner**: DTE & Tax Specialist.
- **Versión**: `1.0.0`
- **Política de Cambios**: Estándar normativo SII Chile.
- **Compatibilidad Hacia Atrás**: Mantenida para folios 2025-2026.
- **Estado de Certificación**: **CERTIFICADO**

---

### Contrato 4: `CTR-004` (XML → SAP)
- **ID**: `CTR-004`
- **Origen**: Matcher DTE SII (`stg_dte_sii`).
- **Destino**: Esquema de contabilización SAP / ERP (`stg_sap_accounting_doc`).
- **Campos Obligatorios**: `sap_doc_id`, `sociedad`, `ejercicio`, `periodo`, `cuenta_contable`, `monto_debe`, `monto_haber`, `folio_dte_referencia`.
- **Campos Opcionales**: `centro_costo`, `asignacion`, `texto_posicion`.
- **Reglas de Validación**: `sum(monto_debe) == sum(monto_haber)` por documento; `sociedad` válida en plan de cuentas.
- **Owner**: SAP Integration Specialist.
- **Versión**: `1.0.0` (Especificado para Fase 5)
- **Política de Cambios**: Requiere RFC formal y aprobación de Contraloría.
- **Compatibilidad Hacia Atrás**: Estructura estándar SAP BAPI/IDoc.
- **Estado de Certificación**: **ESPECIFICADO**

---

### Contrato 5: `CTR-005` (SAP → Settlement Marketplace)
- **ID**: `CTR-005`
- **Origen**: Esquema SAP (`stg_sap_accounting_doc`).
- **Destino**: Informes de liquidación de Marketplace (`marketplace_liquidaciones_v1`).
- **Campos Obligatorios**: `liquidacion_id`, `marketplace`, `periodo_liquidacion`, `monto_bruto_ventas`, `monto_comisiones`, `monto_descuentos`, `monto_neto_liquidado`.
- **Campos Opcionales**: `retenciones_fiscales`, `cobros_logistica`.
- **Reglas de Validación**: `monto_neto_liquidado == bruto - comisiones - descuentos + abonos`; conciliación $0 delta contra cartola de marketplace.
- **Owner**: Settlement Specialist.
- **Versión**: `1.0.0` (Especificado para Fase 6)
- **Política de Cambios**: Cambio de versión ante nuevas estructuras de liquidación de MP.
- **Compatibilidad Hacia Atrás**: Mapeos consolidados en `financial_engine.py`.
- **Estado de Certificación**: **ESPECIFICADO**

---

### Contrato 6: `CTR-006` (Settlement → Pago)
- **ID**: `CTR-006`
- **Origen**: Tabla de liquidaciones (`marketplace_liquidaciones_v1`).
- **Destino**: Registros de órdenes de pago enviadas / transferencias (`stg_pago_origen`).
- **Campos Obligatorios**: `pago_id`, `liquidacion_id`, `fecha_transferencia`, `banco_origen`, `cuenta_origen`, `monto_transferido`, `referencia_bancaria`.
- **Campos Opcionales**: `comprobante_transferencia_url`, `observaciones`.
- **Reglas de Validación**: `monto_transferido` coincide exactamente con `monto_neto_liquidado`; `pago_id` único.
- **Owner**: Treasury Specialist.
- **Versión**: `1.0.0` (Especificado para Fase 6)
- **Política de Cambios**: Aprobación por Tesorería.
- **Compatibilidad Hacia Atrás**: Formato estándar TEF Chile.
- **Estado de Certificación**: **ESPECIFICADO**

---

### Contrato 7: `CTR-007` (Pago → Banco)
- **ID**: `CTR-007`
- **Origen**: Registros de pago (`stg_pago_origen`).
- **Destino**: Cartola bancaria oficial (`stg_cartola_bancaria`).
- **Campos Obligatorios**: `movimiento_bancario_id`, `banco`, `cuenta_bancaria`, `fecha_cartola`, `monto_abono`, `descripcion_movimiento`, `cartola_hash`.
- **Campos Opcionales**: `sucursal`, `rut_depositante`.
- **Reglas de Validación**: Match exacto `referencia_bancaria == descripcion_movimiento` o monto + fecha idéntica; sin duplicados en cartola.
- **Owner**: Treasury & Bank Reconciliation Specialist.
- **Versión**: `1.0.0` (Especificado para Fase 7)
- **Política de Cambios**: Ajuste según banco emisor (Banco de Chile, Santander, BCI).
- **Compatibilidad Hacia Atrás**: Ingesta incremental por fecha.
- **Estado de Certificación**: **ESPECIFICADO**

---

### Contrato 8: `CTR-008` (Banco → Ledger Financiero)
- **ID**: `CTR-008`
- **Origen**: Cartola bancaria (`stg_cartola_bancaria`) y Staging Normalizado.
- **Destino**: `marketplace_ledger_v1` y `marketplace_cierre_financiero_v1`.
- **Campos Obligatorios**: `ledger_id`, `periodo`, `marketplace`, `financial_group` (ingresos, devoluciones, cobros, disponible), `concepto_canonico`, `monto`, `resultado_neto`.
- **Campos Opcionales**: `event_role`, `cash_role`, `pnl_role`.
- **Reglas de Validación**: Asignación obligatoria a uno de los 96 conceptos canónicos; `resultado_neto` en paridad $0 delta con cierre oficial.
- **Owner**: Single Financial Truth Guardian.
- **Versión**: `1.0.0`
- **Política de Cambios**: Inmutable. Modificaciones requieren RFC aprobado.
- **Compatibilidad Hacia Atrás**: Inviolable bajo BASELINE_V6.
- **Estado de Certificación**: **CERTIFICADO**

---

### Contrato 9: `CTR-009` (Ledger → Evidence Layer)
- **ID**: `CTR-009`
- **Origen**: `marketplace_ledger_v1` y DuckDB official DB.
- **Destino**: Archivos de evidencia certificada `evidence/fase_1b/` (`summary.json`, `C1.json` .. `C4.json`).
- **Campos Obligatorios**: `execution_id`, `git_commit`, `timestamp`, `repository`, `unique_tests`, `aggregate_executions`, `implementation_status`, `certification_status`.
- **Campos Opcionales**: `duplicated_files`, `notes`.
- **Reglas de Validación**: Generación automática por harness `validate_fase_1b.py`; no alteración manual; incluye commit y SHA256 de DB.
- **Owner**: Evidence Guardian & QA Auditor.
- **Versión**: `1.0.0`
- **Política de Cambios**: Extensión de campos auditables sin modificar Nivel 1/2 preexistentes.
- **Compatibilidad Hacia Atrás**: Formato JSON schema v1.0.
- **Estado de Certificación**: **CERTIFICADO**

---

### Contrato 10: `CTR-010` (Evidence → Knowledge Layer)
- **ID**: `CTR-010`
- **Origen**: Archivos JSON de Evidence Layer y especificadores de gobierno.
- **Destino**: KnowledgeOS (`KnowledgeOS/01_Canonical/`, `KnowledgeOS/03_Evidence/`).
- **Campos Obligatorios**: `document_id`, `canonical_title`, `version`, `status`, `evidence_ref`, `obsidian_links`.
- **Campos Opcionales**: `tags`, `author`.
- **Reglas de Validación**: Formato Markdown con Header Universal normalizado; enlaces relativos sin referencias rotas.
- **Owner**: Knowledge Engineer.
- **Versión**: `1.0.0`
- **Política de Cambios**: Aprobación en PR de gobernanza.
- **Compatibilidad Hacia Atrás**: Enlaces bidireccionales compatibles con Obsidian.
- **Estado de Certificación**: **ESPECIFICADO**

---

### Contrato 11: `CTR-011` (Knowledge → Copilot)
- **ID**: `CTR-011`
- **Origen**: System Intelligence Layer & KnowledgeOS.
- **Destino**: Financial Copilot API / Interface.
- **Campos Obligatorios**: `question_id`, `canonical_query`, `sql_execution_chain`, `evidence_hash`, `verified_response_payload`, `delta_amount`.
- **Campos Opcionales**: `explicability_markdown`, `chart_series`.
- **Reglas de Validación**: `delta_amount == 0.00` CLP obligatorio; respuesta respaldada en nodo certificado del Dual Graph; cero respuesta generativa sin evidencia.
- **Owner**: AI & Copilot Architect.
- **Versión**: `1.0.0` (Especificado para Fase 8)
- **Política de Cambios**: Prohibida la degradación a respuestas no explicables.
- **Compatibilidad Hacia Atrás**: Schema de respuesta JSON v1.
- **Estado de Certificación**: **ESPECIFICADO**

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:DATA_CONTRACT_REGISTRY_V1` (Tipo: `Registro_Contratos_Datos`)
- `Node:CTR-001` .. `Node:CTR-011` (Tipo: `Contrato_Datos`)

### Execution Graph Nodes
- `ExecNode:VALIDATE_DATA_CONTRACT_SCHEMA` (Process: Evaluación automática de cumplimiento de contratos de datos en pipelines ETL)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: Los contratos formales de las 11 interfaces del sistema end-to-end.
- **CONECTA**: Capa RAW → DuckDB → Ledger → Evidence → Knowledge → Copilot.
- **GARANTIZA**: La Regla de Oro del Proyecto (sin Contrato no hay Implementación).

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[DATA_CONTRACT_REGISTRY_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/DATA_CONTRACT_REGISTRY_V1.md`
