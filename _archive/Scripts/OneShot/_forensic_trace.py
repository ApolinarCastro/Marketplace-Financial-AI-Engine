"""
FORENSE: Traza completa del click a la respuesta.
No modifica nada. Solo evidencia verificable.
"""
from __future__ import annotations
import sys, json
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from api.api import app
from engine.v4.database import DatabaseV4

client = TestClient(app)
db = DatabaseV4.get()

# Find marketplace/period where "Ingresos Brutos" and "Cargo por venta (Venta)" both exist
# by scanning all periods for all marketplaces
print("=== BUSCANDO marketplace/periodo con Ingresos Brutos y Cargo por venta (Venta) ===")
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    periods = db.query(
        "SELECT DISTINCT strftime('%Y-%m', fecha) as p FROM marketplace_ledger_v1 WHERE marketplace=? ORDER BY p DESC",
        [mp]
    )
    for p_row in periods.to_dict('records'):
        p = p_row['p']
        if not p:
            continue
        year, month = p.split('-')
        import calendar
        last_day = calendar.monthrange(int(year), int(month))[1]
        
        desg = client.get(f"/api/v4/cierre/desglose?marketplace={mp}&periodo={p}")
        desg_data = desg.json()
        
        ingresos_total = sum(r['total'] for r in desg_data if r['categoria'] == 'ingresos')
        cargo_subtotal = sum(r['total'] for r in desg_data if r['detalle'] == 'Cargo por venta (Venta)' or r['clasificacion_operativa'] == 'Cargo por venta (Venta)')
        
        if abs(ingresos_total) > 1000000 and abs(cargo_subtotal) > 1000000:
            print(f"  {mp:12s} {p:10s}  ingresos=${ingresos_total:>12,.0f}  cargo_venta=${cargo_subtotal:>12,.0f}")

# Pick the best match and trace both cases
print()
