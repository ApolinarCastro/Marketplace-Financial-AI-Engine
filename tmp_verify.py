import sys, warnings
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
warnings.filterwarnings('ignore')
import duckdb

db_path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\meli_financial_v4.db'
con = duckdb.connect(db_path, read_only=True)

print('=== POST-FIX STATUS ===')
for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    lr = con.execute(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(monto),0),0) as total, MIN(fecha) as min_f, MAX(fecha) as max_f FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").fetchdf().iloc[0]
    cr = con.execute(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(resultado_neto),0),0) as total FROM marketplace_cierre_financiero_v1 WHERE marketplace='{mp}'").fetchdf().iloc[0]
    ar = con.execute(f"SELECT COUNT(*) as n FROM marketplace_auditoria_v1 WHERE marketplace='{mp}'").fetchdf().iloc[0]
    print(f'{mp}: ledger={int(lr["n"]):>6d} rows ${float(lr["total"]):>12,.0f} [{lr["min_f"]} to {lr["max_f"]}] | cierre={int(cr["n"]):>2d} periods ${float(cr["total"]):>12,.0f} | audit={int(ar["n"]):>5d} rows')

print()
print('=== JUNIO 2026 ===')
for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    r = con.execute(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(monto),0),0) as total FROM marketplace_ledger_v1 WHERE marketplace='{mp}' AND fecha >= '2026-06-01' AND fecha <= '2026-06-30'").fetchdf().iloc[0]
    print(f'{mp}: {int(r["n"])} rows ${float(r["total"]):,.0f}')

print()
print('=== ML CIERRE POST-FIX ===')
r = con.execute("""
    SELECT periodo_inicio, periodo_fin, total_ingresos, total_costos_operacionales, total_costos_comerciales, total_ajustes, resultado_neto
    FROM marketplace_cierre_financiero_v1
    WHERE marketplace = 'ML'
    ORDER BY periodo_inicio
""").fetchdf()
print(r.to_string(index=False))

print()
print('=== TOTAL CERTIFIED NETO PER MP ===')
r2 = con.execute("""
    SELECT marketplace, COUNT(*) as periods, ROUND(SUM(resultado_neto),0) as total_neto
    FROM marketplace_cierre_financiero_v1
    GROUP BY marketplace ORDER BY marketplace
""").fetchdf()
print(r2.to_string(index=False))

print()
print('=== GRAND TOTAL NETO ===')
r3 = con.execute("SELECT ROUND(SUM(resultado_neto),0) as gran_total FROM marketplace_cierre_financiero_v1").fetchdf().iloc[0]
print(f'${float(r3["gran_total"]):,.0f}')

total = con.execute("SELECT COUNT(*) as n FROM marketplace_auditoria_v1").fetchdf().iloc[0]
print(f'\nTotal audit rows: {int(total["n"])}')

con.close()
