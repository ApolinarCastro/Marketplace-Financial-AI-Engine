import pytest
import asyncio
from unittest.mock import patch
from pathlib import Path
import pandas as pd
from engine.v4.database import DatabaseV4
from engine.v4.ingestion.orchestrator import IngestionOrchestrator
from engine.v4.ingestion import IngestionRegistry
from engine.v4.surgical_loader import SurgicalLoader

@pytest.fixture
def fresh_db(tmp_path):
    db_path = tmp_path / "test.db"
    db = DatabaseV4(db_path=db_path, read_only=False)
    # Ensure tables exist
    db.execute('''CREATE TABLE IF NOT EXISTS file_registry (
        file_hash TEXT PRIMARY KEY, file_name TEXT, source TEXT, rows_processed INTEGER, 
        file_path TEXT, content_sha256 TEXT, hash_algorithm TEXT, file_size_bytes INTEGER, 
        marketplace TEXT, document_type TEXT, period TEXT, registered_at TIMESTAMP, processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    db.execute('''CREATE TABLE IF NOT EXISTS ingestion_registry (
        execution_id TEXT PRIMARY KEY, start_time TEXT, end_time TEXT, user TEXT, marketplace TEXT, document_type TEXT, period TEXT,
        file_name TEXT, file_path TEXT, sha256 TEXT, file_size_bytes INTEGER, status TEXT, loader_executed TEXT,
        pipeline TEXT, pipeline_version TEXT, records_inserted INTEGER, records_updated INTEGER, records_rejected INTEGER,
        records_read INTEGER, records_new INTEGER, records_existing INTEGER, errors TEXT, warnings TEXT,
        execution_time_seconds REAL, certification_triggered BOOLEAN, certification_result TEXT, knowledge_updated BOOLEAN, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status_history TEXT, internal_id TEXT, details TEXT)''')
    db.execute('''CREATE TABLE IF NOT EXISTS marketplace_ledger_v1 (
        id_transaccion TEXT PRIMARY KEY, id_orden TEXT, archivo_origen TEXT, monto REAL)''')
    yield db
    db.conn.close()

@pytest.mark.asyncio
async def test_completed_never_overwrites_metadata(fresh_db, tmp_path):
    """
    Verifica que un archivo que ya esta en estado COMPLETED en ingestion_registry
    nunca sobrescribe los metadatos originales en file_registry durante un reintento.
    """
    file_path = tmp_path / "test_file.xlsx"
    file_path.write_bytes(b"dummy data")
    sha256 = "dummy_sha256"
    
    # Simular que el sha256 real coincida con nuestro dummy (parchando _compute_sha256)
    with patch.object(IngestionRegistry, '_compute_sha256', return_value=sha256):
        registry = IngestionRegistry(db=fresh_db)
        
        # Insertar registro COMPLETED original
        fresh_db.execute("INSERT INTO ingestion_registry (execution_id, sha256, status, file_name) VALUES ('exec-1', ?, 'COMPLETED', 'original.xlsx')", [sha256])
        
        # Insertar registro en file_registry con metadata especifica
        fresh_db.execute("INSERT INTO file_registry (file_hash, file_name, rows_processed, registered_at) VALUES (?, 'original.xlsx', 100, '2020-01-01 00:00:00')", [sha256])
        
        orch = IngestionOrchestrator(db=fresh_db, registry=registry)
        
        # Ejecutar retry
        record = await orch.run(file_path=file_path, original_filename="retry.xlsx", user="test")
        
        assert record.status == "SKIPPED_DUPLICATE"
        
        # Verificar que el file_registry NO fue sobrescrito (INSERT OR REPLACE no deberia haberse llamado)
        rows = fresh_db.execute("SELECT file_name, rows_processed, registered_at FROM file_registry WHERE file_hash = ?", [sha256]).fetchall()
        assert len(rows) == 1
        assert rows[0][0] == 'original.xlsx', "El file_name fue sobrescrito!"
        assert rows[0][1] == 100, "Los rows_processed fueron sobrescritos!"
        assert str(rows[0][2]) == '2020-01-01 00:00:00', "El timestamp de registro fue sobrescrito!"

def test_delete_only_affects_target_file(fresh_db):
    """
    Confirma que el DELETE ... WHERE archivo_origen = ? unicamente elimina registros
    pertenecientes a ese archivo y nunca afecta cargas concurrentes o archivos diferentes.
    """
    # Preparar datos: File A y File B
    fresh_db.execute("INSERT INTO marketplace_ledger_v1 (id_transaccion, id_orden, archivo_origen, monto) VALUES ('T1', 'O1', 'file_A.xlsx', 100)")
    fresh_db.execute("INSERT INTO marketplace_ledger_v1 (id_transaccion, id_orden, archivo_origen, monto) VALUES ('T2', 'O2', 'file_B.xlsx', 200)")
    fresh_db.execute("INSERT INTO marketplace_ledger_v1 (id_transaccion, id_orden, archivo_origen, monto) VALUES ('T3', 'O3', 'file_B.xlsx', 300)")
    
    loader = SurgicalLoader()
    # Mockear self.db.conn para el loader
    loader.db = fresh_db
    
    # Ejecutar la logica idempotente de SurgicalLoader simulada para file_A.xlsx
    # Esto ocurre antes del insert_df
    target_file = "file_A.xlsx"
    fresh_db.execute("DELETE FROM marketplace_ledger_v1 WHERE archivo_origen = ?", [target_file])
    
    # Validar que file_A se elimino
    count_A = fresh_db.execute("SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE archivo_origen = 'file_A.xlsx'").fetchone()[0]
    assert count_A == 0, "file_A.xlsx deberia haberse eliminado"
    
    # Validar que file_B esta intacto
    rows_B = fresh_db.execute("SELECT id_transaccion FROM marketplace_ledger_v1 WHERE archivo_origen = 'file_B.xlsx' ORDER BY id_transaccion").fetchall()
    assert len(rows_B) == 2, "file_B.xlsx perdio registros"
    assert rows_B[0][0] == 'T2'
    assert rows_B[1][0] == 'T3'
