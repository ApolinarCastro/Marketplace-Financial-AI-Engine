from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pandas as pd
import pytest

from engine.v4.database import DatabaseV4
from engine.v4.ingestion import IngestionRegistry
from engine.v4.ingestion.orchestrator import IngestionOrchestrator
from engine.v4.ingestion.handlers.persistence_engine import PersistenceEngine
from engine.v4.surgical_loader import SurgicalLoader


V9 = Path("data/db/BASELINE_ESTABLE_V9_TRUTH_RECOVERED/meli_financial_v4.db")


def _controlled_ml_fixture(path: Path) -> Path:
    frame = pd.DataFrame(
        [
            {
                "N° de factura fiscal": "033-TRUTH005-0001",
                "Fecha del cargo": "2026-07-01",
                "Número del cargo": "TRUTH005-CARGO-1",
                "Detalle": "Cargo por envíos de Mercado Libre",
                "Valor del cargo": 3150,
                "Número de venta": "TRUTH005-ORDER-1",
                "Total de la venta": 24990,
            }
        ]
    )
    frame.to_excel(path, sheet_name="REPORT", index=False)
    return path


@pytest.fixture
def v9_copy(tmp_path: Path):
    target = tmp_path / "truth005_v9.duckdb"
    shutil.copy2(V9, target)
    db = DatabaseV4(db_path=target, read_only=False)
    db.is_read_only = False
    try:
        yield db
    finally:
        db.close()


def _orchestrator(db: DatabaseV4) -> IngestionOrchestrator:
    loader = SurgicalLoader(db=db)
    persistence = PersistenceEngine(db=db, loader=loader)
    return IngestionOrchestrator(db=db, persistence=persistence, post_persist_stages=False)


@pytest.mark.anyio
async def test_controlled_ml_upload_links_content_registry_and_ledger(v9_copy, tmp_path):
    fixture = _controlled_ml_fixture(tmp_path / "ML_Facturacion_2026-07_TRUTH005.xlsx")
    expected_sha = hashlib.sha256(fixture.read_bytes()).hexdigest()

    record = await _orchestrator(v9_copy).run(fixture, fixture.name, user="truth005")

    assert record.status == "COMPLETED", record.errors
    assert record.sha256 == expected_sha
    assert len(record.sha256) == 64
    assert record.end_time is not None
    assert record.records_read == 1
    assert record.records_new == 1
    assert record.records_existing == 0
    assert record.errors == []

    registry = v9_copy.query(
        "SELECT content_sha256, hash_algorithm, file_size_bytes, marketplace, "
        "document_type, period FROM file_registry WHERE content_sha256 = ?",
        [expected_sha],
    )
    assert len(registry) == 1
    assert registry.iloc[0]["hash_algorithm"] == "SHA-256"

    ledger = v9_copy.query(
        "SELECT id_transaccion, monto, folio_xml, execution_id FROM marketplace_ledger_v1 "
        "WHERE execution_id = ?",
        [record.execution_id],
    )
    assert len(ledger) == 1
    assert ledger.iloc[0]["id_transaccion"].endswith("_1")
    assert ledger.iloc[0]["monto"] == -3150
    assert ledger.iloc[0]["folio_xml"] == "033-TRUTH005-0001"


@pytest.mark.anyio
async def test_identical_reupload_is_registered_and_does_not_duplicate_ledger(v9_copy, tmp_path):
    fixture = _controlled_ml_fixture(tmp_path / "ML_Facturacion_2026-07_TRUTH005.xlsx")
    orchestrator = _orchestrator(v9_copy)

    first = await orchestrator.run(fixture, fixture.name, user="truth005")
    second = await orchestrator.run(fixture, fixture.name, user="truth005")

    assert first.execution_id != second.execution_id
    assert first.sha256 == second.sha256
    assert second.status == "SKIPPED_DUPLICATE", (first.errors, second.errors)
    assert second.records_read == 1
    assert second.records_new == 0
    assert second.records_existing == 1
    assert second.marketplace == "ML"
    assert second.document_type == "facturacion"
    assert second.period == "2026-07"
    assert second.pipeline_version == "ml_v4"
    count = v9_copy.query(
        "SELECT COUNT(*) AS n FROM marketplace_ledger_v1 WHERE execution_id = ?",
        [first.execution_id],
    )
    assert int(count.iloc[0]["n"]) == 1


@pytest.mark.anyio
async def test_started_registry_failure_is_fail_closed(v9_copy, tmp_path, monkeypatch):
    fixture = _controlled_ml_fixture(tmp_path / "ML_Facturacion_2026-07_TRUTH005.xlsx")
    before = v9_copy.count("marketplace_ledger_v1")
    registry = IngestionRegistry(db=v9_copy)
    loader = SurgicalLoader(db=v9_copy)
    persistence = PersistenceEngine(db=v9_copy, loader=loader)
    orchestrator = IngestionOrchestrator(
        db=v9_copy,
        registry=registry,
        persistence=persistence,
        post_persist_stages=False,
    )
    monkeypatch.setattr(registry, "create_record", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("STARTED unavailable")))

    with pytest.raises(RuntimeError, match="STARTED unavailable"):
        await orchestrator.run(fixture, fixture.name, user="truth005")

    assert v9_copy.count("marketplace_ledger_v1") == before
