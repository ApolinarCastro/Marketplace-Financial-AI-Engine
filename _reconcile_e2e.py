"""
Reconciliación rigurosa: por cada marketplace, para cada financial_group:
  SQL directo = API total_sum (server-side) = suma filas retornadas
  Y: panel desglose = API total_sum

NO usa TOTAL SELECCIONADO (que suma filas visibles en frontend).
Usa total_sum del API (cálculo server-side SQL SUM, independiente de paginación).
"""
from __future__ import annotations
import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from api.api import app
from engine.v4.database import DatabaseV4

client = TestClient(app)
db = DatabaseV4.get()

marketplaces = ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']

def get_period(mp):
    r = db.query("SELECT MAX(fecha) as mx FROM marketplace_ledger_v1 WHERE marketplace = ?", [mp])
    mx = r.iloc[0]['mx']
    return str(mx)[:7] if mx is not None else None

def sql_direct_sum(mp, periodo, financial_group=None):
    year, month = periodo.split('-')
    import calendar
    last_day = calendar.monthrange(int(year), int(month))[1]
    p_ini = f"{year}-{month}-01"
    p_fin = f"{year}-{month}-{last_day}"

    if financial_group:
        r = db.query(
            "SELECT COALESCE(SUM(COALESCE(monto,0)),0) as total FROM marketplace_ledger_v1 WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND COALESCE(include_in_operational_pnl,1)=1 AND financial_group = ?",
            [mp, p_ini, p_fin, financial_group]
        )
    else:
        r = db.query(
            "SELECT COALESCE(SUM(COALESCE(monto,0)),0) as total FROM marketplace_ledger_v1 WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND COALESCE(include_in_operational_pnl,1)=1",
            [mp, p_ini, p_fin]
        )
    return float(r.iloc[0]['total'])

def api_ledger_sum(mp, periodo, financial_group=None):
    url = f"/api/v4/ledger?marketplace={mp}&periodo={periodo}&limit=200&filter_zero=true"
    if financial_group:
        url += f"&financial_group={financial_group}"
    r = client.get(url)
    data = r.json()
    return {
        'total_sum': float(data.get('total_sum', 0)),
        'total_count': int(data.get('total_count', 0)),
        'rows_sum': sum(float(row['monto']) for row in data.get('data', []) if row.get('monto') is not None),
        'row_count': len(data.get('data', []))
    }

def get_desglose_panel(mp, periodo):
    r = client.get(f"/api/v4/cierre/desglose?marketplace={mp}&periodo={periodo}")
    data = r.json()
    by_cat = {}
    for row in data:
        cat = row['categoria']
        by_cat[cat] = by_cat.get(cat, 0) + row['total']
    return by_cat

print("=" * 140)
print(f"{'Mp':<10s} {'Periodo':<10s} {'Financial Group':<25s} {'SQL Direct':<16s} {'API total_sum':<16s} {'Rows Sum':<16s} {'Panel':<16s} {'Rows':<6s} {'DIFF':<10s} {'STATUS'}")
print("=" * 140)

all_pass = True

for mp in marketplaces:
    periodo = get_period(mp)
    if not periodo:
        print(f"{mp:<10s} NO DATA")
        continue

    # Get panel desglose
    panel = get_desglose_panel(mp, periodo)
    panel_total = sum(panel.values())

    # Test for each financial_group that exists in desglose
    fg_list = sorted(panel.keys())
    for fg in fg_list:
        sql_sum = sql_direct_sum(mp, periodo, fg)
        api = api_ledger_sum(mp, periodo, fg)
        panel_sum = panel.get(fg, 0)

        sql_api_diff = abs(sql_sum - api['total_sum'])
        api_rows_diff = abs(api['total_sum'] - api['rows_sum'])
        panel_api_diff = abs(panel_sum - api['total_sum'])
        total_diff = sql_api_diff + api_rows_diff + panel_api_diff

        status = "PASS" if total_diff < 1 else "FAIL"
        if status == "FAIL":
            all_pass = False

        print(f"{mp:<10s} {periodo:<10s} {fg:<25s} ${sql_sum:>12,.0f}  ${api['total_sum']:>12,.0f}  ${api['rows_sum']:>12,.0f}  ${panel_sum:>12,.0f}  {api['total_count']:>4d}  ${total_diff:>8,.0f}  {status}")

        if status == "FAIL":
            print(f"  >>> BREAKDOWN: SQL={sql_sum} API_total_sum={api['total_sum']} rows_sum={api['rows_sum']} panel={panel_sum}")

    # Also test unfiltered (all operational)
    sql_all = sql_direct_sum(mp, periodo, None)
    api_all = api_ledger_sum(mp, periodo, None)
    sql_api_diff = abs(sql_all - api_all['total_sum'])
    api_rows_diff = abs(api_all['total_sum'] - api_all['rows_sum'])
    panel_api_diff = abs(panel_total - api_all['total_sum'])
    total_diff = sql_api_diff + api_rows_diff + panel_api_diff
    status = "PASS" if total_diff < 1 else "FAIL"
    if status == "FAIL":
        all_pass = False

    print(f"{mp:<10s} {periodo:<10s} {'(TODOS OPERACIONAL)':<25s} ${sql_all:>12,.0f}  ${api_all['total_sum']:>12,.0f}  ${api_all['rows_sum']:>12,.0f}  ${panel_total:>12,.0f}  {api_all['total_count']:>4d}  ${total_diff:>8,.0f}  {status}")
    print("-" * 140)

print()
print("=" * 140)
print(f"RESULTADO: {'ALL PASS - RECONCILIACIÓN COMPLETA' if all_pass else 'FALLO DETECTADO - INCIDENTE ABIERTO'}")
print("=" * 140)
