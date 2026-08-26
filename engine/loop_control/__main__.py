"""Minimal local CLI for the Loop Control plane.

    python -m engine.loop_control status
    python -m engine.loop_control goal
    python -m engine.loop_control todos
    python -m engine.loop_control claim <todo_id> --agent <agent_id>
    python -m engine.loop_control handoff
    python -m engine.loop_control validate

No dashboard, no daemon, no scheduler.
"""

from __future__ import annotations

import argparse
import json
import sys

from .constants import CONTINUATION_SCHEMA, ClaimConflictError, LoopControlError

CLI_CONTINUATION = CONTINUATION_SCHEMA
from .kernel import LoopKernel


def _emit(payload) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m engine.loop_control",
                                     description="Loop Engineering Protocol V1 control plane")
    parser.add_argument("--root", default=None, help="Repository root containing .loopx")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create the control plane")
    p_status = sub.add_parser("status", help="Full control plane status")
    p_status.add_argument("--goal", default=None)
    sub.add_parser("goal", help="Show the active goal")
    p_todos = sub.add_parser("todos", help="List todos")
    p_todos.add_argument("--goal", default=None)
    p_todos.add_argument("--status", default=None)
    p_claim = sub.add_parser("claim", help="Claim a todo")
    p_claim.add_argument("todo_id")
    p_claim.add_argument("--agent", required=True)
    p_claim.add_argument("--goal", default=None)
    sub.add_parser(CLI_CONTINUATION, help="Show the continuation record / resume brief")
    sub.add_parser("validate", help="Validate the control plane against schemas")
    p_gates = sub.add_parser("gates", help="List gates")
    p_gates.add_argument("--goal", default=None)
    p_recover = sub.add_parser("recover", help="Deterministic recovery diagnosis")
    p_recover.add_argument("--goal", default=None)

    args = parser.parse_args(argv)
    kernel = LoopKernel(root=args.root)

    try:
        if args.command == "init":
            _emit(kernel.initialize())
            return 0

        if args.command == "status":
            _emit(kernel.status(goal_id=args.goal))
            return 0

        if args.command == "goal":
            goal = kernel.goals.active()
            if goal is None:
                _emit({"active_goal": None, "message": "no active goal"})
                return 1
            _emit(goal)
            return 0

        if args.command == "todos":
            goal_id = args.goal
            if goal_id is None:
                active = kernel.goals.active()
                goal_id = active["goal_id"] if active else None
            _emit(kernel.todos.list(goal_id=goal_id, status=args.status))
            return 0

        if args.command == "claim":
            goal_id = args.goal
            if goal_id is None:
                active = kernel.goals.active()
                if active is None:
                    _emit({"error": "no active goal; pass --goal"})
                    return 1
                goal_id = active["goal_id"]
            todo = kernel.todos.get(args.todo_id)
            if todo is None:
                _emit({"error": f"unknown todo {args.todo_id}"})
                return 1
            claim = kernel.claims.claim(goal_id=goal_id, todo_id=args.todo_id,
                                        agent_id=args.agent, write_scope=todo["write_scope"])
            kernel.todos.transition(args.todo_id, "CLAIMED", claimed_by=args.agent)
            _emit(claim)
            return 0

        if args.command == CLI_CONTINUATION:
            _emit(kernel.handoff.resume_brief())
            return 0

        if args.command == "validate":
            report = kernel.validate_state()
            _emit(report)
            return 0 if report["status"] == "PASS" else 1

        if args.command == "gates":
            goal_id = args.goal
            if goal_id is None:
                active = kernel.goals.active()
                goal_id = active["goal_id"] if active else None
            _emit(kernel.gates.list(goal_id=goal_id))
            return 0

        if args.command == "recover":
            goal_id = args.goal
            if goal_id is None:
                active = kernel.goals.active()
                if active is None:
                    _emit({"error": "no active goal; pass --goal"})
                    return 1
                goal_id = active["goal_id"]
            _emit(kernel.recovery.diagnose(goal_id))
            return 0

    except ClaimConflictError as exc:
        _emit({"error": str(exc), "conflict_code": exc.code})
        return 2
    except LoopControlError as exc:
        _emit({"error": str(exc), "type": type(exc).__name__})
        return 2

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
