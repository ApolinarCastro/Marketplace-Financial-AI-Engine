# 6-Q Decomposition Template

**Use this template BEFORE any technical work begins.**
Codex must approve the completed 6-Q before authorizing OpenCode execution.

---

## Task Identification

- **Task ID:** `TASK-XXXX` (from coordination_state.json)
- **Phase:** `PHASE-X.Y` (from Master Plan)
- **Objective (one sentence):**

---

## Q1: What real process is being corrected?

> Describe the actual business/financial process that is broken, incomplete, or uncertified.
> Reference specific marketplace(s), period(s), and current failure mode.

**Answer:**

---

## Q2: What decision must this enable?

> What concrete decision will the Owner (Apolinar) be able to make after this work?
> Examples: "Certify Ripley DTE coverage for audit", "Approve Phase 3 go-live", "Negotiate ML adjustment reduction"

**Answer:**

---

## Q3: What certified data does it use?

> List EXACT sources with certification status:
> - `marketplace_ledger_v1` (certified: 69/69 periods $0 delta)
> - `marketplace_cierre_financiero_v1` (certified: PARIS/RIPLEY $0, FALABELLA $12K ⚠️, ML structural)
> - `dte_truth_v1` (68 XMLs indexed, 0 matched to ledger)
> - RAW files: `01_Raw/RIPLEY/Documentos Recepcionados/` (407 XMLs, NOT certified)
> - Evidence: `governance/RIPLEY_XML_COVERAGE_DISCOVERY.md`

**Answer:**

---

## Q4: What is the cost of error?

> Quantify in dollars, audit risk, or operational impact.
> Examples: "$186.7M Ripley XML coverage uncertified → audit finding risk", "$35.8M RN overstatement if PosCobro paired not excluded"

**Answer:**

---

## Q5: What exists currently?

> Inventory current state: code, data, certifications, gaps.
> Reference specific files, test counts, evidence files.

**Answer:**

---

## Q6: How will success be demonstrated?

> Define measurable, verifiable acceptance criteria.
> Must include: test counts, evidence file paths, delta thresholds, certification gate requirements.

**Answer:**

---

## Codex Authorization

- [ ] All 6-Q answered in writing
- [ ] No contradictions with FOUNDATION_RESET / MASTER_PLAN / DEC-019
- [ ] Single task scope (no parallel capabilities)
- [ ] Owner priority confirmed

**Codex Verdict:** `AUTHORIZED` / `REQUIRES_REMEDIATION` / `BLOCKED`

**Authorized Task ID:** `TASK-XXXX`

**Date:** `YYYY-MM-DD`