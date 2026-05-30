from __future__ import annotations

import sys


def main() -> None:
    print(f"python_executable={sys.executable}")
    print(f"python_version={sys.version.split()[0]}")
    print(f"sys_prefix={sys.prefix}")
    print(f"base_prefix={sys.base_prefix}")

    issues: list[str] = []

    if ".venv" not in sys.executable.lower():
        issues.append("Python no se está ejecutando desde .venv")

    try:
        import fastapi  # noqa: F401
        import duckdb  # noqa: F401
        import pandas  # noqa: F401
        import openpyxl  # noqa: F401
    except Exception as exc:
        issues.append(f"Dependencia Python faltante o rota: {exc}")

    if sys.prefix == sys.base_prefix:
        issues.append("El intérprete no parece estar aislado en un virtualenv")

    if issues:
        print("python_env_status=warning")
        for issue in issues:
            print(f"issue={issue}")
        raise SystemExit(1)

    print("python_env_status=ok")


if __name__ == "__main__":
    main()
