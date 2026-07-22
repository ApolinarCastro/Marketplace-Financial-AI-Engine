# Prototype Spec Template

**1 page. Required for every Phase 2 prototyping task.**

---

## Task Reference

**Task ID:** `TASK-XXXX`
**Scoping Report:** `governance/coordination/TASK-XXXX_scoping_report.md`
**6-Q:** `governance/coordination/TASK-XXXX_6q.md`

---

## 1. Integration Plan (Code-Level)

### 1.1 Files to Modify (Max 3)

| File | Change Type | Lines | Risk |
|------|-------------|-------|------|
| | | | |

### 1.2 New Files (Max 2)

| File | Purpose | Tests |
|------|---------|-------|
| | | |

### 1.3 Public Contracts Used

| Contract | Method | Params | Return |
|----------|--------|--------|--------|
| FinancialEngine | | | |
| LedgerEngine | | | |
| ReconciliationEngine | | | |
| CertificationEngine | | | |
| EvidenceOrchestrator | | | |

---

## 2. Eval Baseline (Before/After)

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Query latency (P95) | ms | ms | `test_copilot_benchmarks.py` |
| Evidence completeness | % | % | `EvidenceOrchestrator.get_evidence_chain()` |
| Certification gate | PASS/FAIL | PASS | `test_certification_gate.py` |
| Regression count | N | 0 | Full suite |

---

## 3. Test Plan (TDD — Tests Written FIRST)

| Test File | Test Function | Expected Behavior |
|-----------|---------------|-------------------|
| | | |
| | | |

**Test command:**
```bash
python -m pytest tests/test_XXXX.py::test_XXXX -v
```

---

## 4. Evidence Generation

```bash
# For certification tasks
python tools/validate_fase_1b.py --task TASK-XXXX --output evidence/fase_1b/TASK-XXXX_<timestamp>.json
```

**Expected evidence fields:**
- `execution_id`: UUID
- `commit`: git SHA
- `timestamp`: ISO8601
- `harness_version`: "1.0.0-r5"
- `unique_tests`: integer
- `aggregate_executions`: integer
- `implementation_status`: IMPLEMENTED/VALIDATED/VERIFIED/CERTIFIED

---

## 5. Rollback Plan

| Step | Command | Verification |
|------|---------|--------------|
| 1 | `git checkout <commit_before_task>` | `git status` clean |
| 2 | `python -m pytest tests/test_certification_gate.py -v` | 27/27 PASS |
| 3 | `python -m pytest tests/ -x -q` | Full regression PASS |

---

## 6. Definition of Done

- [ ] All tests written FIRST (RED)
- [ ] Implementation minimal (GREEN)
- [ ] Full regression PASS (273+/273+)
- [ ] Certification Gate PASS (27/27)
- [ ] Evidence JSON generated with required fields
- [ ] No financial logic in frontend
- [ ] DEC-019 respected
- [ ] Single Financial Truth maintained
- [ ] Modified files reported

**OpenCode Completion Report:** ________________ **Date:** ________________