"""Execution budget and anti-infinite-loop control.

Every spend carries an idempotency_key so that replaying a turn cannot
double-charge the budget.
"""

from __future__ import annotations

from typing import Any

from .constants import DEFAULT_QUOTA_LIMITS
from .state_store import StateStore
from .validation import validate


class QuotaManager:
    def __init__(self, store: StateStore) -> None:
        self.store = store

    def _load(self) -> dict[str, Any]:
        return self.store.read("quota")

    def _save(self, data: dict[str, Any]) -> None:
        self.store.write("quota", data)

    def ensure(self, goal_id: str, limits: dict[str, int] | None = None) -> dict[str, Any]:
        data = self._load()
        if goal_id not in data["goals"]:
            record = {
                "goal_id": goal_id,
                "limits": dict(limits or DEFAULT_QUOTA_LIMITS),
                "turns_consumed": 0,
                "failed_turns": 0,
                "no_progress_turns": 0,
                "validation_failures": 0,
                "scope_expansions": 0,
                "hypothesis_attempts": {},
                "spent_keys": [],
            }
            validate(record, "quota")
            data["goals"][goal_id] = record
            self._save(data)
        return data["goals"][goal_id]

    def get(self, goal_id: str) -> dict[str, Any]:
        return self.ensure(goal_id)

    # ------------------------------------------------------------- spend

    def spend(
        self,
        goal_id: str,
        idempotency_key: str,
        turn: int = 1,
        failed: int = 0,
        no_progress: int = 0,
        validation_failure: int = 0,
        scope_expansion: int = 0,
        hypothesis: str | None = None,
    ) -> dict[str, Any]:
        """Charge the budget once per idempotency_key."""
        self.ensure(goal_id)
        data = self._load()
        record = data["goals"][goal_id]

        if idempotency_key in record["spent_keys"]:
            return {"charged": False, "reason": "IDEMPOTENT_REPLAY", "quota": record}

        record["turns_consumed"] += turn
        record["failed_turns"] += failed
        record["validation_failures"] += validation_failure
        record["scope_expansions"] += scope_expansion
        if no_progress:
            record["no_progress_turns"] += no_progress
        else:
            record["no_progress_turns"] = 0
        if hypothesis:
            record["hypothesis_attempts"][hypothesis] = record["hypothesis_attempts"].get(hypothesis, 0) + 1
        record["spent_keys"].append(idempotency_key)

        validate(record, "quota")
        data["goals"][goal_id] = record
        self._save(data)
        return {"charged": True, "reason": "CHARGED", "quota": record}

    # ------------------------------------------------------------ verdict

    def evaluate(self, goal_id: str, hypothesis: str | None = None) -> dict[str, Any]:
        """Return the canonical turn result implied by the current budget."""
        record = self.ensure(goal_id)
        limits = record["limits"]

        if record["validation_failures"] >= limits["max_validation_failures"]:
            return {
                "result": "QUOTA_EXHAUSTED",
                "reason": (
                    f"validation_failures={record['validation_failures']} reached "
                    f"max_validation_failures={limits['max_validation_failures']}"
                ),
            }

        if hypothesis:
            attempts = record["hypothesis_attempts"].get(hypothesis, 0)
            if attempts >= limits["max_same_hypothesis_attempts"]:
                return {
                    "result": "BLOCKED",
                    "reason": (
                        f"hypothesis '{hypothesis}' attempted {attempts} times, "
                        f"limit is {limits['max_same_hypothesis_attempts']}"
                    ),
                }

        if record["scope_expansions"] > limits["max_scope_expansions"]:
            return {
                "result": "USER_ACTION_REQUIRED",
                "reason": (
                    f"scope_expansions={record['scope_expansions']} exceeds "
                    f"max_scope_expansions={limits['max_scope_expansions']}"
                ),
            }

        if record["no_progress_turns"] >= limits["max_no_progress_turns"]:
            return {
                "result": "REPLAN_REQUIRED",
                "reason": (
                    f"no_progress_turns={record['no_progress_turns']} reached "
                    f"max_no_progress_turns={limits['max_no_progress_turns']}"
                ),
            }

        return {"result": "OK", "reason": "within budget"}

    def reset(self, goal_id: str, approved_gate_id: str) -> dict[str, Any]:
        """Reset counters. Requires an APPROVED QUOTA_RESET gate."""
        gates = self.store.read("gates")["gates"]
        gate = next((g for g in gates if g["gate_id"] == approved_gate_id), None)
        if gate is None:
            raise ValueError(f"unknown gate: {approved_gate_id}")
        if gate["type"] != "QUOTA_RESET" or gate["status"] != "APPROVED":
            raise ValueError("quota reset requires an APPROVED QUOTA_RESET gate")

        data = self._load()
        record = data["goals"][goal_id]
        record.update(
            {
                "failed_turns": 0,
                "no_progress_turns": 0,
                "validation_failures": 0,
                "scope_expansions": 0,
                "hypothesis_attempts": {},
            }
        )
        validate(record, "quota")
        data["goals"][goal_id] = record
        self._save(data)
        return record
