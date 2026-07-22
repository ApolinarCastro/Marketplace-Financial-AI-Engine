"""Ingestion Registry — tracks every ingestion execution.

Registers execution_id, timestamps, user, marketplace, document type,
SHA256, file size, loader, pipeline, record counts, errors, warnings,
certification trigger, and knowledge update status.

Rules:
- Zero financial logic
- Zero direct SQL (uses DatabaseV4 public methods only)
- Never hides errors
"""
from __future__ import annotations
import json
import uuid
import hashlib
import time
from pathlib import Path
from datetime import datetime
from typing import Any
from dataclasses import dataclass, field, asdict

from engine.v4.database import DatabaseV4


@dataclass
class IngestionRecord:
    execution_id: str
    start_time: str
    end_time: str | None
    user: str
    marketplace: str | None
    document_type: str | None
    period: str | None
    file_name: str
    file_path: str
    sha256: str
    file_size_bytes: int
    status: str
    loader_executed: str | None
    pipeline: str | None
    pipeline_version: str | None
    records_inserted: int
    records_updated: int
    records_rejected: int
    records_read: int
    records_new: int
    records_existing: int
    errors: list[str]
    warnings: list[str]
    execution_time_seconds: float | None
    certification_triggered: bool
    certification_result: str | None
    knowledge_updated: bool
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["errors"] = list(self.errors)
        d["warnings"] = list(self.warnings)
        return d


class IngestionRegistry:
    TABLE = "ingestion_registry"

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get(read_only=False)

    def ensure_schema(self):
        self.db.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE} (
                execution_id TEXT PRIMARY KEY,
                start_time TEXT,
                end_time TEXT,
                user TEXT,
                marketplace TEXT,
                document_type TEXT,
                period TEXT,
                file_name TEXT,
                file_path TEXT,
                sha256 TEXT,
                file_size_bytes INTEGER,
                status TEXT,
                loader_executed TEXT,
                pipeline TEXT,
                records_inserted INTEGER DEFAULT 0,
                records_updated INTEGER DEFAULT 0,
                records_rejected INTEGER DEFAULT 0,
                records_read INTEGER DEFAULT 0,
                records_new INTEGER DEFAULT 0,
                records_existing INTEGER DEFAULT 0,
                errors TEXT DEFAULT '[]',
                warnings TEXT DEFAULT '[]',
                execution_time_seconds REAL,
                certification_triggered BOOLEAN DEFAULT FALSE,
                certification_result TEXT,
                knowledge_updated BOOLEAN DEFAULT FALSE,
                details TEXT DEFAULT '{{}}',
                created_at TIMESTAMP DEFAULT current_timestamp
            )
        """)
        for col, col_type in [
            ("records_read", "INTEGER DEFAULT 0"),
            ("records_new", "INTEGER DEFAULT 0"),
            ("records_existing", "INTEGER DEFAULT 0"),
            ("pipeline_version", "TEXT"),
        ]:
            try:
                self.db.execute(f"ALTER TABLE {self.TABLE} ADD COLUMN {col} {col_type}")
            except Exception:
                pass

    def create_record(self, file_name: str, file_path: str, user: str = "system") -> IngestionRecord:
        execution_id = str(uuid.uuid4())
        start_time = datetime.now().isoformat()
        path = Path(file_path)
        sha256 = self._compute_sha256(path)
        file_size_bytes = path.stat().st_size if path.exists() else 0
        record = IngestionRecord(
            execution_id=execution_id, start_time=start_time, end_time=None, user=user,
            marketplace=None, document_type=None, period=None,
            file_name=file_name, file_path=str(path.resolve()),
            sha256=sha256, file_size_bytes=file_size_bytes, status="STARTED",
            loader_executed=None, pipeline=None, pipeline_version=None,
            records_inserted=0, records_updated=0, records_rejected=0,
            records_read=0, records_new=0, records_existing=0,
            errors=[], warnings=[], execution_time_seconds=None,
            certification_triggered=False, certification_result=None, knowledge_updated=False,
        )
        self._persist(record)
        return record

    def update_status(self, record: IngestionRecord, status: str):
        record.status = status
        self._persist(record)

    def update_classification(
        self, record: IngestionRecord, marketplace: str, document_type: str, period: str,
        loader: str, pipeline: str
    ):
        record.marketplace = marketplace
        record.document_type = document_type
        record.period = period
        record.loader_executed = loader
        record.pipeline = pipeline
        record.pipeline_version = pipeline
        if record.status != "FAILED":
            record.status = "CLASSIFIED"
        self._persist(record)

    def update_records(self, record: IngestionRecord, inserted: int = 0, updated: int = 0, rejected: int = 0):
        record.records_inserted += inserted
        record.records_updated += updated
        record.records_rejected += rejected
        self._persist(record)

    def set_record_counts(self, record: IngestionRecord, read: int, new: int, existing: int):
        record.records_read = read
        record.records_new = new
        record.records_existing = existing
        record.records_inserted = new
        self._persist(record)

    def get_completed_by_sha256(self, sha256: str, exclude_execution_id: str) -> IngestionRecord | None:
        rows = self.db.query(
            f"SELECT * FROM {self.TABLE} WHERE sha256 = ? AND execution_id <> ? "
            "AND status = 'COMPLETED' ORDER BY start_time DESC LIMIT 1",
            [sha256, exclude_execution_id],
        )
        if rows.empty:
            return None
        return self._row_to_record(rows.iloc[0])

    def add_error(self, record: IngestionRecord, error: str):
        record.errors.append(error)
        record.status = "FAILED"
        self._persist(record)

    def add_warning(self, record: IngestionRecord, warning: str):
        record.warnings.append(warning)
        self._persist(record)

    def finalize(
        self, record: IngestionRecord,
        status: str | None = None,
        certification_triggered: bool = False,
        certification_result: str | None = None,
        knowledge_updated: bool = False,
    ):
        record.end_time = datetime.now().isoformat()
        record.certification_triggered = certification_triggered
        record.certification_result = certification_result
        record.knowledge_updated = knowledge_updated
        if record.end_time and record.start_time:
            start = datetime.fromisoformat(record.start_time)
            end = datetime.fromisoformat(record.end_time)
            record.execution_time_seconds = (end - start).total_seconds()
        if record.status != "FAILED":
            record.status = status or ("CERTIFIED" if certification_triggered else "PERSISTED")
        self._persist(record)

    def get(self, execution_id: str) -> IngestionRecord | None:
        rows = self.db.query(f"SELECT * FROM {self.TABLE} WHERE execution_id = ?", [execution_id])
        if rows.empty:
            return None
        return self._row_to_record(rows.iloc[0])

    def get_by_filename(self, file_name: str) -> IngestionRecord | None:
        """Get the latest ingestion record for a given filename."""
        from typing import Any
        rows = self.db.query(
            f"SELECT * FROM {self.TABLE} WHERE file_name = ? ORDER BY start_time DESC LIMIT 1",
            [file_name],
        )
        if rows.empty:
            return None
        return self._row_to_record(rows.iloc[0])

    def list(self, limit: int = 50, status: str | None = None, marketplace: str | None = None) -> list[IngestionRecord]:
        sql = f"SELECT * FROM {self.TABLE}"
        params: list[Any] = []
        filters = []
        if status:
            filters.append("status = ?")
            params.append(status)
        if marketplace:
            filters.append("marketplace = ?")
            params.append(marketplace)
        if filters:
            sql += " WHERE " + " AND ".join(filters)
        sql += " ORDER BY start_time DESC LIMIT ?"
        params.append(limit)
        rows = self.db.query(sql, params)
        return [self._row_to_record(r) for _, r in rows.iterrows()]

    def count_by_status(self) -> dict[str, int]:
        rows = self.db.query(f"SELECT status, COUNT(*) as n FROM {self.TABLE} GROUP BY status")
        return {r["status"]: int(r["n"]) for _, r in rows.iterrows()}

    def count_by_marketplace(self) -> dict[str, int]:
        rows = self.db.query(f"SELECT marketplace, COUNT(*) as n FROM {self.TABLE} GROUP BY marketplace")
        result: dict[str, int] = {}
        for _, r in rows.iterrows():
            key = r["marketplace"]
            if key is None or (isinstance(key, float) and key != key):
                key = "UNKNOWN"
            else:
                key = str(key)
            result[key] = int(r["n"])
        return result

    def _compute_sha256(self, path: Path) -> str:
        try:
            return hashlib.sha256(path.read_bytes()).hexdigest()
        except Exception:
            return ""

    def _persist(self, record: IngestionRecord):
        self.ensure_schema()
        d = record.to_dict()
        d["errors"] = json.dumps(d["errors"])
        d["warnings"] = json.dumps(d["warnings"])
        d["details"] = json.dumps(d["details"])
        cols = ", ".join(d.keys())
        placeholders = ", ".join(["?" for _ in d])
        self.db.execute(
            f"INSERT INTO {self.TABLE} ({cols}) VALUES ({placeholders}) "
            f"ON CONFLICT(execution_id) DO UPDATE SET "
            f"status=excluded.status, end_time=excluded.end_time, "
            f"marketplace=COALESCE(excluded.marketplace, ingestion_registry.marketplace), "
            f"document_type=COALESCE(excluded.document_type, ingestion_registry.document_type), "
            f"period=COALESCE(excluded.period, ingestion_registry.period), "
            f"loader_executed=COALESCE(excluded.loader_executed, ingestion_registry.loader_executed), "
            f"pipeline=COALESCE(excluded.pipeline, ingestion_registry.pipeline), "
            f"pipeline_version=COALESCE(excluded.pipeline_version, ingestion_registry.pipeline_version), "
            f"records_inserted=excluded.records_inserted, "
            f"records_updated=excluded.records_updated, "
            f"records_rejected=excluded.records_rejected, "
            f"records_read=excluded.records_read, records_new=excluded.records_new, "
            f"records_existing=excluded.records_existing, "
            f"errors=excluded.errors, warnings=excluded.warnings, "
            f"execution_time_seconds=excluded.execution_time_seconds, "
            f"certification_triggered=excluded.certification_triggered, "
            f"certification_result=excluded.certification_result, "
            f"knowledge_updated=excluded.knowledge_updated",
            list(d.values())
        )

    _SIMPLE_FIELDS = {
        "execution_id", "start_time", "end_time", "user", "marketplace",
        "document_type", "period", "file_name", "file_path", "sha256",
        "file_size_bytes", "status", "loader_executed", "pipeline",
        "pipeline_version",
        "records_inserted", "records_updated", "records_rejected",
        "records_read", "records_new", "records_existing",
        "execution_time_seconds", "certification_triggered",
        "certification_result", "knowledge_updated",
    }

    def _row_to_record(self, row) -> IngestionRecord:
        import pandas as pd
        d = dict(row)
        errors = d.pop("errors", "[]")
        warnings = d.pop("warnings", "[]")
        details = d.pop("details", "{}")
        kwargs = {}
        for k in self._SIMPLE_FIELDS:
            if k not in d:
                continue
            v = d[k]
            if isinstance(v, (float,)) and pd.isna(v):
                kwargs[k] = None
            elif hasattr(v, "item"):
                kwargs[k] = v.item()
            else:
                kwargs[k] = v
        kwargs["errors"] = self._parse_list(errors)
        kwargs["warnings"] = self._parse_list(warnings)
        kwargs["details"] = self._parse_dict(details)
        return IngestionRecord(**kwargs)

    @staticmethod
    def _parse_list(val: Any) -> list[str]:
        if isinstance(val, list):
            return val
        import pandas as pd
        if isinstance(val, float) and pd.isna(val):
            return []
        if not val or val in ("null", "None"):
            return []
        try:
            return json.loads(val) if val else []
        except Exception:
            return []

    @staticmethod
    def _parse_dict(val: Any) -> dict:
        if isinstance(val, dict):
            return val
        import pandas as pd
        if isinstance(val, float) and pd.isna(val):
            return {}
        if not val or val in ("null", "None"):
            return {}
        try:
            return json.loads(val) if val else {}
        except Exception:
            return {}
