"""Deterministic recovery after an interrupted session.

Never restarts the project from zero. Inspects durable state and returns exactly
one decision from RECOVERY_DECISIONS.
"""

from __future__ import annotations

from typing import Any

from .claim_manager import ClaimManager
from .evidence_manager import EvidenceManager
from .gate_manager import GateManager
from .quota_manager import QuotaManager
from .state_store import StateStore
from .todo_manager import TodoManager


class RecoveryEngine:
    def __init__(self, store: StateStore) -> None:
        self.store = store
        self.claims = ClaimManager(store)
        self.todos = TodoManager(store)
        self.gates = GateManager(store)
        self.quota = QuotaManager(store)
        self.evidence = EvidenceManager(store)

    def diagnose(self, goal_id: str) -> dict[str, Any]:
        """Inspect durable state and emit a deterministic recovery decision."""
        goals = self.store.read("active_goal")["goals"]
        goal = goals.get(goal_id)
        if goal is None:
            return {
                "decision": "BLOCK",
                "reason": f"unknown goal {goal_id}",
                "unfinished_turn": None,
                "stale_claims": [],
                "last_evidence": None,
            }

        history = [e for e in self.store.read_run_history() if e.get("goal_id") == goal_id]
        started = {e["turn_id"] for e in history if e.get("event_type") == "TURN_START"}
        ended = {e["turn_id"] for e in history if e.get("event_type") == "TURN_END"}
        unfinished = sorted(started - ended)

        stale = [c for c in self.claims.active_claims()
                 if c["goal_id"] == goal_id and self.claims.is_expired(c)]
        active = [c for c in self.claims.active_claims()
                  if c["goal_id"] == goal_id and not self.claims.is_expired(c)]

        in_flight = [t for t in self.todos.list(goal_id=goal_id)
                     if t["status"] in ("CLAIMED", "RUNNING", "VALIDATING")]

        goal_evidence = self.evidence.list(goal_id=goal_id)
        last_evidence = goal_evidence[-1] if goal_evidence else None

        open_gates = self.gates.open_gates(goal_id)
        quota_verdict = self.quota.evaluate(goal_id)

        base = {
            "goal_id": goal_id,
            "goal_status": goal["status"],
            "unfinished_turn": unfinished[-1] if unfinished else None,
            "unfinished_turns": unfinished,
            "stale_claims": stale,
            "active_claims": active,
            "in_flight_todos": [t["todo_id"] for t in in_flight],
            "last_evidence": last_evidence,
            "open_gates": [g["gate_id"] for g in open_gates],
            "quota": quota_verdict,
        }

        if open_gates:
            return {**base, "decision": "WAIT",
                    "reason": f"{len(open_gates)} open human gate(s) must be resolved first"}

        if quota_verdict["result"] == "QUOTA_EXHAUSTED":
            return {**base, "decision": "BLOCK", "reason": quota_verdict["reason"]}

        if quota_verdict["result"] == "REPLAN_REQUIRED":
            return {**base, "decision": "REPLAN", "reason": quota_verdict["reason"]}

        if goal["status"] in ("COMPLETED", "FAILED", "CANCELLED"):
            return {**base, "decision": "BLOCK",
                    "reason": f"goal is terminal ({goal['status']}); nothing to recover"}

        if stale:
            return {**base, "decision": "REPAIR",
                    "reason": (f"{len(stale)} stale lease(s) detected: "
                               f"{[c['todo_id'] for c in stale]}; recover the lease then resume")}

        if unfinished and in_flight:
            return {**base, "decision": "RESUME",
                    "reason": (f"turn {unfinished[-1]} started but never ended; "
                               f"todo(s) {[t['todo_id'] for t in in_flight]} still in flight")}

        if in_flight:
            return {**base, "decision": "RESUME",
                    "reason": f"todo(s) {[t['todo_id'] for t in in_flight]} are in flight with a live lease"}

        if self.todos.next_available(goal_id) is not None:
            return {**base, "decision": "RESUME",
                    "reason": "no in-flight work; next PENDING todo with satisfied dependencies is available"}

        remaining = [t for t in self.todos.list(goal_id=goal_id) if t["status"] not in ("COMPLETED", "FAILED")]
        if remaining:
            return {**base, "decision": "REPLAN",
                    "reason": (f"{len(remaining)} todo(s) remain but none are startable "
                               "(blocked or unmet dependencies)")}

        return {**base, "decision": "WAIT",
                "reason": "all todos are terminal; goal is ready for validation and closure"}
