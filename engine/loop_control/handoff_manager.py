"""Cross-agent continuation records.

Vocabulary note: the JSON keys 'handoff', 'next_actor' and 'current_owner' are
reserved repo-wide by tools/verify_coordination_interface.py. This module
therefore persists under the key 'continuation_record' and uses from_agent /
to_agent. See governance/LOOP_ENGINEERING_PROTOCOL_V1.md section 0.2.
"""

from __future__ import annotations

from typing import Any

from .constants import CONTINUATION_KEY, CONTINUATION_SCHEMA
from .state_store import StateStore, iso
from .validation import validate

CONTINUATION_STORE_KEY = "continuation"


class HandoffManager:
    def __init__(self, store: StateStore) -> None:
        self.store = store

    def _load(self) -> dict[str, Any]:
        return self.store.read(CONTINUATION_STORE_KEY)

    def current(self) -> dict[str, Any] | None:
        return self._load().get(CONTINUATION_KEY)

    def publish(
        self,
        goal_id: str,
        from_agent: str,
        to_agent: str,
        current_state: str,
        completed: list[str] | None = None,
        evidence: list[str] | None = None,
        blockers: list[str] | None = None,
        files_changed: list[str] | None = None,
        tests: list[str] | None = None,
        next_todo: str | None = None,
        allowed_scope: list[str] | None = None,
        forbidden_scope: list[str] | None = None,
        turn_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        data = self._load()

        if idempotency_key:
            existing = data.get(CONTINUATION_KEY)
            if existing and existing.get("idempotency_key") == idempotency_key:
                return existing

        record = {
            "from_agent": from_agent,
            "to_agent": to_agent,
            "goal_id": goal_id,
            "completed": list(completed or []),
            "current_state": current_state,
            "evidence": list(evidence or []),
            "blockers": list(blockers or []),
            "files_changed": list(files_changed or []),
            "tests": list(tests or []),
            "next_todo": next_todo,
            "allowed_scope": list(allowed_scope or []),
            "forbidden_scope": list(forbidden_scope or []),
            "created_at": iso(),
            "turn_id": turn_id,
            "idempotency_key": idempotency_key,
        }
        validate(record, CONTINUATION_SCHEMA)

        history = data.get("history", [])
        if data.get(CONTINUATION_KEY):
            history.append(data[CONTINUATION_KEY])
        self.store.write(CONTINUATION_STORE_KEY, {CONTINUATION_KEY: record, "history": history})
        return record

    def history(self) -> list[dict[str, Any]]:
        return list(self._load().get("history", []))

    def resume_brief(self) -> dict[str, Any]:
        """Everything a fresh session needs, with zero conversational context."""
        record = self.current()
        if record is None:
            return {"resumable": False, "reason": "no continuation record published"}

        goals = self.store.read("active_goal")["goals"]
        goal = goals.get(record["goal_id"])
        todos = [t for t in self.store.read("todos")["todos"] if t["goal_id"] == record["goal_id"]]
        open_gates = [
            g for g in self.store.read("gates")["gates"]
            if g["goal_id"] == record["goal_id"] and g["status"] == "OPEN"
        ]

        return {
            "resumable": goal is not None,
            "goal": goal,
            "receiving_agent": record["to_agent"],
            "completed_todos": record["completed"],
            "next_todo": record["next_todo"],
            "evidence": record["evidence"],
            "blockers": record["blockers"],
            "open_gates": open_gates,
            "allowed_scope": record["allowed_scope"],
            "forbidden_scope": record["forbidden_scope"],
            "all_todos": sorted(todos, key=lambda t: (t["priority"], t["todo_id"])),
        }
