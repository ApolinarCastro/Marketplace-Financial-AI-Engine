from __future__ import annotations

import json
from urllib.error import URLError
from urllib.request import urlopen

from api.api import app


def server_is_live() -> bool:
    try:
        with urlopen("http://127.0.0.1:3001/", timeout=2) as response:
            return response.status == 200
    except (URLError, TimeoutError):
        return False


def test_all_routes_exist():
    routes = {route.path for route in app.routes}
    expected = {
        "/", "/app", "/exec",
        "/api/v4/ledger", "/api/v4/cierre", "/api/v4/cierre/desglose",
        "/api/v4/dte/count", "/api/v4/dte/samples",
        "/api/v4/test_regex", "/api/v4/debug_audit",
        "/api/v4/auditoria", "/api/v4/correcciones",
        "/api/v4/run-audit", "/api/v4/run-indexer",
        "/api/v4/query",
        "/api/v4/exec/summary", "/api/v4/exec/waterfall",
        "/api/v4/exec/audit-drilldown", "/api/v4/exec/audit-types",
    }
    missing = sorted(expected - routes)
    assert not missing, f"Faltan rutas: {missing}"


def test_dte_count_endpoint():
    if not server_is_live():
        return
    with urlopen("http://127.0.0.1:3001/api/v4/dte/count", timeout=5) as response:
        assert response.status == 200
        data = json.loads(response.read().decode("utf-8"))
        assert "count" in data
