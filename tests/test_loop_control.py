"""Loop Engineering Protocol V1 â€” certification test suite.

Every test operates on an isolated tmp_path control plane. No test touches
01_Raw/, data/db/meli_financial_v4.db, .git/, or governance/coordination/.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.loop_control import LoopKernel
from engine.loop_control.constants import (
    CONFLICT_CODES,
    GOAL_STATUSES,
    RECOVERY_DECISIONS,
    TODO_STATUSES,
    TURN_RESULTS,
    ClaimConflictError,
    LoopControlError,
    SchemaValidationError,
    StateTransitionError,
)
from engine.loop_control.constants import CONTINUATION_SCHEMA as CONTINUATION_SCHEMA
from engine.loop_control.scope import scopes_overlap
from engine.loop_control.state_store import StateStore
from engine.loop_control.validation import validate
from engine.loop_control.policy import MarketplaceProjectPolicy

GOAL = "TEST-GOAL-001"
REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def kernel(tmp_path: Path) -> LoopKernel:
    policy = MarketplaceProjectPolicy(project_root=tmp_path)
    k = LoopKernel(root=tmp_path, repo_root=tmp_path, project_policy=policy)
    k.initialize()
    return k


@pytest.fixture()
def goal(kernel: LoopKernel):
    return kernel.goals.create(
        goal_id=GOAL,
        title="Test goal",
        objective="Prove the protocol",
        completion_criteria=["all todos completed"],
        authority="HUMAN_OWNER",
        scope=["engine/loop_control/**"],
        non_goals=["financial changes"],
        activate=True,
    )


def _add_todo(kernel: LoopKernel, todo_id: str, scope: list[str], deps: list[str] | None = None, priority: int = 10):
    return kernel.todos.add(
        todo_id=todo_id,
        goal_id=GOAL,
        description=f"work for {todo_id}",
        write_scope=scope,
        validation=["pytest -q"],
        priority=priority,
        dependencies=deps or [],
    )


def _run_full_turn(kernel: LoopKernel, todo_id: str, agent: str = "OPENCODE_ENGINEER", next_agent: str | None = None):
    turn = kernel.begin_turn(goal_id=GOAL, agent_id=agent, todo_id=todo_id)
    assert turn["started"] is True
    return kernel.end_turn(
        goal_id=GOAL,
        turn_id=turn["turn_id"],
        agent_id=agent,
        todo_id=todo_id,
        result="VALIDATED_COMPLETION",
        action_summary=f"completed {todo_id}",
        validation_passed=True,
        validation_detail={"command": "pytest -q", "exit_code": 0},
        tests={"suite": "synthetic", "passed": 1, "failed": 0},
        files_changed=[f"engine/loop_control/{todo_id.lower()}.py"],
        next_agent=next_agent,
    )


# --------------------------------------------------------------- lifecycle


def test_goal_lifecycle(kernel: LoopKernel):
    g = kernel.goals.create(
        goal_id=GOAL, title="t", objective="o",
        completion_criteria=["done"], authority="HUMAN_OWNER",
    )
    assert g["status"] == "CREATED"
    assert kernel.goals.active() is None

    kernel.goals.transition(GOAL, "ACTIVE")
    assert kernel.goals.active()["goal_id"] == GOAL

    with pytest.raises(StateTransitionError):
        kernel.goals.transition(GOAL, "COMPLETED")  # ACTIVE -> COMPLETED is illegal

    kernel.goals.transition(GOAL, "VALIDATING")
    kernel.goals.transition(GOAL, "COMPLETED")
    assert kernel.goals.get(GOAL)["status"] == "COMPLETED"
    assert kernel.goals.active() is None

    for status in kernel.goals.get(GOAL), :
        assert status["status"] in GOAL_STATUSES

    # Only one goal may be ACTIVE at a time.
    kernel.goals.create(goal_id="TEST-GOAL-002", title="t2", objective="o2",
                        completion_criteria=["done"], authority="HUMAN_OWNER", activate=True)
    kernel.goals.create(goal_id="TEST-GOAL-003", title="t3", objective="o3",
                        completion_criteria=["done"], authority="HUMAN_OWNER")
    with pytest.raises(StateTransitionError):
        kernel.goals.transition("TEST-GOAL-003", "ACTIVE")


def test_todo_lifecycle(kernel: LoopKernel, goal):
    t = _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    assert t["status"] == "PENDING"
    assert t["claimed_by"] is None

    kernel.todos.transition("TODO-001", "CLAIMED", claimed_by="OPENCODE_ENGINEER")
    assert kernel.todos.get("TODO-001")["claimed_by"] == "OPENCODE_ENGINEER"

    kernel.todos.transition("TODO-001", "RUNNING")
    with pytest.raises(StateTransitionError):
        kernel.todos.transition("TODO-001", "COMPLETED")  # must pass through VALIDATING

    kernel.todos.transition("TODO-001", "VALIDATING")
    kernel.todos.transition("TODO-001", "COMPLETED")
    done = kernel.todos.get("TODO-001")
    assert done["status"] == "COMPLETED"
    assert done["claimed_by"] is None
    assert done["status"] in TODO_STATUSES


def test_todo_dependencies_block_selection(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"], priority=10)
    _add_todo(kernel, "TODO-002", ["engine/loop_control/b.py"], deps=["TODO-001"], priority=5)

    # TODO-002 has higher priority but an unmet dependency.
    assert kernel.todos.next_available(GOAL)["todo_id"] == "TODO-001"
    _run_full_turn(kernel, "TODO-001")
    assert kernel.todos.next_available(GOAL)["todo_id"] == "TODO-002"


# ------------------------------------------------------------------ claims


def test_claim_conflict(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    kernel.claims.claim(GOAL, "TODO-001", "OPENCODE_ENGINEER", ["engine/loop_control/a.py"])

    with pytest.raises(ClaimConflictError) as exc:
        kernel.claims.claim(GOAL, "TODO-001", "CODEX_ENGINEER", ["engine/loop_control/a.py"])
    assert exc.value.code == "ACTIVE_CONFLICT"
    assert exc.value.code in CONFLICT_CODES

    # The kernel surfaces the conflict as a typed turn result rather than raising.
    turn = kernel.begin_turn(GOAL, "CODEX_ENGINEER", todo_id="TODO-001")
    assert turn["started"] is False
    assert turn["result"] == "BLOCKED"
    assert turn["conflict_code"] == "ACTIVE_CONFLICT"


def test_parallel_non_overlapping_claims(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/alpha/**"])
    _add_todo(kernel, "TODO-002", ["engine/loop_control/beta/**"])

    a = kernel.claims.claim(GOAL, "TODO-001", "OPENCODE_ENGINEER", ["engine/loop_control/alpha/**"])
    b = kernel.claims.claim(GOAL, "TODO-002", "CODEX_ENGINEER", ["engine/loop_control/beta/**"])
    assert a["agent_id"] != b["agent_id"]
    assert len(kernel.claims.active_claims()) == 2
    assert kernel.claims.detect_conflicts() == []


def test_overlapping_scope_claims_rejected(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/**"])
    _add_todo(kernel, "TODO-002", ["engine/loop_control/kernel.py"])

    kernel.claims.claim(GOAL, "TODO-001", "OPENCODE_ENGINEER", ["engine/loop_control/**"])
    with pytest.raises(ClaimConflictError) as exc:
        kernel.claims.claim(GOAL, "TODO-002", "CODEX_ENGINEER", ["engine/loop_control/kernel.py"])
    assert exc.value.code == "WRITE_SCOPE_OVERLAP"

    assert scopes_overlap(["engine/loop_control/**"], ["engine/loop_control/kernel.py"]) is True
    assert scopes_overlap(["engine/a/**"], ["engine/b/**"]) is False


def test_stale_lease_recovery(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    kernel.claims.claim(GOAL, "TODO-001", "OPENCODE_ENGINEER", ["engine/loop_control/a.py"], lease_seconds=-1)

    with pytest.raises(ClaimConflictError) as exc:
        kernel.claims.claim(GOAL, "TODO-001", "CODEX_ENGINEER", ["engine/loop_control/a.py"])
    assert exc.value.code == "STALE_LEASE"

    conflicts = kernel.claims.detect_conflicts()
    assert any(c["code"] == "STALE_LEASE" for c in conflicts)

    recovered = kernel.claims.claim(GOAL, "TODO-001", "CODEX_ENGINEER",
                                    ["engine/loop_control/a.py"], force_stale_takeover=True)
    assert recovered["agent_id"] == "CODEX_ENGINEER"
    # Prior claim history is preserved, never deleted.
    history = kernel.claims.history()
    assert any(h["agent_id"] == "OPENCODE_ENGINEER" and h["release_reason"] == "STALE_LEASE_RECOVERED"
               for h in history)


# ------------------------------------------------------------------- gates


def test_gate_enforcement(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    gate = kernel.gates.raise_gate(
        goal_id=GOAL, gate_type="PRODUCTION_PUBLISH",
        reason="Publishing to production requires human sign-off.",
        question="Do you authorize publishing to production?",
    )
    assert gate["status"] == "OPEN"

    turn = kernel.begin_turn(GOAL, "OPENCODE_ENGINEER", todo_id="TODO-001")
    assert turn["started"] is False
    assert turn["result"] == "USER_ACTION_REQUIRED"
    assert "?" in turn["question"]

    # An agent may never resolve its own gate.
    with pytest.raises(LoopControlError, match="human authority"):
        kernel.gates.resolve(gate["gate_id"], "APPROVED", resolved_by="OPENCODE_ENGINEER")

    kernel.gates.resolve(gate["gate_id"], "APPROVED", resolved_by="human:owner")
    assert kernel.gates.get(gate["gate_id"])["status"] == "APPROVED"
    assert kernel.begin_turn(GOAL, "OPENCODE_ENGINEER", todo_id="TODO-001")["started"] is True


def test_gate_requires_concrete_question(kernel: LoopKernel, goal):
    with pytest.raises(LoopControlError, match="concrete question"):
        kernel.gates.raise_gate(
            goal_id=GOAL, gate_type="SCOPE_EXPANSION",
            reason="Something is needed from the owner.",
            question="waiting for owner",
        )


@pytest.mark.parametrize(
    "path",
    ["01_Raw/ML/Facturacion/x.xlsx", "data/db/meli_financial_v4.db",
     ".git/config", ".agents/skills/x.md", "governance/coordination/coordination_state.json"],
)
def test_protected_resource_gate(kernel: LoopKernel, goal, path: str):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/**"])
    verdict = kernel.check_write_intent(GOAL, "TODO-001", "OPENCODE_ENGINEER", [path])
    assert verdict["allowed"] is False
    assert verdict["result"] == "USER_ACTION_REQUIRED"
    assert verdict["gate_id"] is not None
    assert kernel.gates.get(verdict["gate_id"])["type"] == "PROTECTED_RESOURCE"


def test_scope_expansion_gate(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/**"])
    ok = kernel.check_write_intent(GOAL, "TODO-001", "OPENCODE_ENGINEER", ["engine/loop_control/kernel.py"])
    assert ok["allowed"] is True

    bad = kernel.check_write_intent(GOAL, "TODO-001", "OPENCODE_ENGINEER", ["api/api.py"])
    assert bad["allowed"] is False
    assert kernel.gates.get(bad["gate_id"])["type"] == "SCOPE_EXPANSION"


@pytest.mark.parametrize(
    "command",
    ["git filter-repo --path x", "git reset --hard HEAD~5", "git push --force origin main",
     "git branch -D main", "git clean -fdx"],
)
def test_destructive_git_gate(kernel: LoopKernel, goal, command: str):
    verdict = kernel.gates.check_git_command(GOAL, command, agent_id="OPENCODE_ENGINEER")
    assert verdict["allowed"] is False
    assert verdict["result"] == "USER_ACTION_REQUIRED"
    assert kernel.gates.get(verdict["gate_id"])["type"] == "DESTRUCTIVE_GIT"


def test_safe_git_command_needs_no_gate(kernel: LoopKernel, goal):
    assert kernel.gates.check_git_command(GOAL, "git status --short")["allowed"] is True


# ------------------------------------------------------------------- quota


def test_quota_enforcement(kernel: LoopKernel, goal):
    limits = kernel.quota.get(GOAL)["limits"]
    assert limits["max_same_hypothesis_attempts"] == 3
    assert limits["max_no_progress_turns"] == 2
    assert limits["max_validation_failures"] == 3
    assert limits["max_scope_expansions"] == 0

    for i in range(3):
        kernel.quota.spend(GOAL, idempotency_key=f"vf-{i}", validation_failure=1)
    verdict = kernel.quota.evaluate(GOAL)
    assert verdict["result"] == "QUOTA_EXHAUSTED"

    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    turn = kernel.begin_turn(GOAL, "OPENCODE_ENGINEER", todo_id="TODO-001")
    assert turn["started"] is False
    assert turn["result"] == "QUOTA_EXHAUSTED"


def test_same_hypothesis_blocks_after_three(kernel: LoopKernel, goal):
    for i in range(3):
        kernel.quota.spend(GOAL, idempotency_key=f"h-{i}", hypothesis="the-cause-is-X")
    verdict = kernel.quota.evaluate(GOAL, hypothesis="the-cause-is-X")
    assert verdict["result"] == "BLOCKED"
    assert kernel.quota.evaluate(GOAL, hypothesis="a-different-cause")["result"] == "OK"


def test_no_progress_detection(kernel: LoopKernel, goal):
    kernel.quota.spend(GOAL, idempotency_key="np-1", no_progress=1)
    assert kernel.quota.evaluate(GOAL)["result"] == "OK"
    kernel.quota.spend(GOAL, idempotency_key="np-2", no_progress=1)
    assert kernel.quota.evaluate(GOAL)["result"] == "REPLAN_REQUIRED"

    # Real progress resets the counter.
    kernel.quota.spend(GOAL, idempotency_key="np-3", no_progress=0)
    assert kernel.quota.get(GOAL)["no_progress_turns"] == 0
    assert kernel.quota.evaluate(GOAL)["result"] == "OK"


def test_scope_expansion_budget_is_zero(kernel: LoopKernel, goal):
    kernel.quota.spend(GOAL, idempotency_key="se-1", scope_expansion=1)
    assert kernel.quota.evaluate(GOAL)["result"] == "USER_ACTION_REQUIRED"


def test_quota_reset_requires_approved_gate(kernel: LoopKernel, goal):
    kernel.quota.spend(GOAL, idempotency_key="x", validation_failure=3)
    gate = kernel.gates.raise_gate(GOAL, "QUOTA_RESET", "Budget exhausted after 3 validation failures.",
                                   "Do you authorize resetting the quota for this goal?")
    with pytest.raises(ValueError):
        kernel.quota.reset(GOAL, gate["gate_id"])  # still OPEN

    kernel.gates.resolve(gate["gate_id"], "APPROVED", resolved_by="human:owner")
    record = kernel.quota.reset(GOAL, gate["gate_id"])
    assert record["validation_failures"] == 0
    assert kernel.quota.evaluate(GOAL)["result"] == "OK"


# ---------------------------------------------------------------- handoff


def test_handoff(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"], priority=1)
    _add_todo(kernel, "TODO-002", ["engine/loop_control/b.py"], priority=2)

    out = _run_full_turn(kernel, "TODO-001", agent="OPENCODE_ENGINEER", next_agent="CODEX_ENGINEER")
    record = out["continuation_record"]
    assert record["from_agent"] == "OPENCODE_ENGINEER"
    assert record["to_agent"] == "CODEX_ENGINEER"
    assert record["completed"] == ["TODO-001"]
    assert record["next_todo"] == "TODO-002"
    assert record["evidence"]
    validate(record, CONTINUATION_SCHEMA)


def test_cross_agent_handoff(kernel: LoopKernel, goal, tmp_path: Path):
    """Agent B resumes from a cold session with zero conversational context."""
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"], priority=1)
    _add_todo(kernel, "TODO-002", ["engine/loop_control/b.py"], priority=2, deps=["TODO-001"])

    _run_full_turn(kernel, "TODO-001", agent="OPENCODE_ENGINEER", next_agent="CODEX_ENGINEER")

    # Simulate a brand new session: a fresh kernel object reading only from disk.
    fresh = LoopKernel(root=tmp_path, repo_root=tmp_path)
    brief = fresh.handoff.resume_brief()

    assert brief["resumable"] is True
    assert brief["goal"]["goal_id"] == GOAL
    assert brief["receiving_agent"] == "CODEX_ENGINEER"
    assert "TODO-001" in brief["completed_todos"]
    assert brief["next_todo"] == "TODO-002"
    assert brief["evidence"]
    assert brief["open_gates"] == []

    for path in brief["evidence"]:
        assert (tmp_path / path).exists(), f"evidence referenced but missing: {path}"

    out = _run_full_turn(fresh, "TODO-002", agent="CODEX_ENGINEER", next_agent="OPENCODE_ENGINEER")
    assert out["result"] == "VALIDATED_COMPLETION"
    assert fresh.todos.get("TODO-002")["status"] == "COMPLETED"


# ---------------------------------------------------------------- recovery


def test_recovery(kernel: LoopKernel, goal, tmp_path: Path):
    """A turn interrupted while RUNNING is resumed, never restarted from zero."""
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"], priority=1)
    _add_todo(kernel, "TODO-002", ["engine/loop_control/b.py"], priority=2)

    turn = kernel.begin_turn(GOAL, "OPENCODE_ENGINEER", todo_id="TODO-001")
    assert turn["started"] is True
    assert kernel.todos.get("TODO-001")["status"] == "RUNNING"
    # Session dies here: no end_turn is ever called.

    fresh = LoopKernel(root=tmp_path, repo_root=tmp_path)
    diag = fresh.recovery.diagnose(GOAL)

    assert diag["decision"] == "RESUME"
    assert diag["decision"] in RECOVERY_DECISIONS
    assert diag["unfinished_turn"] == turn["turn_id"]
    assert "TODO-001" in diag["in_flight_todos"]
    assert diag["last_evidence"] is not None
    # Prior work is preserved, not discarded.
    assert fresh.todos.get("TODO-001")["status"] == "RUNNING"


def test_recovery_detects_stale_lease(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    kernel.claims.claim(GOAL, "TODO-001", "OPENCODE_ENGINEER", ["engine/loop_control/a.py"], lease_seconds=-1)
    kernel.todos.transition("TODO-001", "CLAIMED", claimed_by="OPENCODE_ENGINEER")
    diag = kernel.recovery.diagnose(GOAL)
    assert diag["decision"] == "REPAIR"
    assert diag["stale_claims"]


def test_recovery_waits_on_open_gate(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    kernel.gates.raise_gate(GOAL, "PROTECTED_RESOURCE", "Needs approval to touch a protected path.",
                            "Do you authorize writing to 01_Raw?")
    diag = kernel.recovery.diagnose(GOAL)
    assert diag["decision"] == "WAIT"
    assert diag["open_gates"]


def test_recovery_blocks_on_terminal_goal(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    _run_full_turn(kernel, "TODO-001")
    kernel.complete_goal(GOAL, "OPENCODE_ENGINEER")
    diag = kernel.recovery.diagnose(GOAL)
    assert diag["decision"] == "BLOCK"
    assert "terminal" in diag["reason"]


# ------------------------------------------------------------ idempotency


def test_idempotent_writeback(kernel: LoopKernel, goal):
    """Critical operations applied three times must not duplicate state."""
    for _ in range(3):
        kernel.goals.create(goal_id=GOAL, title="t", objective="o",
                            completion_criteria=["c"], authority="HUMAN_OWNER")
        _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
        kernel.claims.claim(GOAL, "TODO-001", "OPENCODE_ENGINEER",
                            ["engine/loop_control/a.py"], idempotency_key="claim-key-1")
        kernel.evidence.register(GOAL, path="engine/loop_control/kernel.py", evidence_type="source",
                                 idempotency_key="ev-key-1")
        kernel.log_event(GOAL, "OPENCODE_ENGINEER", "PING", idempotency_key="evt-key-1")
        kernel.handoff.publish(GOAL, "OPENCODE_ENGINEER", "CODEX_ENGINEER", "state",
                               idempotency_key="ho-key-1")

    assert len(kernel.goals.all_goals()) == 1
    assert len(kernel.todos.list()) == 1
    assert len(kernel.claims.active_claims()) == 1
    assert len(kernel.evidence.list(goal_id=GOAL, evidence_type="source")) == 1
    assert len([e for e in kernel.store.read_run_history() if e["event_type"] == "PING"]) == 1
    assert len(kernel.handoff.history()) == 0


def test_idempotent_quota(kernel: LoopKernel, goal):
    for _ in range(3):
        kernel.quota.spend(GOAL, idempotency_key="same-key", turn=1, validation_failure=1)
    record = kernel.quota.get(GOAL)
    assert record["turns_consumed"] == 1
    assert record["validation_failures"] == 1


def test_idempotent_completion(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    _run_full_turn(kernel, "TODO-001")
    for _ in range(3):
        kernel.complete_todo(GOAL, "TODO-001", "OPENCODE_ENGINEER")
    completions = [e for e in kernel.store.read_run_history() if e["event_type"] == "TODO_COMPLETED"]
    assert len(completions) == 1
    assert kernel.todos.get("TODO-001")["status"] == "COMPLETED"


def test_idempotent_state_read(kernel: LoopKernel, goal):
    reads = [json.dumps(kernel.status(GOAL)["goal"], sort_keys=True) for _ in range(3)]
    assert len(set(reads)) == 1


# ------------------------------------------------------------- fail closed


def test_invalid_state_fail_closed(kernel: LoopKernel, goal):
    with pytest.raises(SchemaValidationError):
        validate({"goal_id": "X", "title": "t"}, "goal")  # missing required fields

    with pytest.raises(SchemaValidationError):
        validate({**kernel.goals.get(GOAL), "status": "TOTALLY_MADE_UP"}, "goal")

    with pytest.raises(SchemaValidationError):
        validate({**kernel.goals.get(GOAL), "goal_id": "lowercase bad id"}, "goal")

    with pytest.raises(LoopControlError):
        kernel.end_turn(GOAL, "TURN-x", "OPENCODE_ENGINEER", "TODO-001",
                        result="INVENTED_RESULT", action_summary="x", validation_passed=True)

    # Corrupt state on disk is rejected, never silently repaired.
    store = StateStore(kernel.store.root)
    corrupted = store.read("todos")
    corrupted["todos"].append({"todo_id": "BROKEN", "goal_id": GOAL})
    store.write("todos", corrupted)
    report = LoopKernel(root=kernel.store.root.parent, repo_root=kernel.store.root.parent).validate_state()
    assert report["status"] == "FAIL"
    assert any("todo" in e for e in report["errors"])


def test_empty_state_file_fails_closed(kernel: LoopKernel, goal):
    kernel.store.path("todos").write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        kernel.store.read("todos")


# --------------------------------------------------------------- evidence


def test_evidence_required(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    kernel.todos.transition("TODO-001", "CLAIMED", claimed_by="OPENCODE_ENGINEER")
    kernel.todos.transition("TODO-001", "RUNNING")
    kernel.todos.transition("TODO-001", "VALIDATING")

    with pytest.raises(LoopControlError, match="validation evidence"):
        kernel.complete_todo(GOAL, "TODO-001", "OPENCODE_ENGINEER")


def test_completion_requires_validation(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    turn = kernel.begin_turn(GOAL, "OPENCODE_ENGINEER", todo_id="TODO-001")
    with pytest.raises(LoopControlError, match="requires validation_passed"):
        kernel.end_turn(GOAL, turn["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
                        result="VALIDATED_COMPLETION", action_summary="claimed done",
                        validation_passed=False)


def test_evidence_artifacts_written_per_turn(kernel: LoopKernel, goal, tmp_path: Path):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    turn = kernel.begin_turn(GOAL, "OPENCODE_ENGINEER", todo_id="TODO-001")
    kernel.end_turn(GOAL, turn["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
                    result="VALIDATED_COMPLETION", action_summary="done",
                    validation_passed=True, validation_detail={"exit_code": 0},
                    tests={"passed": 1}, files_changed=["engine/loop_control/a.py"])

    directory = tmp_path / "evidence" / "loop_engineering_v1" / "runs" / GOAL / turn["turn_id"]
    for name in ("precheck.json", "action.json", "validation.json", "tests.json", "diff.json", "handoff.json"):
        assert (directory / name).is_file(), f"missing evidence artifact: {name}"

    for record in kernel.evidence.list(goal_id=GOAL, turn_id=turn["turn_id"]):
        assert record["sha256"], f"evidence without sha256: {record['type']}"
    assert kernel.evidence.verify_index()["status"] == "PASS"


def test_unverifiable_evidence_is_never_pass(kernel: LoopKernel, goal):
    record = kernel.evidence.register(GOAL, path="does/not/exist.json", evidence_type="claimed",
                                      validation_status="PASS")
    assert record["validation_status"] == "UNVERIFIED"
    assert record["sha256"] is None


def test_evidence_index_detects_drift(kernel: LoopKernel, goal, tmp_path: Path):
    target = tmp_path / "artifact.json"
    target.write_text('{"a": 1}', encoding="utf-8")
    kernel.evidence.register(GOAL, path=target, evidence_type="artifact")
    assert kernel.evidence.verify_index()["status"] == "PASS"
    target.write_text('{"a": 2}', encoding="utf-8")
    drift = kernel.evidence.verify_index()
    assert drift["status"] == "FAIL"
    assert drift["mismatched"]


# ------------------------------------------------------------ concurrency


def test_concurrency_scenarios(kernel: LoopKernel, goal):
    """A claims X, B is refused X; then A takes X and B takes Y without collision."""
    _add_todo(kernel, "TODO-X", ["engine/loop_control/x/**"])
    _add_todo(kernel, "TODO-Y", ["engine/loop_control/y/**"])
    _add_todo(kernel, "TODO-Z", ["engine/loop_control/x/inner.py"])

    kernel.claims.claim(GOAL, "TODO-X", "OPENCODE_ENGINEER", ["engine/loop_control/x/**"])

    with pytest.raises(ClaimConflictError) as exc:
        kernel.claims.claim(GOAL, "TODO-X", "CODEX_ENGINEER", ["engine/loop_control/x/**"])
    assert exc.value.code == "ACTIVE_CONFLICT"

    kernel.claims.claim(GOAL, "TODO-Y", "CODEX_ENGINEER", ["engine/loop_control/y/**"])
    assert len(kernel.claims.active_claims()) == 2

    with pytest.raises(ClaimConflictError) as exc2:
        kernel.claims.claim(GOAL, "TODO-Z", "CODEX_ENGINEER", ["engine/loop_control/x/inner.py"])
    assert exc2.value.code == "WRITE_SCOPE_OVERLAP"


# ------------------------------------------------------------ bounded turn


def test_bounded_turn_claims_only_one_todo(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"], priority=1)
    _add_todo(kernel, "TODO-002", ["engine/loop_control/b.py"], priority=2)
    kernel.begin_turn(GOAL, "OPENCODE_ENGINEER")
    active = kernel.claims.active_claims()
    assert len(active) == 1
    assert active[0]["todo_id"] == "TODO-001"
    assert kernel.todos.get("TODO-002")["status"] == "PENDING"


def test_turn_result_vocabulary_is_closed(kernel: LoopKernel, goal):
    assert len(TURN_RESULTS) == 11
    assert "VALIDATED_COMPLETION" in TURN_RESULTS
    assert "DONE" not in TURN_RESULTS
    assert "SUCCESS" not in TURN_RESULTS
    assert "COMPLETE" not in TURN_RESULTS


def test_failed_validation_returns_todo_to_pending(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    turn = kernel.begin_turn(GOAL, "OPENCODE_ENGINEER", todo_id="TODO-001")
    out = kernel.end_turn(GOAL, turn["turn_id"], "OPENCODE_ENGINEER", "TODO-001",
                          result="VALIDATION_FAILED", action_summary="tests failed",
                          validation_passed=False, made_progress=False)
    assert out["result"] == "VALIDATION_FAILED"
    assert kernel.todos.get("TODO-001")["status"] == "PENDING"
    assert kernel.claims.find_active(GOAL, "TODO-001") is None
    assert kernel.quota.get(GOAL)["validation_failures"] == 1


def test_unregistered_agent_rejected(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    with pytest.raises(LoopControlError, match="unregistered agent"):
        kernel.begin_turn(GOAL, "ROGUE_AGENT", todo_id="TODO-001")


def test_peer_registry_has_no_permanent_leader(kernel: LoopKernel):
    agents = kernel.registry()["agents"]
    ids = {a["agent_id"] for a in agents}
    assert {"OPENCODE_ENGINEER", "CODEX_ENGINEER", "AUDITOR", "QA", "RESEARCHER"} <= ids
    for agent in agents:
        assert "leader" not in json.dumps(agent).lower()
        assert set(agent["protected_write_scope"]) >= {"01_Raw/**", "data/db/meli_financial_v4.db"}


def test_goal_completion_requires_all_todos(kernel: LoopKernel, goal):
    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"], priority=1)
    _add_todo(kernel, "TODO-002", ["engine/loop_control/b.py"], priority=2)
    _run_full_turn(kernel, "TODO-001")
    with pytest.raises(LoopControlError, match="outstanding todos"):
        kernel.complete_goal(GOAL, "OPENCODE_ENGINEER")
    _run_full_turn(kernel, "TODO-002")
    assert kernel.complete_goal(GOAL, "OPENCODE_ENGINEER")["status"] == "COMPLETED"


# ------------------------------------------------- repo compatibility guards


def test_no_forbidden_coordination_tokens():
    """Loop Control must not break tools/verify_coordination_interface.py.

    That verifier bans four reserved coordination tokens outside its allowlist:
    the uppercase current-task marker and the double-quoted JSON forms of
    handoff, next_actor and current_owner. It also flags filenames containing
    'coordination'.
    """
    # Tokens are assembled rather than spelled literally: writing them out would
    # make this very test file an offender under the same rule.
    q = '"'
    reserved_words = "handoff next_actor current_owner".split()
    forbidden = ["CURRENT" + "_TASK"] + [q + w + q for w in reserved_words]
    roots = [
        REPO_ROOT / "engine" / "loop_control",
        REPO_ROOT / "governance" / "LOOP_ENGINEERING_PROTOCOL_V1.md",
        REPO_ROOT / "evidence" / "loop_engineering_v1",
    ]
    offenders: list[str] = []
    for root in roots:
        files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
        for path in files:
            if "__pycache__" in path.parts:
                continue
            if "coordination" in path.name.lower():
                offenders.append(f"{path.name}: filename contains 'coordination'")
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden:
                if token in text:
                    offenders.append(f"{path.name}: contains {token}")
    assert offenders == [], offenders


def test_runtime_control_plane_is_git_ignored():
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".loopx/" in gitignore


def test_kernel_contains_no_financial_logic():
    """The control plane must never become a second financial source of truth.

    The official DB path is permitted in constants.py for the sole purpose of
    declaring it a PROTECTED resource; that is a guard, not financial logic.
    """
    banned = ["marketplace_ledger", "duckdb", "SELECT ", "financial_group",
              "cierre_financiero", "import sqlite3", "engine.v4"]
    offenders: list[str] = []
    for path in (REPO_ROOT / "engine" / "loop_control").rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in banned:
            if token in text:
                offenders.append(f"{path.name}: {token}")
        if "meli_financial_v4" in text and path.name != "constants.py":
            offenders.append(f"{path.name}: references the official DB outside the protected-resource list")
    assert offenders == [], offenders

    protected = json.dumps(LoopKernel.__module__)  # keep import used
    assert protected
    from engine.loop_control.constants import DEFAULT_PROTECTED_RESOURCES
    assert "data/db/meli_financial_v4.db" in DEFAULT_PROTECTED_RESOURCES


def test_schemas_are_wellformed():
    schema_dir = REPO_ROOT / "engine" / "loop_control" / "schemas"
    names = {p.name for p in schema_dir.glob("*.schema.json")}
    assert {"goal.schema.json", "todo.schema.json", "gate.schema.json", "claim.schema.json",
            "handoff.schema.json", "run_event.schema.json", "quota.schema.json",
            "evidence.schema.json"} <= names
    for path in schema_dir.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        assert schema["type"] == "object"
        assert schema["required"]


def test_cli_commands_execute(kernel: LoopKernel, goal, tmp_path: Path):
    from engine.loop_control.__main__ import main

    _add_todo(kernel, "TODO-001", ["engine/loop_control/a.py"])
    root = str(tmp_path)
    assert main(["--root", root, "status"]) == 0
    assert main(["--root", root, "goal"]) == 0
    assert main(["--root", root, "todos"]) == 0
    assert main(["--root", root, "gates"]) == 0
    assert main(["--root", root, "recover"]) == 0
    assert main(["--root", root, "claim", "TODO-001", "--agent", "OPENCODE_ENGINEER"]) == 0
    assert main(["--root", root, "claim", "TODO-001", "--agent", "CODEX_ENGINEER"]) == 2
    assert main(["--root", root, CONTINUATION_SCHEMA]) == 0
    assert main(["--root", root, "validate"]) == 0
