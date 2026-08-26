# CODEX ADAPTER — Loop Engineering Protocol V1

**Agent id:** `CODEX_ENGINEER`
**Control plane:** `.loopx/` (the SAME plane OpenCode uses)
**Specification:** `governance/LOOP_ENGINEERING_PROTOCOL_V1.md`

The contract is **identical** to `OPENCODE_ADAPTER.md`. Only `agent_id` differs.

---

## 1. ONE CONTROL PLANE

There is no `.codex_state` and no `.opencode_state`.

```
.loopx/          <- shared, authoritative, git-ignored
```

Creating a Codex-private coordination store is a protocol violation. Both agents
read and write the same files, guarded by claims and leases.

---

## 2. Same pipeline

```
READ STATE -> CHECK GATE -> CHECK QUOTA -> CLAIM TODO -> PRE-EVIDENCE
  -> EXECUTE -> VALIDATE -> POST-EVIDENCE -> WRITEBACK -> HANDOFF -> CONTINUE
```

```python
from engine.loop_control import LoopKernel

kernel = LoopKernel()
turn = kernel.begin_turn(goal_id=GOAL, agent_id="CODEX_ENGINEER")
```

If OpenCode holds a live lease on that todo, `begin_turn` returns
`result="BLOCKED"` with `conflict_code="ACTIVE_CONFLICT"`. That is correct
behaviour, not an error to route around.

If the lease has expired, the code is `STALE_LEASE`. Recover deterministically:

```python
kernel.claims.claim(GOAL, todo_id, "CODEX_ENGINEER",
                    write_scope=todo["write_scope"], force_stale_takeover=True)
```

The prior claim is moved to `claims.history` and never deleted.

---

## 3. Receiving a handoff from OpenCode

```
.venv\Scripts\python.exe -m engine.loop_control handoff
```

The resume brief returns goal, completed todos, next todo, evidence paths,
blockers, open gates, allowed scope, and forbidden scope. That is sufficient to
continue with zero conversational context. If it is not sufficient, the previous
agent's handoff was defective — report it rather than guessing.

---

## 4. Returning a handoff to OpenCode

Set `next_agent="OPENCODE_ENGINEER"` in `end_turn`.

---

## 5. Governance interaction

`governance/coordination/` remains the canonical human governance channel and is
a protected resource. Loop Control never rewrites it automatically. Codex's role
as `gate_authority` in that channel is separate from Loop Control gates, which
require a **non-agent** human resolver.

---

## 6. Reserved vocabulary

`tools/verify_coordination_interface.py` forbids four reserved coordination
tokens outside its allowlist: the uppercase current-task marker, and the
double-quoted JSON forms of `handoff`, `next_actor` and `current_owner`.
Loop Control artifacts therefore use `continuation_record`, `receiving_agent`,
and `holding_agent`. Do not reintroduce the reserved keys into `.loopx/` or
`evidence/loop_engineering_v1/`; a test enforces this.
