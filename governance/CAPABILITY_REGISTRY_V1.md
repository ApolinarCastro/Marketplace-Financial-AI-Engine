---
id: CAPABILITY_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: Lead Technical Product Owner & QA Lead
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - PMO_REGISTRY_V1
  - ARCHITECTURE_REGISTRY_V1
  - DATA_CONTRACT_REGISTRY_V1
  - EVIDENCE_REGISTRY_V1
relacionado_con:
  - MATURITY_REGISTRY_V1
  - KNOWLEDGE_CANONICAL_REGISTRY_V1
  - FINANCIAL_COPILOT_QUESTION_REGISTRY_V1
---

# REGISTRO MAESTRO DE CAPACIDADES DEL SISTEMA V1

## Propósito
Establecer el inventario oficial, estatus de certificación y nivel de madurez de todas las **Capacidades Funcionales y Técnicas** del **Marketplace Financial AI Engine**. Aplica estrictamente los principios de **Strict Governance First** y la **Regla de Oro del Proyecto**.

---

## Reglas Inviolables de Clasificación de Capacidades

> [!CAUTION]
> 1. **Prohibición de Declaración Prematura**: No se declarará ninguna capacidad como `IMPLEMENTADA` si únicamente existe documentación.
> 2. **Evidencia Obligatoria para Certificación**: No se declarará ninguna capacidad como `CERTIFICADA` sin un registro de evidencia reproducible con hash SHA-256 e `execution_id` en `EVIDENCE_REGISTRY_V1.md`.

---

## Catálogo Maestro de Capacidades

### 1. `CAP-DB-CORE` (Persistencia OLAP DuckDB Core)
- **capability_id**: `CAP-DB-CORE`
- **nombre**: "Persistencia Financiera OLAP DuckDB Core"
- **descripcion**: "Gestión inmutable y determinista de la base de datos oficial `meli_financial_v4.db` en DuckDB V1.5.1."
- **objetivo**: Proveer motor de consulta OLAP de alta velocidad con integridad referencial $0 delta.
- **owner**: Database Architect | **componente**: `data/db/meli_financial_v4.db`
- **capa_arquitectonica**: Data Layer (Capa 7)
- **contratos_requeridos**: `CTR-008` (Banco → Ledger)
- **evidencias_requeridas**: `EVID-DB-001` (SHA256: `311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9`)
- **preguntas_financieras_soportadas**: Preguntas 1 a 10 (Todas)
- **marketplace_aplicable**: `CONSOLIDADO` (MELI, Paris, Ripley, Falabella)
- **dependencias**: Sistema de archivos Read-Only | **bloqueadores**: Ninguno
- **pruebas_requeridas**: `tests/test_golden.py`, Verificación Hash DB
- **estado**: **PRODUCTIVA** | **madurez**: Nivel 5 (Productivo)
- **certificacion**: BASELINE_V6 Official Certification | **fecha**: 2026-05-30
- **observaciones**: DB inmutable congelada en Phase 0.

---

### 2. `CAP-LEDGER-V1` (Ledger Financiero Consolidado)
- **capability_id**: `CAP-LEDGER-V1`
- **nombre**: "Ledger Financiero Consolidado 4 Marketplaces"
- **descripcion**: "Motor de doble entrada que consolida transacciones en los 96 conceptos financieros canónicos."
- **objetivo**: Cuadratura de Ventas Brutas y Devoluciones con $0 descalce en 69/69 períodos.
- **owner**: Single Financial Truth Guardian | **componente**: `engine/v4/surgical_loader.py`
- **capa_arquitectonica**: Financial Engine (Capa 5) / Domain Layer (Capa 4)
- **contratos_requeridos**: `CTR-002`, `CTR-008`
- **evidencias_requeridas**: `EVID-DB-001`
- **preguntas_financieras_soportadas**: Pregunta 1 (Ventas), Pregunta 5 (Devoluciones)
- **marketplace_aplicable**: `CONSOLIDADO`
- **dependencias**: `CAP-DB-CORE` | **bloqueadores**: Ninguno
- **pruebas_requeridas**: Regression suite `tests/`
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: Certificación 69/69 períodos $0 delta | **fecha**: 2026-05-30
- **observaciones**: Mantiene $0 delta histórico.

---

### 3. `CAP-CIERRE-V1` (Cierre Financiero y Resultado Neto)
- **capability_id**: `CAP-CIERRE-V1`
- **nombre**: "Cierre Financiero Mensual de Resultado Neto"
- **descripcion**: "Computo automático del Resultado Neto mensual disponible por marketplace y consolidado corporativo."
- **objetivo**: Determinar la liquidez real disponible con paridad probada.
- **owner**: Lead Financial Engineer | **componente**: `engine/v4/domain/financial_engine.py`
- **capa_arquitectonica**: Financial Engine (Capa 5)
- **contratos_requeridos**: `CTR-005`, `CTR-008`
- **evidencias_requeridas**: `EVID-DB-001`, `EVID-RIPLEY-CLASSIF-001`
- **preguntas_financieras_soportadas**: Pregunta 3 (¿Qué me pagaron?), Pregunta 10 (Margen Real)
- **marketplace_aplicable**: `CONSOLIDADO`
- **dependencias**: `CAP-LEDGER-V1` | **bloqueadores**: Ninguno
- **pruebas_requeridas**: Test de cierre mensual
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: Paris/Ripley $0 delta, Falabella $12K delta controlado | **fecha**: 2026-06-03
- **observaciones**: Cierre inmutable.

---

### 4. `CAP-RIPLEY-CLASSIF` (Clasificación de Liquidaciones Ripley)
- **capability_id**: `CAP-RIPLEY-CLASSIF`
- **nombre**: "Motor de Clasificación y Cierre Ripley Post-B2.5C"
- **descripcion**: "Clasificación de 62,502 filas de transacciones Ripley con semántica a pagar/liquidación."
- **objetivo**: Lograr 100% de cobertura y $0 delta en 17/17 meses de Ripley.
- **owner**: Financial Data Engineer | **componente**: `engine/v4/surgical_loader.py`
- **capa_arquitectonica**: Financial Engine (Capa 5)
- **contratos_requeridos**: `CTR-002`, `CTR-005`
- **evidencias_requeridas**: `EVID-RIPLEY-CLASSIF-001`
- **preguntas_financieras_soportadas**: Pregunta 3, Pregunta 9
- **marketplace_aplicable**: `RIPLEY`
- **dependencias**: `CAP-LEDGER-V1` | **bloqueadores**: Ninguno
- **pruebas_requeridas**: Clean runs de clasificación Ripley
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: B2.5C Ripley Certification ($206.9M neto) | **fecha**: 2026-06-03
- **observaciones**: Cobertura 100% verificada.

---

### 5. `CAP-ML-POSCOBRO` (Trazabilidad Poscobro Mercado Libre)
- **capability_id**: `CAP-ML-POSCOBRO`
- **nombre**: "Trazabilidad Forense Poscobro Mercado Libre"
- **descripcion**: "Trazabilidad de 5,728 filas de ROOT_EVENTS ($172.6M) demostrando equivalencia de comisiones y deducciones de seller."
- **objetivo**: Probar que ROOT_EVENT es Ingreso para ML y Costo/Deducción para el Seller.
- **owner**: Senior Data Scientist | **componente**: Domain Layer / Poscobro Engine
- **capa_arquitectonica**: Domain Layer (Capa 4)
- **contratos_requeridos**: `CTR-002`, `CTR-005`
- **evidencias_requeridas**: `EVID-SELLER-REALITY-001`
- **preguntas_financieras_soportadas**: Pregunta 2 (¿Qué me cobraron?)
- **marketplace_aplicable**: `MELI`
- **dependencias**: `CAP-LEDGER-V1` | **bloqueadores**: Ninguno
- **pruebas_requeridas**: Forensic single order trace
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: Triple Play Certification ($172.6M Poscobro) | **fecha**: 2026-06-06
- **observaciones**: Trazabilidad forense probada.

---

### 6. `CAP-UI-FORMAT` (Paridad de Formato en Interfaz Gráfica)
- **capability_id**: `CAP-UI-FORMAT`
- **nombre**: "Paridad de Formato Monetario CLP en Tableros Gerencial y Auditor"
- **descripcion**: "Renderizado unificado en CLP sin decimales y tooltips explicativos de KPI cards."
- **objetivo**: Garantizar paridad visual $0 delta entre JSON API y vistas HTML.
- **owner**: Frontend Lead | **componente**: `templates/dashboard.html`, `templates/executive_dashboard.html`
- **capa_arquitectonica**: Presentation Layer (Capa 1)
- **contratos_requeridos**: `CTR-011`
- **evidencias_requeridas**: `EVID-SURGICAL-FIX-001`
- **preguntas_financieras_soportadas**: Pregunta 8, Pregunta 10
- **marketplace_aplicable**: `CONSOLIDADO`
- **dependencias**: API Layer | **bloqueadores**: Ninguno
- **pruebas_requeridas**: Manual visual rendering verification
- **estado**: **CERTIFICADA** | **madurez**: Nivel 4 (Certificado)
- **certificacion**: Post-F5-08 Surgical Fix Certification | **fecha**: 2026-07-27
- **observaciones**: Cero alteración backend.

---

### 7. `CAP-DUAL-GRAPH` (Modelo de Grafos Duales de Arquitectura)
- **capability_id**: `CAP-DUAL-GRAPH`
- **nombre**: "Modelado de Grafos Duales (Knowledge Graph + Execution Graph)"
- **descripcion**: "Especificación formal del sistema de doble grafo para auditoría, trazabilidad y detección de SPOF."
- **objetivo**: Modelar 24 nodos KG, 26 nodos EG, 29 relaciones y 16 casos de análisis forense.
- **owner**: Graph Architect | **componente**: Governance Specs
- **capa_arquitectonica**: Knowledge Graph (Capa 9) / Execution Graph (Capa 10)
- **contratos_requeridos**: `CTR-010`, `CTR-011`
- **evidencias_requeridas**: `DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md`
- **preguntas_financieras_soportadas**: Preguntas 1 a 10
- **marketplace_aplicable**: `CONSOLIDADO`
- **dependencias**: KnowledgeOS | **bloqueadores**: Ninguno
- **pruebas_requeridas**: Cross-document validation
- **estado**: **ESPECIFICADA** | **madurez**: Nivel 1 (Especificado)
- **certificacion**: Phase 0 Task 4 Specification Sign-Off | **fecha**: 2026-07-27
- **observaciones**: Especificación completa entregada en Task 4.

---

### 8. `CAP-SYSTEM-INTELLIGENCE` (Capa de Inteligencia y Puertas de Seguridad)
- **capability_id**: `CAP-SYSTEM-INTELLIGENCE`
- **nombre**: "Capa System Intelligence y Puerta Anti-Alucinación"
- **descripcion**: "Orquestación semántica, jerarquía de 8 fuentes y fallback obligatorio ante evidencia insuficiente."
- **objetivo**: Garantizar que ninguna respuesta del Copilot carezca de evidencia probatoria $0 delta.
- **owner**: AI & Copilot Architect | **componente**: Governance Specs
- **capa_arquitectonica**: System Intelligence (Capa 11)
- **contratos_requeridos**: `CTR-011`
- **evidencias_requeridas**: `SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md`
- **preguntas_financieras_soportadas**: Preguntas 1 a 10
- **marketplace_aplicable**: `CONSOLIDADO`
- **dependencias**: `CAP-DUAL-GRAPH` | **bloqueadores**: Ninguno
- **pruebas_requeridas**: Fallback policy validation
- **estado**: **ESPECIFICADA** | **madurez**: Nivel 1 (Especificado)
- **certificacion**: Phase 0 Task 4 Specification Sign-Off | **fecha**: 2026-07-27
- **observaciones**: Especificación completa entregada en Task 4.

---

### 9. `CAP-COPILOT-CORE` (Financial Copilot Certificado)
- **capability_id**: `CAP-COPILOT-CORE`
- **nombre**: "Financial Copilot Certificado de Respuestas Explicables"
- **descripcion**: "Interfaz inteligente para responder las 10 Preguntas Financieras Estratégicas respaldadas por evidencia."
- **objetivo**: Proporcionar respuestas corporativas $0 delta con explicabilidad completa.
- **owner**: Lead Product TPO | **componente**: Financial Copilot Interface
- **capa_arquitectonica**: Financial Copilot (Capa 12)
- **contratos_requeridos**: `CTR-011`
- **evidencias_requeridas**: `FINANCIAL_COPILOT_QUESTION_REGISTRY_V1.md`
- **preguntas_financieras_soportadas**: Preguntas 1 a 10
- **marketplace_aplicable**: `CONSOLIDADO`
- **dependencias**: `CAP-SYSTEM-INTELLIGENCE` | **bloqueadores**: Desarrollo programado para Fase 8
- **pruebas_requeridas**: Golden Copilot Question Suite
- **estado**: **ESPECIFICADA** | **madurez**: Nivel 1 (Especificado)
- **certificacion**: Phase 0 Master Plan Sign-Off | **fecha**: 2026-07-27
- **observaciones**: Programado para implementación en Fase 8.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:CAPABILITY_REGISTRY_V1` (Tipo: `Registro_Capacidades`)
- `Node:CAP-DB-CORE` .. `Node:CAP-COPILOT-CORE` (Tipo: `Capacidad_Sistema`)

### Execution Graph Nodes
- `ExecNode:VERIFY_CAPABILITY_STATUS` (Process: Auditar cumplimiento de criterios para estados IMPLEMENTADA/CERTIFICADA)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: El inventario oficial de capacidades y su madurez real.
- **VINCULA**: Capacidades con [EVIDENCE_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/EVIDENCE_REGISTRY_V1.md) y [DATA_CONTRACT_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/DATA_CONTRACT_REGISTRY_V1.md).
- **AFECTA**: [MATURITY_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/MATURITY_REGISTRY_V1.md).

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[CAPABILITY_REGISTRY_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/CAPABILITY_REGISTRY_V1.md`
