"""
DOC-04 FIX verification — /api/v4/exec/cobros-breakdown server-side contract.
The route must return the exact shape consumed by both dashboards:
{matrix: [{concept, <MP>..., total}], mps: [...], total_cobros: number, concept_totals: {...}}.
"""
import sys
import os
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient  # noqa: E402

from api.api import app  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_route_exists(client):
    r = client.get("/api/v4/exec/cobros-breakdown", params={"periodo": "2026-01"})
    assert r.status_code == 200, f"Unexpected status: {r.status_code} {r.text}"


def test_contract_shape(client):
    r = client.get("/api/v4/exec/cobros-breakdown", params={"periodo": "2026-01"})
    data = r.json()
    assert "matrix" in data, "missing 'matrix'"
    assert "mps" in data, "missing 'mps'"
    assert "total_cobros" in data, "missing 'total_cobros'"
    assert "concept_totals" in data, "missing 'concept_totals'"
    assert isinstance(data["matrix"], list)
    assert isinstance(data["mps"], list)
    assert isinstance(data["total_cobros"], (int, float))
    for row in data["matrix"]:
        assert "concept" in row, f"row missing 'concept': {row}"
        assert "total" in row, f"row missing 'total': {row}"
        for mp in data["mps"]:
            assert mp in row, f"row missing MP column '{mp}': {row}"


def test_marketplace_filter(client):
    """Filtering by a marketplace present in the unfiltered result must narrow mps to it."""
    all_r = client.get("/api/v4/exec/cobros-breakdown", params={"periodo": "2026-01"})
    all_data = all_r.json()
    mps_all = all_data["mps"]
    if not mps_all:
        pytest.skip("no costos data for 2026-01 in test DB")
    target = mps_all[0]
    r = client.get("/api/v4/exec/cobros-breakdown", params={"periodo": "2026-01", "marketplace": target})
    data = r.json()
    assert data["mps"] == [target], f"expected [{target}], got {data['mps']}"


def test_total_matches_matrix_sum(client):
    r = client.get("/api/v4/exec/cobros-breakdown", params={"periodo": "2026-01"})
    data = r.json()
    matrix_total = sum(row["total"] for row in data["matrix"])
    assert abs(matrix_total - data["total_cobros"]) < 1.0, (
        f"matrix sum {matrix_total} != total_cobros {data['total_cobros']}"
    )


def test_bad_periodo_rejected(client):
    r = client.get("/api/v4/exec/cobros-breakdown", params={"periodo": "not-a-date"})
    assert r.status_code == 400


def test_no_frontend_concept_mapping():
    """FIX-2 — mapDetalleToConcept and DETALLE_TO_CONCEPT must be gone from all templates."""
    templates_dir = ROOT / "templates"
    forbidden = ["mapDetalleToConcept", "DETALLE_TO_CONCEPT"]
    offenders = []
    for tmpl in templates_dir.glob("*.html"):
        content = tmpl.read_text(encoding="utf-8")
        for token in forbidden:
            if token in content:
                offenders.append(f"{tmpl.name}: contains '{token}'")
    assert not offenders, "Client-side concept mapping detected:\n" + "\n".join(offenders)
