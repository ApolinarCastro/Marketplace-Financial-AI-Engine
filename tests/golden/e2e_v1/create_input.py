import openpyxl
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT_DIR = SCRIPT_DIR / "input"
INPUT_DIR.mkdir(exist_ok=True)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Sheet1"

# Header row matching ML Facturacion format
ws.append(["Venta", "Detalle", "Valor del cargo", "Total de la venta", "Fecha"])

# Fixture rows - same as f3_03 but for E2E_V1
fixture_rows = [
    ("E2E-001", "Cargo por venta", 9500.0, 50000.0, "2026-06-01"),
    ("E2E-002", "Cargo por venta", 5700.0, 30000.0, "2026-06-02"),
    ("E2E-001", "Anulación del cargo por venta", -9500.0, 50000.0, "2026-06-15"),
    ("E2E-003", "Envío", 1500.0, 0.0, "2026-06-03"),
    ("E2E-004", "Publicidad", 2000.0, 0.0, "2026-06-04"),
]

for r in fixture_rows:
    ws.append(list(r))

# Save to the golden dataset input directory
output_path = INPUT_DIR / "ML_Facturacion_E2E_V1.xlsx"
wb.save(output_path)
print(f"Created: {output_path}")
print(f"Rows: {len(fixture_rows)}")