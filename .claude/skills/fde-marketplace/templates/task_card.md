# Task Card — FDE Marketplace

**Task ID:** `TASK-XXXX`
**Phase:** `PHASE-X.Y`
**Date:** `YYYY-MM-DD`

---

## 1. 6-Q Summary

| Q | Answer |
|---|--------|
| **Q1** Process corrected | |
| **Q2** Decision enabled | |
| **Q3** Certified data used | |
| **Q4** Cost of error | |
| **Q5** Current state | |
| **Q6** Success demo | |

---

## 2. Scope

- **Files to modify:** (max 3, list exactly)
- **Tests to add:** (file + count)
- **Evidence to produce:** `evidence/fase_X/YYYY.json`

---

## 3. Pre-Conditions (Codex Verified)

- [ ] Phase X-1 CERTIFIED
- [ ] 6-Q approved by Codex
- [ ] Scoping checklist PASS
- [ ] Single task registered in `coordination_state.json`

---

## 4. Execution Log (OpenCode Updates)

| Time | Action | File | Status |
|------|--------|------|--------|
| | | | |

---

## 5. Test Results

```bash
# Regression
python -m pytest tests/ -x -q
# Result: ___/___ PASS

# Certification Gate
python -m pytest tests/test_certification_gate.py -v
# Result: ___/27 PASS

# New Tests
python -m pytest tests/test_XXXX.py -v
# Result: ___/___ PASS
```

---

## 6. Evidence Generated

| File | execution_id | Classification |
|------|--------------|----------------|
| | | |

---

## 7. Codex Verdict

- [ ] **APPROVED_TO_CONTINUE** — Next task authorized
- [ ] **REQUIRES_REMEDIATION** — Fixes needed (detail below)
- [ ] **BLOCKED_BY_EVIDENCE** — Evidence insufficient
- [ ] **REJECTED** — Governance violation
- [ ] **CERTIFIED** — 3 clean runs, gate PASS

**Remediation Notes:**

---

## 8. Next Task (if approved)

**Task ID:** `TASK-YYYY`
**Objective:**

---

**OpenCode Signature:** ________________ **Codex Signature:** ________________