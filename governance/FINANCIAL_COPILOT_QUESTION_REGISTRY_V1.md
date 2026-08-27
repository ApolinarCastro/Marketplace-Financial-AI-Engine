---
id: FINANCIAL_COPILOT_QUESTION_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: AI & Copilot Architect / Financial Auditor
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - ARCHITECTURE_REGISTRY_V1
  - DATA_CONTRACT_REGISTRY_V1
  - EVIDENCE_REGISTRY_V1
  - SYSTEM_INTELLIGENCE_SPECIFICATION_V1
relacionado_con:
  - END_TO_END_RECONCILIATION_ROADMAP_V1
  - KNOWLEDGE_CANONICAL_REGISTRY_V1
  - CAPABILITY_REGISTRY_V1
---

# REGISTRO MAESTRO DE PREGUNTAS ESTRATÉGICAS DEL FINANCIAL COPILOT V1

## Propósito
Establecer la especificación formal, cadena de evidencia probatoria y esquemas de respuesta inmutables para las **10 Preguntas Financieras Estratégicas** que responderá el **Financial Copilot**. Garantiza respuestas $0 delta, explicables y con cero tolerancia a la alucinación.

---

## Regla de Respuesta Inviolable ante Evidencia Faltante

> [!CAUTION]
> ### POLÍTICA ANTI-ALUCINACIÓN SUPREMA
> Cuando el sistema detecte que no existe la evidencia probatoria $0 delta requerida o un contrato de datos no está certificado, la respuesta **ÚNICA Y OBLIGATORIA** emitida será:
>
> **"No se puede responder con evidencia suficiente."**
>
> Queda estrictamente prohibido realizar estimaciones, inferencias de cifras o inventar montos no verificados en la base de datos oficial.

---

## Registro Canónico de las 10 Preguntas Financieras Estratégicas

### Pregunta 1: ¿Qué vendí?
- **question_id**: `Q-001`
- **pregunta**: "¿Qué vendí?"
- **descripcion**: Consulta de Ventas Brutas consolidadas por período, marketplace y SKU sin deducción de comisiones.
- **intencion**: `INTENT_VENTAS_BRUTAS`
- **owner**: Financial Data Engineer
- **marketplace**: `CONSOLIDADO` (MELI, Paris, Ripley, Falabella)
- **periodo**: Período mensual seleccionado YYYY-MM
- **contratos_requeridos**: `CTR-001`, `CTR-002`, `CTR-008`
- **evidencias_requeridas**: `EVID-DB-001` (DB Hash: `311c78e2b7...`)
- **lineage_requerido**: `LIN-001` → `LIN-002` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: `CAP-LEDGER-V1`, `CAP-DB-CORE`
- **componentes_involucrados**: DuckDB, `marketplace_ledger_v1`, API `/api/v4/cierre/desglose`
- **consultas_requeridas**: `SELECT sum(monto) FROM marketplace_ledger_v1 WHERE financial_group = 'ingresos'`
- **restricciones**: Excluir devoluciones y cobros operacionales.
- **politica_respuesta**: Retornar monto total en CLP formato moneda, tabla por marketplace y citas a `EVID-DB-001`.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: 100% (Certificado)
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: 69/69 períodos $0 delta en Ventas.

---

### Pregunta 2: ¿Qué me cobraron?
- **question_id**: `Q-002`
- **pregunta**: "¿Qué me cobraron?"
- **descripcion**: Consulta detallada de comisiones, costos logísticos, publicidad, servicios y deducciones operacionales retenidas.
- **intencion**: `INTENT_DESGLOSE_COBROS`
- **owner**: Cost Analyst
- **marketplace**: `CONSOLIDADO`
- **periodo**: Período mensual seleccionado YYYY-MM
- **contratos_requeridos**: `CTR-002`, `CTR-005`, `CTR-008`
- **evidencias_requeridas**: `EVID-SELLER-REALITY-001`, `EVID-DB-001`
- **lineage_requerido**: `LIN-002` → `LIN-005` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: `CAP-ML-POSCOBRO`, `CAP-LEDGER-V1`
- **componentes_involucrados**: DuckDB, `marketplace_ledger_v1`, Economic Dictionary
- **consultas_requeridas**: `SELECT concepto_canonico, sum(monto) FROM marketplace_ledger_v1 WHERE financial_group = 'cobros' GROUP BY concepto_canonico`
- **restricciones**: Desglose obligatorio en los 96 conceptos canónicos.
- **politica_respuesta**: Retornar total cobros, matriz por concepto y marketplace, respaldada en ROOT_EVENTS.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: 100% (Certificado)
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: Triple Play Certification ($172.6M ROOT_EVENTS).

---

### Pregunta 3: ¿Qué me pagaron?
- **question_id**: `Q-003`
- **pregunta**: "¿Qué me pagaron?"
- **descripcion**: Consulta del líquido disponible efectivamente transferido o depositado por los marketplaces.
- **intencion**: `INTENT_RESULTADO_NETO_LIQUIDADO`
- **owner**: Treasury Specialist
- **marketplace**: `CONSOLIDADO`
- **periodo**: Período mensual seleccionado YYYY-MM
- **contratos_requeridos**: `CTR-005`, `CTR-006`, `CTR-008`
- **evidencias_requeridas**: `EVID-RIPLEY-CLASSIF-001`, `EVID-DB-001`
- **lineage_requerido**: `LIN-005` → `LIN-006` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: `CAP-RIPLEY-CLASSIF`, `CAP-CIERRE-V1`
- **componentes_involucrados**: `marketplace_cierre_financiero_v1`, API `/api/v4/exec/summary`
- **consultas_requeridas**: `SELECT resultado_neto FROM marketplace_cierre_financiero_v1 WHERE periodo = ? AND marketplace = ?`
- **restricciones**: Cuadratura exacta contra Resultado Neto oficial.
- **politica_respuesta**: Retornar monto neto en CLP, desglose por MP y respaldo en cierres certificados.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: 100% (Certificado)
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: Ripley 17/17 meses $206.9M neto, Paris $0 delta.

---

### Pregunta 4: ¿Qué falta por cobrar?
- **question_id**: `Q-004`
- **pregunta**: "¿Qué falta por cobrar?"
- **descripcion**: Identificación de fondos retenidos, liquidaciones pendientes o descalces de pago por cobrar a los marketplaces.
- **intencion**: `INTENT_SALDO_PENDIENTE`
- **owner**: Controller Financiero
- **marketplace**: `CONSOLIDADO`
- **periodo**: Período acumulado a la fecha
- **contratos_requeridos**: `CTR-005`, `CTR-006`
- **evidencias_requeridas**: Informes de Liquidación y Liberaciones
- **lineage_requerido**: `LIN-005` → `LIN-006` → `LIN-008` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: `CAP-CIERRE-V1`
- **componentes_involucrados**: DuckDB, `stg_pago_origen`, `marketplace_liquidaciones_v1`
- **consultas_requeridas**: `SELECT sum(monto_neto_liquidado - monto_transferido) FROM marketplace_liquidaciones_v1`
- **restricciones**: Diferenciar saldos en período normal de cobros vencidos.
- **politica_respuesta**: Reportar monto por cobrar por marketplace con antigüedad de saldo.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: 90% (Validado)
- **estado**: **VALIDADA** | **madurez**: Nivel 3 (Validado)
- **certificacion**: Validada en Sprints B2.5C y G6.

---

### Pregunta 5: ¿Qué devoluciones existen?
- **question_id**: `Q-005`
- **pregunta**: "¿Qué devoluciones existen?"
- **descripcion**: Desglose de anulaciones de venta, notas de crédito y reversiones procesadas.
- **intencion**: `INTENT_DEVOLUCIONES`
- **owner**: Single Financial Truth Guardian
- **marketplace**: `CONSOLIDADO`
- **periodo**: Período mensual seleccionado YYYY-MM
- **contratos_requeridos**: `CTR-001`, `CTR-002`, `CTR-008`
- **evidencias_requeridas**: `EVID-DB-001`
- **lineage_requerido**: `LIN-001` → `LIN-002` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: `CAP-LEDGER-V1`
- **componentes_involucrados**: `marketplace_ledger_v1`
- **consultas_requeridas**: `SELECT sum(monto) FROM marketplace_ledger_v1 WHERE financial_group = 'devoluciones'`
- **restricciones**: Reversión directa de Ingresos Brutos.
- **politica_respuesta**: Reportar monto de devoluciones y ratio porcentaje sobre ventas brutas.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: 100% (Certificado)
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: 69/69 períodos $0 delta en Devoluciones.

---

### Pregunta 6: ¿Qué XML o DTE respalda la operación?
- **question_id**: `Q-006`
- **pregunta**: "¿Qué XML o DTE respalda la operación?"
- **descripcion**: Trazabilidad tributaria de folios DTE SII (Facturas, Notas de Crédito) asociados a la transacción o período.
- **intencion**: `INTENT_RESPALDO_DTE`
- **owner**: DTE & Tax Specialist
- **marketplace**: `PARIS` / `RIPLEY` / `MELI` / `FALABELLA`
- **periodo**: Período mensual seleccionado YYYY-MM
- **contratos_requeridos**: `CTR-003` (Normalización → XML)
- **evidencias_requeridas**: Informes de Cobertura DTE Paris y Ripley
- **lineage_requerido**: `LIN-002` → `LIN-003` → `LIN-010` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: `CAP-DTE-COVERAGE`
- **componentes_involucrados**: `engine/v4/dte_indexer.py`, `stg_dte_sii`
- **consultas_requeridas**: `SELECT folio_dte, tipo_dte, monto_total FROM stg_dte_sii WHERE rut_emisor = ?`
- **restricciones**: DTEs validados con RUT e importe SII.
- **politica_respuesta**: Presentar folio DTE, tipo de documento (33/61), monto y estado de cobertura.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: 85% (Validado)
- **estado**: **VALIDADA** | **madurez**: Nivel 3 (Validado - Paris 82.6%).
- **certificacion**: Validada en Paris XML Activation & Recertification.

---

### Pregunta 7: ¿Qué registro SAP respalda la operación?
- **question_id**: `Q-007`
- **pregunta**: "¿Qué registro SAP respalda la operación?"
- **descripcion**: Consulta del número de documento contable ERP SAP asociado al asiento de venta o cobro.
- **intencion**: `INTENT_RESPALDO_SAP`
- **owner**: SAP Integration Specialist
- **marketplace**: `CONSOLIDADO`
- **periodo**: Período mensual seleccionado YYYY-MM
- **contratos_requeridos**: `CTR-004` (XML → SAP)
- **evidencias_requeridas**: Asientos Contables SAP Registrados
- **lineage_requerido**: `LIN-003` → `LIN-004` → `LIN-010` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: Integración SAP ERP (Fase 5)
- **componentes_involucrados**: `stg_sap_accounting_doc`
- **consultas_requeridas**: `SELECT sap_doc_id, cuenta_contable, monto_debe FROM stg_sap_accounting_doc`
- **restricciones**: Requiere implementación de Fase 5.
- **politica_respuesta**: Reportar documento contable SAP, sociedad y posición contable.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: Nivel 1 (Especificado)
- **estado**: **ESPECIFICADA** | **madurez**: Nivel 1 (Especificado)
- **certificacion**: Programado para Fase 5.

---

### Pregunta 8: ¿Qué movimiento bancario respalda el pago?
- **question_id**: `Q-008`
- **pregunta**: "¿Qué movimiento bancario respalda el pago?"
- **descripcion**: Identificación del abono en la cartola bancaria corporativa correspondiente a la transferencia de liquidación.
- **intencion**: `INTENT_RESPALDO_BANCO`
- **owner**: Bank Reconciliation Specialist
- **marketplace**: `CONSOLIDADO`
- **periodo**: Período mensual seleccionado YYYY-MM
- **contratos_requeridos**: `CTR-007` (Pago → Banco)
- **evidencias_requeridas**: Cartola Bancaria Oficial Registrada
- **lineage_requerido**: `LIN-006` → `LIN-007` → `LIN-008` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: Conciliación Bancaria (Fase 7)
- **componentes_involucrados**: `stg_cartola_bancaria`
- **consultas_requeridas**: `SELECT movimiento_bancario_id, fecha_cartola, monto_abono FROM stg_cartola_bancaria`
- **restricciones**: Requiere implementación de Fase 7.
- **politica_respuesta**: Presentar ID de movimiento bancario, fecha de abono y código TEF.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: Nivel 1 (Especificado)
- **estado**: **ESPECIFICADA** | **madurez**: Nivel 1 (Especificado)
- **certificacion**: Programado para Fase 7.

---

### Pregunta 9: ¿Qué cargo, comisión o descuento está oculto o no explicado?
- **question_id**: `Q-009`
- **pregunta**: "¿Qué cargo, comisión o descuento está oculto o no explicado?"
- **descripcion**: Detección de divergencias, cargos por penalidad, cobros logísticos o abonos no mapeados en el Economic Dictionary.
- **intencion**: `INTENT_CARGOS_NO_EXPLICADOS`
- **owner**: Single Financial Truth Guardian
- **marketplace**: `CONSOLIDADO`
- **periodo**: Período mensual seleccionado YYYY-MM
- **contratos_requeridos**: `CTR-002`, `CTR-005`, `CTR-008`
- **evidencias_requeridas**: `EVID-DB-001`, `EVID-SELLER-REALITY-001`
- **lineage_requerido**: `LIN-002` → `LIN-005` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: `CAP-LEDGER-V1`, `CAP-ML-POSCOBRO`
- **componentes_involucrados**: `marketplace_ledger_v1`
- **consultas_requeridas**: `SELECT * FROM marketplace_ledger_v1 WHERE concepto_canonico IS NULL OR concepto_canonico = 'OTROS_NO_CLASIFICADOS'`
- **restricciones**: Cero tolerancia a descalces > $0 sin justificación.
- **politica_respuesta**: Reportar $0 descalce en conceptos certificados o listar transacciones en revisión.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: 100% (Certificado)
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: 96 conceptos mapeados 100% explicados.

---

### Pregunta 10: ¿Cuál es el margen financiero real?
- **question_id**: `Q-010`
- **pregunta**: "¿Cuál es el margen financiero real?"
- **descripcion**: Cómputo del margen financiero neto porcentual (Resultado Neto / Ventas Brutas) respaldado por la verdad financiera corporativa.
- **intencion**: `INTENT_MARGEN_FINANCIERO_REAL`
- **owner**: Single Financial Truth Guardian & Controller
- **marketplace**: `CONSOLIDADO`
- **periodo**: Período mensual seleccionado YYYY-MM
- **contratos_requeridos**: `CTR-001` a `CTR-008` (Todos los de backend)
- **evidencias_requeridas**: `EVID-DB-001`, `EVID-RIPLEY-CLASSIF-001`
- **lineage_requerido**: `LIN-001` a `LIN-009` → `LIN-011` → `LIN-012`
- **capacidades_requeridas**: `CAP-CIERRE-V1`, `CAP-LEDGER-V1`
- **componentes_involucrados**: `marketplace_cierre_financiero_v1`
- **consultas_requeridas**: `SELECT (resultado_neto / venta_bruta) * 100 AS margen_pct FROM marketplace_cierre_financiero_v1`
- **restricciones**: Resultado Neto en paridad $0 delta auditada.
- **politica_respuesta**: Presentar margen porcentual por marketplace, waterfall financiero explicativo y citas a cierres.
- **respuesta_cuando_no_exista_evidencia**: "No se puede responder con evidencia suficiente."
- **nivel_confianza**: 100% (Certificado)
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: Certificación de Margen Real G5.6 y G5.7.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:FINANCIAL_COPILOT_QUESTION_REGISTRY_V1` (Tipo: `Registro_Preguntas_Copilot`)
- `Node:Q-001` .. `Node:Q-010` (Tipo: `Pregunta_Estratégica`)

### Execution Graph Nodes
- `ExecNode:VERIFY_COPILOT_EVIDENCE_CHAINS` (Process: Auditar completitud de contratos y evidencias requeridas para responder Q-001 a Q-010)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: Los contratos de respuesta para las 10 Preguntas Financieras Estratégicas del Copilot.
- **VINCULA**: [SYSTEM_INTELLIGENCE_SPECIFICATION_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md) con las evidencias de `EVIDENCE_REGISTRY_V1.md`.
- **AFECTA**: La interfaz conversacional final del Financial Copilot.

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[FINANCIAL_COPILOT_QUESTION_REGISTRY_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/FINANCIAL_COPILOT_QUESTION_REGISTRY_V1.md`
