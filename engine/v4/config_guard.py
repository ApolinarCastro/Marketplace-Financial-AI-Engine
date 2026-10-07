"""Runtime mode + production write guard for ingestion surfaces.

Separates TEST / CONTROLLED / PRODUCTION explicitly via MF_RUNTIME_MODE
(default TEST, fail-closed). No caller may assume PRODUCTION from missing
configuration. Write authorization is decided here, never inline in handlers.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

VALID_MODES = ("TEST", "CONTROLLED", "PRODUCTION")
DEFAULT_MODE = "TEST"
ENV_VAR = "MF_RUNTIME_MODE"


def get_runtime_mode() -> str:
    """Return the runtime mode. Unknown or missing values fall back to TEST."""
    mode = (os.environ.get(ENV_VAR, "") or "").strip().upper()
    return mode if mode in VALID_MODES else DEFAULT_MODE


def resolve_production_db_path() -> Path:
    """Canonical production database path (resolved, no symlinks)."""
    from engine.v4.database import DatabaseV4

    return Path(DatabaseV4.DB_PATH).resolve()


def is_production_db_path(path: str | Path | None) -> bool:
    """True only when the target resolves exactly to the production DB file."""
    if path is None:
        return False
    try:
        return Path(path).resolve() == resolve_production_db_path()
    except Exception:
        return False


def authorize_db_write(
    target_db_path: str | Path | None,
    *,
    confirmed: bool = False,
    mode: str | None = None,
) -> dict[str, Any]:
    """Decide whether a DB write is authorized.

    Rules:
    - unconfirmed writes are never authorized (WRITE_NOT_CONFIRMED);
    - TEST mode never touches the production DB file, even confirmed;
    - CONTROLLED / PRODUCTION allow confirmed writes (operator-supervised).
    """
    active = (mode or get_runtime_mode()).strip().upper()
    if active not in VALID_MODES:
        active = DEFAULT_MODE
    if not confirmed:
        return {"allowed": False, "code": "WRITE_NOT_CONFIRMED",
                "mode": active, "production_target": is_production_db_path(target_db_path)}
    if active == "TEST" and is_production_db_path(target_db_path):
        return {"allowed": False, "code": "PRODUCTION_WRITE_BLOCKED_IN_TEST",
                "mode": active, "production_target": True}
    return {"allowed": True, "code": "AUTHORIZED",
            "mode": active, "production_target": is_production_db_path(target_db_path)}
