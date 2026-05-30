from database.duckdb_manager import get_db
from engine.loader import scan_raw_files, register_files


def discover_and_register() -> list[dict]:
    """Scan 01_Raw/ and register new files in stg_file_registry."""
    db = get_db()
    files = scan_raw_files()
    register_files(db, files)
    return files
