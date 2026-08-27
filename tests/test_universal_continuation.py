"""Test continuation record standardization."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from engine.loop_control import LoopKernel
from engine.loop_control.policy import SyntheticProjectAPolicy


@pytest.fixture
def kernel():
    tmp = tempfile.mkdtemp()
    policy = SyntheticProjectAPolicy(Path(tmp))
    kernel = LoopKernel(root=tmp, repo_root=Path(tmp), project_policy=policy)
    kernel.initialize()
    return kernel


def test_continuation_record_no_reserved_tokens(kernel):
    """Verify continuation record avoids reserved coordination tokens."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)

    turn = kernel.begin_turn("TEST-GOAL", "OPENCODE_ENGINEER")
    kernel.end_turn(
        "TEST-GOAL", turn["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
        result="VALIDATED_COMPLETION", action_summary="done",
        validation_passed=True, next_agent="CODEX_ENGINEER",
    )

    record = kernel.handoff.current()
    assert record is not None

    # Verify NO reserved tokens as JSON keys
    assert "handoff" not in record
    assert "next_actor" not in record
    assert "current_owner" not in record

    # Verify correct keys
    assert "from_agent" in record
    assert "to_agent" in record
    assert "receiving_agent" not in record  # internal term, not in JSON
    assert "holding_agent" not in record   # internal term, not in JSON


def test_continuation_record_schema_valid(kernel):
    """Verify record validates against schema."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)

    turn = kernel.begin_turn("TEST-GOAL", "OPENCODE_ENGINEER")
    kernel.end_turn(
        "TEST-GOAL", turn["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
        result="VALIDATED_COMPLETION", action_summary="done",
        validation_passed=True, next_agent="CODEX_ENGINEER",
    )

    record = kernel.handoff.current()
    from engine.loop_control.validation import validate
    validate(record, "handoff")  # Should not raise


def test_continuation_record_fields(kernel):
    """Verify all required fields present."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)

    turn = kernel.begin_turn("TEST-GOAL", "OPENCODE_ENGINEER")
    kernel.end_turn(
        "TEST-GOAL", turn["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
        result="VALIDATED_COMPLETION", action_summary="done",
        validation_passed=True, next_agent="CODEX_ENGINEER",
    )

    record = kernel.handoff.current()
    required = [
        "from_agent", "to_agent", "goal_id", "completed", "current_state",
        "evidence", "blockers", "files_changed", "tests", "next_todo",
        "allowed_scope", "forbidden_scope", "created_at"
    ]
    for field in required:
        assert field in record, f"missing field: {field}"


def test_cross_agent_continuation_opencode_codex(kernel):
    """OpenCode -> Codex continuation."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)
    kernel.todos.add("TODO-002", "TEST-GOAL", "test", ["tests/**"], ["pytest"], priority=2)

    # OpenCode completes
    turn1 = kernel.begin_turn("TEST-GOAL", "OPENCODE_ENGINEER")
    kernel.end_turn(
        "TEST-GOAL", turn1["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
        result="VALIDATED_COMPLETION", action_summary="done",
        validation_passed=True, next_agent="CODEX_ENGINEER",
    )

    # Codex continues
    turn2 = kernel.begin_turn("TEST-GOAL", "CODEX_ENGINEER")
    assert turn2["started"]
    assert turn2["todo"]["todo_id"] == "TODO-002"

    record = kernel.handoff.current()
    assert record["from_agent"] == "OPENCODE_ENGINEER"
    assert record["to_agent"] == "CODEX_ENGINEER"


def test_cross_agent_continuation_codex_opencode(kernel):
    """Codex -> OpenCode continuation."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["tests/**"], ["pytest"], priority=1)
    kernel.todos.add("TODO-002", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=2)

    # Codex completes
    turn1 = kernel.begin_turn("TEST-GOAL", "CODEX_ENGINEER")
    kernel.end_turn(
        "TEST-GOAL", turn1["turn_id"], "CODEX_ENGINEER", "TODO-001",
        result="VALIDATED_COMPLETION", action_summary="done",
        validation_passed=True, next_agent="OPENCODE_ENGINEER",
    )

    # OpenCode continues
    turn2 = kernel.begin_turn("TEST-GOAL", "OPENCODE_ENGINEER")
    assert turn2["started"]
    assert turn2["todo"]["todo_id"] == "TODO-002"

    record = kernel.handoff.current()
    assert record["from_agent"] == "CODEX_ENGINEER"
    assert record["to_agent"] == "OPENCODE_ENGINEER"


def test_continuation_history_preserved(kernel):
    """History of continuations is preserved."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)
    kernel.todos.add("TODO-002", "TEST-GOAL", "test", ["tests/**"], ["pytest"], priority=2)
    kernel.todos.add("TODO-003", "TEST-GOAL", "test", ["docs/**"], ["pytest"], priority=3)

    for agent, todo in [("OPENCODE_ENGINEER", "TODO-001"), ("CODEX_ENGINEER", "TODO-002"), ("OPENCODE_ENGINEER", "TODO-003")]:
        turn = kernel.begin_turn("TEST-GOAL", agent)
        kernel.end_turn(
            "TEST-GOAL", turn["turn_id"], agent, todo,
            result="VALIDATED_COMPLETION", action_summary="done",
            validation_passed=True, next_agent="CODEX_ENGINEER" if agent == "OPENCODE_ENGINEER" else "OPENCODE_ENGINEER",
        )

    # Check history
    history = kernel.handoff.history()
    assert len(history) == 3  # All 3 continuations preserved
    assert history[0]["from_agent"] == "OPENCODE_ENGINEER"
    assert history[1]["from_agent"] == "CODEX_ENGINEER"
    assert history[2]["from_agent"] == "OPENCODE_ENGINEER"


def test_resume_brief_reconstructible(kernel):
    """Fresh session can reconstruct state from disk alone."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)

    turn = kernel.begin_turn("TEST-GOAL", "OPENCODE_ENGINEER")
    kernel.end_turn(
        "TEST-GOAL", turn["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
        result="VALIDATED_COMPLETION", action_summary="done",
        validation_passed=True, next_agent="CODEX_ENGINEER",
    )

    # Fresh kernel - cold session
    fresh = LoopKernel(root=kernel.store.root, repo_root=kernel.repo_root)
    brief = fresh.handoff.resume_brief()

    assert brief["resumable"] is True
    assert brief["goal"]["goal_id"] == "TEST-GOAL"
    assert brief["receiving_agent"] == "CODEX_ENGINEER"
    assert "TODO-001" in brief["completed_todos"]
    assert brief["next_todo"] is None  # All todos completed
    assert len(brief["evidence"]) > 0


def test_continuation_forbidden_scope_from_policy(kernel):
    """Forbidden scope comes from project policy."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)

    turn = kernel.begin_turn("TEST-GOAL", "OPENCODE_ENGINEER")
    kernel.end_turn(
        "TEST-GOAL", turn["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
        result="VALIDATED_COMPLETION", action_summary="done",
        validation_passed=True, next_agent="CODEX_ENGINEER",
    )

    record = kernel.handoff.current()
    forbidden = record["forbidden_scope"]
    assert ".git/**" in forbidden
    assert "secrets/**" in forbidden