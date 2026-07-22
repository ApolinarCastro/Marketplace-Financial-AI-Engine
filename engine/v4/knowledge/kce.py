"""KnowledgeConsolidationEngine (KCE) — main orchestrator.

Automatically learns from:
  - marketplace_auditoria_v1 (audit findings)
  - governance/*.md (DECs, RFCs, certification reports)
  - knowledge/taxonomy/*.json (taxonomy files)

Outputs:
  - Updated knowledge_index.yaml with auto-discovered entries
  - Retention recommendations per governance file
  - Coverage reports (what knowledge is vs. is not yet absorbed into code)
"""
from __future__ import annotations
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

from engine.v4.knowledge.audit_scanner import AuditScanner
from engine.v4.knowledge.decision_parser import DecisionParser, ParsedDecision
from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
from engine.v4.knowledge.retention_manager import RetentionManager


logger = logging.getLogger("meli.kce")

ROOT = Path(__file__).resolve().parent.parent.parent.parent


@dataclass
class KCEConfig:
    governance_dir: str | Path = ""
    knowledge_index_path: str | Path = ""
    taxonomy_dir: str | Path = ""
    dry_run: bool = False
    overwrite_existing: bool = False
    auto_archive: bool = False


@dataclass
class KCEResult:
    audit_entries: list[dict] = field(default_factory=list)
    decision_entries: list[dict] = field(default_factory=list)
    taxonomy_entries: list[dict] = field(default_factory=list)
    index_added: int = 0
    index_updated: int = 0
    files_scanned: int = 0
    retention_recommendations: list[dict] = field(default_factory=list)
    coverage_gaps: list[dict] = field(default_factory=list)


class KnowledgeConsolidationEngine:
    def __init__(self, db=None, config: KCEConfig | None = None):
        self.db = db
        self.cfg = config or KCEConfig()
        self.cfg.governance_dir = self.cfg.governance_dir or str(ROOT / "governance")
        self.cfg.knowledge_index_path = self.cfg.knowledge_index_path or str(ROOT / "knowledge_index.yaml")
        self.cfg.taxonomy_dir = self.cfg.taxonomy_dir or str(ROOT / "KnowledgeBase" / "Marketplace" / "Taxonomy")

        self.audit_scanner = AuditScanner(db) if db else None
        self.decision_parser = DecisionParser(self.cfg.governance_dir)
        self.indexer = KnowledgeIndexer(self.cfg.knowledge_index_path)
        self.retention = RetentionManager()

    def consolidate(self) -> KCEResult:
        result = KCEResult()

        # 1. Scan audits → knowledge entries
        if self.audit_scanner:
            audit_entries = self.audit_scanner.scan()
            result.audit_entries = [
                {"id": e.knowledge_id, "type": e.knowledge_type, "title": e.title,
                 "summary": e.summary, "status": e.status}
                for e in audit_entries
            ]

        # 2. Parse governance files → knowledge entries
        decisions = self.decision_parser.scan_all()
        result.files_scanned = len(set(d.file_path for d in decisions))
        result.decision_entries = [
            {"id": d.knowledge_id, "type": d.knowledge_type, "title": d.title,
             "summary": d.summary, "status": d.status}
            for d in decisions
        ]

        # 3. Scan taxonomy files → knowledge entries
        result.taxonomy_entries = self._scan_taxonomies()

        # 4. Merge into knowledge_index.yaml
        all_new = result.audit_entries + result.decision_entries + result.taxonomy_entries
        if not self.cfg.dry_run:
            added, updated = self.indexer.merge(all_new, overwrite=self.cfg.overwrite_existing)
            result.index_added = len(added)
            result.index_updated = len(updated)
        else:
            result.index_added = len(all_new)
            result.index_updated = 0

        # 5. Coverage analysis: which knowledge IDs are referenced in source code
        result.coverage_gaps = self._analyze_coverage_gaps(all_new)

        # 6. Retention recommendations
        if self.cfg.auto_archive:
            result.retention_recommendations = self._generate_retention_recs()

        return result

    def _scan_taxonomies(self) -> list[dict]:
        tax_dir = Path(self.cfg.taxonomy_dir)
        entries: list[dict] = []
        if not tax_dir.is_dir():
            return entries
        for fpath in sorted(tax_dir.glob("*.json")):
            mp = fpath.stem.replace("_v1", "").replace("_v2", "").upper()
            sig_count = 0
            noise_count = 0
            try:
                import json
                data = json.loads(fpath.read_text(encoding="utf-8"))
                dc = data.get("detalle_classification", {})
                for v in dc.values():
                    if isinstance(v, dict):
                        if v.get("signal", True):
                            sig_count += 1
                        else:
                            noise_count += 1
            except Exception:
                pass
            entries.append({
                "id": f"TAXONOMY-{mp}",
                "type": "taxonomy",
                "title": f"{mp} Signal/Noise Taxonomy",
                "summary": f"{sig_count} SIGNAL / {noise_count} NOISE from {fpath.name}",
                "status": "CERTIFIED",
            })
        return entries

    def _analyze_coverage_gaps(self, all_entries: list[dict]) -> list[dict]:
        gaps: list[dict] = []
        codebase_ids = self._find_codebase_references()
        for entry in all_entries:
            kid = entry.get("id", "")
            if kid not in codebase_ids:
                gaps.append({
                    "knowledge_id": kid,
                    "title": entry.get("title", ""),
                    "status": entry.get("status", ""),
                    "type": entry.get("type", ""),
                    "reason": "Not referenced in Python source code",
                })
        return gaps

    def _find_codebase_references(self) -> set[str]:
        refs: set[str] = set()
        engine_dir = ROOT / "engine" / "v4"
        if not engine_dir.is_dir():
            return refs
        for fpath in engine_dir.rglob("*.py"):
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
                for m in __import__("re").finditer(r"\b(DEC-\d{3}|RFC_\w+|AUDIT-\w+|TAXONOMY-\w+|CERT-\w+)\b", text):
                    refs.add(m.group(1))
            except Exception:
                pass
        return refs

    def _generate_retention_recs(self) -> list[dict]:
        coverage_ids = self._find_codebase_references()
        entries = self.indexer.read()
        recs: list[dict] = []
        for entry in entries:
            action = self.retention.suggest_action(entry, coverage_ids)
            if action != "KEEP":
                recs.append({
                    "knowledge_id": entry.get("id"),
                    "current_status": entry.get("status"),
                    "suggested_action": action,
                })
        return recs

    def status_report(self) -> dict:
        entries = self.indexer.read()
        by_type: dict[str, int] = {}
        by_status: dict[str, int] = {}
        for e in entries:
            by_type[e.get("type", "unknown")] = by_type.get(e.get("type", "unknown"), 0) + 1
            by_status[e.get("status", "unknown")] = by_status.get(e.get("status", "unknown"), 0) + 1
        return {
            "total_entries": len(entries),
            "by_type": by_type,
            "by_status": by_status,
        }
