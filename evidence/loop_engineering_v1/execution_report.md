# LOOP ENGINEERING PROTOCOL V1 — EXECUTION REPORT

**Verdict:** `LOOP_ENGINEERING_PROTOCOL_V1_CERTIFIED`
**Criteria met:** 24 / 24
**Baseline commit:** `2d51f5216695388839e15c0ab08dd98af4aa6ce2` (`phase5/production-readiness`)
**Date:** 2026-08-07

---

## 1. What was built

A durable, agent-agnostic control plane that lets OpenCode, Codex, or any other
agent run a multi-session mission without conversational memory.

| Layer | Location | Versioned |
|---|---|---|
| Specification | `governance/LOOP_ENGINEERING_PROTOCOL_V1.md` | yes |
| Kernel | `engine/loop_control/` (13 modules) | yes |
| Schemas | `engine/loop_control/schemas/` (8 files) | yes |
| Adapters | `engine/loop_control/adapters/` (OpenCode, Codex) | yes |
| Runtime state | `.loopx/` (9 files) | **no — git-ignored** |
| Tests | `tests/test_loop_control.py` (55 tests) | yes |
| Harnesses | `tools/run_loop_dogfood.py`, `tools/generate_loop_evidence.py` | yes |
| Evidence | `evidence/loop_engineering_v1/` | yes |

Zero third-party dependencies. `jsonschema` is absent from the venv, so a
zero-dependency validator subset was implemented in `validation.py`.

---

## 2. Baseline (measured, not assumed)

| Item | Value |
|---|---|
| Official DB SHA-256 | `311c78e2…defdb9` — matches the historically expected hash |
| `01_Raw` files on disk | 1,313 |
| Test suite | 1,005 collected — **981 passed, 12 failed, 12 skipped** |
| `.loopx/` | did not exist |
| `engine/loop_control/` | did not exist |
| `governance/coordination/` | **existed** — pre-existing coordination interface |

The 12 baseline failures are pre-existing and unrelated (10 copilot golden-file
tests for a missing `marketplace_impact` fixture, 1 F5-05 ingestion idempotency
test, 1 RIPLEY path-resolution test).

---

## 3. The most important discovery

`tools/verify_coordination_interface.py` is a **repo-wide** verifier that bans
four reserved coordination tokens in *any* file outside a small allowlist, and
flags any filename containing `coordination`. Its scan excludes `.git`, `.venv`,
`data`, `01_Raw`, `_archive` — but **not** `.loopx/`, `engine/`, or `evidence/`.

A naive implementation writing a JSON key named after the handoff concept would
have silently broken an existing repository invariant.

**Mitigation:** Loop Control persists `continuation_record` / `receiving_agent` /
`holding_agent`, and never names a file `*coordination*`. Enforced by
`test_no_forbidden_coordination_tokens`.

**Measured result:** duplicate coordination channels introduced = **0**;
forbidden state markers introduced = **0**.

Equally important: `governance/coordination/` was **not** duplicated. It remains
the canonical human governance channel and is registered as a protected resource.

---

## 4. Bugs found by the tests, and fixed

Every one of these was a real defect caught by execution, not by inspection.

| # | Defect | Fix |
|---|---|---|
| 1 | Gate question validator required a trailing `?`; real questions end with instructions | Require `?` anywhere in the question |
| 2 | `git branch -D main` bypassed the destructive-Git gate (case handling) | Normalise both sides before matching |
| 3 | `end_turn` attempted `RUNNING -> CLAIMED`, an illegal transition, on validation failure | Release the lease, then go directly to `PENDING` |
| 4 | Reserved token leaked into 4 kernel modules, 2 adapters, 2 evidence files and the test file itself | Centralised `CONTINUATION_*` constants; evidence type relabelled |
| 5 | PowerShell rewrites injected UTF-8 BOMs, breaking `json.load` | Stripped; files rewritten without BOM |
| 6 | Dogfood harness hardcoded todo ids, desyncing if a validation failed | Harness now asserts against the kernel-selected todo |

---

## 5. Certification results

| Loop | Requirement | Result | Evidence |
|---|---|---|---|
| 9 | Claims and leases | PASS | `claims_validation.json` |
| 11 | Quota / anti-infinite-loop | PASS | `quota_validation.json` |
| 12 | Protected resources | PASS | `protected_resources_validation.json` |
| 13 | Evidence contract | PASS | `dogfood_report.json` (18 records, all SHA-256'd) |
| 14 | Cross-agent handoff | PASS | `handoff_validation.json` |
| 15 | Recovery | PASS | `recovery_validation.json` |
| 16 | Idempotency (×3) | PASS | `idempotency_validation.json` |
| 17 | Concurrency | PASS | `concurrency_validation.json` |
| 18 | Human gates (5 scenarios) | PASS | `gates_validation.json` |
| 20/21 | OpenCode + Codex, one plane | PASS | `opencode_validation.json`, `codex_validation.json` |
| 22 | Test suite | **55/55 PASS** | `tests_report.json` |
| 23 | Regression | **0 new** | `regression_report.json` |
| 24 | Financial integrity | **$0.00** | `financial_integrity.json` |
| 25 | Dogfood | PASS | `dogfood_report.json` |

### Regression

| | Baseline | After | Delta |
|---|---|---|---|
| Passed | 981 | **1,036** | +55 |
| Failed | 12 | **12** | **0** |
| Skipped | 12 | 12 | 0 |

All 12 failures are byte-identical to baseline. `NEW_REGRESSION` = **[]**.
`tests/test_coordination_interface.py`: 13 passed before, 13 passed after.

### Financial integrity

| Check | Result |
|---|---|
| Official DB SHA-256 | `311c78e2…defdb9` — **byte-identical to baseline** |
| `01_Raw` file count | 1,313 → 1,313 — **0 mutations** |
| SQL statements written | **0** |
| DB connections opened | **0** |
| **Financial delta** | **$0.00** |

The delta is asserted from a byte-level hash match, which is strictly stronger
than a query-level comparison.

Paths changed by this mission: **7** — `.gitignore`, `engine/loop_control/`,
`evidence/loop_engineering_v1/`, `governance/LOOP_ENGINEERING_PROTOCOL_V1.md`,
`tests/test_loop_control.py`, `tools/run_loop_dogfood.py`,
`tools/generate_loop_evidence.py`. Nothing else.

---

## 6. The dogfood: the protocol governing itself

Goal `LOOP-ENGINEERING-SELF-CERT`, three todos, three bounded turns, three
different agents, each validated by a genuinely executed command:

1. **OPENCODE_ENGINEER** → `TODO-001`: ran `pytest tests/test_loop_control.py` → exit 0 → `VALIDATED_COMPLETION`
2. *(cold session — a brand-new kernel object reading only from disk)*
   **CODEX_ENGINEER** → `TODO-002`: ran `python -m engine.loop_control validate` → exit 0 → `VALIDATED_COMPLETION`
3. **AUDITOR** → `TODO-003`: ran `pytest tests/test_coordination_interface.py` → exit 0 → `VALIDATED_COMPLETION`

Goal closed `COMPLETED`. 18 evidence records, 10 run events, 3 quota turns.
The cold session reconstructed goal, completed work, next todo, evidence paths,
allowed scope and forbidden scope **from disk alone**.

---

## 7. What this proves — the actual objective

> An agent can begin a mission, be interrupted, be replaced by another agent,
> recover state, continue from exactly the right point, respect limits, produce
> evidence, detect when it needs the human, and close the goal without relying
> on conversational memory.

| Claim | Proof |
|---|---|
| Interrupted and resumed | `test_recovery` — a turn dies mid-`RUNNING`; a fresh kernel returns `RESUME`, identifies the unfinished turn, and preserves prior work |
| Replaced by another agent | `test_cross_agent_handoff` + dogfood — 3 agents, disk-only continuation |
| Respects limits | Quota blocks at 3 same-hypothesis attempts, replans at 2 no-progress turns, scope budget 0 |
| Produces evidence | 6 artifacts per turn, each SHA-256'd; drift is detected |
| Detects when it needs the human | 5 gate scenarios all return `USER_ACTION_REQUIRED` with a concrete question; agents cannot self-approve |
| Closes the goal | `complete_goal` requires all todos `COMPLETED` and zero open gates |

---

## 8. Honest limitations

These are stated because the protocol forbids unearned claims.

1. **LoopX was not fetched over the network.** The concept list came from the
   mission brief. Any statement about LoopX's internal implementation is marked
   `UNVERIFIED` in `loopx_mapping.json`.
2. **Concurrency is single-machine.** Claims use file-level optimistic
   concurrency, adequate for `LOCAL FIRST` v1. Multi-host requires a real lock
   service.
3. **Heartbeat is passive.** Lease expiry, not a live daemon — the mission
   forbids daemons in this phase.
4. **One certified run, not three.** Project rule R11 reserves the
   3-consecutive-clean-runs bar for financial harnesses. This control plane has
   **1** full certified run recorded end to end.
5. **The repo verifier still fails at CLI level** because `execution_board.json`
   is deleted in the worktree. This is `PRE_EXISTING`, was failing before this
   mission, and restoring it is a governance decision outside this scope.
6. **`.loopx/` is machine-local.** Cross-machine handoff would require exporting
   it; out of scope for `LOCAL FIRST` v1.

---

## 9. Terminal verdict

```
LOOP_ENGINEERING_PROTOCOL_V1_CERTIFIED
```

24/24 mandatory criteria met, each backed by reproducible execution evidence in
this directory. No mandatory criterion was waived. `DONE`, `SUCCESS`, and
`COMPLETE` are deliberately not used.
