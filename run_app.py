from __future__ import annotations

import sys

import uvicorn


def validate_runtime() -> None:
    executable = sys.executable.replace("/", "\\").lower()
    if ".venv\\scripts\\python.exe" not in executable:
        raise SystemExit("ERROR: usar Scripts\\run_python.bat run_app.py")


if __name__ == "__main__":
    validate_runtime()
    uvicorn.run("api.api:app", host="127.0.0.1", port=8003, reload=False)
