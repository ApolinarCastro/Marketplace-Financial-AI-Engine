import duckdb, json
con = duckdb.connect('data/db/meli_financial_v4.db')

results = {}
all_pass = True

# 1. financial_group NULL = 0 for P&L concepts
r = con.execute("""
    SELECT COUNT(*) as null_fg FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle != 'A pagar' AND financial_group IS NULL
""").fetchone()
c1 = r[0] == 0
results['1_financial_group_null_pl'] = {'value': r[0], 'pass': c1}
print(f"1. RIPLEY P&L financial_group NULL: {r[0]} rows {'PASS' if c1 else 'FAIL'}")

# 2. clasificacion_operativa NULL = 0 for RIPLEY
r = con.execute("""
    SELECT COUNT(*) as null_co FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND clasificacion_operativa IS NULL
""").fetchone()
c2 = r[0] == 0
results['2_clasificacion_null'] = {'value': r[0], 'pass': c2}
print(f"2. RIPLEY clasificacion_operativa NULL: {r[0]} rows {'PASS' if c2 else 'FAIL'}")

# 3. include_in_operational_pnl populated
r = con.execute("""
    SELECT 
        COUNT(CASE WHEN include_in_operational_pnl IS NOT NULL THEN 1 END) as not_null,
        COUNT(*) as total
    FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY'
""").fetchone()
c3 = r[0] == r[1]
results['3_pnl_flag_populated'] = {'value': f"{r[0]}/{r[1]}", 'pass': c3}
print(f"3. include_in_operational_pnl populated: {r[0]}/{r[1]} rows {'PASS' if c3 else 'FAIL'}")

# 4. Dashboard != $0 (RIPLEY has neto != 0)
r = con.execute("""
    SELECT COUNT(*) as periods, SUM(resultado_neto) as total_neto
    FROM marketplace_cierre_financiero_v1 WHERE marketplace = 'RIPLEY'
""").fetchone()
c4 = r[1] != 0
results['4_dashboard_not_zero'] = {'value': float(r[1]), 'pass': c4}
print(f"4. Dashboard neto != $0: ${r[1]:,.2f} {'PASS' if c4 else 'FAIL'}")

# 5. Dashboard = API = DB (verify cierre = ledger P&L)
pl_amount = con.execute("""
    SELECT COALESCE(SUM(CASE WHEN l.financial_group IN ('ingresos','devoluciones','costos_operacionales','costos_comerciales','ajustes') THEN l.monto ELSE 0 END),0)
    FROM marketplace_ledger_v1 l
    WHERE l.marketplace = 'RIPLEY' AND l.detalle != 'A pagar'
""").fetchone()[0]
cierre_neto = float(r[1])
c5 = abs(pl_amount) == abs(cierre_neto)
results['5_db_equals_cierre'] = {'ledger_pl': float(pl_amount), 'cierre_neto': cierre_neto, 'pass': c5}
print(f"5. Ledger P&L = Cierre Neto: ${pl_amount:,.2f} vs ${cierre_neto:,.2f} {'PASS' if c5 else 'FAIL'}")

# 6. 17/17 months present
r = con.execute("SELECT COUNT(DISTINCT strftime(periodo_inicio, '%Y-%m')) as months FROM marketplace_cierre_financiero_v1 WHERE marketplace='RIPLEY'").fetchone()
c6 = r[0] == 17
results['6_seventeen_months'] = {'value': r[0], 'pass': c6}
print(f"6. 17/17 months: {r[0]} {'PASS' if c6 else 'FAIL'}")

# 7. ML unchanged
r_ml = con.execute("SELECT COUNT(*) as cnt, SUM(resultado_neto) as neto FROM marketplace_cierre_financiero_v1 WHERE marketplace='ML'").fetchone()
c7_ml = r_ml[0] == 50 and abs(float(r_ml[1]) - 1684500601.30) < 0.01
results['7_ml_unchanged'] = {'periods': r_ml[0], 'neto': float(r_ml[1]), 'pass': c7_ml}
print(f"7. ML unchanged: periods={r_ml[0]}, neto=${r_ml[1]:,.2f} {'PASS' if c7_ml else 'FAIL'}")

# 8. PARIS unchanged
r_paris = con.execute("SELECT COUNT(*) as cnt, SUM(resultado_neto) as neto FROM marketplace_cierre_financiero_v1 WHERE marketplace='PARIS'").fetchone()
c7_paris = r_paris[0] == 18 and abs(float(r_paris[1]) - 756209866.00) < 0.01
results['8_paris_unchanged'] = {'periods': r_paris[0], 'neto': float(r_paris[1]), 'pass': c7_paris}
print(f"8. PARIS unchanged: periods={r_paris[0]}, neto=${r_paris[1]:,.2f} {'PASS' if c7_paris else 'FAIL'}")

# 9. FALABELLA unchanged
r_fal = con.execute("SELECT COUNT(*) as cnt, SUM(resultado_neto) as neto FROM marketplace_cierre_financiero_v1 WHERE marketplace='FALABELLA'").fetchone()
c7_fal = r_fal[0] == 24 and abs(float(r_fal[1]) - 2583016.00) < 0.01
results['9_falabella_unchanged'] = {'periods': r_fal[0], 'neto': float(r_fal[1]), 'pass': c7_fal}
print(f"9. FALABELLA unchanged: periods={r_fal[0]}, neto=${r_fal[1]:,.2f} {'PASS' if c7_fal else 'FAIL'}")

all_pass = all([
    c1, c2, c3, c4, c5,
    c6, c7_ml, c7_paris, c7_fal
])
results['all_pass'] = all_pass
print(f"\nFASE 3: {'ALL 9 CHECKS PASS' if all_pass else 'SOME CHECKS FAILED'}")

with open('_fase3_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
con.close()
