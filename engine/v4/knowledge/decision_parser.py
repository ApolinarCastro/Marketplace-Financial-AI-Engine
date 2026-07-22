"""KCE Module 2: DecisionParser — extracts structured knowledge from governance Markdown files."""
from __future__ import annotations
import re
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ParsedDecision:
    knowledge_id: str
    knowledge_type: str = "governance"
    title: str = ""
    summary: str = ""
    status: str = "ACTIVE"
    file_path: str = ""
    tags: list[str] = field(default_factory=list)


GOVERNANCE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "governance"

RE_DEC = re.compile(r"^#+\s*(DEC-\d{3})\b", re.MULTILINE)
RE_RFC = re.compile(r"^#+\s*(RFC_\w+)", re.MULTILINE)
RE_TITLE = re.compile(r"^#+\s+(.+)$", re.MULTILINE)
RE_STATUS = re.compile(r"\b(ACTIVE|PENDING|SUPERSEDED|CERTIFIED|OPEN|RESOLVED|FAIL|PASS)\b")
RE_DELTA = re.compile(r"\$0\s*delta", re.IGNORECASE)
RE_VERDICT = re.compile(r"(VERDICTO|VERDICT|RESULT|CONCLUSION)\s*[:\-]?\s*(.+)", re.IGNORECASE | re.MULTILINE)


class DecisionParser:
    def __init__(self, governance_dir: str | Path | None = None):
        self.dir = Path(governance_dir) if governance_dir else GOVERNANCE_DIR

    def parse_file(self, path: Path) -> list[ParsedDecision]:
        decisions: list[ParsedDecision] = []
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(self.dir.parent) if self.dir.parent in path.parents else str(path)

        title_match = RE_TITLE.search(text)
        title = title_match.group(1).strip() if title_match else path.stem

        first_line = text.split("\n")[0].strip("# ").strip() if text.strip() else ""

        all_ids: list[str] = []
        for m in RE_DEC.finditer(text):
            all_ids.append(m.group(1))
        if not all_ids:
            for m in RE_RFC.finditer(text):
                all_ids.append(m.group(1))

        if not all_ids:
            did = re.sub(r"[^A-Z0-9_]", "_", path.stem.upper())[:30]
            if re.search(r"certif|audit|report", path.stem, re.IGNORECASE):
                did = f"DOC-{did}"

            status = "CERTIFIED" if "CERTIFIED" in text or "PASS" in text.upper()[:200] else "ACTIVE"
            decisions.append(ParsedDecision(
                knowledge_id=did,
                title=title if title != first_line else path.stem,
                summary=self._extract_summary(text, path.stem),
                status=status,
                file_path=rel,
            ))
            return decisions

        shared = self._extract_summary(text, path.stem)
        for kid in all_ids:
            status = self._detect_status(text, kid)
            decisions.append(ParsedDecision(
                knowledge_id=kid if not kid.startswith("DEC-") or len(kid) >= 5 else kid,
                title=title,
                summary=shared,
                status=status,
                file_path=rel,
                tags=self._extract_tags(text),
            ))
        return decisions

    def scan_all(self) -> list[ParsedDecision]:
        if not self.dir.is_dir():
            return []
        all_decisions: list[ParsedDecision] = []
        for fpath in sorted(self.dir.rglob("*.md")):
            try:
                all_decisions.extend(self.parse_file(fpath))
            except Exception:
                pass
        return all_decisions

    @staticmethod
    def _extract_summary(text: str, fallback: str) -> str:
        for m in RE_VERDICT.finditer(text):
            v = m.group(2).strip()
            if v and len(v) > 5:
                return v[:200]
        lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 30]
        return lines[0][:200] if lines else fallback

    @staticmethod
    def _detect_status(text: str, kid: str) -> str:
        statuses = RE_STATUS.findall(text)
        if "SUPERSEDED" in statuses:
            return "SUPERSEDED"
        if "CERTIFIED" in statuses:
            return "CERTIFIED"
        if "FAIL" in statuses:
            return "FAIL"
        if "PASS" in statuses:
            return "CERTIFIED"
        if re.search(r"\bOBSOLETO\b", text):
            return "OBSOLETE"
        return "ACTIVE"

    @staticmethod
    def _extract_tags(text: str) -> list[str]:
        tags = []
        for mp in ["ML", "RIPLEY", "PARIS", "FALABELLA"]:
            if mp in text:
                tags.append(mp)
        if "CERT" in text[:200]:
            tags.append("CERTIFICATION")
        if "RFC" in text[:200]:
            tags.append("RFC")
        return tags
