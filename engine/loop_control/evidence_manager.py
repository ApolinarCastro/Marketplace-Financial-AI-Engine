"""Evidence contract.

PASS is only ever assigned when the referenced artifact exists on disk and its
SHA-256 was computed from that file. Anything else is UNVERIFIED.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .state_store import StateStore, find_repo_root, iso, new_id, sha256_file
from .validation import validate

EVIDENCE_ROOT = Path("evidence") / "loop_engineering_v1" / "runs"


class EvidenceManager:
    def __init__(self, store: StateStore, repo_root: Path | None = None) -> None:
        self.store = store
        self.repo_root = (repo_root or find_repo_root()).resolve()

    def _load(self) -> dict[str, Any]:
        return self.store.read("evidence_index")

    def _save(self, data: dict[str, Any]) -> None:
        self.store.write("evidence_index", data)

    def turn_dir(self, goal_id: str, turn_id: str) -> Path:
        return self.repo_root / EVIDENCE_ROOT / goal_id / turn_id

    # ------------------------------------------------------------ writes

    def write_artifact(
        self,
        goal_id: str,
        turn_id: str,
        name: str,
        payload: dict[str, Any],
        todo_id: str | None = None,
        evidence_type: str | None = None,
        validation_status: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Write a JSON artifact and register it in the evidence index."""
        directory = self.turn_dir(goal_id, turn_id)
        directory.mkdir(parents=True, exist_ok=True)
        filename = name if name.endswith(".json") else f"{name}.json"
        target = directory / filename
        target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        return self.register(
            goal_id=goal_id,
            todo_id=todo_id,
            turn_id=turn_id,
            evidence_type=evidence_type or filename.removesuffix(".json"),
            path=target,
            validation_status=validation_status,
            idempotency_key=idempotency_key or f"{goal_id}:{turn_id}:{filename}",
        )

    def register(
        self,
        goal_id: str,
        path: Path | str,
        evidence_type: str,
        todo_id: str | None = None,
        turn_id: str | None = None,
        validation_status: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        data = self._load()

        if idempotency_key:
            for record in data["evidence"]:
                if record.get("idempotency_key") == idempotency_key:
                    return record

        target = Path(path)
        absolute = target if target.is_absolute() else (self.repo_root / target)
        digest = sha256_file(absolute)

        if validation_status is None:
            validation_status = "PASS" if digest else "UNVERIFIED"
        elif validation_status == "PASS" and digest is None:
            validation_status = "UNVERIFIED"

        try:
            rel = absolute.resolve().relative_to(self.repo_root).as_posix()
        except ValueError:
            rel = absolute.as_posix()

        record = {
            "evidence_id": new_id("EV"),
            "goal_id": goal_id,
            "todo_id": todo_id,
            "turn_id": turn_id,
            "type": evidence_type,
            "path": rel,
            "sha256": digest,
            "created_at": iso(),
            "validation_status": validation_status,
            "idempotency_key": idempotency_key,
        }
        validate(record, "evidence")
        data["evidence"].append(record)
        self._save(data)
        return record

    # ------------------------------------------------------------- reads

    def list(
        self,
        goal_id: str | None = None,
        todo_id: str | None = None,
        turn_id: str | None = None,
        evidence_type: str | None = None,
    ) -> list[dict[str, Any]]:
        records = self._load()["evidence"]
        if goal_id:
            records = [r for r in records if r["goal_id"] == goal_id]
        if todo_id:
            records = [r for r in records if r["todo_id"] == todo_id]
        if turn_id:
            records = [r for r in records if r.get("turn_id") == turn_id]
        if evidence_type:
            records = [r for r in records if r["type"] == evidence_type]
        return records

    def has_passing_validation(self, goal_id: str, todo_id: str) -> bool:
        return any(
            r["validation_status"] == "PASS"
            for r in self.list(goal_id=goal_id, todo_id=todo_id, evidence_type="validation")
        )

    def verify_index(self) -> dict[str, Any]:
        """Re-hash every registered artifact and report drift."""
        results = {"total": 0, "verified": 0, "missing": [], "mismatched": []}
        for record in self._load()["evidence"]:
            results["total"] += 1
            absolute = self.repo_root / record["path"]
            digest = sha256_file(absolute)
            if digest is None:
                results["missing"].append(record["path"])
            elif record["sha256"] and digest != record["sha256"]:
                results["mismatched"].append(record["path"])
            else:
                results["verified"] += 1
        results["status"] = "PASS" if not results["missing"] and not results["mismatched"] else "FAIL"
        return results
