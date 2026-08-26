# OPENCODE ADAPTER — Loop Engineering Protocol V1

**Agent id:** `OPENCODE_ENGINEER`
**Control plane:** `.loopx/` (shared — NOT private to OpenCode)
**Specification:** `governance/LOOP_ENGINEERING_PROTOCOL_V1.md`

This adapter does **not** reimplement the kernel. It tells OpenCode how to call it.

---

## 1. Read state first. Always.

```
.venv\Scripts\python.exe -m engine.loop_control status
```

If a continuation record exists, read the resume brief:

```
.venv\Scripts\python.exe -m engine.loop_control handoff
```

Never rely on conversation history. The control plane is the state.

---

## 2. Diagnose before acting

```
.venv\Scripts\python.exe -m engine.loop_control recover
```

Act on the returned decision:

| Decision | Action |
|---|---|
| `RESUME` | Continue with the indicated todo. |
| `REPAIR` | Recover the stale lease, then resume. |
| `REPLAN` | Do not retry. Report and request replanning. |
| `WAIT` | Stop. Report the open gate or pending validation. |
| `BLOCK` | Stop. Report the proven blocker. |

---

## 3. Execute exactly one bounded turn

```python
from engine.loop_control import LoopKernel

kernel = LoopKernel()
turn = kernel.begin_turn(goal_id=GOAL, agent_id="OPENCODE_ENGINEER", hypothesis="...")

if not turn["started"]:
    # USER_ACTION_REQUIRED | BLOCKED | WAIT | QUOTA_EXHAUSTED | REPLAN_REQUIRED
    # Report turn["result"] verbatim. Do not improvise a workaround.
    ...
```

Rules for the turn body:

1. Work **only** on `turn["todo"]["todo_id"]`. Do not claim additional todos.
2. Before writing any file, check the intent:

```python
verdict = kernel.check_write_intent(GOAL, todo_id, "OPENCODE_ENGINEER", ["path/a.py"])
if not verdict["allowed"]:
    # A gate was raised. Stop and surface verdict["gate_id"] with its question.
    ...
```

3. Never write outside `turn["todo"]["write_scope"]`. Scope budget is 0.
4. Never touch `01_Raw/`, `data/db/meli_financial_v4.db`, `.git/`, `.agents/`,
   or `governance/coordination/` without an APPROVED gate.
5. Run the commands listed in `turn["todo"]["validation"]`. Real execution only.
   Mock results may never be reported as PASS.

---

## 4. Close the turn with evidence

```python
kernel.end_turn(
    goal_id=GOAL,
    turn_id=turn["turn_id"],
    agent_id="OPENCODE_ENGINEER",
    todo_id=todo_id,
    result="VALIDATED_COMPLETION",   # closed enum only
    action_summary="what actually changed",
    validation_passed=True,          # must reflect real command output
    validation_detail={"command": "...", "exit_code": 0, "passed": 12},
    tests={"suite": "tests/test_loop_control.py", "passed": 30, "failed": 0},
    files_changed=["engine/loop_control/kernel.py"],
    next_agent="CODEX_ENGINEER",
)
```

`end_turn` writes `precheck/action/validation/tests/diff/handoff` under
`evidence/loop_engineering_v1/runs/<goal>/<turn>/`, charges quota idempotently,
transitions the todo, and publishes the continuation record.

`validation_passed=True` with no real command output is a protocol violation.

---

## 5. Continue or stop

Continue automatically only while:

- no gate is `OPEN`,
- quota `evaluate()` returns `OK`,
- a startable todo exists.

Stop immediately on `USER_ACTION_REQUIRED`, `BLOCKED`, `QUOTA_EXHAUSTED`, or
`VALIDATED_COMPLETION` of the goal. When stopping for a gate, quote the gate's
`question` verbatim. Never write "waiting for owner" without the question.

---

## 6. Prohibited

- Creating a private `.opencode_state`. There is exactly ONE control plane.
- Resolving a gate. `resolve()` rejects registered agent ids by design.
- Inventing a state or turn result outside the closed enums.
- Editing the financial core (`engine/v4/`) under this protocol without an RFC.
