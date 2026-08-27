"""Test universal adapter interface."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from engine.loop_control import LoopKernel
from engine.loop_control.adapter import (
    AgentAdapter,
    OpenCodeAdapter,
    CodexAdapter,
    ClaudeAdapter,
    get_adapter,
    TurnResult,
    TurnCompletion,
)
from engine.loop_control.policy import SyntheticProjectAPolicy


@pytest.fixture
def kernel():
    """Create a kernel with a temporary directory that persists for the test."""
    tmp = tempfile.mkdtemp()
    policy = SyntheticProjectAPolicy(Path(tmp))
    kernel = LoopKernel(root=tmp, repo_root=Path(tmp), project_policy=policy)
    kernel.initialize()
    return kernel


def test_adapter_factory(kernel):
    for agent_id in ("OPENCODE_ENGINEER", "CODEX_ENGINEER", "AUDITOR", "QA", "RESEARCHER"):
        adapter = get_adapter(kernel, agent_id)
        assert isinstance(adapter, AgentAdapter)
        assert adapter.agent_id == agent_id
        assert adapter.runtime_name in ("opencode", "codex", "claude")


def test_opencode_adapter(kernel):
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["**"], ["pytest"], priority=1)

    adapter = OpenCodeAdapter(kernel, "OPENCODE_ENGINEER")

    # Read state
    state = adapter.read_state("TEST-GOAL")
    assert state["active_goal_id"] == "TEST-GOAL"

    # Diagnose
    diag = adapter.diagnose("TEST-GOAL")
    assert diag["decision"] in ("RESUME", "WAIT", "BLOCK", "REPLAN", "REPAIR")

    # Claim todo
    turn = adapter.claim_todo("TEST-GOAL", hypothesis="test")
    assert turn.started is True
    assert turn.todo["todo_id"] == "TODO-001"
    assert turn.result == "OK"

    # Check write intent
    verdict = adapter.check_write_intent("TEST-GOAL", "TODO-001", ["src/file.py"])
    assert verdict["allowed"] is True

    # Submit transition
    completion = adapter.submit_transition(
        goal_id="TEST-GOAL",
        turn_id=turn.turn_id,
        todo_id="TODO-001",
        result="VALIDATED_COMPLETION",
        action_summary="test",
        validation_passed=True,
    )
    assert completion.result == "VALIDATED_COMPLETION"
    assert completion.continuation_record is not None

    # Continue or stop
    assert adapter.continue_or_stop("TEST-GOAL", turn) is True


def test_codex_adapter(kernel):
    adapter = CodexAdapter(kernel, "CODEX_ENGINEER")
    assert adapter.runtime_name == "codex"


def test_claude_adapter(kernel):
    adapter = ClaudeAdapter(kernel, "CLAUDE_ENGINEER")
    assert adapter.runtime_name == "claude"


def test_adapter_delegates_to_kernel(kernel):
    """Verify adapters delegate to kernel, don't implement lifecycle."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["**"], ["pytest"], priority=1)

    adapter = get_adapter(kernel, "OPENCODE_ENGINEER")
    turn = adapter.claim_todo("TEST-GOAL", hypothesis="test")

    # The adapter should NOT have implemented claim logic itself
    # It should delegate to kernel.claims.claim
    assert turn.started is True
    claim = kernel.claims.find_active("TEST-GOAL", "TODO-001")
    assert claim is not None
    assert claim["agent_id"] == "OPENCODE_ENGINEER"


def test_write_intent_uses_kernel_gates(kernel):
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)

    adapter = get_adapter(kernel, "OPENCODE_ENGINEER")
    turn = adapter.claim_todo("TEST-GOAL", hypothesis="test")

    # In-scope write
    verdict = adapter.check_write_intent("TEST-GOAL", "TODO-001", ["src/file.py"])
    assert verdict["allowed"] is True

    # Out-of-scope write
    verdict = adapter.check_write_intent("TEST-GOAL", "TODO-001", ["docs/file.md"])
    assert verdict["allowed"] is False
    assert verdict["result"] == "USER_ACTION_REQUIRED"
    assert "gate_id" in verdict


def test_adapter_has_no_lifecycle_logic():
    """Verify adapter classes don't contain lifecycle implementation."""
    import inspect
    for cls in (OpenCodeAdapter, CodexAdapter, ClaudeAdapter):
        methods = [m for m in dir(cls) if not m.startswith("_")]
        # Should not have lifecycle methods
        lifecycle_methods = [
            "claim", "complete_todo", "complete_goal", "transition",
            "raise_gate", "resolve_gate", "spend", "evaluate",
            "log_event", "publish", "transition",
        ]
        for lm in lifecycle_methods:
            assert not hasattr(cls, lm), f"{cls.__name__} should not have {lm}"


def test_universal_adapter_interface_exists():
    """Verify the abstract base class defines the contract."""
    import inspect
    assert inspect.isabstract(AgentAdapter)
    abstract_methods = AgentAdapter.__abstractmethods__
    # Only runtime_name is abstract; other methods have base implementations
    assert "runtime_name" in abstract_methods