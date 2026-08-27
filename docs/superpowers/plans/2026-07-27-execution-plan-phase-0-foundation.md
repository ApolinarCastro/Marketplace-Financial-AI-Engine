# [EXECUTION_PLAN_PHASE_0_FOUNDATION_V3] Master Implementation Plan (APPROVED)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Status:** ✅ APPROVED / MASTER PLAN  
**Goal:** Establish the master certified baseline and pure governance specifications for Phase 0 Foundation V3 (`EXECUTION_PLAN_PHASE_0_FOUNDATION_V3`), serving as the project's official Master Plan. Guarantees that all future financial AI evolution preserves the certified financial engine, consolidates knowledge, enforces auditability, and enables controlled expansion toward full financial reconciliation.

---

# LA REGLA DE ORO DEL PROYECTO

> [!CAUTION]
> ### REGLA DE ORO DE IMPLEMENTACIÓN Y CERTIFICACIÓN
> **"Ninguna capacidad podrá considerarse implementada si no existe:**
> 1. **Contrato de Datos**
> 2. **Evidencia Registrada**
> 3. **Trazabilidad Completa**
> 4. **Registro Canónico**
> 5. **Pruebas Automatizadas**
> 6. **Certificación Oficial (cuando aplique)"**

---

# UNIVERSAL REGISTRY HEADER STANDARD

Every canonical and governance registry MUST contain the following standardized metadata header:

```markdown
---
id: [REGISTRY-ID]
version: [VERSION, e.g. 1.0.0]
fecha: [YYYY-MM-DD]
estado: [ESPECIFICADO | IMPLEMENTADO | VALIDADO | CERTIFICADO]
owner: [NAME / ROLE]
ultima_revision: [YYYY-MM-DD]
dependencias: [DEP-01, DEP-02]
relacionado_con: [REF-01, REF-02]
---
```

---

# OFFICIAL PROJECT MASTER SEQUENCE

```
FASE 0 — Gobierno y Arquitectura (CURRENT)
        ↓
FASE 1 — Corrección de Deuda Técnica
        ↓
FASE 2 — KnowledgeOS + Dual Graph + Inventario
        ↓
FASE 3 — Contratos de Datos
        ↓
FASE 4 — XML / DTE
        ↓
FASE 5 — SAP
        ↓
FASE 6 — Liquidaciones Marketplace
        ↓
FASE 7 — Conciliación Bancaria
        ↓
FASE 8 — Financial Copilot Certificado
```

---

## Maturity Model Scale (Niveles 0–5)

| Nivel | Estado | Criterio |
| :--- | :--- | :--- |
| **0** | **Idea** | Concepto propuesto en inbox |
| **1** | **Especificado** | Documentado en especificaciones y contratos de datos |
| **2** | **Implementado** | Código escrito y funcional |
| **3** | **Validado** | Pruebas unitarias/integradas PASS |
| **4** | **Certificado** | Evidencia reproducible con execution_id y 3 clean runs |
| **5** | **Productivo** | En operación congelada sin regresión |

---

## Governance Deliverables (Phase 0 Foundation)

### Task 1: Master PMO, Baseline, Technical Debt & Decisions
**Files:**
- Create: `governance/PMO_REGISTRY_V1.md`
- Create: `governance/BASELINE_POST_SURGICAL_FIX.md`
- Create: `governance/SURGICAL_FIX_REGISTRY.md`
- Create: `governance/TECHNICAL_DEBT_REGISTRY_V1.md`
- Create: `governance/DECISION_REGISTRY_V1.md`
- Create: `governance/MATURITY_REGISTRY_V1.md`

- [ ] **Step 1: Write `PMO_REGISTRY_V1.md`**
  Establish master PMO audit registry tracking Objetivo, CAP, Estado, Evidencia, Dependencias, Riesgo, Responsable, Fecha, and Certificación across all work packages.
- [ ] **Step 2: Write `BASELINE_POST_SURGICAL_FIX.md`**
  Record branch `phase5/production-readiness`, commit `2d51f52`, official DB SHA256 `311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9`, worktree status, test baseline state, certified artifacts, and closed surgical fixes.
- [ ] **Step 3: Write `SURGICAL_FIX_REGISTRY.md`**
  Document `POST_F5_08_CLP_FORMAT_PARITY_FIX` and `POST_F5_08_DTE_COVERAGE_STATUS_RENDER_FIX` with exact cause, code changes, evidence, and verification.
- [ ] **Step 4: Write `TECHNICAL_DEBT_REGISTRY_V1.md`**
  Populate initial `TECHNICAL_DEBT_BACKLOG` with historical items `TD-001` through `TD-008`.
- [ ] **Step 5: Write `DECISION_REGISTRY_V1.md`**
  Establish architectural decision record (ADR) registry with fields ADR-ID, Fecha, Problema, Decisión, Alternativas descartadas, Justificación, Impacto, Estado, Referencias.
- [ ] **Step 6: Write `MATURITY_REGISTRY_V1.md`**
  Map system components and capabilities across Maturity Levels 0 to 5.

---

### Task 2: Architecture Registry and Data Contract Registry
**Files:**
- Create: `governance/ARCHITECTURE_REGISTRY_V1.md`
- Create: `governance/DATA_CONTRACT_REGISTRY_V1.md`

- [ ] **Step 1: Write `ARCHITECTURE_REGISTRY_V1.md`**
  Define official system map across all layers detailing components, responsibilities, dependencies, criticality, owner, and certification status.
- [ ] **Step 2: Write `DATA_CONTRACT_REGISTRY_V1.md`**
  Specify interface data contracts across Marketplace, RAW, XML, SAP, Settlement, Bank, Ledger, and Copilot specifying Origen, Destino, Campos, Llaves, Cardinalidad, Validaciones, Versión, Responsable, and Estado.

---

### Task 3: Evidence Registry and KnowledgeOS Specification
**Files:**
- Create: `governance/EVIDENCE_REGISTRY_V1.md`
- Create: `governance/KNOWLEDGE_OS_SPECIFICATION.md`

- [ ] **Step 1: Write `EVIDENCE_REGISTRY_V1.md`**
  Create evidence catalog schema specifying ID, Tipo, Origen, Archivo, Hash, Relacionado con, Certificación, and Estado.
- [ ] **Step 2: Write `KNOWLEDGE_OS_SPECIFICATION.md`**
  Detail directory taxonomy (`00_Inbox` to `99_Quarantine`), Obsidian navigation rules, 3-tier taxonomy (Inventory, Analysis, Consolidation), and Knowledge Lifecycle Pipeline (`INBOX → Clasificación → Inventario → Grafo → Canonical → Certificación → Obsidian → Archivo`).

---

### Task 4: Dual Graph Model, System Intelligence Layer, and Roadmap
**Files:**
- Create: `governance/DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md`
- Create: `governance/SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md`
- Create: `governance/END_TO_END_RECONCILIATION_ROADMAP_V1.md`

- [ ] **Step 1: Write `DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md`**
  Specify dual Knowledge Graph + Execution Graph architecture with 15 node types, 13 edge relation types, and technical debt impact path modeling (`TD-001`..`TD-008`).
- [ ] **Step 2: Write `SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md`**
  Specify `System Intelligence` layer architecture (`Financial Engine → Knowledge Layer → Dual Graph Layer → System Intelligence → Financial Copilot`).
- [ ] **Step 3: Write `END_TO_END_RECONCILIATION_ROADMAP_V1.md`**
  Document target 10-stage reconciliation pipeline.

---

### Task 5: Define Canonical Registries
**Files:**
- Create: `governance/KNOWLEDGE_CANONICAL_REGISTRY_V1.md`
- Create: `governance/CAPABILITY_REGISTRY_V1.md`
- Create: `governance/DATA_LINEAGE_REGISTRY_V1.md`
- Create: `governance/EXTERNAL_REFERENCE_ADOPTION_MATRIX_V1.md`
- Create: `governance/FINANCIAL_COPILOT_QUESTION_REGISTRY_V1.md`

- [ ] **Step 1: Write `KNOWLEDGE_CANONICAL_REGISTRY_V1.md`**
  Define canonical financial terms and single-source-of-truth definitions.
- [ ] **Step 2: Write `CAPABILITY_REGISTRY_V1.md`**
  Classify capabilities per FASE 1B-R11 into IMPLEMENTED, VALIDATED, and CERTIFIED.
- [ ] **Step 3: Write `DATA_LINEAGE_REGISTRY_V1.md`**
  Map complete data lineage from RAW through XML, SAP, Liquidaciones, Banco, Ledger, to Copilot.
- [ ] **Step 4: Write `EXTERNAL_REFERENCE_ADOPTION_MATRIX_V1.md`**
  Map external references and framework standards adoption matrix.
- [ ] **Step 5: Write `FINANCIAL_COPILOT_QUESTION_REGISTRY_V1.md`**
  Define exact evidence response chains for the 10 core financial questions.

---

## Verification Plan

### Automated Verification
- Verify official DuckDB hash matches `311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9`.
- Run `git status` to verify zero modified files in `data/db/`, `engine/`, or `api/` (pure governance specification mode).

### Manual Verification
- Review all generated `.md` governance specification files to ensure 100% alignment with `EXECUTION_PLAN_PHASE_0_FOUNDATION_V3` Master Plan.
