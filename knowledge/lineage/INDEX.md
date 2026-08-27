---
id: KNOWLEDGE_LINEAGE_INDEX_V1
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: Senior Data Engineer & Lineage Architect
ultima_revision: 2026-07-27
dependencias:
  - DATA_LINEAGE_REGISTRY_V1
  - DATA_CONTRACT_REGISTRY_V1
  - EVIDENCE_REGISTRY_V1
  - CAPABILITY_REGISTRY_V1
  - FINANCIAL_COPILOT_QUESTION_REGISTRY_V1
relacionado_con:
  - KNOWLEDGE_OS_SPECIFICATION_V1
  - DUAL_GRAPH_ARCHITECTURE_MODEL_V1
---

# KNOWLEDGEOS — DATA LINEAGE MASTER INDEX

## Propósito
Índice Maestro de Linaje de Datos en **KnowledgeOS**, conectando de forma determinista la cadena completa de 13 etapas y 12 eslabones de linaje (`LIN-001` a `LIN-012`) con sus contratos, evidencias, capacidades y preguntas financieras.

---

## Matriz Canónica de Linaje de Datos (12 Eslabones)

| Lineage ID | Origen | Destino | Contrato | Evidencia | Capacidad | Madurez | Certificación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `LIN-001` | Marketplace APIs | `01_Raw/` | `CTR-001` | SHA256 Hashes | `CAP-RAW-001` | Nivel 4 | CERTIFICADO |
| `LIN-002` | `01_Raw/` | Staging DuckDB | `CTR-002` | `EVID-DB-001` | `CAP-INGEST-V4` | Nivel 5 | CERTIFICADO |
| `LIN-003` | Staging Raw | XML DTE SII | `CTR-003` | Paris/Ripley XML | `CAP-DTE-001` | Nivel 3 | VALIDADO |
| `LIN-004` | XML DTE | SAP ERP | `CTR-004` | SAP Audit Log | `CAP-SAP-001` | Nivel 1 | ESPECIFICADO |
| `LIN-005` | SAP Staging | Settlement MP | `CTR-005` | `EVID-RIPLEY-CLASSIF` | `CAP-SETTLE-001` | Nivel 4 | CERTIFICADO |
| `LIN-006` | Settlement MP | Pago Origen | `CTR-006` | Liberaciones ML/Ripley | `CAP-PAY-001` | Nivel 3 | VALIDADO |
| `LIN-007` | Pago Origen | Cartola Bancaria | `CTR-007` | Cartolas Bancarias | `CAP-BANK-001` | Nivel 1 | ESPECIFICADO |
| `LIN-008` | Cartola Bancaria | Ledger Financiero | `CTR-008` | `EVID-DB-001` | `CAP-LEDGER-V1` | Nivel 5 | CERTIFICADO |
| `LIN-009` | Ledger Financiero | Evidence Layer | `CTR-009` | `EVID-HARNESS-001` | `CAP-EVID-001` | Nivel 4 | CERTIFICADO |
| `LIN-010` | Evidence Layer | Knowledge Layer | `CTR-010` | `KNOWLEDGE_OS_SPEC` | `CAP-KNOW-001` | Nivel 4 | CERTIFICADO |
| `LIN-011` | Knowledge Layer | System Intelligence | `CTR-011` | `SYSTEM_INTEL_SPEC` | `CAP-INTEL-001` | Nivel 1 | ESPECIFICADO |
| `LIN-012` | System Intel | Financial Copilot | `CTR-011` | `Q_REGISTRY_V1` | `CAP-COPILOT-V1` | Nivel 4 | CERTIFICADO |

---

## Mapeo por Pregunta Financiera Estratégica (10 Preguntas)

| Question ID | Pregunta | Ruta de Linaje Requerida | Estado Trazabilidad |
| :--- | :--- | :--- | :--- |
| `Q-001` | ¿Qué vendí? | `LIN-001` → `LIN-002` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012` | TRAZABLE ($0 delta) |
| `Q-002` | ¿Qué me cobraron? | `LIN-001` → `LIN-002` → `LIN-005` → `LIN-008` → `LIN-009` → `LIN-012` | TRAZABLE ($0 delta) |
| `Q-003` | ¿Qué me pagaron? | `LIN-001` → `LIN-005` → `LIN-006` → `LIN-008` → `LIN-009` → `LIN-012` | TRAZABLE (Validado) |
| `Q-004` | ¿Qué falta por cobrar? | `LIN-005` → `LIN-006` → `LIN-007` → `LIN-008` → `LIN-009` → `LIN-012` | ESPECIFICADO |
| `Q-005` | ¿Qué devoluciones existen? | `LIN-001` → `LIN-002` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012` | TRAZABLE ($0 delta) |
| `Q-006` | ¿Qué XML respalda? | `LIN-002` → `LIN-003` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012` | TRAZABLE (Paris 82.6%) |
| `Q-007` | ¿Qué documento SAP respalda? | `LIN-003` → `LIN-004` → `LIN-005` → `LIN-008` → `LIN-009` → `LIN-012` | ESPECIFICADO |
| `Q-008` | ¿Qué movimiento bancario respalda? | `LIN-006` → `LIN-007` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012` | ESPECIFICADO |
| `Q-009` | ¿Qué cargos no explicados existen? | `LIN-002` → `LIN-005` → `LIN-008` → `LIN-009` → `LIN-011` → `LIN-012` | TRAZABLE ($0 delta) |
| `Q-010` | ¿Cuál es el margen financiero real? | `LIN-001` → `LIN-002` → `LIN-005` → `LIN-008` → `LIN-009` → `LIN-012` | TRAZABLE ($0 delta) |

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[KNOWLEDGE_LINEAGE_INDEX_V1]]
- Mapeo de navegación: `knowledge/lineage/INDEX.md`
