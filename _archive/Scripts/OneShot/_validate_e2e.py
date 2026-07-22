"""
E2E Validation: SQL = API = UI
Tests both rewritten endpoints for all marketplaces.
"""
from __future__ import annotations
import sys, json
sys.path.insert(0, '.')
from engine.v4.database import DatabaseV4
from api.api import app
from fastapi.testclient import TestClient

client = TestClient(app)
db = DatabaseV4.get()

marketplaces = ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']
cases = {
    'ML': [
        ('ingresos', "Cargo por venta"),
        ('devoluciones', "Devoluci\u00f3n de venta"),
    ],
    'RIPLEY': [
        ('ingresos', "Importe del pedido"),
        ('devoluciones', "Pedidos reembolsados"),
    ],
    'PARIS': [
        ('ingresos', "Venta"),
        ('devoluciones', "Devoluci\u00f3n"),
    ],
    'FALABELLA': [
        ('costos_comerciales', "Cobro por comisi\u00f3n por venta"),
        ('costos_operacionales', "Cobro por cofinanciamiento log\u00edstico"),
    ],
}

def get_period(mp):
    r = db.query("SELECT MAX(fecha) as mx FROM marketplace_ledger_v1 WHERE marketplace = ?", [mp])
    mx = r.iloc[0]['mx']
    if mx is None:
        return None
    return str(mx)[:7]

print("=" * 120)
print(f"{'Marketplace':<14s} {'Categor\u00eda':<25s} {'Per\u00edodo':<10s} {'SUM SQL':<16s} {'SUM API':<16s} {'SUM LEDGER':<16s} {'DIFF':<12s} {'STATUS'}")
print("-" * 120)

all_pass = True

for mp in marketplaces:
    periodo = get_period(mp)
    if not periodo:
        print(f"{mp:<14s} {'NO DATA':<25s}")
        continue

    year, month = periodo.split('-')
    import calendar
    last_day = calendar.monthrange(int(year), int(month))[1]
    p_ini = f"{year}-{month}-01"
    p_fin = f"{year}-{month}-{last_day}"

    # 1. GET DESGLOSE (API)
    resp = client.get(f"/api/v4/cierre/desglose?marketplace={mp}&periodo={periodo}")
    desglose = resp.json()

    # Build sum by financial_group from desglose response
    desglose_by_fg = {}
    for row in desglose:
        cat = row['categoria']
        desglose_by_fg[cat] = desglose_by_fg.get(cat, 0) + row['total']

    # 2. SQL DIRECT SUM (same conditions as desglose endpoint)
    sql = """
        SELECT COALESCE(financial_group, 'sin_clasificar') as fg,
               SUM(COALESCE(monto, 0)) as total
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND COALESCE(include_in_operational_pnl, 1) = 1
        GROUP BY fg
    """
    sql_result = db.query(sql, [mp, p_ini, p_fin])
    sql_by_fg = {}
    for _, row in sql_result.iterrows():
        sql_by_fg[str(row['fg'])] = float(row['total'])

    # 3. TEST CASES
    for cat, label in cases[mp]:
        # SQL sum
        sql_sum = sql_by_fg.get(cat, 0)

        # API sum (from desglose)
        api_sum = desglose_by_fg.get(cat, 0)

        # API Ledger sum
        ledger_resp = client.get(
            f"/api/v4/ledger?marketplace={mp}&periodo={periodo}&financial_group={cat}&limit=1000&filter_zero=true"
        )
        ledger_json = ledger_resp.json()
        ledger_sum = float(ledger_json.get('total_sum', 0))

        diff = abs(sql_sum - api_sum) + abs(api_sum - ledger_sum)
        status = "PASS" if diff < 1 else "FAIL"

        if status == "FAIL":
            all_pass = False

        print(f"{mp:<14s} {label:<25s} {periodo:<10s} ${sql_sum:>12,.0f}  ${api_sum:>12,.0f}  ${ledger_sum:>12,.0f}  ${diff:>8,.0f}  {status}")

        # If FAIL, show details
        if status == "FAIL":
            print(f"  >>> SQL={sql_sum}  API={api_sum}  LEDGER={ledger_sum}")

    # 4. TOTAL desglose = total ledger (full period, no financial_group filter)
    total_sql = sum(sql_by_fg.values())
    total_desglose = sum(desglose_by_fg.values())
    ledger_all_resp = client.get(
        f"/api/v4/ledger?marketplace={mp}&periodo={periodo}&limit=1000&filter_zero=true"
    )
    ledger_all = ledger_all_resp.json()
    total_ledger = float(ledger_all.get('total_sum', 0))
    total_diff = abs(total_desglose - total_ledger)
    total_status = "PASS" if total_diff < 1 else "FAIL"
    if total_status == "FAIL":
        all_pass = False
    print(f"{mp:<14s} {'TOTAL OPERACIONAL':<25s} {periodo:<10s} ${total_sql:>12,.0f}  ${total_desglose:>12,.0f}  ${total_ledger:>12,.0f}  ${total_diff:>8,.0f}  {total_status}")
    print("-" * 120)

print()
print("=" * 120)
print(f"OVERALL: {'ALL PASS' if all_pass else 'FAILURES DETECTED - INCIDENTE ABIERTO'}")
print("=" * 120)
