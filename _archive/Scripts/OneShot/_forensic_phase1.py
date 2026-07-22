from __future__ import annotations
import sys
sys.path.insert(0, '.')
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import FINANCIAL_STRUCTURE

db = DatabaseV4.get()

# 1. View definition
r = db.query("SELECT sql FROM sqlite_master WHERE type='view' AND name='financial_operational_view_v1'")
if not r.empty:
    print("=== VIEW: financial_operational_view_v1 ===")
    print(r.iloc[0]['sql'])
else:
    print("=== financial_operational_view_v1: NOT FOUND ===")
print()

# 2. Distinct financial_group values in ledger_v1
r = db.query("SELECT DISTINCT COALESCE(financial_group,'?') as fg, COUNT(*) as cnt, SUM(COALESCE(monto,0)) as total FROM marketplace_ledger_v1 GROUP BY fg ORDER BY cnt DESC")
print("=== financial_group values in marketplace_ledger_v1 ===")
for row in r.to_dict('records'):
    print(f"  {str(row['fg']):35s} cnt={row['cnt']:>7d}  total=${row['total']:>14,.0f}")
print()

# 3. Distinct financial_group values in clasificado_v1
r2 = db.query("SELECT DISTINCT COALESCE(financial_group,'?') as fg, COUNT(*) as cnt FROM marketplace_ledger_clasificado_v1 GROUP BY fg ORDER BY cnt DESC")
print("=== financial_group values in marketplace_ledger_clasificado_v1 ===")
for row in r2.to_dict('records'):
    print(f"  {str(row['fg']):35s} cnt={row['cnt']:>7d}")
print()

# 4. Print FINANCIAL_STRUCTURE
print("=== FINANCIAL_STRUCTURE (from marketplace_auditor.py) ===")
for cat, concepts in FINANCIAL_STRUCTURE.items():
    print(f"  {cat}:")
    for c in concepts:
        print(f"    - {c}")
print()

# 5. Check desglose endpoint vs direct DB for each marketplace
marketplaces = ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']
for mp in marketplaces:
    df_period = db.query("SELECT MAX(fecha) as mx FROM marketplace_ledger_v1 WHERE marketplace = ?", [mp])
    mx = df_period.iloc[0]['mx']
    if mx is None:
        print(f"{mp}: SKIP (no data)")
        continue
    mx_str = str(mx)[:7]
    year, month = mx_str.split('-')
    import calendar
    last_day = calendar.monthrange(int(year), int(month))[1]
    p_ini = f"{year}-{month}-01"
    p_fin = f"{year}-{month}-{last_day}"

    # What desglose SHOULD return (using financial_group from ledger_v1 directly)
    sql_direct = """
        SELECT COALESCE(financial_group,'?') as financial_group, detalle, tipo_movimiento,
               SUM(COALESCE(monto,0)) as total, COUNT(*) as cnt
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
        GROUP BY financial_group, detalle, tipo_movimiento
        ORDER BY total ASC
    """
    direct = db.query(sql_direct, [mp, p_ini, p_fin])
    
    print(f"=== {mp} [{mx_str}] Direct DB by financial_group ===")
    for row in direct.to_dict('records'):
        fg = str(row['financial_group'])
        det = str(row['detalle'])[:50]
        tm = str(row['tipo_movimiento'])
        print(f"  fg={fg:25s} detalle={det:50s} tipo={tm:20s} cnt={row['cnt']:>4d}  total=${row['total']:>12,.0f}")
    
    # Compare with what desglose endpoint returns via heuristic
    sql_heuristic = """
        SELECT clasificacion_operativa, detalle, tipo_movimiento,
               SUM(COALESCE(monto,0)) as total, COUNT(*) as cnt
        FROM financial_operational_view_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
        GROUP BY clasificacion_operativa, detalle, tipo_movimiento
        ORDER BY total ASC
    """
    heuristic = db.query(sql_heuristic, [mp, p_ini, p_fin])
    
    print()
    print(f"=== {mp} [{mx_str}] Heuristic (via financial_operational_view_v1) ===")
    for row in heuristic.to_dict('records'):
        cl = str(row['clasificacion_operativa'])
        det = str(row['detalle'])[:50]
        tm = str(row['tipo_movimiento'])
        print(f"  clasif={cl:30s} detalle={det:50s} tipo={tm:20s} cnt={row['cnt']:>4d}  total=${row['total']:>12,.0f}")
    
    # Compare totals
    direct_total = float(direct['total'].sum())
    heuristic_total = float(heuristic['total'].sum())
    print(f"\n  DIRECT TOTAL: ${direct_total:>12,.0f}")
    print(f"  HEURISTIC TOTAL: ${heuristic_total:>12,.0f}")
    print(f"  DIFF: ${abs(direct_total - heuristic_total):>8,.0f}  {'OK' if abs(direct_total - heuristic_total) < 0.01 else 'MISMATCH'}")
    print()
