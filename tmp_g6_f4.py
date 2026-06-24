import duckdb
db = duckdb.connect('data/db/meli_financial_v4.db')

# Check ALL-TIME exact-amount pairs (same id_orden, same monto, diff concept, both op_pnl=1)
r = db.execute("""
    SELECT COUNT(*) as pairs_cnt,
           ROUND(SUM(a.monto), 2) as total_amount,
           COUNT(DISTINCT a.id_orden) as unique_orders
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden 
        AND a.monto = b.monto 
        AND a.id_transaccion <> b.id_transaccion
        AND a.fecha = b.fecha
    WHERE a.marketplace = ? AND b.marketplace = ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
      AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
""", ['ML', 'ML']).fetchall()

t = db.execute("SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1 WHERE marketplace = ?", ['ML']).fetchall()

print("ALL-TIME EXACT-MATCH PAIRS (both op_pnl=1, same fecha, same amount):")
print(f"  Paired entries:          {r[0][0]:5d}")
print(f"  Total amount:            ${r[0][1]:>12,.2f}")
print(f"  Unique orders affected:  {r[0][2]:5d}")
print(f"")
print(f"  ML Resultado Neto (all): ${t[0][0]:>12,.2f}")
print(f"  Inflation %:              {r[0][1]/t[0][0]*100:.2f}%")

# Same for Arre+Posc
r2 = db.execute("""
    SELECT COUNT(*) as pairs_cnt,
           ROUND(SUM(a.monto), 2) as total_amount,
           COUNT(DISTINCT a.id_orden) as unique_orders
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden 
        AND a.monto = b.monto 
        AND a.id_transaccion <> b.id_transaccion
        AND a.fecha = b.fecha
    WHERE a.marketplace = ? AND b.marketplace = ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa LIKE '%Arrepentimiento%'
      AND b.clasificacion_operativa LIKE '%Poscobro%'
      AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
""", ['ML', 'ML']).fetchall()

print(f"\nArre+Posc exact pairs (both op_pnl=1, same fecha, same amount):")
print(f"  Paired entries:          {r2[0][0]:5d}")
print(f"  Amount:                  ${r2[0][1]:>12,.2f}")
print(f"  Unique orders:           {r2[0][2]:5d}")
print(f"  % of all-time RN:        {r2[0][1]/t[0][0]*100:.2f}%")

# ALL pairs (any type) with exact amount
r3 = db.execute("""
    SELECT COUNT(*) as pairs_cnt,
           ROUND(SUM(a.monto), 2) as total_amount,
           COUNT(DISTINCT a.id_orden) as unique_orders
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden 
        AND a.monto = b.monto 
        AND a.id_transaccion <> b.id_transaccion
        AND a.fecha = b.fecha
    WHERE a.marketplace = ? AND b.marketplace = ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
""", ['ML', 'ML']).fetchall()
ta = db.execute("SELECT ROUND(SUM(monto),2) FROM marketplace_ledger_v1 WHERE marketplace=? AND financial_group='ajustes'", ['ML']).fetchall()

print(f"\nALL exact-amount pairs (any op_pnl):")
print(f"  Paired entries:          {r3[0][0]:5d}")
print(f"  Amount:                  ${r3[0][1]:>12,.2f}")
print(f"  Unique orders:           {r3[0][2]:5d}")
print(f"  % of ML ajustes total:   {r3[0][1]/ta[0][0]*100:.2f}%")

db.close()
