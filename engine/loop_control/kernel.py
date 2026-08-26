"""Loop Control Kernel.

Coordinates goals, todos, claims, gates, quota, evidence, continuation and
recovery into a single bounded turn.

Explicit non-responsibilities: no financial logic, no DTE matching, no
reconciliation, no classification, no Truth Engine, no Exception Engine, no SQL.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .claim_manager import ClaimManager
from .constants import (
    CONTINUATION_FILENAME,
    CONTINUATION_KEY,
    CONTINUATION_SCHEMA,
    DEFAULT_LEASE_SECONDS,
    PROTOCOL_VERSION,
    TURN_RESULTS,
    ClaimConflictError,
    LoopControlError,
)

# Artifact filename is mandated by the protocol spec; the evidence *type* label
# deliberately differs so the index never serializes a reserved coordination key.
CONTINUATION_ARTIFACT = CONTINUATION_FILENAME
CONTINUATION_TYPE = "continuation"
from .evidence_manager import EvidenceManager
from .gate_manager import GateManager
from .goal_manager import GoalManager
from .handoff_manager import HandoffManager
from .policy import ProjectPolicy
from .quota_manager import QuotaManager
from .recovery import RecoveryEngine
from .state_store import StateStore, find_repo_root, iso, new_id
from .todo_manager import TodoManager
from .validation import validate


class LoopKernel:
    def __init__(
        self,
        root: Path | str | None = None,
        repo_root: Path | None = None,
        project_policy: ProjectPolicy | None = None,
    ) -> None:
        self.repo_root = (repo_root or find_repo_root()).resolve()
        self.project_policy = project_policy
        self.store = StateStore(root if root is not None else self.repo_root)
        if not self.store.exists():
            self.store.initialize(project_policy=project_policy)
        self.goals = GoalManager(self.store)
        self.todos = TodoManager(self.store)
        self.claims = ClaimManager(self.store)
        self.gates = GateManager(self.store)
        self.quota = QuotaManager(self.store)
        self.evidence = EvidenceManager(self.store, repo_root=self.repo_root)
        self.handoff = HandoffManager(self.store)
        self.recovery = RecoveryEngine(self.store)

    # ------------------------------------------------------------- setup

    def initialize(self, force: bool = False) -> dict[str, Any]:
        return self.store.initialize(force=force, project_policy=self.project_policy)

    def registry(self) -> dict[str, Any]:
        return self.store.read("registry")

    def agent(self, agent_id: str) -> dict[str, Any]:
        # First check ProjectPolicy if available
        if self.project_policy:
            scopes = self.project_policy.allowed_write_scopes
            if agent_id in scopes:
                # Build agent record from policy
                return {
                    "agent_id": agent_id,
                    "allowed_write_scope": scopes[agent_id],
                    "protected_write_scope": self.project_policy.protected_resources,
                    "runtime": "any",
                    "status": "AVAILABLE",
                }
        # Fallback to registry
        for entry in self.registry().get("agents", []):
            if entry["agent_id"] == agent_id:
                return entry
        # Last resort: auto-register from project policy defaults if available
        if self.project_policy:
            scopes = self.project_policy.allowed_write_scopes
            if agent_id in scopes:
                return {
                    "agent_id": agent_id,
                    "allowed_write_scope": scopes[agent_id],
                    "protected_write_scope": self.project_policy.protected_resources,
                    "runtime": "any",
                    "status": "AVAILABLE",
                }
        raise LoopControlError(f"unregistered agent: {agent_id}")

    def register_agent(self, agent: dict[str, Any]) -> dict[str, Any]:
        required = {"agent_id", "capabilities", "allowed_write_scope", "protected_write_scope", "runtime", "status"}
        missing = required - set(agent)
        if missing:
            raise LoopControlError(f"agent record missing fields: {sorted(missing)}")
        registry = self.registry()
        for idx, existing in enumerate(registry["agents"]):
            if existing["agent_id"] == agent["agent_id"]:
                registry["agents"][idx] = agent
                break
        else:
            registry["agents"].append(agent)
        self.store.write("registry", registry)
        return agent

    # --------------------------------------------------------- run events

    def log_event(
        self,
        goal_id: str,
        agent_id: str,
        event_type: str,
        turn_id: str | None = None,
        todo_id: str | None = None,
        result: str | None = None,
        detail: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any] | None:
        if idempotency_key:
            for event in self.store.read_run_history():
                if event.get("idempotency_key") == idempotency_key:
                    return event
        event = {
            "event_id": new_id("EVT"),
            "goal_id": goal_id,
            "turn_id": turn_id,
            "todo_id": todo_id,
            "agent_id": agent_id,
            "event_type": event_type,
            "result": result,
            "detail": detail,
            "created_at": iso(),
            "idempotency_key": idempotency_key,
        }
        validate(event, "run_event")
        self.store.append_run_event(event)
        return event

    # -------------------------------------------------------- bounded turn

    def begin_turn(
        self,
        goal_id: str,
        agent_id: str,
        todo_id: str | None = None,
        lease_seconds: int = DEFAULT_LEASE_SECONDS,
        hypothesis: str | None = None,
    ) -> dict[str, Any]:
        """READ STATE -> CHECK GATE -> CHECK QUOTA -> CLAIM -> PRE-EVIDENCE."""
        self.agent(agent_id)

        goal = self.goals.get(goal_id)
        if goal is None:
            raise LoopControlError(f"unknown goal: {goal_id}")

        turn_id = new_id("TURN")

        open_gates = self.gates.open_gates(goal_id)
        if open_gates:
            self.log_event(goal_id, agent_id, "TURN_REJECTED", turn_id=turn_id,
                           result="USER_ACTION_REQUIRED",
                           detail=f"open gates: {[g['gate_id'] for g in open_gates]}")
            return {
                "started": False,
                "turn_id": turn_id,
                "result": "USER_ACTION_REQUIRED",
                "open_gates": open_gates,
                "question": open_gates[0].get("question"),
            }

        verdict = self.quota.evaluate(goal_id, hypothesis=hypothesis)
        if verdict["result"] != "OK":
            self.log_event(goal_id, agent_id, "TURN_REJECTED", turn_id=turn_id,
                           result=verdict["result"], detail=verdict["reason"])
            return {"started": False, "turn_id": turn_id, **verdict}

        if todo_id is None:
            candidate = self.todos.next_available(goal_id)
            if candidate is None:
                self.log_event(goal_id, agent_id, "TURN_REJECTED", turn_id=turn_id,
                               result="WAIT", detail="no startable todo")
                return {"started": False, "turn_id": turn_id, "result": "WAIT",
                        "reason": "no PENDING todo with satisfied dependencies"}
            todo_id = candidate["todo_id"]

        todo = self.todos.get(todo_id)
        if todo is None:
            raise LoopControlError(f"unknown todo: {todo_id}")
        if not self.todos.dependencies_met(todo_id):
            return {"started": False, "turn_id": turn_id, "result": "WAIT",
                    "reason": f"unmet dependencies: {todo['dependencies']}"}

        try:
            claim = self.claims.claim(
                goal_id=goal_id,
                todo_id=todo_id,
                agent_id=agent_id,
                write_scope=todo["write_scope"],
                lease_seconds=lease_seconds,
                idempotency_key=f"{goal_id}:{todo_id}:{agent_id}:{turn_id}",
            )
        except ClaimConflictError as exc:
            self.log_event(goal_id, agent_id, "CLAIM_CONFLICT", turn_id=turn_id,
                           todo_id=todo_id, result="BLOCKED", detail=f"{exc.code}: {exc}")
            return {"started": False, "turn_id": turn_id, "result": "BLOCKED",
                    "conflict_code": exc.code, "reason": str(exc)}

        if todo["status"] == "PENDING":
            self.todos.transition(todo_id, "CLAIMED", claimed_by=agent_id)
        self.todos.transition(todo_id, "RUNNING", claimed_by=agent_id)

        self.log_event(goal_id, agent_id, "TURN_START", turn_id=turn_id, todo_id=todo_id)

        precheck = {
            "turn_id": turn_id,
            "goal_id": goal_id,
            "todo_id": todo_id,
            "agent_id": agent_id,
            "protocol_version": PROTOCOL_VERSION,
            "goal_status": goal["status"],
            "todo_write_scope": todo["write_scope"],
            "validation_contract": todo["validation"],
            "lease_expires_at": claim["expires_at"],
            "hypothesis": hypothesis,
            "open_gates": [],
            "quota": self.quota.get(goal_id),
            "created_at": iso(),
        }
        self.evidence.write_artifact(goal_id, turn_id, "precheck", precheck,
                                     todo_id=todo_id, evidence_type="precheck")

        return {"started": True, "turn_id": turn_id, "result": "OK",
                "todo": self.todos.get(todo_id), "claim": claim, "precheck": precheck}

    def check_write_intent(self, goal_id: str, todo_id: str, agent_id: str, paths: list[str]) -> dict[str, Any]:
        todo = self.todos.get(todo_id)
        allowed = todo["write_scope"] if todo else None
        goal = self.goals.get(goal_id)
        protected = goal["protected_resources"] if goal else None
        return self.gates.check_write_intent(
            goal_id=goal_id, paths=paths, protected_resources=protected,
            allowed_scope=allowed, agent_id=agent_id,
        )

    def end_turn(
        self,
        goal_id: str,
        turn_id: str,
        agent_id: str,
        todo_id: str,
        result: str,
        action_summary: str,
        validation_passed: bool,
        validation_detail: dict[str, Any] | None = None,
        tests: dict[str, Any] | None = None,
        files_changed: list[str] | None = None,
        blockers: list[str] | None = None,
        next_agent: str | None = None,
        hypothesis: str | None = None,
        made_progress: bool = True,
    ) -> dict[str, Any]:
        """VALIDATE -> POST-EVIDENCE -> WRITEBACK -> HANDOFF -> CONTINUATION."""
        if result not in TURN_RESULTS:
            raise LoopControlError(f"invalid turn result '{result}'; must be one of {list(TURN_RESULTS)}")

        self.evidence.write_artifact(
            goal_id, turn_id, "action",
            {"turn_id": turn_id, "todo_id": todo_id, "agent_id": agent_id,
             "summary": action_summary, "files_changed": list(files_changed or []),
             "hypothesis": hypothesis, "created_at": iso()},
            todo_id=todo_id, evidence_type="action",
        )

        self.evidence.write_artifact(
            goal_id, turn_id, "validation",
            {"turn_id": turn_id, "todo_id": todo_id, "passed": validation_passed,
             "detail": validation_detail or {}, "created_at": iso()},
            todo_id=todo_id, evidence_type="validation",
            validation_status="PASS" if validation_passed else "FAIL",
        )

        self.evidence.write_artifact(
            goal_id, turn_id, "tests", {"turn_id": turn_id, "tests": tests or {}, "created_at": iso()},
            todo_id=todo_id, evidence_type="tests",
        )

        self.evidence.write_artifact(
            goal_id, turn_id, "diff",
            {"turn_id": turn_id, "files_changed": list(files_changed or []), "created_at": iso()},
            todo_id=todo_id, evidence_type="diff",
        )

        self.quota.spend(
            goal_id=goal_id,
            idempotency_key=f"quota:{goal_id}:{turn_id}",
            turn=1,
            failed=0 if validation_passed else 1,
            no_progress=0 if made_progress else 1,
            validation_failure=0 if validation_passed else 1,
            hypothesis=hypothesis,
        )

        if result == "VALIDATED_COMPLETION":
            if not validation_passed:
                raise LoopControlError("VALIDATED_COMPLETION requires validation_passed=True")
            self.todos.transition(todo_id, "VALIDATING", claimed_by=agent_id)
            self.complete_todo(goal_id, todo_id, agent_id)
        elif result in ("VALIDATION_FAILED", "REPAIR_REQUIRED", "REPLAN_REQUIRED",
                        "HOST_FAILURE", "WRITEBACK_FAILED"):
            self.claims.release(goal_id, todo_id, agent_id, reason=result)
            self.todos.transition(todo_id, "PENDING")
        elif result in ("BLOCKED", "USER_ACTION_REQUIRED", "QUOTA_EXHAUSTED", "WAIT"):
            self.todos.transition(todo_id, "BLOCKED", claimed_by=agent_id)
            self.claims.release(goal_id, todo_id, agent_id, reason=result)
        # VALIDATED_PROGRESS keeps the todo RUNNING and the lease held.

        next_todo = self.todos.next_available(goal_id)
        goal = self.goals.get(goal_id) or {}
        record = self.handoff.publish(
            goal_id=goal_id,
            from_agent=agent_id,
            to_agent=next_agent or agent_id,
            current_state=f"turn {turn_id} ended with {result}: {action_summary}",
            completed=[t["todo_id"] for t in self.todos.list(goal_id=goal_id, status="COMPLETED")],
            evidence=[r["path"] for r in self.evidence.list(goal_id=goal_id, turn_id=turn_id)],
            blockers=list(blockers or []),
            files_changed=list(files_changed or []),
            tests=[str(k) for k in (tests or {})],
            next_todo=next_todo["todo_id"] if next_todo else None,
            allowed_scope=next_todo["write_scope"] if next_todo else [],
            forbidden_scope=goal.get("protected_resources", []),
            turn_id=turn_id,
            idempotency_key=f"handoff:{goal_id}:{turn_id}",
        )

        self.evidence.write_artifact(goal_id, turn_id, CONTINUATION_ARTIFACT, {CONTINUATION_KEY: record},
                                     todo_id=todo_id, evidence_type=CONTINUATION_TYPE)

        self.log_event(goal_id, agent_id, "TURN_END", turn_id=turn_id, todo_id=todo_id,
                       result=result, detail=action_summary,
                       idempotency_key=f"turn_end:{goal_id}:{turn_id}")

        return {"turn_id": turn_id, "result": result,
                "todo": self.todos.get(todo_id),
                CONTINUATION_KEY: record,
                "quota": self.quota.get(goal_id),
                "next_todo": next_todo["todo_id"] if next_todo else None}

    # --------------------------------------------------------- completion

    def complete_todo(self, goal_id: str, todo_id: str, agent_id: str) -> dict[str, Any]:
        """Completion requires a PASS validation evidence record."""
        todo = self.todos.get(todo_id)
        if todo is None:
            raise LoopControlError(f"unknown todo: {todo_id}")
        if todo["status"] == "COMPLETED":
            return todo
        if todo["evidence_required"] and not self.evidence.has_passing_validation(goal_id, todo_id):
            raise LoopControlError(
                f"cannot complete {todo_id}: no validation evidence with status PASS. "
                "Completion requires reproducible validation."
            )
        if todo["status"] != "VALIDATING":
            self.todos.transition(todo_id, "VALIDATING", claimed_by=agent_id)
        completed = self.todos.transition(todo_id, "COMPLETED")
        self.claims.release(goal_id, todo_id, agent_id, reason="COMPLETED")
        self.log_event(goal_id, agent_id, "TODO_COMPLETED", todo_id=todo_id, result="VALIDATED_COMPLETION",
                       idempotency_key=f"complete:{goal_id}:{todo_id}")
        return completed

    def complete_goal(self, goal_id: str, agent_id: str) -> dict[str, Any]:
        todos = self.todos.list(goal_id=goal_id)
        outstanding = [t["todo_id"] for t in todos if t["status"] != "COMPLETED"]
        if outstanding:
            raise LoopControlError(f"cannot complete goal {goal_id}: outstanding todos {outstanding}")
        open_gates = self.gates.open_gates(goal_id)
        if open_gates:
            raise LoopControlError(f"cannot complete goal {goal_id}: open gates {[g['gate_id'] for g in open_gates]}")
        self.goals.transition(goal_id, "VALIDATING")
        goal = self.goals.transition(goal_id, "COMPLETED")
        self.log_event(goal_id, agent_id, "GOAL_COMPLETED", result="VALIDATED_COMPLETION",
                       idempotency_key=f"goal_complete:{goal_id}")
        return goal

    # ------------------------------------------------------------- status

    def status(self, goal_id: str | None = None) -> dict[str, Any]:
        active = self.goals.active()
        target = goal_id or (active["goal_id"] if active else None)
        payload: dict[str, Any] = {
            "protocol_version": PROTOCOL_VERSION,
            "control_plane": str(self.store.root),
            "active_goal_id": active["goal_id"] if active else None,
            "agents": [a["agent_id"] for a in self.registry().get("agents", [])],
            "goal": None,
            "todos": [],
            "open_gates": [],
            "active_claims": [],
            "conflicts": self.claims.detect_conflicts(),
            "quota": None,
            "recovery": None,
            CONTINUATION_KEY: self.handoff.current(),
        }
        if target:
            payload["goal"] = self.goals.get(target)
            payload["todos"] = self.todos.list(goal_id=target)
            payload["open_gates"] = self.gates.open_gates(target)
            payload["active_claims"] = [c for c in self.claims.active_claims() if c["goal_id"] == target]
            payload["quota"] = self.quota.get(target)
            payload["recovery"] = self.recovery.diagnose(target)
        return payload

    def validate_state(self) -> dict[str, Any]:
        """Re-validate the whole control plane against schemas. FAIL CLOSED."""
        errors: list[str] = []
        checks: list[str] = []

        try:
            for goal in self.goals.all_goals():
                validate(goal, "goal")
                checks.append(f"goal:{goal['goal_id']}")
        except Exception as exc:
            errors.append(f"goal: {exc}")

        try:
            for todo in self.todos.list():
                validate(todo, "todo")
                checks.append(f"todo:{todo['todo_id']}")
        except Exception as exc:
            errors.append(f"todo: {exc}")

        try:
            for gate in self.gates.list():
                validate(gate, "gate")
                checks.append(f"gate:{gate['gate_id']}")
        except Exception as exc:
            errors.append(f"gate: {exc}")

        try:
            for claim in self.claims.active_claims():
                validate(claim, "claim")
                checks.append(f"claim:{claim['todo_id']}")
        except Exception as exc:
            errors.append(f"claim: {exc}")

        try:
            for record in self.store.read("quota")["goals"].values():
                validate(record, "quota")
                checks.append(f"quota:{record['goal_id']}")
        except Exception as exc:
            errors.append(f"quota: {exc}")

        try:
            for event in self.store.read_run_history():
                validate(event, "run_event")
            checks.append("run_history")
        except Exception as exc:
            errors.append(f"run_event: {exc}")

        current = self.handoff.current()
        if current is not None:
            try:
                validate(current, CONTINUATION_SCHEMA)
                checks.append(CONTINUATION_KEY)
            except Exception as exc:
                errors.append(f"handoff: {exc}")

        evidence_check = self.evidence.verify_index()
        if evidence_check["status"] != "PASS":
            errors.append(f"evidence index drift: {evidence_check}")

        return {
            "status": "PASS" if not errors else "FAIL",
            "checks_performed": len(checks),
            "errors": errors,
            "evidence": evidence_check,
        }
