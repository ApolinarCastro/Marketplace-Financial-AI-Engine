from __future__ import annotations

import sys
import signal
import logging

import uvicorn
from engine.v4.database import DatabaseV4

logger = logging.getLogger("run_app")


def validate_runtime() -> None:
    executable = sys.executable.replace("/", "\\").lower()
    if ".venv\\scripts\\python.exe" not in executable:
        raise SystemExit("ERROR: usar Scripts\\run_python.bat run_app.py")


def shutdown_handler(signum, frame):
    logger.warning(f"Received signal {signum}, shutting down gracefully...")
    DatabaseV4.reset()
    sys.exit(0)


if __name__ == "__main__":
    validate_runtime()
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    uvicorn.run("api.api:app", host="127.0.0.1", port=8003, reload=False)
