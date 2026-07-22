# Scoping Report Template

**Max 5 pages. Required for every Phase 1+ task.**

---

## 1. Executive Summary (½ page)

**Task ID:** `TASK-XXXX`
**Phase:** `PHASE-X.Y`
**Owner Priority:** `P0` / `P1` / `P2`

**One-sentence objective:**

**Key decision enabled:**

**Certified data sources used:**

**Estimated effort:** `X` days / `Y` OpenCode sessions

---

## 2. Stakeholder Map (RACI)

| Role | Name | Responsible | Accountable | Consulted | Informed |
|------|------|-------------|-------------|-----------|----------|
| Product Owner | Apolinar Castro | | ☐ | | ☐ |
| Technical Lead (Codex) | | | ☐ | | |
| Executor (OpenCode) | | ☐ | | | |
| Domain Expert | | | | ☐ | |
| Auditor | | | | | ☐ |

---

## 3. Pain Matrix (What's Broken)

| Pain Point | Marketplace | Period | Current State | Impact ($/Risk) | Certification Ref |
|------------|-------------|--------|---------------|-----------------|-------------------|
| | | | | | |
| | | | | | |

---

## 4. Concrete Specification

### 4.1 Inputs (Certified Only)

| Source | Table/Endpoint | Certification Status | Filter/Criteria |
|--------|----------------|---------------------|-----------------|
| Ledger | `marketplace_ledger_v1` | ✅ 69/69 $0 delta | `LOWER(financial_group) IN (...)` |
| Cierre | `marketplace_cierre_financiero_v1` | ✅ PARIS/RIPLEY $0 | `periodo = ?` |
| Taxonomy | `knowledge/taxonomy/*_v1.json` | ✅ DEC-033 certified | `signal_mode=SIGNAL` |
| Evidence | `EvidenceOrchestrator` | ✅ P40 FASE 2 | `get_evidence_chain(...)` |

### 4.2 Processing Logic (Pseudocode)

```
# NO financial calculations here — reference public contracts only
result = FinancialEngine.query_ledger(
    marketplace=mp,
    financial_group=group,
    signal_mode="SIGNAL",
    period=period
)
# ... orchestration only
```

### 4.3 Outputs

| Output | Format | Destination | Certification |
|--------|--------|-------------|---------------|
| | | | |

---

## 5. ROI & Risk

### 5.1 Quantified Benefit

| Metric | Current | Target | Delta | Source |
|--------|---------|--------|-------|--------|
| | | | | |

### 5.2 Cost of Error (from 6-Q Q4)

### 5.3 Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| | | | |

---

## 6. Recommendation

- [ ] **PROCEED** — Scope authorized, single task registered
- [ ] **REVISE** — 6-Q incomplete, rescope required
- [ ] **DEFER** — Dependencies not met (gate blocking)
- [ ] **REJECT** — Violates governance, no path forward

**Codex Authorization:** ________________ **Date:** ________________

**Owner Approval:** ________________ **Date:** ________________