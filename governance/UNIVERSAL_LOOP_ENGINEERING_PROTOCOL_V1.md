# UNIVERSAL LOOP ENGINEERING PROTOCOL V1

**Status:** CANONICAL SPECIFICATION
**Scope:** Universal agent control plane — domain-agnostic
**Extracted from:** Marketplace Financial AI Engine (certified pilot)
**Version:** 1.0.0

---

## 0. PURPOSE

This protocol defines a durable, auditable, agent-agnostic control plane so that
any agent (OpenCode, Codex, Claude Code, or custom) can execute a multi-session
mission without depending on conversational memory.

**Fundamental rule:**

> Chat memory is NOT project state.

Durable project state lives in files. Any agent can reconstruct the mission from
those files alone.

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
| DOMAIN AGNOSTIC | Core contains zero domain-specific logic. |

---

## 2. ARCHITECTURE

```
Project
  │
  ├── Project Policy
  │      ├── protected_resources
  │      ├── validation_commands
  │      ├── evidence_requirements
  │      ├── project_specific_gates
  │      └── quota_limits
  │
  ▼
Universal Loop Control Plane
  │
  ├── Goal
  ├── Todo
  ├── Claim
  ├── Lease
  ├── Gate
  ├── Quota
  ├── Evidence
  ├── Run History
  ├── Continuation Record
  └── Recovery
  │
  ├───────────────┬────────────────┐
  ▼               ▼                ▼
OpenCode         Codex          Custom Agent
```

**The Universal Core NEVER contains:**
- Marketplace, Financial, DTE, XML, SAP, DuckDB, ledger, reconciliation, classification
- Any project-specific resource paths
- Any project-specific validation logic

**The Project Policy CONTAINS:**
- Protected resource paths
- Allowed write scopes per agent
- Validation commands
- Evidence requirements
- Quota limits
- Human gate actions

---

## 3. ENTITY CONTRACTS

### 3.1 Goal

| Field | Type | Required |
|---|---|---|
| `goal_id` | string | yes |
| `title` | string | yes |
| `objective` | string | yes |
| `scope` | string[] | yes |
| `non_goals` | string[] | yes |
| `created_at` | string | yes |
| `status` | enum | yes |
| `authority` | string | yes |
| `protected_resources` | string[] | yes |
| `completion_criteria` | string[] | yes |
| `revision` | integer | no |

### 3.2 Todo

| Field | Type | Required |
|---|---|---|
| `todo_id` | string | yes |
| `goal_id` | string | yes |
| `description` | string | yes |
| `priority` | integer | yes |
| `status` | enum | yes |
| `claimed_by` | string \| null | yes |
| `write_scope` | string[] | yes |
| `dependencies` | string[] | yes |
| `validation` | string[] | yes |
| `evidence_required` | boolean | yes |
| `revision` | integer | no |

### 3.3 Gate

| Field | Type | Required |
|---|---|---|
| `gate_id` | string | yes |
| `goal_id` | string | yes |
| `type` | enum | yes |
| `reason` | string | yes |
| `question` | string | yes |
| `required_authority` | string | yes |
| `status` | enum | yes |
| `created_at` | string | yes |
| `resolved_at` | string \| null | yes |
| `resolved_by` | string \| null | no |

### 3.4 Claim

| Field | Type | Required |
|---|---|---|
| `goal_id` | string | yes |
| `todo_id` | string | yes |
| `agent_id` | string | yes |
| `claimed_at` | string | yes |
| `expires_at` | string | yes |
| `write_scope` | string[] | yes |
| `revision` | integer | no |
| `idempotency_key` | string \| null | no |

### 3.5 Evidence

| Field | Type | Required |
|---|---|---|
| `evidence_id` | string | yes |
| `goal_id` | string | yes |
| `todo_id` | string \| null | yes |
| `turn_id` | string \| null | yes |
| `type` | string | yes |
| `path` | string | yes |
| `sha256` | string \| null | yes |
| `created_at` | string | yes |
| `validation_status` | enum | yes |

### 3.6 Continuation Record

Stored under key `continuation_record`.

| Field | Type | Required |
|---|---|---|
| `goal_id` | string | yes |
| `from_agent` | string | yes |
| `receiving_agent` | string | yes |
| `completed` | string[] | yes |
| `current_state` | string | yes |
| `evidence` | string[] | yes |
| `blockers` | string[] | yes |
| `files_changed` | string[] | yes |
| `validation` | object | yes |
| `next_todo` | string \| null | yes |
| `allowed_scope` | string[] | yes |
| `forbidden_scope` | string[] | yes |
| `created_at` | string | yes |

---

## 4. CANONICAL STATE VOCABULARY

### 4.1 Goal Status

`CREATED`, `ACTIVE`, `WAITING_HUMAN`, `BLOCKED`, `VALIDATING`, `COMPLETED`, `FAILED`, `CANCELLED`

### 4.2 Todo Status

`PENDING`, `CLAIMED`, `RUNNING`, `VALIDATING`, `COMPLETED`, `BLOCKED`, `FAILED`

### 4.3 Turn Result

`VALIDATED_PROGRESS`, `VALIDATED_COMPLETION`, `REPAIR_REQUIRED`, `REPLAN_REQUIRED`,
`USER_ACTION_REQUIRED`, `WAIT`, `BLOCKED`, `HOST_FAILURE`, `VALIDATION_FAILED`,
`WRITEBACK_FAILED`, `QUOTA_EXHAUSTED`

### 4.4 Conflict Codes

`STALE_LEASE`, `ACTIVE_CONFLICT`, `WRITE_SCOPE_OVERLAP`

### 4.5 Recovery Decision

`RESUME`, `REPAIR`, `REPLAN`, `WAIT`, `BLOCK`

### 4.6 Gate Types

`PROTECTED_RESOURCE`, `SCOPE_EXPANSION`, `DESTRUCTIVE_OPERATION`, `PRODUCTION_PUBLISH`, `QUOTA_RESET`

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

---

## 6. QUOTA POLICY (DEFAULTS)

```
max_same_hypothesis_attempts = 3
max_no_progress_turns        = 2
max_validation_failures      = 3
max_scope_expansions         = 0
```

Configurable per project via ProjectPolicy.

---

## 7. PROJECT POLICY CONTRACT

Every project MUST provide a `ProjectPolicy` implementing:

```python
class ProjectPolicy:
    project_id: str
    project_root: Path
    protected_resources: list[str]
    allowed_write_scopes: dict[str, list[str]]  # agent_id -> scopes
    validation_commands: dict[str, list[str]]   # todo_id -> commands
    evidence_root: Path
    runtime_state_root: Path
    human_gate_actions: dict[str, callable]     # gate_type -> handler
    quota_limits: QuotaLimits
```

The universal kernel consumes this policy; it does not define it.

---

## 8. AGENT REGISTRY

Default peer model — no permanent leader:

| Field | Required |
|---|---|
| `agent_id` | yes |
| `runtime` | yes |
| `capabilities` | yes |
| `allowed_write_scope` | yes |
| `protected_write_scope` | yes |
| `status` | yes |

Authority derives from: **Goal + Claim + WriteScope + Gate**

---

## 9. RUNTIME STATE ROOT

Configurable. Default: `.loopx/`

Must support:
- `.loopx/`
- Custom directory
- Temporary isolated test directory

---

## 10. TERMINAL VERDICTS

Only three:
- `UNIVERSAL_LOOP_ENGINEERING_PROTOCOL_V1_CERTIFIED`
- `PARTIAL_WITH_PROVEN_BLOCKER`
- `FAILED_WITH_EVIDENCE`

`DONE`, `SUCCESS`, `COMPLETE` prohibited while mandatory criteria unmet.

---

## 11. CLI

```
python -m engine.loop_control status
python -m engine.loop_control goal
python -m engine.loop_control todos
python -m engine.loop_control claim <todo_id> --agent <agent_id>
python -m engine.loop_control handoff
python -m engine.loop_control validate
python -m engine.loop_control doctor
```

No dashboard. No daemon. No scheduler.