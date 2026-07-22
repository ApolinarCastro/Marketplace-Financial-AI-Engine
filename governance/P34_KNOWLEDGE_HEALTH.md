# P34 — Knowledge Health

**Date:** 2026-07-09
**Scope:** governance/, knowledge/, knowledge_index.yaml, AGENTS.md

---

## 1. Governance Documents (governance/)

### 1.1 Overview

| Metric | Value |
|---|---|
| Total files | 356 |
| Total size | ~1.39 MB |
| VIGENTE | 286 (80.3%) |
| HISTÓRICO | 50 (14.0%) |
| OBSOLETO | 14 (3.9%) |
| DUPLICADO | 6 (1.7%) |

### 1.2 Obsoletos (14 files)

14 archivos contienen conclusiones invalidadas o explícitamente rechazadas:

| File | Size | Reason |
|---|---|---|
| `PARIS_DUPLICATE_FINAL_CERTIFICATION.md` | 4,611 | Error $21.2M/1,573 grupos (DEC-020, sobrestimó 93%) |
| `PARIS_DUPLICATE_FINANCIAL_SIMULATION.md` | 3,836 | Alimentó la conclusión errónea |
| `PARIS_DUPLICATE_INVARIANTS.md` | 2,695 | Parte de análisis erróneo |
| `PARIS_DUPLICATE_REMOVAL_CANDIDATES.md` | 6,589 | Parte de análisis erróneo |
| `PARIS_DUPLICATE_ROOT_CAUSE_CERTIFICATION.md` | 3,447 | Parte de análisis erróneo |
| `PARIS_DUPLICATES_FORENSIC_REPORT.md` | 6,347 | Parte de análisis erróneo |
| `PARIS_ECONOMIC_MODEL_COMPARISON.md` | 4,547 | V1, INVALIDATED por V2 |
| `PARIS_ECONOMIC_MODEL_FINAL_CERTIFICATION.md` | 3,824 | V1 final, INVALIDATED por V2 |
| `RIPLEY_GROSS_REVENUE_CERTIFICATION.md` | 8,477 | **RECHAZADO** en título, día-parsing gap |
| `EVENT_REGISTRY_V1.md` | 16,782 | Superseded by `knowledge/core/EVENT_REGISTRY_V2.md` |
| `MARKETPLACE_CHARGE_RECONCILIATION_CERTIFICATION.md` | 15,282 | V1, superseded by V2 |
| `PARIS_DUPLICATE_FINAL_CERTIFICATION.md` (subdir) | 4,611 | Duplicado |
| `PARIS_BUSINESS_MODEL_FINAL_CERTIFICATION.md` | var | INVALIDATED by V3 per AGENTS.md |

### 1.3 Históricos (50 files)

- `archive/` (4 files): V5-era data, archived explicitly
- `certifications/` (3 files): Pre-lock snapshots
- `FCG_REPORTS/` (19 files): One-time certification gate artifacts
- `CIERRE_FINANCIERO_*.md` (3 files): DRAFT plans, never implemented
- `RFC-001-RIPLEY-*`, `RFC-PARIS-XML-*`: RFCs whose implementation is complete
- `MATRIZ_REMEDIACION_V6.md`: V6 remediation, completed
- `P22Z_PROJECT_CLOSURE.md`: Baseline already established
- `POSCOBRO_PAIRED_REMOVAL_EXECUTION_PLAN.md`: DEC-019 already executed
- `FRONTEND_BACKEND_RECONCILIATION_REPORT.md`: Issues resolved in 12C-12F
- `PHASE_12B_FRONTEND_ALIGNMENT_REPORT.md`: Issues resolved
- `EVIDENCE_EXPLORER_UX_SPEC.md`: Never implemented as separate feature
- `EXECUTIVE_MARKETPLACE_SCORECARD.md`: Superseded by implemented dashboard
- `FINANCIAL_EVIDENCE_CHAIN_DESIGN.md`: Fully implemented in Phase 12
- `KNOWLEDGE_BASE_BLUEPRINT.md`: Superseded by Phase 12.6 implementation
- `OBSIDIAN_GOVERNANCE_MODEL.md`: Design concept, never implemented
- `PRODUCTION_DECISION.md`, `PRODUCTION_GO_NOGO.md`, `PRODUCTION_IMPACT_SIMULATION.md`: One-time assessments
- `PYTHON_EXPERT_CODE_REVIEW.md`: One-time code review
- `RCA_ENCODING_BUG.md`: Bug already fixed
- `S2_RISK_ASSESSMENT.md`: One-time survey
- `SHOPIFY_READINESS_V2.md`: Shopify not yet active
- `BASELINE_STATUS.txt`, `FREEZE_ACTIVO.txt`: Baseline already set
- `BEFORE_AFTER_DASHBOARD_EVIDENCE.md`: Evidence of past state
- `BPP_RESIDUAL_CERTIFICATION.md`, `BPP_RESIDUAL_FIX_REPORT.md`: Fix already applied
- `CHANGE_LOG.md`, `CHANGE_TEMPLATE.txt`: Barely maintained
- `DECISIONS_LOG.md` (reclassified): Has 1,647 bytes but only 5 decisions vs governance/decisions/ with structured DEC files
- `DOCUMENT_CONSISTENCY_AUDIT.md`: One-time T2 pre-flight
- `GIT_STRATEGY.md`: Strategy already established
- `GOVERNANCE_LAYER_V1.md`: Superseded by knowledge/core/
- `INCIDENT_PROTOCOL.txt`: Superseded by AGENTS.md procedures
- `INDEX_VALIDATION_REPORT.md`: One-time
- `execute_remediation.py`: One-time script, already run

### 1.4 Duplicados (6 files)

| Files | Issue |
|---|---|
| `SKILLS_REGISTRY.json` (1,844B) + `SKILLS_REGISTRY.md` (1,839B) | Same data, different format. Both superseded by SKILLS_REGISTRY_V1.md |
| `phase12b_raw.json` (11,079B) + `phase12b_raw_results.json` (11,777B) | Raw analysis artifacts. Findings absorbed into PHASE_12B_* reports |

---

## 2. KnowledgeBase (knowledge/)

### 2.1 Overview

| Metric | Value |
|---|---|
| Total files | 110 |
| Total size | ~190 KB |
| PERMANENT | 88 (80.0%) |
| ELIMINABLE | 25 (22.7%) |
| ARCHIVABLE | 14 (12.7%) |
| Empty directories | 2 (RFC/, Skills/) |

### 2.2 Core Knowledge Files (88 permanentes)

Key clusters:

**Architecture (21 files):**
- `CONCEPT_REGISTRY_V2.md` (23KB) — 96 concepts, universal catalog **CORE**
- `EVENT_REGISTRY_V2.md` (9KB) — Universal event roles, causality rules R001-R007 **CORE**
- `CASH_ROLE_REGISTRY_V1.md` (10KB) — Cash role assignments per MP **CORE**
- `FINANCIAL_GOVERNANCE_CORE_V1.md` (5KB) — Pipeline rules **CORE**
- 3 abstract frameworks (Cash Reality, Event Model, Traceability)
- RIPLEY ETL contract + transformation spec (active implementation refs)
- 12 supporting files (gap analysis, field mapping, templates)

**Audits (5 files):**
- `POSCOBRO_FLOW_FINANCIAL_TRUTH.md` (5.7KB) — Authoritative flow analysis
- 4 UX12-related certifications

**Taxonomies (4 files):** **CORE**
- `ml_v1.json` (20KB) — 70/71 SIGNAL **CERTIFIED**
- `ripley_v1.json` (7KB) — 12/32 SIGNAL **CERTIFIED**
- `falabella_v1.json` (4.4KB) — 15/16 SIGNAL **CERTIFIED**
- `paris_v1.json` (3.8KB) — 14/15 SIGNAL **CERTIFIED**

**Marketplace models (16 files):**
- ML: 10 V1 model files (cash reality, conciliation, facturation, event model, etc.)
- RIPLEY: 20 validation/promotion files (operational detail)

### 2.3 Eliminables (25 files)

20 "Legacy [category] artifact" stub files + 5 tiny KO status files (one-liners):

- `Architecture/DOCUMENTARY_RECONCILIATION.md` (58B) — stub
- `Architecture/ECONOMIC_EVENT_TRUTH.md` (52B) — stub
- `Architecture/FINANCIAL_UI_RECONCILIATION.md` (67B) — stub
- `Architecture/SALE_TO_BANK_TRUTH.md` (50B) — stub
- `Audits/DOCUMENTARY_RECONCILIATION.md` (58B) — **DUPLICATE** of Architecture version
- `Audits/ECONOMIC_EVENT_TRUTH.md` (52B) — **DUPLICATE** of Architecture version
- `Audits/SALE_TO_BANK_TRUTH.md` (50B) — **DUPLICATE** of Architecture version
- `Audits/SEMANTIC_TRUTH_AUDIT.md` (52B) — stub
- `Certifications/BACKUP_CERTIFICATION.md` (60B) — stub
- `Certifications/FINANCIAL_UI_RECONCILIATION.md` (67B) — **DUPLICATE**
- `Certifications/KNOWLEDGE_CONTINUITY_CERTIFICATION.md` (74B) — stub
- `DEC/DEC-014_FRONTEND_ZERO_LOGIC.md` (56B) — stub
- `DEC/DEC-015_AJUSTES_RETENCIONES_NOT_RECONCILED.md` (71B) — stub
- `DEC/DEC-016_FINANCIAL_LABEL_TRUTH.md` (58B) — stub
- `DEC/DEC-019_POSCOBRO_PAIRED_REMOVAL.md` (60B) — stub
- `Playbooks/AUDIT_PLAYBOOK.md` (49B) — stub
- `Playbooks/CERTIFICATION_PLAYBOOK.md` (57B) — stub
- `Playbooks/DEPLOYMENT_PLAYBOOK.md` (54B) — stub
- `Playbooks/INCIDENT_RESPONSE_PLAYBOOK.md` (61B) — stub
- `Playbooks/ROLLBACK_PLAYBOOK.md` (52B) — stub
- `Certifications/KO-RI-DATA-0001.md` (70B) — one-liner
- `Certifications/KO-RI-DOMAIN-0001.md` (47B) — one-liner
- `Certifications/KO-RI-GAPS-0001.md` (95B) — one-liner
- `Certifications/KO-RI-VALIDATION-0001.md` (56B) — one-liner
- `Certifications/KO_TEMPLATE.md` (556B) — empty template

### 2.4 Archivable (14 files)

Empty templates or empty index files:

- 8 `Engines/*.md` files (all fields blank)
- 4 `Marketplace/{MP}.md` files (all fields blank)
- 2 `Indexes/INDEX_ARCHITECTURE.md`, `INDEX_INCIDENTS.md` (title only)

---

## 3. knowledge_index.yaml Status

### 3.1 Overview

19 entries total. 12 governance, 2 certification, 2 audit, 3 taxonomy.

### 3.2 Issues

| Issue | Details |
|---|---|
| **Missing core files** | No entries for CONCEPT_REGISTRY_V2, CASH_ROLE_REGISTRY_V1, EVENT_REGISTRY_V2, or any taxonomy JSON |
| **Missing ML model files** | 10 ML V1 model files not referenced |
| **DEC references don't resolve** | Index references DEC-009, DEC-020, DEC-022, DEC-024, DEC-025, DEC-026 with no `governance/decisions/` files matching |
| **No file paths** | Uses abstract IDs only — no link to actual files |
| **Manual only** | `yaml` file, zero automated update code |

---

## 4. Automated Learning

### Result: DOES NOT EXIST

- Zero Python files that consume audits, extract decisions, or update the knowledge base
- `knowledge_index.yaml` is maintained manually
- No pipeline to convert governance documents → knowledge entries
- No NLP/LLM component to summarize or classify new documents
- Tests (`test_knowledge.py`) only validate YAML syntax and entry structure — they do not auto-populate

### What is missing

A `KnowledgeLearningEngine` that would:

1. **Trigger**: After `run_audit()` completes, scan marketplace_auditoria_v1 for new findings
2. **Extract**: Parse governance markdown files for decision patterns (DEC-XXX, RFC titles, certification PASS/FAIL status)
3. **Index**: Auto-populate `knowledge_index.yaml` with new entries
4. **Cleanup**: Flag governance/ files whose content has been superseded or whose knowledge has been absorbed
5. **Track**: Maintain version history of knowledge (when a DEC was created, when a certification was superseded)

Currently, 356 governance files + 110 knowledge files = 466 markdown/json files representing ~1.58 MB of knowledge, all manually maintained with zero automation.

---

## 5. Health Summary

| Dimension | Status | Evidence |
|---|---|---|
| Governance completeness | 80.3% vigente | 286/356 files still current |
| KnowledgeBase content | 80.0% permanent | 88/110 files have substantive content |
| Index coverage | 43% miss rate | 19 indexed vs 38+ core files unindexed |
| Automation | **0%** | No auto-learning pipeline exists |
| Stub pollution | 22.7% of KB | 25 stub files with <100 bytes each |
| Repository debris | 85 files | 47.8 MB of temp/output/scratch at root |
| Cross-ref accuracy | **Broken** | Index references DECs without file paths |
