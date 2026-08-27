"""Dogfood harness: govern the Loop Engineering certification with Loop Control.

Creates the LOOP-ENGINEERING-SELF-CERT goal, drives three real todos through
bounded turns (each validated by an actually-executed command), performs a
cross-agent continuation, and closes the goal.

Writes evidence/loop_engineering_v1/dogfood_report.json.

Read-only with respect to 01_Raw/, data/db/, .git/ and governance/coordination/.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from engine.loop_control import LoopKernel  # noqa: E402
from engine.loop_control.state_store import iso  # noqa: E402

GOAL = "LOOP-ENGINEERING-SELF-CERT"
PY = str(REPO_ROOT / ".venv" / "Scripts" / "python.exe")


def run(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=900)
    tail = (proc.stdout or "").strip().splitlines()[-6:]
    return {"command": " ".join(cmd), "exit_code": proc.returncode, "stdout_tail": tail}


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(131072), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    db = REPO_ROOT / "data" / "db" / "meli_financial_v4.db"
    raw_before = sum(1 for _ in (REPO_ROOT / "01_Raw").rglob("*") if _.is_file())
    db_before = sha256(db)

    kernel = LoopKernel()
    kernel.initialize()

    kernel.goals.create(
        goal_id=GOAL,
        title="Loop Engineering Protocol V1 self-certification",
        objective="Prove the control plane can govern its own certification end to end.",
        completion_criteria=[
            "kernel test suite executes and passes",
            "control plane validates against schemas",
            "cross-agent continuation is reconstructible from disk alone",
        ],
        authority="HUMAN_OWNER",
        scope=["engine/loop_control/**", "tests/test_loop_control.py", "evidence/loop_engineering_v1/**"],
        non_goals=["any financial change", "any RAW mutation", "any official DB mutation"],
        activate=True,
    )

    kernel.todos.add("TODO-001", GOAL, "Execute the Loop Control test suite",
                     ["tests/test_loop_control.py"],
                     [f"{PY} -m pytest tests/test_loop_control.py -q"], priority=1)
    kernel.todos.add("TODO-002", GOAL, "Validate the control plane against schemas",
                     ["evidence/loop_engineering_v1/**"],
                     [f"{PY} -m engine.loop_control validate"], priority=2, dependencies=["TODO-001"])
    kernel.todos.add("TODO-003", GOAL, "Verify the coordination interface did not regress",
                     ["engine/loop_control/**"],
                     [f"{PY} -m pytest tests/test_coordination_interface.py -q"],
                     priority=3, dependencies=["TODO-002"])

    turns: list[dict] = []

    # --- TODO-001, executed by OPENCODE_ENGINEER -------------------------
    t1 = kernel.begin_turn(GOAL, "OPENCODE_ENGINEER", hypothesis="kernel-suite-green")
    assert t1["started"], t1
    todo1 = t1["todo"]["todo_id"]
    assert todo1 == "TODO-001", f"kernel selected {todo1}, expected TODO-001"
    r1 = run([PY, "-m", "pytest", "tests/test_loop_control.py", "-q", "-p", "no:cacheprovider"])
    out1 = kernel.end_turn(
        GOAL, t1["turn_id"], "OPENCODE_ENGINEER", todo1,
        result="VALIDATED_COMPLETION" if r1["exit_code"] == 0 else "VALIDATION_FAILED",
        action_summary="ran the Loop Control certification suite",
        validation_passed=r1["exit_code"] == 0,
        validation_detail=r1,
        tests={"suite": "tests/test_loop_control.py", "exit_code": r1["exit_code"]},
        files_changed=[],
        next_agent="CODEX_ENGINEER",
        hypothesis="kernel-suite-green",
    )
    turns.append({"todo": todo1, "agent": "OPENCODE_ENGINEER", "result": out1["result"], "validation": r1})

    # --- Cross-agent continuation: cold session, disk only ---------------
    cold = LoopKernel()
    brief = cold.handoff.resume_brief()
    continuation_ok = (
        brief["resumable"] is True
        and brief["receiving_agent"] == "CODEX_ENGINEER"
        and "TODO-001" in brief["completed_todos"]
        and brief["next_todo"] == "TODO-002"
        and bool(brief["evidence"])
    )

    # --- TODO-002, executed by CODEX_ENGINEER ----------------------------
    t2 = cold.begin_turn(GOAL, "CODEX_ENGINEER", hypothesis="state-schema-valid")
    assert t2["started"], t2
    todo2 = t2["todo"]["todo_id"]
    assert todo2 == "TODO-002", f"kernel selected {todo2}, expected TODO-002 (TODO-001 may have failed)"
    r2 = run([PY, "-m", "engine.loop_control", "validate"])
    out2 = cold.end_turn(
        GOAL, t2["turn_id"], "CODEX_ENGINEER", todo2,
        result="VALIDATED_COMPLETION" if r2["exit_code"] == 0 else "VALIDATION_FAILED",
        action_summary="validated the control plane against all schemas",
        validation_passed=r2["exit_code"] == 0,
        validation_detail=r2,
        tests={"suite": "engine.loop_control validate", "exit_code": r2["exit_code"]},
        files_changed=[],
        next_agent="AUDITOR",
        hypothesis="state-schema-valid",
    )
    turns.append({"todo": todo2, "agent": "CODEX_ENGINEER", "result": out2["result"], "validation": r2})

    # --- TODO-003, executed by AUDITOR -----------------------------------
    audit = LoopKernel()
    t3 = audit.begin_turn(GOAL, "AUDITOR", hypothesis="no-coordination-regression")
    assert t3["started"], t3
    todo3 = t3["todo"]["todo_id"]
    assert todo3 == "TODO-003", f"kernel selected {todo3}, expected TODO-003"
    r3 = run([PY, "-m", "pytest", "tests/test_coordination_interface.py", "-q", "-p", "no:cacheprovider"])
    out3 = audit.end_turn(
        GOAL, t3["turn_id"], "AUDITOR", todo3,
        result="VALIDATED_COMPLETION" if r3["exit_code"] == 0 else "VALIDATION_FAILED",
        action_summary="confirmed the pre-existing coordination interface still passes its suite",
        validation_passed=r3["exit_code"] == 0,
        validation_detail=r3,
        tests={"suite": "tests/test_coordination_interface.py", "exit_code": r3["exit_code"]},
        files_changed=[],
        next_agent="OPENCODE_ENGINEER",
        hypothesis="no-coordination-regression",
    )
    turns.append({"todo": todo3, "agent": "AUDITOR", "result": out3["result"], "validation": r3})

    final = LoopKernel()
    goal_record = final.complete_goal(GOAL, "AUDITOR")
    state_report = final.validate_state()

    db_after = sha256(db)
    raw_after = sum(1 for _ in (REPO_ROOT / "01_Raw").rglob("*") if _.is_file())

    all_completed = all(t["result"] == "VALIDATED_COMPLETION" for t in turns)
    report = {
        "evidence_id": "LOOP_ENG_V1_DOGFOOD",
        "goal_id": GOAL,
        "executed_at": iso(),
        "agents_used": ["OPENCODE_ENGINEER", "CODEX_ENGINEER", "AUDITOR"],
        "turns": turns,
        "cross_agent_continuation": {
            "reconstructed_from_disk_only": continuation_ok,
            "receiving_agent": brief.get("receiving_agent"),
            "completed_todos": brief.get("completed_todos"),
            "next_todo": brief.get("next_todo"),
            "evidence_count": len(brief.get("evidence", [])),
        },
        "goal_final_status": goal_record["status"],
        "control_plane_validation": state_report,
        "quota_consumed": final.quota.get(GOAL),
        "run_events": len([e for e in final.store.read_run_history() if e["goal_id"] == GOAL]),
        "evidence_records": len(final.evidence.list(goal_id=GOAL)),
        "integrity": {
            "official_db_sha256_before": db_before,
            "official_db_sha256_after": db_after,
            "official_db_unchanged": db_before == db_after,
            "raw_file_count_before": raw_before,
            "raw_file_count_after": raw_after,
            "raw_mutations": raw_after - raw_before,
        },
        "verdict": "PASS" if (
            all_completed
            and continuation_ok
            and goal_record["status"] == "COMPLETED"
            and state_report["status"] == "PASS"
            and db_before == db_after
            and raw_before == raw_after
        ) else "FAIL",
    }

    out = REPO_ROOT / "evidence" / "loop_engineering_v1" / "dogfood_report.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "goal_status": report["goal_final_status"],
                      "turns": len(turns), "report": str(out.relative_to(REPO_ROOT))}, indent=2))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
