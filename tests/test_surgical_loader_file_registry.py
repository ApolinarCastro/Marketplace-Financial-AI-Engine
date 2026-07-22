import hashlib

from engine.v4.database import DatabaseV4
from engine.v4.surgical_loader import SurgicalLoader


def test_register_file_uses_full_content_sha256(tmp_path):
    raw_file = tmp_path / "sample.xlsx"
    raw_file.write_bytes(b"truth-001-content")
    db = DatabaseV4(tmp_path / "test.db", read_only=False)
    loader = SurgicalLoader.__new__(SurgicalLoader)
    loader.db = db

    try:
        loader._register_file(raw_file, "ML", 7)
        row = db.query(
            "SELECT file_hash, file_name, source, rows_processed FROM file_registry"
        ).iloc[0]
    finally:
        db.close()

    assert row["file_hash"] == hashlib.sha256(raw_file.read_bytes()).hexdigest()
    assert row["file_name"] == raw_file.name
    assert row["source"] == "ML"
    assert row["rows_processed"] == 7
