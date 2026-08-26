# UNIVERSAL AGENT ADAPTER INTERFACE — Loop Engineering Protocol V1

**Specification:** `governance/UNIVERSAL_LOOP_ENGINEERING_PROTOCOL_V1.md`
**Implementation:** `engine/loop_control/adapter.py`

---

## 1. PURPOSE

Define a **minimal common interface** that all agent adapters (OpenCode, Codex, Claude Code, custom) must implement.

**Core principle:** Adapters do NOT control lifecycle. They delegate to `LoopKernel`.

---

## 2. ADAPTER CONTRACT

Every adapter implements:

```python
class AgentAdapter(ABC):
    def read_state(self, goal_id: str | None = None) -> dict
    def diagnose(self, goal_id: str) -> dict
    def claim_todo(self, goal_id: str, todo_id: str | None = None, hypothesis: str | None = None) -> TurnResult
    def check_write_intent(self, goal_id: str, todo_id: str, paths: list[str]) -> dict
    def execute_turn(self, goal_id: str, turn_id: str, todo_id: str, **kwargs) -> TurnCompletion
    def write_evidence(self, goal_id: str, turn_id: str, name: str, payload: dict, ...) -> dict
    def submit_transition(self, goal_id: str, turn_id: str, todo_id: str, result: str, ...) -> TurnCompletion
    def write_continuation(self, goal_id: str, turn_id: str, todo_id: str) -> dict
    def continue_or_stop(self, goal_id: str, turn_result: TurnResult) -> bool
```

---

## 3. TURN RESULT TYPES

```python
@dataclass
class TurnResult:
    started: bool
    turn_id: str | None
    result: str  # from closed enum
    todo: dict | None
    claim: dict | None
    precheck: dict | None
    open_gates: list[dict] | None
    question: str | None
    reason: str | None
    conflict_code: str | None  # STALE_LEASE | ACTIVE_CONFLICT | WRITE_SCOPE_OVERLAP
```

```python
@dataclass
class TurnCompletion:
    turn_id: str
    result: str
    todo: dict | None
    continuation_record: dict | None
    quota: dict | None
    next_todo: str | None
```

---

## 4. BOUNDED TURN FLOW (via adapter)

```python
adapter = get_adapter(kernel, agent_id)

# 1. Read state
state = adapter.read_state(goal_id)

# 2. Diagnose recovery
diag = adapter.diagnose(goal_id)

# 3. Claim todo (enters bounded turn)
turn = adapter.claim_todo(goal_id, hypothesis="my-hypothesis")

if not turn.started:
    # Handle: USER_ACTION_REQUIRED | BLOCKED | WAIT | QUOTA_EXHAUSTED | REPLAN_REQUIRED
    report(turn.result, turn.question, turn.reason)
    stop()

# 4. Check write intent before any file write
verdict = adapter.check_write_intent(goal_id, turn.todo["todo_id"], ["path/a.py"])
if not verdict["allowed"]:
    # Gate raised - surface verdict["gate_id"] and verdict["question"]
    stop()

# 5. Execute bounded work (agent-specific)
result = adapter.execute_turn(goal_id, turn.turn_id, turn.todo["todo_id"],
                              validation_passed=True, ...)

# 6. Submit transition (writes evidence, charges quota, publishes continuation)
completion = adapter.submit_transition(...)

# 7. Decide continuation
if not adapter.continue_or_stop(goal_id, turn):
    stop()
```

---

## 5. IMPLEMENTED ADAPTERS

| Adapter | Runtime | Class |
|---------|---------|-------|
| OpenCodeAdapter | opencode | `OpenCodeAdapter` |
| CodexAdapter | codex | `CodexAdapter` |
| ClaudeAdapter | claude | `ClaudeAdapter` |

All share the **same kernel** and **same control plane** (`.loopx/`).

---

## 6. FACTORY

```python
from engine.loop_control.adapter import get_adapter

adapter = get_adapter(kernel, "OPENCODE_ENGINEER")
```

---

## 7. PROHIBITED FOR ADAPTERS

- Implementing lifecycle logic (goal/todo/claim/quota transitions)
- Writing directly to `.loopx/` files
- Creating private state stores (`.opencode_state`, `.codex_state`, etc.)
- Resolving gates (human authority only)
- Inventing states outside closed enums

---

## 8. MARKETPLACE-SPECIFIC REMOVALS

The following marketplace-specific rules were **removed** from adapters:

- ❌ "Never touch `01_Raw/`, `data/db/meli_financial_v4.db`, `.git/`, `.agents/`, `governance/coordination/`"
- ❌ "Run the commands listed in `turn['todo']['validation']`"
- ❌ Financial core references (`engine/v4/`)

**Replaced with universal rules:**
- ✅ "Check write intent via `check_write_intent()` before any write"
- ✅ "Protected resources defined by ProjectPolicy"
- ✅ "Validation commands defined by ProjectPolicy"

---

## 9. TEST

```bash
python -m pytest tests/test_universal_adapters.py -q
```