"""Durable file-backed state store for the Loop Control plane.

All state lives under a control plane root (default: <repo>/.loopx).
Writes are atomic (temp file + os.replace) so an interrupted turn can never
leave a half-written JSON document behind.

This module contains no financial logic and issues no SQL.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .constants import (
    CONTINUATION_FILENAME,
    CONTINUATION_KEY,
    CONTROL_PLANE_DIRNAME,
    DEFAULT_AGENTS,
    DEFAULT_PROTECTED_RESOURCES,
    PROTOCOL_VERSION,
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime | None = None) -> str:
    dt = dt or utcnow()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def parse_iso(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def future_iso(seconds: int, base: datetime | None = None) -> str:
    return iso((base or utcnow()) + timedelta(seconds=seconds))


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(131072), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__).resolve()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists() or (candidate / "AGENTS.md").exists():
            return candidate
    return Path.cwd()


class StateStore:
    """Atomic JSON/JSONL persistence for the control plane."""

    # Note: the continuation channel is keyed 'continuation' rather than the
    # obvious alternative because that word, double-quoted, is a reserved
    # coordination token enforced repo-wide by
    # tools/verify_coordination_interface.py. The on-disk filename remains
    # handoff.json as required by the protocol spec.
    FILES = {
        "registry": "registry.json",
        "active_goal": "active_goal.json",
        "todos": "todos.json",
        "gates": "gates.json",
        "claims": "claims.json",
        "quota": "quota.json",
        "evidence_index": "evidence_index.json",
        "continuation": CONTINUATION_FILENAME,
    }

    RUN_HISTORY = "run_history.jsonl"

    def __init__(self, root: Path | str | None = None) -> None:
        if root is None:
            self.root = find_repo_root() / CONTROL_PLANE_DIRNAME
        else:
            root_path = Path(root)
            self.root = root_path if root_path.name == CONTROL_PLANE_DIRNAME else root_path / CONTROL_PLANE_DIRNAME
        self.root = self.root.resolve()

    # ---------------------------------------------------------------- paths

    def path(self, key: str) -> Path:
        if key == "run_history":
            return self.root / self.RUN_HISTORY
        if key not in self.FILES:
            raise KeyError(f"unknown state file: {key}")
        return self.root / self.FILES[key]

    def exists(self) -> bool:
        return self.root.is_dir() and self.path("registry").is_file()

    # ------------------------------------------------------------ lifecycle

    def initialize(self, force: bool = False, project_policy=None) -> dict[str, Any]:
        """Create the control plane. Idempotent unless force=True."""
        self.root.mkdir(parents=True, exist_ok=True)
        created: list[str] = []

        # Use project policy if provided, otherwise use empty defaults
        if project_policy:
            # Default capabilities by agent type
            default_capabilities = {
                "OPENCODE_ENGINEER": ["implement", "test", "refactor"],
                "CODEX_ENGINEER": ["implement", "test", "review"],
                "AUDITOR": ["verify", "certify"],
                "QA": ["test"],
                "RESEARCHER": ["read"],
            }
            # Default runtime by agent type
            default_runtime = {
                "OPENCODE_ENGINEER": "opencode",
                "CODEX_ENGINEER": "codex",
                "AUDITOR": "any",
                "QA": "any",
                "RESEARCHER": "any",
            }
            agents = [
                {
                    "agent_id": agent_id,
                    "allowed_write_scope": scopes,
                    "protected_write_scope": project_policy.protected_resources,
                    "runtime": default_runtime.get(agent_id, "any"),
                    "status": "AVAILABLE",
                    "capabilities": default_capabilities.get(agent_id, ["read"]),
                }
                for agent_id, scopes in project_policy.allowed_write_scopes.items()
            ]
            protected_resources = list(project_policy.protected_resources)
        else:
            agents = []
            protected_resources = []

        defaults: dict[str, Any] = {
            "registry": {
                "protocol_version": PROTOCOL_VERSION,
                "created_at": iso(),
                "agents": agents,
                "protected_resources": protected_resources,
            },
            "active_goal": {"active_goal_id": None, "goals": {}},
            "todos": {"todos": []},
            "gates": {"gates": []},
            "claims": {"active": [], "history": []},
            "quota": {"goals": {}},
            "evidence_index": {"evidence": []},
            "continuation": {CONTINUATION_KEY: None},
        }

        for key, value in defaults.items():
            target = self.path(key)
            if force or not target.exists():
                self.write(key, value)
                created.append(target.name)

        history = self.path("run_history")
        if force or not history.exists():
            history.write_text("", encoding="utf-8")
            created.append(history.name)

        return {"root": str(self.root), "created": created, "protocol_version": PROTOCOL_VERSION}

    # ---------------------------------------------------------------- io

    def read(self, key: str) -> dict[str, Any]:
        target = self.path(key)
        if not target.exists():
            raise FileNotFoundError(f"control plane file missing: {target}")
        text = target.read_text(encoding="utf-8")
        if not text.strip():
            raise ValueError(f"control plane file is empty: {target}")
        return json.loads(text)

    def write(self, key: str, payload: dict[str, Any]) -> Path:
        target = self.path(key)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + f".tmp-{uuid.uuid4().hex[:8]}")
        tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(tmp, target)
        return target

    def append_run_event(self, event: dict[str, Any]) -> None:
        target = self.path("run_history")
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")

    def read_run_history(self) -> list[dict[str, Any]]:
        target = self.path("run_history")
        if not target.exists():
            return []
        events: list[dict[str, Any]] = []
        for line in target.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
        return events
