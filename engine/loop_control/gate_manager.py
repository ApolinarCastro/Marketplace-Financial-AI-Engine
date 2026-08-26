"""Human gates.

An agent can raise a gate. An agent can never resolve one: resolve() rejects any
resolver whose identity is a registered agent_id. Authority belongs to humans.
"""

from __future__ import annotations

from typing import Any

from .constants import (
    DESTRUCTIVE_OPERATION_PATTERNS,
    GATE_TYPES,
    LoopControlError,
)
from .scope import matched_pattern
from .state_store import StateStore, iso, new_id
from .validation import validate


class GateManager:
    def __init__(self, store: StateStore) -> None:
        self.store = store

    def _load(self) -> dict[str, Any]:
        return self.store.read("gates")

    def _save(self, data: dict[str, Any]) -> None:
        self.store.write("gates", data)

    def _registered_agent_ids(self) -> set[str]:
        registry = self.store.read("registry")
        return {a["agent_id"] for a in registry.get("agents", [])}

    # ------------------------------------------------------------- reads

    def list(self, goal_id: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        gates = self._load()["gates"]
        if goal_id:
            gates = [g for g in gates if g["goal_id"] == goal_id]
        if status:
            gates = [g for g in gates if g["status"] == status]
        return gates

    def open_gates(self, goal_id: str) -> list[dict[str, Any]]:
        return self.list(goal_id=goal_id, status="OPEN")

    def get(self, gate_id: str) -> dict[str, Any] | None:
        for gate in self._load()["gates"]:
            if gate["gate_id"] == gate_id:
                return gate
        return None

    # ------------------------------------------------------------ writes

    def raise_gate(
        self,
        goal_id: str,
        gate_type: str,
        reason: str,
        question: str,
        required_authority: str = "HUMAN_OWNER",
        requested_by: str | None = None,
        target: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        if gate_type not in GATE_TYPES:
            raise LoopControlError(f"unknown gate type: {gate_type}")
        if not question or "?" not in question:
            raise LoopControlError(
                "a gate must ask a concrete question containing '?'; "
                "'waiting for owner' is not an acceptable gate"
            )

        data = self._load()

        if idempotency_key:
            for gate in data["gates"]:
                if gate.get("idempotency_key") == idempotency_key:
                    return gate

        for gate in data["gates"]:
            if (
                gate["status"] == "OPEN"
                and gate["goal_id"] == goal_id
                and gate["type"] == gate_type
                and gate.get("target") == target
            ):
                return gate

        gate = {
            "gate_id": new_id("GATE"),
            "goal_id": goal_id,
            "type": gate_type,
            "reason": reason,
            "question": question,
            "required_authority": required_authority,
            "status": "OPEN",
            "created_at": iso(),
            "resolved_at": None,
            "resolved_by": None,
            "requested_by": requested_by,
            "target": target,
            "idempotency_key": idempotency_key,
        }
        validate(gate, "gate")
        data["gates"].append(gate)
        self._save(data)
        return gate

    def resolve(self, gate_id: str, decision: str, resolved_by: str) -> dict[str, Any]:
        if decision not in ("APPROVED", "REJECTED"):
            raise LoopControlError(f"invalid gate decision: {decision}")
        if resolved_by in self._registered_agent_ids():
            raise LoopControlError(
                f"agent '{resolved_by}' cannot resolve a gate; human authority is required"
            )

        data = self._load()
        for idx, gate in enumerate(data["gates"]):
            if gate["gate_id"] != gate_id:
                continue
            if gate["status"] != "OPEN":
                return gate
            gate["status"] = decision
            gate["resolved_at"] = iso()
            gate["resolved_by"] = resolved_by
            validate(gate, "gate")
            data["gates"][idx] = gate
            self._save(data)
            return gate
        raise LoopControlError(f"unknown gate: {gate_id}")

    # ------------------------------------------------------- enforcement

    def check_write_intent(
        self,
        goal_id: str,
        paths: list[str],
        protected_resources: list[str] | None = None,
        allowed_scope: list[str] | None = None,
        agent_id: str | None = None,
    ) -> dict[str, Any]:
        """Classify a write intent. Never performs the write."""
        protected = protected_resources or self.store.read("registry").get("protected_resources", [])
        violations: list[dict[str, str]] = []
        out_of_scope: list[str] = []

        for path in paths:
            pattern = matched_pattern(path, protected)
            if pattern:
                violations.append({"path": path, "protected_pattern": pattern})
                continue
            if allowed_scope is not None and not matched_pattern(path, allowed_scope):
                out_of_scope.append(path)

        if violations:
            targets = ",".join(sorted({v["protected_pattern"] for v in violations}))
            gate = self.raise_gate(
                goal_id=goal_id,
                gate_type="PROTECTED_RESOURCE",
                reason=(
                    f"Write intent touches protected resource(s): {violations}. "
                    "Protected resources require explicit human authorization."
                ),
                question=(
                    f"Do you authorize writing to the protected resource(s) {targets}? "
                    "Answer APPROVED or REJECTED."
                ),
                requested_by=agent_id,
                target=targets,
            )
            return {
                "allowed": False,
                "result": "USER_ACTION_REQUIRED",
                "gate_id": gate["gate_id"],
                "violations": violations,
            }

        if out_of_scope:
            gate = self.raise_gate(
                goal_id=goal_id,
                gate_type="SCOPE_EXPANSION",
                reason=(
                    f"Write intent falls outside the claimed write_scope: {out_of_scope}. "
                    "Scope expansion budget is 0."
                ),
                question=(
                    f"Do you authorize expanding the write scope to include {out_of_scope}? "
                    "Answer APPROVED or REJECTED."
                ),
                requested_by=agent_id,
                target=",".join(sorted(out_of_scope)),
            )
            return {
                "allowed": False,
                "result": "USER_ACTION_REQUIRED",
                "gate_id": gate["gate_id"],
                "out_of_scope": out_of_scope,
            }

        return {"allowed": True, "result": "OK", "gate_id": None}

    def check_git_command(self, goal_id: str, command: str, agent_id: str | None = None) -> dict[str, Any]:
        lowered = command.lower()
        for pattern in DESTRUCTIVE_OPERATION_PATTERNS:
            if pattern.lower() in lowered:
                gate = self.raise_gate(
                    goal_id=goal_id,
                    gate_type="DESTRUCTIVE_GIT",
                    reason=(
                        f"Command '{command}' matches destructive Git pattern '{pattern}'. "
                        "History-altering operations are never agent-authorized."
                    ),
                    question=(
                        f"Do you authorize running the destructive Git command '{command}'? "
                        "Answer APPROVED or REJECTED."
                    ),
                    requested_by=agent_id,
                    target=command,
                )
                return {
                    "allowed": False,
                    "result": "USER_ACTION_REQUIRED",
                    "gate_id": gate["gate_id"],
                    "pattern": pattern,
                }
        return {"allowed": True, "result": "OK", "gate_id": None}
