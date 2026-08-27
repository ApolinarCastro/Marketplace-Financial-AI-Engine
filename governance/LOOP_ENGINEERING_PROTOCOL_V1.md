# LOOP ENGINEERING PROTOCOL V1

**Status:** CANONICAL SPECIFICATION
**Scope:** Agent control plane. Non-financial.
**Effective:** 2026-08-07
**Implementation:** `engine/loop_control/`
**Runtime state:** `.loopx/` (git-ignored)
**Evidence:** `evidence/loop_engineering_v1/`

---

## 0. PURPOSE

This protocol defines a durable, auditable, agent-agnostic control plane so that
OpenCode, Codex, Claude Code, or any other agent can execute a multi-session
mission without depending on conversational memory.

**Fundamental rule:**

> Chat memory is NOT project state.

Durable project state lives in files. Any agent can reconstruct the mission from
those files alone.

### 0.1 What this protocol is NOT

- It is **not** a financial engine.
- It does **not** replace `governance/coordination/` as the canonical human
  coordination channel.
- It does **not** introduce a second financial source of truth.
- It does **not** introduce a runtime dependency on LoopX.
- It does **not** run a daemon, scheduler, dashboard, or cloud service.

### 0.2 Relationship to `governance/coordination/`

`governance/coordination/` remains the **canonical human/agent governance channel**
(contract, registry, state, execution reports, reviews).

Loop Control is the **executable layer**: it enforces bounded turns, claims,
quota, evidence, and recovery mechanically. It is advisory with respect to
governance and never overrides it.

**Hard compatibility constraint.** `tools/verify_coordination_interface.py`
forbids four reserved coordination tokens in files outside its allowlist: the
uppercase current-task marker, and the double-quoted JSON forms of `handoff`,
`next_actor` and `current_owner`. It also flags filenames containing
`coordination` outside `governance/coordination/`. Therefore Loop Control:

- uses `continuation_record` instead of `handoff` as a JSON key,
- uses `receiving_agent` instead of `next_actor`,
- uses `holding_agent` instead of `current_owner`,
- never names a file `*coordination*`.

This constraint is enforced by `tests/test_loop_control.py::test_no_forbidden_coordination_tokens`.

---

## 1. GOVERNING PRINCIPLES

| Principle | Meaning |
|---|---|
| EVIDENCE FIRST | No transition is valid without evidence on disk. |
| BOUNDED EXECUTION | One agent execution = exactly one bounded turn. |
| DETERMINISTIC STATE | Closed state vocabulary. No dynamically invented states. |
| HUMAN AUTHORITY | Protected resources require a human gate. Agents cannot self-approve. |
| PEER AGENT COORDINATION | No permanent leader. Authority = goal + claim + write_scope + gate. |
| IDEMPOTENT WRITEBACK | Every mutating operation carries an `idempotency_key`. |
| REPRODUCIBLE VALIDATION | Completion requires a validation record, not an assertion. |
| FAIL CLOSED | Malformed state is rejected, never silently repaired. |

---

## 2. ENTITY CONTRACTS

### 2.1 Goal

| Field | Type | Required | Notes |
|---|---|---|---|
| `goal_id` | string | yes | Uppercase, `^[A-Z0-9_\-]{3,64}$` |
| `title` | string | yes | |
| `objective` | string | yes | What terminal outcome is being pursued |
| `scope` | string[] | yes | Path globs the goal may touch |
| `non_goals` | string[] | yes | Explicit exclusions |
| `created_at` | string | yes | ISO-8601 UTC, `Z` suffix |
| `status` | enum | yes | See §3.1 |
| `authority` | string | yes | Who authorized the goal |
| `protected_resources` | string[] | yes | Globs requiring a human gate |
| `completion_criteria` | string[] | yes | Must be non-empty |
| `updated_at` | string | no | |
| `revision` | integer | no | Optimistic concurrency counter |

### 2.2 Todo

| Field | Type | Required | Notes |
|---|---|---|---|
| `todo_id` | string | yes | `^[A-Z0-9_\-]{3,64}$` |
| `goal_id` | string | yes | Must reference an existing goal |
| `description` | string | yes | |
| `priority` | integer | yes | Lower = more urgent |
| `status` | enum | yes | See §3.2 |
| `claimed_by` | string \| null | yes | `agent_id` or null |
| `write_scope` | string[] | yes | Path globs this todo may write |
| `dependencies` | string[] | yes | `todo_id` list |
| `validation` | string[] | yes | Commands/checks proving completion |
| `evidence_required` | boolean | yes | |

### 2.3 Gate

| Field | Type | Required | Notes |
|---|---|---|---|
| `gate_id` | string | yes | |
| `goal_id` | string | yes | |
| `type` | enum | yes | `PROTECTED_RESOURCE`, `SCOPE_EXPANSION`, `DESTRUCTIVE_GIT`, `PRODUCTION_PUBLISH`, `QUOTA_RESET` |
| `reason` | string | yes | Must contain a concrete question |
| `required_authority` | string | yes | e.g. `HUMAN_OWNER` |
| `status` | enum | yes | `OPEN`, `APPROVED`, `REJECTED` |
| `created_at` | string | yes | |
| `resolved_at` | string \| null | yes | |
| `resolved_by` | string \| null | no | Must NOT be a registered `agent_id` |
| `question` | string | no | Explicit decision requested |

A gate whose `reason` does not state what decision is needed is invalid.
`"waiting for owner"` is not an acceptable reason.

### 2.4 Claim

| Field | Type | Required | Notes |
|---|---|---|---|
| `goal_id` | string | yes | |
| `todo_id` | string | yes | |
| `agent_id` | string | yes | Must be registered |
| `claimed_at` | string | yes | |
| `expires_at` | string | yes | `claimed_at + lease_seconds` |
| `write_scope` | string[] | yes | Copied from the todo |
| `revision` | integer | no | |
| `heartbeat_at` | string | no | |
| `released_at` | string | no | Present on historical claims |

Uniqueness key: `(goal_id, todo_id)` among **active** claims.

### 2.5 Evidence

| Field | Type | Required |
|---|---|---|
| `evidence_id` | string | yes |
| `goal_id` | string | yes |
| `todo_id` | string \| null | yes |
| `type` | string | yes |
| `path` | string | yes |
| `sha256` | string \| null | yes |
| `created_at` | string | yes |
| `validation_status` | enum | yes — `PASS`, `FAIL`, `UNVERIFIED` |

`PASS` is only permitted when the referenced file exists and its SHA-256 was
computed from the file on disk. Otherwise the status is `UNVERIFIED`.

### 2.6 Continuation Record (handoff)

Stored in `.loopx/handoff.json` under the key `continuation_record`.

| Field | Type | Required | Notes |
|---|---|---|---|
| `from_agent` | string | yes | |
| `to_agent` | string | yes | |
| `goal_id` | string | yes | |
| `completed` | string[] | yes | Completed `todo_id`s |
| `current_state` | string | yes | Human-readable situation |
| `evidence` | string[] | yes | Evidence paths |
| `blockers` | string[] | yes | |
| `files_changed` | string[] | yes | |
| `tests` | string[] | yes | |
| `next_todo` | string \| null | yes | |
| `allowed_scope` | string[] | yes | |
| `forbidden_scope` | string[] | yes | |
| `created_at` | string | yes | |

The receiving agent MUST be able to resume using only this record plus the
control plane files.

---

## 3. CANONICAL STATE VOCABULARY

State values are closed sets. An agent that writes a value outside these sets
causes a FAIL CLOSED rejection.

### 3.1 Goal status

`CREATED`, `ACTIVE`, `WAITING_HUMAN`, `BLOCKED`, `VALIDATING`, `COMPLETED`, `FAILED`, `CANCELLED`

Permitted transitions:

```
CREATED       -> ACTIVE | CANCELLED
ACTIVE        -> WAITING_HUMAN | BLOCKED | VALIDATING | FAILED | CANCELLED
WAITING_HUMAN -> ACTIVE | BLOCKED | CANCELLED
BLOCKED       -> ACTIVE | FAILED | CANCELLED
VALIDATING    -> COMPLETED | ACTIVE | FAILED
COMPLETED     -> (terminal)
FAILED        -> (terminal)
CANCELLED     -> (terminal)
```

### 3.2 Todo status

`PENDING`, `CLAIMED`, `RUNNING`, `VALIDATING`, `COMPLETED`, `BLOCKED`, `FAILED`

Permitted transitions:

```
PENDING    -> CLAIMED
CLAIMED    -> RUNNING | PENDING | BLOCKED | FAILED
RUNNING    -> VALIDATING | BLOCKED | FAILED | PENDING
VALIDATING -> COMPLETED | FAILED | RUNNING
BLOCKED    -> PENDING | FAILED
COMPLETED  -> (terminal)
FAILED     -> (terminal)
```

`VALIDATING -> COMPLETED` requires a validation evidence record with
`validation_status == "PASS"`.

### 3.3 Turn result

`VALIDATED_PROGRESS`, `VALIDATED_COMPLETION`, `REPAIR_REQUIRED`, `REPLAN_REQUIRED`,
`USER_ACTION_REQUIRED`, `WAIT`, `BLOCKED`, `HOST_FAILURE`, `VALIDATION_FAILED`,
`WRITEBACK_FAILED`, `QUOTA_EXHAUSTED`

### 3.4 Conflict codes

`STALE_LEASE`, `ACTIVE_CONFLICT`, `WRITE_SCOPE_OVERLAP`

### 3.5 Recovery decision

`RESUME`, `REPAIR`, `REPLAN`, `WAIT`, `BLOCK`

---

## 4. CONTROL PLANE LAYOUT

```
.loopx/                     # git-ignored, mutable runtime
    registry.json           # agents + protected resources + protocol version
    active_goal.json        # {"active_goal_id": <id|null>, "goals": {...}}
    todos.json              # {"todos": [...]}
    gates.json              # {"gates": [...]}
    claims.json             # {"active": [...], "history": [...]}
    quota.json              # {"goals": {<goal_id>: {...}}}
    run_history.jsonl       # append-only turn events
    evidence_index.json     # {"evidence": [...]}
    handoff.json            # {"continuation_record": {...}|null}
```

Versioned (public):

```
governance/LOOP_ENGINEERING_PROTOCOL_V1.md
engine/loop_control/**
evidence/loop_engineering_v1/**
```

No secrets and no financial row data may be written into `.loopx/`.

---

## 5. BOUNDED TURN PIPELINE

```
READ STATE
  -> CHECK GATE            (any OPEN gate for the goal => USER_ACTION_REQUIRED)
  -> CHECK QUOTA           (exhausted => QUOTA_EXHAUSTED)
  -> CLAIM TODO            (conflict => BLOCKED)
  -> CAPTURE PRE-EVIDENCE  (precheck.json)
  -> EXECUTE BOUNDED ACTION
  -> VALIDATE              (validation.json)
  -> CAPTURE POST-EVIDENCE (tests.json, diff.json)
  -> WRITEBACK             (idempotent, schema-validated)
  -> HANDOFF               (continuation record)
  -> DECIDE CONTINUATION   (typed TurnResult)
```

A turn may not claim additional todos. Any need to widen scope yields
`REPLAN_REQUIRED` or `USER_ACTION_REQUIRED`, never silent expansion.

---

## 6. QUOTA POLICY (V1 DEFAULTS)

```
max_same_hypothesis_attempts = 3
max_no_progress_turns        = 2
max_validation_failures      = 3
max_scope_expansions         = 0
```

Counters tracked per goal: `turns_consumed`, `failed_turns`, `no_progress_turns`,
`validation_failures`, `scope_expansions`, `hypothesis_attempts{}`.

Rules:

- No new evidence for 2 consecutive turns -> `REPLAN_REQUIRED`.
- Same hypothesis fails 3 times -> `BLOCKED`.
- Any scope expansion attempt -> `USER_ACTION_REQUIRED` (budget is 0).
- Validation failures reach 3 -> `QUOTA_EXHAUSTED`.

Quota may only be reset by an approved `QUOTA_RESET` gate.

---

## 7. PROTECTED RESOURCES

Registered by default:

```
01_Raw/**
data/db/meli_financial_v4.db
.git/**
.agents/**
governance/coordination/**
```

Any write intent matching a protected glob raises a `PROTECTED_RESOURCE` gate and
returns `USER_ACTION_REQUIRED`. Read-only access is permitted without a gate.

Destructive Git operations (`filter-repo`, `reset --hard`, `push --force`,
history rewrite) raise a `DESTRUCTIVE_GIT` gate unconditionally.

---

## 8. AGENT REGISTRY

Default peers:

| agent_id | role |
|---|---|
| `OPENCODE_ENGINEER` | implementation |
| `CODEX_ENGINEER` | implementation |
| `AUDITOR` | verification, read-mostly |
| `QA` | test execution |
| `RESEARCHER` | read-only investigation |

Each agent declares `agent_id`, `capabilities`, `allowed_write_scope`,
`protected_write_scope`, `runtime`, `status`.

There is no permanent leader. Authority is derived, never assumed from the
agent's name.

---

## 9. EVIDENCE CONTRACT

Per turn:

```
evidence/loop_engineering_v1/runs/<goal_id>/<turn_id>/
    precheck.json
    action.json
    validation.json
    tests.json
    diff.json
    handoff.json
```

Every artifact records SHA-256 where a concrete file is referenced.
An assertion without evidence is recorded as `UNVERIFIED` and never as `PASS`.

---

## 10. IDEMPOTENCY

Mutating operations accept an `idempotency_key`. A repeated key is a no-op that
returns the original result. This covers claim, writeback, quota spend,
completion, evidence registration, and run events.

Applying the same operation three times must not produce duplicate todos,
claims, evidence rows, completion events, quota consumption, or run events.

---

## 11. TERMINAL VERDICTS

Only three mission verdicts are permitted:

- `LOOP_ENGINEERING_PROTOCOL_V1_CERTIFIED`
- `PARTIAL_WITH_PROVEN_BLOCKER`
- `FAILED_WITH_EVIDENCE`

`DONE`, `SUCCESS`, and `COMPLETE` are prohibited while any mandatory criterion
is unmet.

---

## 12. CLI

```
python -m engine.loop_control status
python -m engine.loop_control goal
python -m engine.loop_control todos
python -m engine.loop_control claim <todo_id> --agent <agent_id>
python -m engine.loop_control handoff
python -m engine.loop_control validate
```

No dashboard. No daemon. No scheduler.
