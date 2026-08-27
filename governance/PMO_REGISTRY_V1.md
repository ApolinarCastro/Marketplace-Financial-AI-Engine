---
id: PMO_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: TUKE Master Governance PMO
ultima_revision: 2026-07-27
dependencias: [EXECUTION_PLAN_PHASE_0_FOUNDATION_V3]
relacionado_con: [AGENTS.md, ARCHITECTURE_REGISTRY_V1, CAPABILITY_REGISTRY_V1]
---

# REGISTRO MAESTRO DE PMO Y CONTROL AUDITABLE V1

## Propósito
Constituir el centro de control maestro y auditoría del **Marketplace Financial AI Engine**. Registra todos los paquetes de trabajo, objetivos, capacidades, estados de avance real, evidencias auditables, riesgos, dependencias y certificaciones oficiales bajo la norma **Strict Governance First**.

---

## Regla de Oro del Proyecto

> [!CAUTION]
> ### REGLA DE ORO DE IMPLEMENTACIÓN Y CERTIFICACIÓN
> **Ninguna capacidad podrá considerarse implementada si no existe:**
> 1. **Contrato de Datos**
> 2. **Evidencia Registrada**
> 3. **Trazabilidad Completa**
> 4. **Registro Canónico**
> 5. **Pruebas Automatizadas**
> 6. **Certificación Oficial (cuando aplique)**

---

## Matriz de Paquetes de Trabajo (Work Packages & Control Units)

| ID | Objetivo | CAP Asociado | Estado | Nivel Madurez | Evidencia | Dependencias | Riesgo | Responsable | Fecha | Certificación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WP-F0-01** | Infraestructura de Gobierno & Baseline Post Fix | CAP-F0-01 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/BASELINE_POST_SURGICAL_FIX.md` | Ninguna | NULO | PMO Lead | 2026-07-27 | PENDIENTE |
| **WP-F0-02** | Registro Maestro de Fixes Quirúrgicos | CAP-F0-02 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/SURGICAL_FIX_REGISTRY.md` | WP-F0-01 | NULO | Lead QA | 2026-07-27 | PENDIENTE |
| **WP-F0-03** | Backlog Histórico de Deuda Técnica | CAP-F0-03 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/TECHNICAL_DEBT_REGISTRY_V1.md` | WP-F0-01 | BAJO | Debt Reviewer | 2026-07-27 | PENDIENTE |
| **WP-F0-04** | Registro de Decisiones de Arquitectura (ADR) | CAP-F0-04 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/DECISION_REGISTRY_V1.md` | WP-F0-01 | NULO | Chief Architect | 2026-07-27 | PENDIENTE |
| **WP-F0-05** | Modelo de Madurez de Componentes | CAP-F0-05 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/MATURITY_REGISTRY_V1.md` | WP-F0-01 | NULO | PMO Lead | 2026-07-27 | PENDIENTE |
| **WP-F0-06** | Especificación de Arquitectura de Sistemas | CAP-F0-06 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/ARCHITECTURE_REGISTRY_V1.md` | WP-F0-01 | BAJO | Solution Architect | Pending Task 2 | PENDIENTE |
| **WP-F0-07** | Especificación de Contratos de Datos | CAP-F0-07 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/DATA_CONTRACT_REGISTRY_V1.md` | WP-F0-06 | MEDIO | Data Architect | Pending Task 2 | PENDIENTE |
| **WP-F0-08** | Especificación del Catálogo de Evidencias | CAP-F0-08 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/EVIDENCE_REGISTRY_V1.md` | WP-F0-01 | NULO | Evidence Guardian | Pending Task 3 | PENDIENTE |
| **WP-F0-09** | Especificación KnowledgeOS y Pipeline | CAP-F0-09 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/KNOWLEDGE_OS_SPECIFICATION.md` | WP-F0-01 | NULO | Knowledge Eng | Pending Task 3 | PENDIENTE |
| **WP-F0-10** | Especificación Dual Graph Model | CAP-F0-10 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md` | WP-F0-06, WP-F0-09 | BAJO | Graph Architect | Pending Task 4 | PENDIENTE |
| **WP-F0-11** | Especificación System Intelligence Layer | CAP-F0-11 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md` | WP-F0-10 | BAJO | AI Architect | Pending Task 4 | PENDIENTE |
| **WP-F0-12** | Hoja de Ruta de Conciliación Integral | CAP-F0-12 | ESPECIFICADO | Nivel 1 (Especificado) | `governance/END_TO_END_RECONCILIATION_ROADMAP_V1.md` | WP-F0-07 | NULO | Lead Financial Eng | Pending Task 4 | PENDIENTE |
| **WP-F0-13** | Registros Canónicos Financieros & Copilot | CAP-F0-13 | CERTIFICADO | Nivel 4 (Certificado) | `governance/FINANCIAL_COPILOT_QUESTION_REGISTRY_V1.md` | WP-F0-07, WP-F0-11 | MEDIO | Single Truth Agent | 2026-07-27 | CERTIFICADO |
| **WP-F1-01** | Corrección Deuda Técnica Suites & Ingesta | CAP-TD-001 | CERTIFICADO | Nivel 4 (Certificado) | `evidence/fase_1b/CAP-TD-001.json` | TD-001 | BAJO | Lead QA & Engine Arch | 2026-07-27 | CERTIFICADO |
| **WP-F1-02** | Contratos de Datos API & Pydantic v2 | CAP-TD-002 | CERTIFICADO | Nivel 4 (Certificado) | `evidence/fase_1b/CAP-TD-002.json` | TD-002 | MEDIO | API & Solution Arch | 2026-07-27 | CERTIFICADO |
| **WP-F1-03** | Unificación Módulo de Formateo UI | CAP-TD-003 | CERTIFICADO | Nivel 4 (Certificado) | `evidence/fase_1b/CAP-TD-003.json` | TD-003 | MEDIO | Frontend & UX Lead | 2026-07-27 | CERTIFICADO |
| **WP-F1-04** | Despliegue Estructura KnowledgeOS | CAP-TD-004 | CERTIFICADO | Nivel 4 (Certificado) | `evidence/fase_1b/CAP-TD-004.json` | TD-004 | MEDIO | Knowledge Engineer | 2026-07-27 | CERTIFICADO |
| **WP-F1-05** | Data Lineage & Integración Canónica | CAP-TD-005 | CERTIFICADO | Nivel 4 (Certificado) | `evidence/fase_1b/CAP-TD-005.json` | TD-005 | ALTO | Senior Data Engineer | 2026-07-27 | CERTIFICADO |
| **WP-F1-06** | Normalización Canónica 10 Preguntas Copilot | CAP-TD-006 | CERTIFICADO | Nivel 4 (Certificado) | `evidence/fase_1b/CAP-TD-006.json` | TD-006 | CRÍTICO | AI & Copilot Architect | 2026-07-27 | CERTIFICADO |
| **WP-F1-07** | Grafo Dual Ejecutable y Conexión de Nodos | CAP-TD-007 | CERTIFICADO | Nivel 4 (Certificado) | `evidence/fase_1b/CAP-TD-007.json` | TD-007 | MEDIO | Graph Architect | 2026-07-27 | CERTIFICADO |
| **WP-F1-08** | RAW Files Indexing & Integrity Registry | CAP-TD-008 | CERTIFICADO | Nivel 4 (Certificado) | `evidence/fase_1b/CAP-TD-008.json` | TD-008 | ALTO | Senior Data Engineer | 2026-07-27 | CERTIFICADO |
| **WP-F2-01** | Baseline Ejecutable de Conciliación End-to-End | CAP-F2-001 | CERTIFICADO | Nivel 4 (Certificado) | `evidence/fase_2/CAP-F2-001.json` | N/A | CRÍTICO | Financial & Lead Arch | 2026-07-27 | CERTIFICADO |

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:PMO_REGISTRY_V1` (Tipo: `Registro_Gobierno`)
- `Node:REGLA_DE_ORO` (Tipo: `Regla_Sistema`)
- `Node:WORK_PACKAGE_CATALOG` (Tipo: `Catalogo_Control`)

### Execution Graph Nodes
- `ExecNode:PMO_AUDIT_CHECK` (Process: Auditar estado de paquetes de trabajo y entregables en CI/CD)
- `ExecNode:GOVERNANCE_GATE` (Process: Bloquear transición de fase sin certificación 100%)

---

## Trazabilidad y Relaciones
- **IMPLEMENTA**: [EXECUTION_PLAN_PHASE_0_FOUNDATION_V3](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/docs/superpowers/plans/2026-07-27-execution-plan-phase-0-foundation.md)
- **DEPENDE_DE**: [AGENTS.md](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/AGENTS.md)
- **CERTIFICA**: Baseline certificado de gobierno Fase 0
- **AFECTA**: Todas las fases futuras (Fase 1 a Fase 8)

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[PMO_REGISTRY_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/PMO_REGISTRY_V1.md`
