"""
Pytest configuration and shared fixtures for F4 test isolation.
"""
import gc
import shutil
import datetime
import hashlib
import os
import pytest
import duckdb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "db" / "meli_financial_v4.db"
V8_BASELINE = ROOT / "data" / "db" / "baseline_estable_v8_candidate_20260717" / "meli_financial_v4.db"

# External temp root (mandatory via env, fallback to system temp)
F4_TEMP_ROOT = Path(os.environ.get("F4_TEMP_ROOT", os.path.join(os.environ.get("TEMP", "/tmp"), "f4_v8"))).resolve()
TEMP_V8_BASE = F4_TEMP_ROOT / "tmp_f4_v8"


# ── V8 Temporary Copy (session-scoped) ────────────────────────────────

@pytest.fixture(scope="session")
def v8_temp_db_path():
    """Create a V8 candidate temp copy once per session."""
    if TEMP_V8_BASE.exists():
        shutil.rmtree(TEMP_V8_BASE, ignore_errors=True)
    TEMP_V8_BASE.mkdir(parents=True)
    temp_db = TEMP_V8_BASE / "meli_financial_v4.db"
    shutil.copy2(V8_BASELINE, temp_db)
    sha = hashlib.sha256(temp_db.read_bytes()).hexdigest().upper()
    print(f"[V8 TEMP] Created: {temp_db}")
    print(f"[V8 TEMP] Size: {temp_db.stat().st_size}")
    print(f"[V8 TEMP] SHA-256: {sha}")
    print(f"[V8 TEMP] Source: {V8_BASELINE}")
    yield temp_db
    from engine.v4.database import DatabaseV4
    DatabaseV4.reset()
    gc.collect()
    if TEMP_V8_BASE.exists():
        shutil.rmtree(TEMP_V8_BASE, ignore_errors=True)


@pytest.fixture(scope="session", autouse=True)
def v8_interceptor(v8_temp_db_path):
    """Redirect DatabaseV4 singleton to V8 temp copy for entire F4 session.
    
    All tests in F4 suites use V8 candidate instead of official DB.
    Explicit DatabaseV4(db_path=...) or _instance hijack is still possible
    for tests that need their own DB (e.g. test_f4_traceability).
    """
    from engine.v4.database import DatabaseV4
    DatabaseV4.reset()
    gc.collect()
    interceptor = DatabaseV4(db_path=str(v8_temp_db_path), read_only=True)
    DatabaseV4._instance = interceptor
    DatabaseV4._shutdown_registered = True
    ts = datetime.datetime.now().isoformat()
    print(f"[V8 INTERCEPTOR] DatabaseV4 singleton → {v8_temp_db_path} at {ts}")
    yield
    DatabaseV4.reset()
    gc.collect()


# ── Connection Evidence ────────────────────────────────────────────────

_CONNECTION_LOG: list[dict] = []


def log_connection(test: str, path: str, read_only: bool, ts: str):
    _CONNECTION_LOG.append({
        "test": test,
        "absolute_path": str(Path(path).resolve()),
        "read_only": read_only,
        "timestamp": ts,
    })


@pytest.fixture(scope="session")
def connection_evidence():
    """Return the connection log for audit."""
    return _CONNECTION_LOG


# ── F4 Shared Fixtures (module-scoped) ─────────────────────────────────

@pytest.fixture(scope="module")
def v8_db(v8_temp_db_path):
    """Module-scoped DatabaseV4 bound to V8 temp copy (read-only, with evidence)."""
    from engine.v4.database import DatabaseV4
    db = DatabaseV4(db_path=str(v8_temp_db_path), read_only=True)
    ts = datetime.datetime.now().isoformat()
    log_connection(
        test=__name__,
        path=str(v8_temp_db_path),
        read_only=True,
        ts=ts,
    )
    print(f"[V8 DB] path={v8_temp_db_path}, read_only=True, ts={ts}")
    yield db
    db.close()


@pytest.fixture(scope="module")
def v8_fe(v8_db):
    """Module-scoped FinancialEngine bound to V8 temp DB (explicit db injection)."""
    from engine.v4.domain.financial_engine import FinancialEngine
    ts = datetime.datetime.now().isoformat()
    fe = FinancialEngine(db=v8_db)
    print(f"[V8 FE] db_path={v8_db.db_path}, ts={ts}")
    yield fe