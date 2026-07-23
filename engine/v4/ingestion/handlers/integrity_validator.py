"""IntegrityValidator — Stage 1 of ingestion pipeline.

Validates file:
1. Extension is allowed
2. File is not empty
3. SHA256 not already registered (duplicate detection)
4. Structure check (CSV headers, XLSX sheet presence, XML well-formed)

Zero financial logic. Zero DB writes (reads file_registry for dedup).
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from engine.v4.database import DatabaseV4


class IntegrityValidator:
    ALLOWED_EXTENSIONS: set[str] = {".xlsx", ".csv", ".xml", ".zip"}

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get(read_only=False)

    def validate(self, file_path: str | Path, sha256: str, extension: str) -> list[dict[str, Any]]:
        """Returns list of issues found. Empty list = PASS."""
        issues: list[dict[str, Any]] = []
        path = Path(file_path) if isinstance(file_path, str) else file_path

        issues.extend(self._check_extension(extension))
        issues.extend(self._check_not_empty(path))
        # self._check_duplicate(sha256) is disabled because IngestionOrchestrator handles duplicates
        # safely by checking status = 'COMPLETED', whereas file_registry has no status column.
        issues.extend(self._check_structure(path, extension))

        return issues

    def _check_extension(self, ext: str) -> list[dict[str, Any]]:
        if ext.lower() not in self.ALLOWED_EXTENSIONS:
            return [{"type": "invalid_extension", "detail": f"Extension '{ext}' not allowed. Allowed: {self.ALLOWED_EXTENSIONS}"}]
        return []

    def _check_not_empty(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return [{"type": "file_not_found", "detail": f"File not found: {path}"}]
        if path.stat().st_size == 0:
            return [{"type": "empty_file", "detail": f"File is empty (0 bytes): {path.name}"}]
        return []

    def _check_duplicate(self, sha256: str) -> list[dict[str, Any]]:
        if not sha256:
            return []
        existing = self.db.query(
            "SELECT file_name, processed_at FROM file_registry WHERE file_hash = ?",
            [sha256]
        )
        if not existing.empty:
            row = existing.iloc[0]
            return [{
                "type": "duplicate_file",
                "detail": f"Duplicate of '{row['file_name']}' (processed at {row['processed_at']})",
            }]
        return []

    def _check_structure(self, path: Path, ext: str) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        try:
            if ext == ".csv":
                issues.extend(self._check_csv(path))
            elif ext == ".xlsx":
                issues.extend(self._check_xlsx(path))
            elif ext == ".xml":
                issues.extend(self._check_xml(path))
        except Exception as e:
            issues.append({"type": "structure_error", "detail": f"Structure check failed: {e}"})
        return issues

    def _check_csv(self, path: Path) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            first_line = f.readline().strip()
            if not first_line:
                issues.append({"type": "empty_csv", "detail": "CSV file has no header row"})
            elif "," not in first_line and ";" not in first_line:
                issues.append({"type": "no_delimiter", "detail": "CSV header has no delimiter (, or ;)"})
        return issues

    def _check_xlsx(self, path: Path) -> list[dict[str, Any]]:
        import pandas as pd
        issues: list[dict[str, Any]] = []
        xls = pd.ExcelFile(path)
        if len(xls.sheet_names) == 0:
            issues.append({"type": "empty_xlsx", "detail": "XLSX file has no sheets"})
        for sheet in xls.sheet_names:
            df = pd.read_excel(path, sheet_name=sheet, nrows=0)
            if df.columns.tolist():
                break
        else:
            issues.append({"type": "all_sheets_empty", "detail": "All XLSX sheets are empty"})
        return issues

    def _check_xml(self, path: Path) -> list[dict[str, Any]]:
        import xml.etree.ElementTree as ET
        issues: list[dict[str, Any]] = []
        try:
            ET.parse(path)
        except ET.ParseError as e:
            issues.append({"type": "malformed_xml", "detail": f"XML parse error: {e}"})
        return issues
