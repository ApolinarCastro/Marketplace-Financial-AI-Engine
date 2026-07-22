"""KCE Module 3: KnowledgeIndexer — reads and writes knowledge_index.yaml with dedup."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml


ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_PATH = ROOT / "knowledge_index.yaml"


class KnowledgeIndexer:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else DEFAULT_PATH

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data or "knowledge" not in data:
            return []
        return data["knowledge"]

    def write(self, entries: list[dict]):
        validated = []
        seen: set[str] = set()
        for e in entries:
            kid = e.get("id", "")
            if not kid or kid in seen:
                continue
            seen.add(kid)
            validated.append({
                "id": kid,
                "type": e.get("type", "governance"),
                "title": e.get("title", ""),
                "summary": e.get("summary", ""),
                "status": e.get("status", "ACTIVE"),
            })
        with open(self.path, "w", encoding="utf-8") as f:
            yaml.dump({"knowledge": validated}, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    def merge(self, new_entries: list[dict], overwrite: bool = False) -> tuple[list[dict], list[dict]]:
        existing = self.read()
        existing_map = {e["id"]: e for e in existing}

        added: list[dict] = []
        updated: list[dict] = []
        for ne in new_entries:
            kid = ne.get("id", "")
            if not kid:
                continue
            if kid in existing_map:
                if overwrite:
                    existing_map[kid] = ne
                    updated.append(ne)
            else:
                existing_map[kid] = ne
                added.append(ne)

        merged = list(existing_map.values())
        self.write(merged)
        return added, updated

    def get(self, knowledge_id: str) -> dict | None:
        entries = self.read()
        for e in entries:
            if e["id"] == knowledge_id:
                return e
        return None

    def build_knowledge_index(self) -> bool:
        """(C1) Rebuild knowledge_index.yaml from governance + audit + taxonomy sources.

        Uses KnowledgeConsolidationEngine to scan all sources, then merge into index.
        Returns True if at least one entry was added or updated.
        """
        try:
            from engine.v4.knowledge.kce import KnowledgeConsolidationEngine, KCEConfig
            engine = KnowledgeConsolidationEngine(
                config=KCEConfig(
                    knowledge_index_path=str(self.path),
                    overwrite_existing=True,
                )
            )
            result = engine.consolidate()
            return result.index_added > 0 or result.index_updated > 0
        except ImportError:
            return self._build_minimal()
        except Exception:
            import logging
            logging.getLogger("meli.kce").exception("build_knowledge_index failed")
            return False

    def _build_minimal(self) -> bool:
        """Fallback: scan governance/ directory directly with DecisionParser."""
        try:
            from engine.v4.knowledge.decision_parser import DecisionParser
            parser = DecisionParser()
            decisions = parser.scan_all()
            new_entries = [
                {"id": d.knowledge_id, "type": d.knowledge_type, "title": d.title,
                 "summary": d.summary, "status": d.status}
                for d in decisions
            ]
            if not new_entries:
                return False
            added, updated = self.merge(new_entries, overwrite=True)
            return len(added) + len(updated) > 0
        except Exception:
            import logging
            logging.getLogger("meli.kce").exception("build_knowledge_index fallback failed")
            return False

    def search(self, keyword: str, type_filter: str | None = None, status_filter: str | None = None) -> list[dict]:
        entries = self.read()
        kw = keyword.lower()
        results = []
        for e in entries:
            if kw and kw not in e.get("title", "").lower() and kw not in e.get("summary", "").lower():
                continue
            if type_filter and e.get("type") != type_filter:
                continue
            if status_filter and e.get("status") != status_filter:
                continue
            results.append(e)
        return results
