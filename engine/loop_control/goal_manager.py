"""Goal lifecycle. Exactly one goal may be ACTIVE at a time."""

from __future__ import annotations

from typing import Any

from .constants import (
    DEFAULT_PROTECTED_RESOURCES,
    GOAL_TRANSITIONS,
    LoopControlError,
    StateTransitionError,
)
from .state_store import StateStore, iso
from .validation import validate


class GoalManager:
    def __init__(self, store: StateStore) -> None:
        self.store = store

    # ------------------------------------------------------------- reads

    def _load(self) -> dict[str, Any]:
        return self.store.read("active_goal")

    def all_goals(self) -> list[dict[str, Any]]:
        return list(self._load()["goals"].values())

    def get(self, goal_id: str) -> dict[str, Any] | None:
        return self._load()["goals"].get(goal_id)

    def active(self) -> dict[str, Any] | None:
        data = self._load()
        gid = data.get("active_goal_id")
        return data["goals"].get(gid) if gid else None

    # ------------------------------------------------------------ writes

    def create(
        self,
        goal_id: str,
        title: str,
        objective: str,
        completion_criteria: list[str],
        authority: str,
        scope: list[str] | None = None,
        non_goals: list[str] | None = None,
        protected_resources: list[str] | None = None,
        activate: bool = False,
    ) -> dict[str, Any]:
        data = self._load()
        if goal_id in data["goals"]:
            return data["goals"][goal_id]

        goal = {
            "goal_id": goal_id,
            "title": title,
            "objective": objective,
            "scope": list(scope or []),
            "non_goals": list(non_goals or []),
            "created_at": iso(),
            "updated_at": iso(),
            "status": "CREATED",
            "authority": authority,
            "protected_resources": list(protected_resources or DEFAULT_PROTECTED_RESOURCES),
            "completion_criteria": list(completion_criteria),
            "revision": 0,
        }
        validate(goal, "goal")

        data["goals"][goal_id] = goal
        self.store.write("active_goal", data)

        if activate:
            self.transition(goal_id, "ACTIVE")
            return self.get(goal_id)  # type: ignore[return-value]
        return goal

    def transition(self, goal_id: str, new_status: str) -> dict[str, Any]:
        data = self._load()
        goal = data["goals"].get(goal_id)
        if goal is None:
            raise LoopControlError(f"unknown goal: {goal_id}")

        current = goal["status"]
        if current == new_status:
            return goal
        allowed = GOAL_TRANSITIONS.get(current, ())
        if new_status not in allowed:
            raise StateTransitionError(
                f"illegal goal transition {current} -> {new_status} (allowed: {list(allowed)})"
            )

        if new_status == "ACTIVE":
            other = data.get("active_goal_id")
            if other and other != goal_id:
                other_goal = data["goals"].get(other, {})
                if other_goal.get("status") not in ("COMPLETED", "FAILED", "CANCELLED"):
                    raise StateTransitionError(
                        f"goal {other} is already ACTIVE; only one active goal is permitted"
                    )

        goal["status"] = new_status
        goal["updated_at"] = iso()
        goal["revision"] = int(goal.get("revision", 0)) + 1
        validate(goal, "goal")

        if new_status == "ACTIVE":
            data["active_goal_id"] = goal_id
        elif data.get("active_goal_id") == goal_id and new_status in ("COMPLETED", "FAILED", "CANCELLED"):
            data["active_goal_id"] = None

        data["goals"][goal_id] = goal
        self.store.write("active_goal", data)
        return goal
