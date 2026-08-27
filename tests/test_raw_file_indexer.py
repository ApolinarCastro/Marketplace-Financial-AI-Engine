"""Tests for Phase 1.b CAP-TD-008 — RAW Files Indexing & Integrity Registry."""
from __future__ import annotations
import pytest
from pathlib import Path
import tempfile
import shutil
from engine.v4.ingestion.raw_file_indexer import RawFileIndexer, RAWFileRecord
from engine.v4.knowledge.dual_graph import DualGraphRegistry


@pytest.fixture
def temp_raw_dir():
    temp_dir = tempfile.mkdtemp()
    raw_root = Path(temp_dir) / "01_Raw"
    raw_root.mkdir()

    # Create mock marketplace subdirectories and files
    ml_dir = raw_root / "ML" / "2026-03"
    ml_dir.mkdir(parents=True)
    (ml_dir / "ventas_ml.csv").write_text("order_id,monto\n1,1000\n", encoding="utf-8")
    
    paris_dir = raw_root / "PARIS" / "2026-04"
    paris_dir.mkdir(parents=True)
    (paris_dir / "reporte_paris.xlsx").write_bytes(b"PK\x03\x04mock_excel_bytes")

    # Empty file
    (raw_root / "ML" / "empty_file.csv").write_text("", encoding="utf-8")

    # Unsupported extension
    (raw_root / "ML" / "notes.unsupported").write_text("some text", encoding="utf-8")

    # Duplicate file content
    ripley_dir = raw_root / "RIPLEY" / "2026-03"
    ripley_dir.mkdir(parents=True)
    (ripley_dir / "dup_ventas.csv").write_text("order_id,monto\n1,1000\n", encoding="utf-8")

    yield raw_root

    shutil.rmtree(temp_dir)


class TestRAWFileIndexer:
    def test_scan_discovers_all_files(self, temp_raw_dir):
        indexer = RawFileIndexer(root_dir=temp_raw_dir)
        records = indexer.scan(execution_id="EXEC-TEST-001")
        assert len(records) == 5

    def test_streaming_sha256_reproducible(self, temp_raw_dir):
        indexer = RawFileIndexer(root_dir=temp_raw_dir)
        f_path = temp_raw_dir / "ML" / "2026-03" / "ventas_ml.csv"
        hash1 = indexer.compute_streaming_sha256(f_path)
        hash2 = indexer.compute_streaming_sha256(f_path)
        assert hash1 == hash2
        assert len(hash1) == 64

    def test_marketplace_detection(self, temp_raw_dir):
        indexer = RawFileIndexer(root_dir=temp_raw_dir)
        records = indexer.scan()
        mp_map = {r.file_name: r.marketplace for r in records}
        assert mp_map["ventas_ml.csv"] == "ML"
        assert mp_map["reporte_paris.xlsx"] == "PARIS"
        assert mp_map["dup_ventas.csv"] == "RIPLEY"

    def test_period_detection(self, temp_raw_dir):
        indexer = RawFileIndexer(root_dir=temp_raw_dir)
        records = indexer.scan()
        p_map = {r.file_name: r.period for r in records}
        assert p_map["ventas_ml.csv"] == "2026-03"
        assert p_map["reporte_paris.xlsx"] == "2026-04"

    def test_integrity_detection(self, temp_raw_dir):
        indexer = RawFileIndexer(root_dir=temp_raw_dir)
        records = indexer.scan()
        int_map = {r.file_name: r.integrity_status for r in records}
        assert int_map["ventas_ml.csv"] == "VALID"
        assert int_map["empty_file.csv"] == "EMPTY"
        assert int_map["notes.unsupported"] == "UNSUPPORTED"

    def test_duplicate_detection(self, temp_raw_dir):
        indexer = RawFileIndexer(root_dir=temp_raw_dir)
        records = indexer.scan()
        dup_records = [r for r in records if r.duplicate_type == "DUPLICATE_CONTENT"]
        assert len(dup_records) == 1
        assert dup_records[0].file_name == "dup_ventas.csv"
        assert dup_records[0].duplicate_of is not None

    def test_idempotency_run_comparison(self, temp_raw_dir):
        indexer = RawFileIndexer(root_dir=temp_raw_dir)
        run1 = indexer.scan(execution_id="EXEC-RUN-1")
        run2 = indexer.scan(execution_id="EXEC-RUN-2")
        diff = indexer.compare_runs(run1, run2)
        assert diff["is_idempotent"] is True
        assert diff["new_files"] == 0
        assert diff["changed_files"] == 0
        assert diff["missing_files"] == 0

    def test_raw_mutations_zero(self, temp_raw_dir):
        indexer = RawFileIndexer(root_dir=temp_raw_dir)
        indexer.scan()
        assert indexer.raw_mutations == 0


class TestDualGraphTD008Integration:
    def test_dual_graph_has_td008_nodes(self):
        graph = DualGraphRegistry()
        assert graph.get_node("CAP-TD-008") is not None
        assert graph.get_node("EVID-TD-008") is not None
        assert graph.get_node("TD-008") is not None
        assert graph.get_node("EXEC_RAW_INDEXER") is not None
        assert graph.audit_orphan_nodes() == []
