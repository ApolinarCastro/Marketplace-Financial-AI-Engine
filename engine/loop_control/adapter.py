"""Universal Agent Adapter Interface.

This module defines the minimal common interface that all agent adapters
(OpenCode, Codex, Claude, etc.) must implement. Adapters do NOT control
lifecycle directly — they delegate to the LoopKernel.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class TurnResult:
    """Result of a bounded turn execution."""
    started: bool
    turn_id: str | None
    result: str
    todo: dict[str, Any] | None = None
    claim: dict[str, Any] | None = None
    precheck: dict[str, Any] | None = None
    open_gates: list[dict[str, Any]] | None = None
    question: str | None = None
    reason: str | None = None
    conflict_code: str | None = None


@dataclass
class TurnCompletion:
    """Result of turn completion."""
    turn_id: str
    result: str
    todo: dict[str, Any] | None
    continuation_record: dict[str, Any] | None
    quota: dict[str, Any] | None
    next_todo: str | None


class AgentAdapter(abc.ABC):
    """Abstract base class for agent adapters.

    Adapters provide a runtime-specific interface to the universal kernel.
    They do NOT implement lifecycle logic — they delegate to LoopKernel.
    """

    def __init__(self, kernel: Any, agent_id: str) -> None:
        self.kernel = kernel
        self.agent_id = agent_id

    @property
    @abc.abstractmethod
    def runtime_name(self) -> str:
        """Human-readable runtime name (e.g., 'opencode', 'codex', 'claude')."""
        ...

    # ---------------------------------------------------------- lifecycle

    def read_state(self, goal_id: str | None = None) -> dict[str, Any]:
        """Read full control plane state."""
        return self.kernel.status(goal_id)

    def diagnose(self, goal_id: str) -> dict[str, Any]:
        """Run recovery diagnosis."""
        return self.kernel.recovery.diagnose(goal_id)

    def claim_todo(self, goal_id: str, todo_id: str | None = None, hypothesis: str | None = None) -> TurnResult:
        """Begin a bounded turn. Returns TurnResult with started flag."""
        turn = self.kernel.begin_turn(
            goal_id=goal_id,
            agent_id=self.agent_id,
            todo_id=todo_id,
            hypothesis=hypothesis,
        )
        return TurnResult(
            started=turn["started"],
            turn_id=turn.get("turn_id"),
            result=turn.get("result"),
            todo=turn.get("todo"),
            claim=turn.get("claim"),
            precheck=turn.get("precheck"),
            open_gates=turn.get("open_gates"),
            question=turn.get("question"),
            reason=turn.get("reason"),
            conflict_code=turn.get("conflict_code"),
        )

    def check_write_intent(self, goal_id: str, todo_id: str, paths: list[str]) -> dict[str, Any]:
        """Check if a write intent is allowed."""
        return self.kernel.check_write_intent(goal_id, todo_id, self.agent_id, paths)

    def execute_turn(self, goal_id: str, turn_id: str, todo_id: str, **kwargs) -> TurnCompletion:
        """Execute the bounded turn body. Must be implemented by adapter."""
        raise NotImplementedError("Subclasses must implement execute_turn")

    def write_evidence(self, goal_id: str, turn_id: str, name: str, payload: dict[str, Any],
                       todo_id: str | None = None, evidence_type: str | None = None,
                       validation_status: str | None = None) -> dict[str, Any]:
        """Write an evidence artifact."""
        return self.kernel.evidence.write_artifact(
            goal_id, turn_id, name, payload,
            todo_id=todo_id, evidence_type=evidence_type,
            validation_status=validation_status,
        )

    def submit_transition(self, goal_id: str, turn_id: str, todo_id: str, result: str,
                          action_summary: str, validation_passed: bool,
                          validation_detail: dict[str, Any] | None = None,
                          tests: dict[str, Any] | None = None,
                          files_changed: list[str] | None = None,
                          blockers: list[str] | None = None,
                          next_agent: str | None = None,
                          hypothesis: str | None = None,
                          made_progress: bool = True) -> TurnCompletion:
        """Submit turn completion and get continuation record."""
        out = self.kernel.end_turn(
            goal_id=goal_id,
            turn_id=turn_id,
            agent_id=self.agent_id,
            todo_id=todo_id,
            result=result,
            action_summary=action_summary,
            validation_passed=validation_passed,
            validation_detail=validation_detail,
            tests=tests,
            files_changed=files_changed,
            blockers=blockers,
            next_agent=next_agent,
            hypothesis=hypothesis,
            made_progress=made_progress,
        )
        return TurnCompletion(
            turn_id=out["turn_id"],
            result=out["result"],
            todo=out.get("todo"),
            continuation_record=out.get("continuation_record"),
            quota=out.get("quota"),
            next_todo=out.get("next_todo"),
        )

    def write_continuation(self, goal_id: str, turn_id: str, todo_id: str) -> dict[str, Any]:
        """Write continuation artifact."""
        record = self.kernel.handoff.current()
        if record:
            return self.kernel.evidence.write_artifact(
                goal_id, turn_id, "handoff", {"continuation_record": record},
                todo_id=todo_id, evidence_type="handoff",
            )
        return {}

    # ---------------------------------------------------------- utilities

    def continue_or_stop(self, goal_id: str, turn_result: TurnResult) -> bool:
        """Determine whether to continue or stop based on turn result."""
        if not turn_result.started:
            # Turn was rejected - check if we should wait or stop
            if turn_result.result in ("USER_ACTION_REQUIRED", "BLOCKED", "QUOTA_EXHAUSTED"):
                return False  # Stop and report
            if turn_result.result == "WAIT":
                return False  # Stop and wait
            if turn_result.result == "REPLAN_REQUIRED":
                return False  # Stop and request replanning
        return True  # Continue


class OpenCodeAdapter(AgentAdapter):
    """OpenCode-specific adapter."""

    @property
    def runtime_name(self) -> str:
        return "opencode"

    def execute_turn(self, goal_id: str, turn_id: str, todo_id: str, **kwargs) -> TurnCompletion:
        """OpenCode executes via CLI or direct Python."""
        # The actual work is done by the agent; this just provides the interface
        return self.submit_transition(goal_id, turn_id, todo_id, **kwargs)


class CodexAdapter(AgentAdapter):
    """Codex-specific adapter."""

    @property
    def runtime_name(self) -> str:
        return "codex"

    def execute_turn(self, goal_id: str, turn_id: str, todo_id: str, **kwargs) -> TurnCompletion:
        return self.submit_transition(goal_id, turn_id, todo_id, **kwargs)


class ClaudeAdapter(AgentAdapter):
    """Claude Code-specific adapter."""

    @property
    def runtime_name(self) -> str:
        return "claude"

    def execute_turn(self, goal_id: str, turn_id: str, todo_id: str, **kwargs) -> TurnCompletion:
        return self.submit_transition(goal_id, turn_id, todo_id, **kwargs)


def get_adapter(kernel: Any, agent_id: str) -> AgentAdapter:
    """Factory function to get the appropriate adapter."""
    adapters = {
        "OPENCODE_ENGINEER": OpenCodeAdapter,
        "CODEX_ENGINEER": CodexAdapter,
        "AUDITOR": OpenCodeAdapter,  # uses same interface
        "QA": OpenCodeAdapter,
        "RESEARCHER": OpenCodeAdapter,
    }
    adapter_class = adapters.get(agent_id, OpenCodeAdapter)
    return adapter_class(kernel, agent_id)