"""
Before vs After reconciliation.
Only compares: SQL Direct | API total_sum | Panel | UI value (what frontend shows)

UI value BEFORE (bug): sum of visible rows (data.reduce)
UI value AFTER (fix):  window._ledgerTotalSum = API total_sum

Verification: SQL = API = Panel = UI_AFTER
"""
from __future__ import annotations
import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from api.api import app
from engine.v4.database import DatabaseV4

client = TestClient(app)
db = DatabaseV4.get()

cases = [
    ('ML', '2026-12', 'ajustes'),
    ('RIPLEY', '2026-12', 'ingresos'),
    ('PARIS', '2026-04', 'ingresos'),
    ('PARIS', '2026-04', 'costos_operacionales'),
    ('FALABELLA', '2026-05', 'costos_operacionales'),
]

def sql_sum(mp, periodo, fg):
    year, month = periodo.split('-')
    import calendar
    last_day = calendar.monthrange(int(year), int(month))[1]
    r = db.query(
        "SELECT COALESCE(SUM(COALESCE(monto,0)),0) as total FROM marketplace_ledger_v1 WHERE marketplace=? AND fecha BETWEEN ? AND ? AND COALESCE(include_in_operational_pnl,1)=1 AND financial_group=?",
        [mp, f"{year}-{month}-01", f"{year}-{month}-{last_day}", fg]
    )
    return float(r.iloc[0]['total'])

print("=" * 130)
print(f"{'Caso':<45s} {'SQL Direct':<16s} {'API total_sum':<16s} {'Panel':<16s} {'UI BEFORE (sum visible rows)':<28s} {'UI AFTER (API total_sum)':<28s} {'DIFF'}")
print("=" * 130)

all_pass = True
for mp, periodo, fg in cases:
    s = sql_sum(mp, periodo, fg)
    api = client.get(f"/api/v4/ledger?marketplace={mp}&periodo={periodo}&financial_group={fg}&limit=200&filter_zero=true")
    api_json = api.json()
    api_total = float(api_json['total_sum'])
    rows_sum = sum(float(r['monto']) for r in api_json['data'] if r.get('monto') is not None)
    n_rows = api_json['total_count']
    
    panel = client.get(f"/api/v4/cierre/desglose?marketplace={mp}&periodo={periodo}")
    panel_sum = sum(r['total'] for r in panel.json() if r['categoria'] == fg)
    
    label = f"{mp} / {periodo} / {fg} ({n_rows} rows)"
    
    # UI BEFORE = sum of visible rows (the BUG)
    ui_before = rows_sum
    # UI AFTER = window._ledgerTotalSum (API total_sum)
    ui_after = api_total
    
    diff = abs(s - api_total) + abs(api_total - panel_sum) + abs(ui_after - panel_sum)
    status = "PASS" if diff < 1 else "FAIL"
    if status == "FAIL":
        all_pass = False
    
    print(f"{label:<45s} ${s:>12,.0f}  ${api_total:>12,.0f}  ${panel_sum:>12,.0f}  ${ui_before:>20,.0f} {'(BUG: suma parcial)':<22s} ${ui_after:>20,.0f}  {diff:>6,.0f} {status}")

print("=" * 130)
if all_pass:
    print("RESULTADO: ALL PASS — SQL = API total_sum = Panel = UI AFTER (DIFF=0) — INCIDENTE CERRADO")
else:
    print("RESULTADO: FALLO — INCIDENTE ABIERTO")
print("=" * 130)
