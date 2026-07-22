"""KnowledgeTrigger — Stage 5 of ingestion pipeline.

Updates knowledge artifacts after successful ingestion:
1. KnowledgeIndexer refresh (DECs, RFCs, audit findings → knowledge_index.yaml)
2. Pattern detection (new detalle values from ledger)
3. PatternRegistry sync (structured patterns from governance)
4. Obsidian export (patterns → markdown vault)

Zero financial logic. Reads ledger detalle values only.
"""
from __future__ import annotations
from typing import Any

from engine.v4.database import DatabaseV4


class KnowledgeTrigger:
    def __init__(
        self,
        db: DatabaseV4 | None = None,
        knowledge_indexer: Any = None,
        pattern_registry: Any = None,
        obsidian_path: str | None = None,
    ):
        self.db = db or DatabaseV4.get(read_only=False)
        self.indexer = knowledge_indexer
        self.registry = pattern_registry
        self.obsidian_path = obsidian_path
        self._has_indexer = knowledge_indexer is not None
        self._has_registry = pattern_registry is not None

    def trigger(self, marketplace: str, period: str | None = None) -> dict[str, Any]:
        result: dict[str, Any] = {
            "knowledge_index": {"executed": False, "status": "SKIPPED", "reason": "No indexer provided"},
            "new_patterns": [],
            "obsidian_written": 0,
            "errors": [],
        }

        if self._has_indexer:
            try:
                idx_result = self.indexer.build_knowledge_index()
                result["knowledge_index"]["executed"] = True
                result["knowledge_index"]["status"] = "PASS" if idx_result else "DEGRADED"
            except Exception as e:
                result["knowledge_index"]["status"] = "ERROR"
                result["errors"].append(f"KnowledgeIndexer failed: {e}")

        try:
            new_detalles = self._find_new_detalles(marketplace)
            result["new_patterns"] = new_detalles
        except Exception as e:
            result["errors"].append(f"Pattern detection failed: {e}")

        if self._has_registry:
            try:
                from pathlib import Path
                vault = Path(self.obsidian_path) if self.obsidian_path else None
                if vault and vault.exists():
                    result["obsidian_written"] = self.registry.to_obsidian(vault)
            except Exception as e:
                result["errors"].append(f"Obsidian export failed: {e}")

        overall = (
            result["knowledge_index"]["status"] != "ERROR"
            and len(result["errors"]) == 0
        )
        result["overall_status"] = "PASS" if overall else "DEGRADED"
        return result

    def _find_new_detalles(self, marketplace: str) -> list[dict[str, Any]]:
        rows = self.db.query(
            "SELECT detalle, COUNT(*) as cnt, SUM(monto) as total, "
            "MIN(monto) < 0 as has_negative "
            "FROM marketplace_ledger_v1 "
            "WHERE LOWER(marketplace) = LOWER(?) AND detalle IS NOT NULL AND detalle != '' "
            "GROUP BY detalle "
            "ORDER BY cnt DESC",
            [marketplace],
        )
        return [
            {
                "detalle": r["detalle"],
                "count": int(r["cnt"]),
                "total_amount": float(r["total"]) if r["total"] else 0.0,
                "has_negative": bool(r["has_negative"]),
            }
            for _, r in rows.iterrows()
        ]
