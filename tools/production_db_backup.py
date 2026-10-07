"""Verified production database backup / verify / restore-test.

Commands:
  python tools/production_db_backup.py backup
  python tools/production_db_backup.py verify <backup_file>
  python tools/production_db_backup.py restore-test <backup_file> [--dest DIR]

Rules enforced:
- production DB is SOURCE + READ-ONLY, never written, never replaced by this tool;
- backup refused when an active WAL artifact exists next to production;
- every backup carries a manifest JSON; SHA256(source) must equal SHA256(backup);
- restore-test copies to an isolated temp path only; production is never overwritten;
- corrupted backups are rejected by SHA mismatch or DuckDB open failure.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOL_VERSION = "1.0.0"
BACKUP_DIRNAME = "backups"
CRITICAL_TABLES = (
    "marketplace_ledger_v1",
    "marketplace_ledger_clasificado_v1",
    "marketplace_cierre_financiero_v1",
    "dte_truth_v1",
    "document_match_v1",
)


def production_db_path() -> Path:
    from engine.v4 import database as _dbmod

    return Path(_dbmod.DB_PATH).resolve()


def backup_dir() -> Path:
    d = Path("data") / BACKUP_DIRNAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def wal_artifacts(db_path: Path) -> list[str]:
    found = []
    for suffix in (".wal", "-wal", ".db-wal", ".db-shm", ".db-journal", "-shm", "-journal"):
        candidate = Path(str(db_path) + suffix)
        if candidate.exists():
            found.append(candidate.name)
    return found


def git_commit() -> str | None:
    try:
        import subprocess

        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=15)
        sha = (out.stdout or "").strip()
        return sha or None
    except Exception:
        return None


def cmd_backup() -> dict:
    from engine.v4.database import DatabaseV4  # noqa: F401 (ensures canonical path contract)

    src = production_db_path()
    if not src.exists():
        return {"status": "FAIL", "error": f"production DB missing: {src}"}
    wal = wal_artifacts(src)
    if wal:
        return {"status": "BLOCKED", "error": "ACTIVE_DUCKDB_WAL",
                "wal_artifacts": wal}
    source_size = src.stat().st_size
    source_sha = sha256_file(src)
    stamp = utc_stamp()
    name = f"meli_financial_v4_{stamp}_{source_sha[:12]}.db"
    dest_dir = backup_dir()
    dest = dest_dir / name
    if dest.exists():
        return {"status": "FAIL", "error": f"refusing to overwrite existing backup: {name}"}
    shutil.copy2(src, dest)
    backup_sha = sha256_file(dest)
    if backup_sha != source_sha:
        dest.unlink(missing_ok=True)
        return {"status": "FAIL", "error": "SOURCE_SHA256 != BACKUP_SHA256",
                "source_sha256": source_sha, "backup_sha256": backup_sha}
    manifest = {
        "backup_version": TOOL_VERSION,
        "created_at": stamp,
        "source_filename": src.name,
        "backup_filename": name,
        "source_size_bytes": source_size,
        "backup_size_bytes": dest.stat().st_size,
        "source_sha256": source_sha,
        "backup_sha256": backup_sha,
        "git_commit": git_commit(),
        "database_engine": "duckdb",
        "verification_status": "SHA_MATCHED",
    }
    manifest_path = dest.with_suffix(dest.suffix + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"status": "PASS", "backup_file": str(dest),
            "manifest_file": str(manifest_path), "manifest": manifest}


def _open_counts(db_path: Path) -> dict:
    import duckdb

    con = duckdb.connect(str(db_path), read_only=True)
    try:
        con.execute("SELECT 1").fetchone()
        tables: dict = {}
        for t in CRITICAL_TABLES:
            try:
                tables[t] = int(con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
            except Exception as e:
                tables[t] = f"MISSING: {type(e).__name__}"
        cols = {}
        try:
            rows = con.execute(
                "SELECT table_name, column_name, data_type "
                "FROM information_schema.columns WHERE table_name IN ("
                + ",".join(f"'{t}'" for t in CRITICAL_TABLES) + ")").fetchall()
            for table_name, column_name, data_type in rows:
                cols.setdefault(table_name, []).append(f"{column_name}:{data_type}")
        except Exception:
            pass
        return {"open": True, "tables": tables, "schema": cols}
    finally:
        con.close()


def cmd_verify(backup_file: str) -> dict:
    src = production_db_path()
    bf = Path(backup_file)
    if not bf.exists():
        return {"status": "FAIL", "error": f"backup file missing: {backup_file}"}
    manifest_path = bf.with_suffix(bf.suffix + ".manifest.json")
    manifest = None
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            manifest = None
    backup_sha = sha256_file(bf)
    manifest_ok = bool(manifest) and manifest.get("backup_sha256") == backup_sha
    try:
        backup_info = _open_counts(bf)
    except Exception as e:
        return {"status": "FAIL", "error": f"BACKUP_DB_OPEN_FAILED: {type(e).__name__}: {e}",
                "backup_sha256": backup_sha, "manifest_ok": manifest_ok}
    try:
        source_info = _open_counts(src)
    except Exception as e:
        return {"status": "FAIL", "error": f"SOURCE_DB_OPEN_FAILED: {type(e).__name__}: {e}"}
    schema_match = all(
        backup_info["schema"].get(t) == source_info["schema"].get(t)
        for t in CRITICAL_TABLES if t in backup_info["schema"])
    row_match = all(
        backup_info["tables"].get(t) == source_info["tables"].get(t)
        for t in CRITICAL_TABLES)
    ok = manifest_ok and schema_match and row_match
    return {
        "status": "PASS" if ok else "FAIL",
        "backup_file": str(bf),
        "backup_sha256": backup_sha,
        "manifest_ok": manifest_ok,
        "backup_tables": backup_info["tables"],
        "source_tables": source_info["tables"],
        "schema_match": schema_match,
        "row_counts_match": row_match,
    }


def cmd_restore_test(backup_file: str, dest_dir: str | None = None) -> dict:
    src = production_db_path()
    bf = Path(backup_file)
    if not bf.exists():
        return {"status": "FAIL", "error": f"backup file missing: {backup_file}"}
    if bf.resolve() == src.resolve():
        return {"status": "FAIL", "error": "refusing to restore over the backup source itself"}
    target_dir = Path(dest_dir) if dest_dir else Path("data/db/tmp_pfo_restore_test")
    if target_dir.resolve() == src.parent.resolve() and target_dir.name == src.parent.name:
        pass
    target_dir.mkdir(parents=True, exist_ok=True)
    restored = target_dir / "meli_financial_v4_restored.db"
    if restored.exists():
        return {"status": "FAIL", "error": f"refusing to overwrite existing restore target: {restored}"}
    if restored.resolve() == src.resolve():
        return {"status": "FAIL", "error": "restore target resolves to production DB; refusing"}
    shutil.copy2(bf, restored)
    backup_sha = sha256_file(bf)
    restored_sha = sha256_file(restored)
    if restored_sha != backup_sha:
        restored.unlink(missing_ok=True)
        return {"status": "FAIL", "error": "RESTORED_SHA256 != BACKUP_SHA256"}
    try:
        restored_info = _open_counts(restored)
    except Exception as e:
        restored.unlink(missing_ok=True)
        return {"status": "FAIL", "error": f"RESTORED_DB_OPEN_FAILED: {type(e).__name__}: {e}"}
    try:
        source_info = _open_counts(src)
    except Exception as e:
        return {"status": "FAIL", "error": f"SOURCE_DB_OPEN_FAILED: {type(e).__name__}: {e}"}
    schema_match = all(
        restored_info["schema"].get(t) == source_info["schema"].get(t)
        for t in CRITICAL_TABLES if t in restored_info["schema"])
    row_match = all(
        restored_info["tables"].get(t) == source_info["tables"].get(t)
        for t in CRITICAL_TABLES)
    ok = schema_match and row_match
    return {
        "status": "PASS" if ok else "FAIL",
        "restore_path": str(restored),
        "restore_sha256": restored_sha,
        "backup_sha256": backup_sha,
        "source_sha256": sha256_file(src),
        "restored_tables": restored_info["tables"],
        "source_tables": source_info["tables"],
        "schema_match": schema_match,
        "row_counts_match": row_match,
    }


def main(argv: list[str]) -> dict:
    if len(argv) < 2 or argv[1] not in ("backup", "verify", "restore-test"):
        return {"status": "FAIL", "error": "usage: backup | verify <file> | restore-test <file> [--dest DIR]"}
    if argv[1] == "backup":
        return cmd_backup()
    if argv[1] == "verify":
        if len(argv) < 3:
            return {"status": "FAIL", "error": "verify requires <backup_file>"}
        return cmd_verify(argv[2])
    dest = None
    if "--dest" in argv:
        i = argv.index("--dest")
        dest = argv[i + 1] if i + 1 < len(argv) else None
    if len(argv) < 3:
        return {"status": "FAIL", "error": "restore-test requires <backup_file>"}
    return cmd_restore_test(argv[2], dest)


if __name__ == "__main__":
    import sys as _sys

    result = main(list(_sys.argv))
    print(json.dumps(result, indent=2, default=str))
    _sys.exit(0 if result.get("status") == "PASS" else 1)
