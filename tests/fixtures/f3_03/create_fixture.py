"""Create synthetic ML Facturacion fixture for F3-03 controlled ingestion."""
import hashlib
import shutil
import os
import openpyxl
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent
FIXTURE_FILE = FIXTURE_DIR / "f3_03_fixture.xlsx"
FACTURACION_DIR = Path("01_Raw/ML/Facturacion")
COPY_NAME = "_f3_03_fixture.xlsx"

def compute_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def create_fixture_xlsx(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["Venta", "Detalle", "Valor del cargo", "Total de la venta", "Fecha"])
    ws.append(["F3-03-001", "Cargo por venta", 9500.0, 50000.0, "2026-06-01"])
    ws.append(["F3-03-002", "Cargo por venta", 5700.0, 30000.0, "2026-06-02"])
    ws.append(["F3-03-001", "Anulaci\u00f3n del cargo por venta", -9500.0, 50000.0, "2026-06-15"])
    ws.append(["F3-03-003", "Env\u00edo", 1500.0, 0.0, "2026-06-03"])
    ws.append(["F3-03-004", "Publicidad", 2000.0, 0.0, "2026-06-04"])
    wb.save(path)

def deploy():
    create_fixture_xlsx(FIXTURE_FILE)
    sha = compute_sha256(FIXTURE_FILE)
    print(f"Fixture created: {FIXTURE_FILE} ({os.path.getsize(FIXTURE_FILE)} bytes, SHA256={sha})")
    dest = FACTURACION_DIR / COPY_NAME
    shutil.copy2(FIXTURE_FILE, dest)
    print(f"Deployed to: {dest} ({compute_sha256(dest)} same={compute_sha256(dest) == sha})")
    return sha

def remove():
    dest = FACTURACION_DIR / COPY_NAME
    if dest.exists():
        dest.unlink()
        print(f"Removed: {dest}")
    if FIXTURE_FILE.exists():
        FIXTURE_FILE.unlink()
        print(f"Removed: {FIXTURE_FILE}")

if __name__ == "__main__":
    deploy()
