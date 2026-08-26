"""RAW Files Indexing & Integrity Registry Module — CAP-TD-008.

Fulfills Phase 1.b surgical specification for TD-008.
Provides deterministic, streaming SHA-256 computation, relative path normalization,
marketplace & period discovery, duplicate detection, integrity status, and evidence generation
WITHOUT mutating any RAW files or modifying official DuckDB database.
"""
from __future__ import annotations
import os
import re
import hashlib
import datetime
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any, Literal


IntegrityStatus = Literal["VALID", "INVALID", "EMPTY", "UNREADABLE", "UNSUPPORTED"]
RegistryStatus = Literal["NEW", "REGISTERED", "DUPLICATE", "CHANGED", "MISSING"]
ProcessingStatus = Literal["NOT_PROCESSED", "PROCESSING", "PROCESSED", "FAILED"]


@dataclass
class RAWFileRecord:
    file_id: str
    content_hash: str
    relative_path: str
    file_name: str
    extension: str
    marketplace: str
    source_domain: str
    report_type: str
    period: str
    period_source: str
    size_bytes: int
    modified_at: str
    discovered_at: str
    integrity_status: IntegrityStatus
    registry_status: RegistryStatus
    processing_status: ProcessingStatus
    duplicate_type: str = "NOT_DUPLICATE"
    duplicate_of: str | None = None
    execution_id: str | None = None
    evidence_id: str | None = None
    error_code: str | None = None
    error_detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RawFileIndexer:
    """Canonical, reproducible, and auditable indexer for RAW files."""

    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".xml", ".json", ".txt", ".zip", ".parquet"}

    MARKETPLACE_PATTERNS = {
        "FALABELLA": [r"falabella", r"fala", r"01_raw/falabella"],
        "ML": [r"mercadolibre", r"meli", r"\bml\b", r"01_raw/ml"],
        "PARIS": [r"paris", r"01_raw/paris"],
        "RIPLEY": [r"ripley", r"01_raw/ripley"],
        "SHOPIFY": [r"shopify", r"01_raw/shopify"],
        "SAP": [r"sap", r"01_raw/sap"],
        "DTE": [r"dte", r"sii", r"01_raw/dte"],
        "BANCO": [r"banco", r"cartola", r"01_raw/banco"],
    }

    def __init__(self, root_dir: str | Path = "01_Raw"):
        self.root_dir = Path(root_dir).resolve()
        self.raw_mutations = 0

    @staticmethod
    def compute_streaming_sha256(file_path: Path, block_size: int = 65536) -> str:
        """Calculates streaming SHA-256 hash in blocks without loading full file to memory."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(block_size):
                    hasher.update(chunk)
            return hasher.hexdigest().lower()
        except Exception as e:
            return f"UNREADABLE:{e}"

    @staticmethod
    def normalize_relative_path(file_path: Path, root_dir: Path) -> str:
        """Produces a deterministic, multiplatform relative path string."""
        try:
            rel = file_path.resolve().relative_to(root_dir.resolve())
            return str(rel).replace("\\", "/")
        except ValueError:
            return str(file_path).replace("\\", "/")

    def detect_marketplace(self, relative_path: str, file_name: str) -> str:
        clean_path = relative_path.lower().replace("\\", "/")
        clean_name = file_name.lower()
        
        # Check path first
        parts = clean_path.split("/")
        if len(parts) > 1:
            first_dir = parts[0].upper()
            if first_dir in self.MARKETPLACE_PATTERNS:
                return first_dir

        for mp, patterns in self.MARKETPLACE_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, clean_path) or re.search(pat, clean_name):
                    return mp

        return "UNKNOWN"

    def detect_period(self, relative_path: str, file_name: str) -> tuple[str, str]:
        clean_str = f"{relative_path}/{file_name}"
        
        # YYYY-MM or YYYY/MM pattern
        match_ym = re.search(r"\b(202[0-9])[-/](0[1-9]|1[0-2])\b", clean_str)
        if match_ym:
            return f"{match_ym.group(1)}-{match_ym.group(2)}", "PATH" if match_ym.group(0) in relative_path else "FILENAME"

        # YYYYMM pattern
        match_compact = re.search(r"\b(202[0-9])(0[1-9]|1[0-2])\b", clean_str)
        if match_compact:
            return f"{match_compact.group(1)}-{match_compact.group(2)}", "FILENAME"

        return "UNKNOWN", "UNKNOWN"

    def detect_integrity(self, file_path: Path, size_bytes: int, extension: str) -> IntegrityStatus:
        if not file_path.exists():
            return "INVALID"
        if size_bytes == 0:
            return "EMPTY"
        if extension.lower() not in self.SUPPORTED_EXTENSIONS:
            return "UNSUPPORTED"
        try:
            with open(file_path, "rb") as f:
                f.read(16)
            return "VALID"
        except Exception:
            return "UNREADABLE"

    def scan(self, execution_id: str = "EXEC-SCAN-LOCAL", dry_run: bool = True) -> list[RAWFileRecord]:
        """Scans root_dir and constructs deterministic list of RAWFileRecord."""
        records: list[RAWFileRecord] = []
        if not self.root_dir.exists():
            return records

        discovered_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # Collect all files recursively
        all_files = sorted([p for p in self.root_dir.rglob("*") if p.is_file()])
        
        # Pass 1: Extract file properties and compute hashes
        temp_records = []
        content_hash_map: dict[str, list[str]] = {}

        for p in all_files:
            rel_path = self.normalize_relative_path(p, self.root_dir)
            ext = p.suffix.lower()
            size = p.stat().st_size
            mod_time = datetime.datetime.fromtimestamp(p.stat().st_mtime, tz=datetime.timezone.utc).isoformat()
            
            content_hash = self.compute_streaming_sha256(p)
            mp = self.detect_marketplace(rel_path, p.name)
            period, p_src = self.detect_period(rel_path, p.name)
            integrity = self.detect_integrity(p, size, ext)
            
            # Deterministic file_id
            id_str = f"{mp}|{rel_path}|{content_hash}"
            file_id = f"RAW-{hashlib.sha256(id_str.encode()).hexdigest()[:12]}"

            if content_hash not in content_hash_map:
                content_hash_map[content_hash] = []
            content_hash_map[content_hash].append(file_id)

            rec = RAWFileRecord(
                file_id=file_id,
                content_hash=content_hash,
                relative_path=rel_path,
                file_name=p.name,
                extension=ext,
                marketplace=mp,
                source_domain="MARKETPLACE" if mp in ("ML", "PARIS", "RIPLEY", "FALABELLA", "SHOPIFY") else "OTHER",
                report_type="RAW_DATA",
                period=period,
                period_source=p_src,
                size_bytes=size,
                modified_at=mod_time,
                discovered_at=discovered_at,
                integrity_status=integrity,
                registry_status="REGISTERED",
                processing_status="NOT_PROCESSED",
                execution_id=execution_id,
                evidence_id=f"EVID-{file_id}",
            )
            temp_records.append(rec)

        # Pass 2: Detect duplicates deterministically
        for rec in temp_records:
            matching_ids = content_hash_map.get(rec.content_hash, [])
            if len(matching_ids) > 1:
                canonical_id = matching_ids[0]
                if rec.file_id != canonical_id:
                    rec.duplicate_type = "DUPLICATE_CONTENT"
                    rec.duplicate_of = canonical_id
                    rec.registry_status = "DUPLICATE"
            records.append(rec)

        return records

    def compare_runs(self, run1: list[RAWFileRecord], run2: list[RAWFileRecord]) -> dict[str, Any]:
        """Compares two scan runs and reports diff stats."""
        r1_map = {r.file_id: r for r in run1}
        r2_map = {r.file_id: r for r in run2}

        new_files = [fid for fid in r2_map if fid not in r1_map]
        missing_files = [fid for fid in r1_map if fid not in r2_map]
        changed_files = [
            fid for fid in r1_map
            if fid in r2_map and r1_map[fid].content_hash != r2_map[fid].content_hash
        ]

        return {
            "new_files": len(new_files),
            "changed_files": len(changed_files),
            "missing_files": len(missing_files),
            "is_idempotent": len(new_files) == 0 and len(changed_files) == 0 and len(missing_files) == 0,
        }

    def generate_report(self, records: list[RAWFileRecord], execution_id: str, dry_run: bool = True) -> dict[str, Any]:
        mp_counts: dict[str, int] = {}
        ext_counts: dict[str, int] = {}
        period_counts: dict[str, int] = {}
        dup_counts = {"DUPLICATE_CONTENT": 0, "NOT_DUPLICATE": 0}

        for r in records:
            mp_counts[r.marketplace] = mp_counts.get(r.marketplace, 0) + 1
            ext_counts[r.extension] = ext_counts.get(r.extension, 0) + 1
            period_counts[r.period] = period_counts.get(r.period, 0) + 1
            if r.duplicate_type in dup_counts:
                dup_counts[r.duplicate_type] += 1
            else:
                dup_counts[r.duplicate_type] = 1

        return {
            "execution_id": execution_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "root_dir": str(self.root_dir),
            "dry_run": dry_run,
            "total_files": len(records),
            "valid_files": sum(1 for r in records if r.integrity_status == "VALID"),
            "empty_files": sum(1 for r in records if r.integrity_status == "EMPTY"),
            "unsupported_files": sum(1 for r in records if r.integrity_status == "UNSUPPORTED"),
            "duplicates": dup_counts,
            "marketplaces": mp_counts,
            "extensions": ext_counts,
            "periods": period_counts,
            "raw_mutations": self.raw_mutations,
        }
