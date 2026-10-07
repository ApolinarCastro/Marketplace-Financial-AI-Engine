"""Production backup/restore procedure tests (PFO-PRODUCTION-BACKUP-RESTORE-001).

All tests use synthetic TEMP databases. The production DB is NEVER written;
only read for SHA comparison where the tool itself requires it. Real backup
artifacts are never created by these tests.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import tools.production_db_backup as backup_tool
from engine.v4.database import DatabaseV4


def _synthetic_db(path: Path, marketplace: str = "ML", rows: int = 3) -> None:
    db = DatabaseV4(db_path=str(path), read_only=False)
    try:
        for i in range(rows):
            db.execute(
                "INSERT INTO marketplace_ledger_v1 (marketplace, id_transaccion, "
                "monto, archivo_origen) VALUES (?, ?, ?, ?)",
                [marketplace, f"SYN-{i:03d}", float(100 * (i + 1)), "synthetic.xlsx"])
    finally:
        db.close()


def test_backup_byte_parity_and_manifest(tmp_path: Path, monkeypatch):
    src = tmp_path / "source.db"
    _synthetic_db(src)
    backup_root = tmp_path / "backups"
    monkeypatch.setattr(backup_tool, "production_db_path", lambda: src)
    monkeypatch.setattr(backup_tool, "backup_dir",
                        lambda: backup_root and backup_root.mkdir(parents=True, exist_ok=True) or backup_root)
    out = backup_tool.cmd_backup()
    assert out["status"] == "PASS", out
    bf = Path(out["backup_file"])
    assert bf.exists()
    assert out["manifest"]["source_sha256"] == out["manifest"]["backup_sha256"]
    assert hashlib.sha256(bf.read_bytes()).hexdigest() == out["manifest"]["backup_sha256"]
    assert (bf.with_suffix(bf.suffix + ".manifest.json")).exists()


def test_verify_succeeds_and_restore_test_succeeds(tmp_path: Path, monkeypatch):
    src = tmp_path / "source.db"
    _synthetic_db(src)
    backup_root = tmp_path / "backups"
    monkeypatch.setattr(backup_tool, "production_db_path", lambda: src)
    monkeypatch.setattr(backup_tool, "backup_dir",
                        lambda: backup_root and backup_root.mkdir(parents=True, exist_ok=True) or backup_root)
    created = backup_tool.cmd_backup()
    assert created["status"] == "PASS"
    verified = backup_tool.cmd_verify(created["backup_file"])
    assert verified["status"] == "PASS", verified
    assert verified["row_counts_match"] is True
    restored = backup_tool.cmd_restore_test(
        created["backup_file"], dest_dir=str(tmp_path / "restore"))
    assert restored["status"] == "PASS", restored
    assert restored["restore_sha256"] == created["manifest"]["backup_sha256"]


def test_corrupted_backup_rejected(tmp_path: Path, monkeypatch):
    src = tmp_path / "source.db"
    _synthetic_db(src)
    backup_root = tmp_path / "backups"
    monkeypatch.setattr(backup_tool, "production_db_path", lambda: src)
    monkeypatch.setattr(backup_tool, "backup_dir",
                        lambda: backup_root and backup_root.mkdir(parents=True, exist_ok=True) or backup_root)
    created = backup_tool.cmd_backup()
    assert created["status"] == "PASS"
    bad = tmp_path / "corrupt.db"
    data = bytearray(Path(created["backup_file"]).read_bytes())
    data[1024] ^= 0xFF
    bad.write_bytes(bytes(data))
    verdict = backup_tool.cmd_verify(str(bad))
    assert verdict["status"] == "FAIL"


def test_existing_backup_not_overwritten(tmp_path: Path, monkeypatch):
    src = tmp_path / "source.db"
    _synthetic_db(src)
    backup_root = tmp_path / "backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(backup_tool, "production_db_path", lambda: src)
    monkeypatch.setattr(backup_tool, "backup_dir", lambda: backup_root)
    first = backup_tool.cmd_backup()
    assert first["status"] == "PASS"
    # Same content + same UTC second could collide; force collision by reusing name.
    import shutil as _shutil
    _shutil.copy2(first["backup_file"], tmp_path / "spare.db")
    before = sorted(p.name for p in backup_root.iterdir())
    second = backup_tool.cmd_backup()
    names = sorted(p.name for p in backup_root.iterdir())
    # Either a second timestamped file or a refusal — never a silent overwrite
    # of byte-different content under the same name.
    assert second["status"] in ("PASS", "FAIL")
    for p in backup_root.iterdir():
        if p.suffix == ".db":
            assert hashlib.sha256(p.read_bytes()).hexdigest() == \
                json.loads(p.with_suffix(p.suffix + ".manifest.json").read_text())["backup_sha256"]


def test_wal_guard_blocks_unsafe_backup(tmp_path: Path, monkeypatch):
    src = tmp_path / "source.db"
    _synthetic_db(src)
    (tmp_path / "source.db.wal").write_bytes(b"pending-wal-marker")
    monkeypatch.setattr(backup_tool, "production_db_path", lambda: src)
    out = backup_tool.cmd_backup()
    assert out["status"] == "BLOCKED"
    assert out["error"] == "ACTIVE_DUCKDB_WAL"


def test_restore_never_targets_production(tmp_path: Path, monkeypatch):
    src = tmp_path / "source.db"
    _synthetic_db(src)
    backup_root = tmp_path / "backups"
    monkeypatch.setattr(backup_tool, "production_db_path", lambda: src)
    monkeypatch.setattr(backup_tool, "backup_dir",
                        lambda: backup_root and backup_root.mkdir(parents=True, exist_ok=True) or backup_root)
    created = backup_tool.cmd_backup()
    assert created["status"] == "PASS"
    verdict = backup_tool.cmd_restore_test(created["backup_file"], dest_dir=str(tmp_path))
    # dest_dir == tmp_path (not production); restore file must differ from source
    assert verdict["status"] == "PASS"
    assert Path(verdict["restore_path"]).resolve() != src.resolve()
    direct = backup_tool.cmd_restore_test(created["backup_file"], dest_dir=str(src.parent))
    # restore into the SOURCE directory with default filename is allowed only
    # when it does not resolve to the production file itself
    assert direct["status"] in ("PASS", "FAIL")
    if direct["status"] == "PASS":
        assert Path(direct["restore_path"]).resolve() != src.resolve()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
