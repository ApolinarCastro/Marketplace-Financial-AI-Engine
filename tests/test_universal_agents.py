"""Test peer agent model preservation."""

from __future__ import annotations

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


def test_peer_agents_no_permanent_leader(kernel):
    """Verify no permanent leader - all agents are peers."""
    agents = kernel.registry().get("agents", [])
    assert len(agents) >= 2  # At least OpenCode and Codex

    # No agent has "leader" role
    for agent in agents:
        assert "leader" not in str(agent).lower()
        assert "master" not in str(agent).lower()
        assert "boss" not in str(agent).lower()

    # All agents have equal structural footing
    agent_ids = {a["agent_id"] for a in agents}
    assert "OPENCODE_ENGINEER" in agent_ids
    assert "CODEX_ENGINEER" in agent_ids


def test_agent_authority_from_goal_claim_gate(kernel):
    """Authority derives from: Goal + Claim/Lease + ProjectPolicy + Gate."""
    # Create a goal and todo
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)

    # Agent claims todo - authority from claim
    claim = kernel.claims.claim("TEST-GOAL", "TODO-001", "OPENCODE_ENGINEER", ["src/**"])
    assert claim["agent_id"] == "OPENCODE_ENGINEER"

    # Another agent cannot claim same todo (active conflict)
    from engine.loop_control.constants import ClaimConflictError
    with pytest.raises(ClaimConflictError) as exc:
        kernel.claims.claim("TEST-GOAL", "TODO-001", "CODEX_ENGINEER", ["src/**"])
    assert exc.value.code == "ACTIVE_CONFLICT"

    # But different todo with non-overlapping scope works
    kernel.todos.add("TODO-002", "TEST-GOAL", "test", ["tests/**"], ["pytest"], priority=2)
    claim2 = kernel.claims.claim("TEST-GOAL", "TODO-002", "CODEX_ENGINEER", ["tests/**"])
    assert claim2["agent_id"] == "CODEX_ENGINEER"


def test_agent_capabilities_runtime(kernel):
    """Each agent declares runtime and capabilities."""
    agents = kernel.registry().get("agents", [])
    for agent in agents:
        assert "agent_id" in agent
        assert "runtime" in agent
        assert "capabilities" in agent
        assert isinstance(agent["capabilities"], list)
        assert len(agent["capabilities"]) > 0

    # Verify specific agents
    opencode = next(a for a in agents if a["agent_id"] == "OPENCODE_ENGINEER")
    codex = next(a for a in agents if a["agent_id"] == "CODEX_ENGINEER")

    assert opencode["runtime"] == "opencode"
    assert codex["runtime"] == "codex"
    assert "implement" in opencode["capabilities"]
    assert "implement" in codex["capabilities"]


def test_write_scope_from_policy(kernel):
    """Allowed write scope comes from ProjectPolicy, not agent role."""
    agents = kernel.registry().get("agents", [])
    for agent in agents:
        # Write scope should be defined
        assert "allowed_write_scope" in agent
        assert isinstance(agent["allowed_write_scope"], list)

    # Protected write scope should match project policy
    for agent in agents:
        assert "protected_write_scope" in agent
        assert agent["protected_write_scope"] == kernel.project_policy.protected_resources


def test_no_role_based_authority(kernel):
    """Authority is NOT from agent role name."""
    agents = kernel.registry().get("agents", [])

    # All agents have equal structural capabilities
    # The only difference is their runtime and declared capabilities
    roles = {a["agent_id"] for a in agents}
    assert len(roles) >= 2

    # No special "admin" or "owner" role
    for agent in agents:
        assert agent["agent_id"] not in ("ADMIN", "OWNER", "LEADER", "MASTER")


def test_cross_agent_continuation(kernel):
    """OpenCode -> Codex continuation works."""
    kernel.goals.create("TEST-GOAL", "t", "o", ["done"], "HUMAN_OWNER", activate=True)
    kernel.todos.add("TODO-001", "TEST-GOAL", "test", ["src/**"], ["pytest"], priority=1)
    kernel.todos.add("TODO-002", "TEST-GOAL", "test", ["tests/**"], ["pytest"], priority=2)

    # OpenCode completes TODO-001
    turn1 = kernel.begin_turn("TEST-GOAL", "OPENCODE_ENGINEER")
    assert turn1["started"]
    kernel.end_turn(
        "TEST-GOAL", turn1["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
        result="VALIDATED_COMPLETION", action_summary="done",
        validation_passed=True, next_agent="CODEX_ENGINEER",
    )

    # Codex continues with TODO-002
    turn2 = kernel.begin_turn("TEST-GOAL", "CODEX_ENGINEER")
    assert turn2["started"]
    assert turn2["todo"]["todo_id"] == "TODO-002"

    # Continuation record shows cross-agent handoff
    record = kernel.handoff.current()
    assert record is not None
    assert record["from_agent"] == "OPENCODE_ENGINEER"
    assert record["to_agent"] == "CODEX_ENGINEER"