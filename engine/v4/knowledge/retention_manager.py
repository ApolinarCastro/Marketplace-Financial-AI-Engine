"""KCE Module 4: RetentionManager — file lifecycle and status transitions."""
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent.parent.parent

_LIFECYCLE = {
    "ACTIVE": {"ABSORBED", "OBSOLETE", "SUPERSEDED"},
    "ABSORBED": {"ARCHIVED"},
    "ARCHIVED": {"DELETED"},
    "OBSOLETE": {"ARCHIVED", "DELETED"},
    "SUPERSEDED": {"ARCHIVED"},
    "CERTIFIED": {"SUPERSEDED", "OBSOLETE"},
    "FAIL": {"OBSOLETE"},
    "PENDING": {"ACTIVE", "OBSOLETE"},
    "OPEN": {"RESOLVED", "OBSOLETE"},
    "RESOLVED": {"ARCHIVED"},
}


@dataclass
class FileRecord:
    path: Path
    relative_path: str
    size_bytes: int
    modified_ts: datetime
    knowledge_ids: list[str] = field(default_factory=list)
    recommended_action: str = "KEEP"


class RetentionManager:
    def __init__(self, root: str | Path | None = None):
        self.root = Path(root) if root else ROOT

    def allowed_transition(self, current: str, target: str) -> bool:
        return target in _LIFECYCLE.get(current, set())

    def suggest_action(self, entry: dict, governance_coverage: set[str]) -> str:
        kid = entry.get("id", "")
        status = entry.get("status", "ACTIVE")
        ktype = entry.get("type", "governance")

        if kid in governance_coverage:
            return "KEEP"
        if status == "ABSORBED":
            return "ARCHIVE"
        if status == "SUPERSEDED":
            return "ARCHIVE"
        if status == "OBSOLETE":
            return "ARCHIVE"
        if ktype == "taxonomy" and status == "CERTIFIED":
            return "KEEP"
        if status == "PENDING":
            return "MONITOR"
        return "KEEP"

    def scan_files(self, directory: str | Path, pattern: str = "*.md") -> list[FileRecord]:
        base = Path(directory) if isinstance(directory, str | Path) else directory
        files: list[FileRecord] = []
        for fpath in sorted(base.rglob(pattern)):
            try:
                stat = fpath.stat()
                files.append(FileRecord(
                    path=fpath,
                    relative_path=str(fpath.relative_to(self.root)),
                    size_bytes=stat.st_size,
                    modified_ts=datetime.fromtimestamp(stat.st_mtime),
                ))
            except Exception:
                pass
        return files
