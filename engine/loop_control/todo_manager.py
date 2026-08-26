"""Todo lifecycle. Completion requires a PASS validation record."""

from __future__ import annotations

from typing import Any

from .constants import TODO_TRANSITIONS, LoopControlError, StateTransitionError
from .state_store import StateStore, iso
from .validation import validate


class TodoManager:
    def __init__(self, store: StateStore) -> None:
        self.store = store

    def _load(self) -> dict[str, Any]:
        return self.store.read("todos")

    def _save(self, data: dict[str, Any]) -> None:
        self.store.write("todos", data)

    # ------------------------------------------------------------- reads

    def list(self, goal_id: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        todos = self._load()["todos"]
        if goal_id:
            todos = [t for t in todos if t["goal_id"] == goal_id]
        if status:
            todos = [t for t in todos if t["status"] == status]
        return sorted(todos, key=lambda t: (t["priority"], t["todo_id"]))

    def get(self, todo_id: str) -> dict[str, Any] | None:
        for todo in self._load()["todos"]:
            if todo["todo_id"] == todo_id:
                return todo
        return None

    def dependencies_met(self, todo_id: str) -> bool:
        todo = self.get(todo_id)
        if todo is None:
            return False
        for dep in todo["dependencies"]:
            dep_todo = self.get(dep)
            if dep_todo is None or dep_todo["status"] != "COMPLETED":
                return False
        return True

    def next_available(self, goal_id: str) -> dict[str, Any] | None:
        for todo in self.list(goal_id=goal_id, status="PENDING"):
            if self.dependencies_met(todo["todo_id"]):
                return todo
        return None

    # ------------------------------------------------------------ writes

    def add(
        self,
        todo_id: str,
        goal_id: str,
        description: str,
        write_scope: list[str],
        validation: list[str],
        priority: int = 100,
        dependencies: list[str] | None = None,
        evidence_required: bool = True,
    ) -> dict[str, Any]:
        data = self._load()
        for existing in data["todos"]:
            if existing["todo_id"] == todo_id:
                return existing

        todo = {
            "todo_id": todo_id,
            "goal_id": goal_id,
            "description": description,
            "priority": priority,
            "status": "PENDING",
            "claimed_by": None,
            "write_scope": list(write_scope),
            "dependencies": list(dependencies or []),
            "validation": list(validation),
            "evidence_required": evidence_required,
            "revision": 0,
            "updated_at": iso(),
        }
        validate(todo, "todo")
        data["todos"].append(todo)
        self._save(data)
        return todo

    def transition(self, todo_id: str, new_status: str, claimed_by: str | None = "__keep__") -> dict[str, Any]:
        data = self._load()
        for idx, todo in enumerate(data["todos"]):
            if todo["todo_id"] != todo_id:
                continue

            current = todo["status"]
            if current != new_status:
                allowed = TODO_TRANSITIONS.get(current, ())
                if new_status not in allowed:
                    raise StateTransitionError(
                        f"illegal todo transition {current} -> {new_status} (allowed: {list(allowed)})"
                    )

            todo["status"] = new_status
            if claimed_by != "__keep__":
                todo["claimed_by"] = claimed_by
            if new_status in ("PENDING", "COMPLETED", "FAILED"):
                todo["claimed_by"] = None
            todo["updated_at"] = iso()
            todo["revision"] = int(todo.get("revision", 0)) + 1
            validate(todo, "todo")

            data["todos"][idx] = todo
            self._save(data)
            return todo

        raise LoopControlError(f"unknown todo: {todo_id}")
