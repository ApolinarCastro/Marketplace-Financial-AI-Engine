"""PersistenceEngine — Stage 3 of ingestion pipeline.

Persists data:
1. Register file in file_registry
2. Delegate to SurgicalLoader for actual DB persistence

Zero financial logic. Zero direct ledger manipulation.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Callable

from engine.v4.database import DatabaseV4
from engine.v4.surgical_loader import SurgicalLoader


class PersistenceEngine:
    def __init__(
        self,
        db: DatabaseV4 | None = None,
        loader: Any = None,
    ):
        self.db = db or DatabaseV4.get(read_only=False)
        self._loader = loader

    def _get_loader(self) -> Any:
        if self._loader is not None:
            return self._loader
        return SurgicalLoader()

    def persist(
        self, file_path: str | Path, marketplace: str, sha256: str,
        execution_id: str | None = None, document_type: str | None = None,
        period: str | None = None,
    ) -> dict[str, Any]:
        path = Path(file_path) if isinstance(file_path, str) else file_path
        result: dict[str, Any] = {
            "file_registered": False,
            "loader_executed": False,
            "records_inserted": 0,
            "records_updated": 0,
            "records_rejected": 0,
            "errors": [],
            "warnings": [],
            "records_read": 0,
            "records_existing": 0,
        }

        self.db.register_file(
            str(path),
            path.name,
            marketplace,
            sha256,
            0,
            document_type,
            period,
        )
        result["file_registered"] = True

        loader = self._get_loader()
        try:
            if execution_id is None:
                count = loader.load_marketplace(marketplace)
            else:
                count = loader.load_file(path, marketplace, execution_id=execution_id)
            result["loader_executed"] = True
            result["records_inserted"] = int(count) if count else 0
        except Exception as e:
            result["errors"].append(f"Loader failed: {e}")

        result["records_read"] = result["records_inserted"]

        return result
