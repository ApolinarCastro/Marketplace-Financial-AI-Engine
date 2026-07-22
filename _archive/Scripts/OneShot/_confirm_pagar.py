import duckdb
con = duckdb.connect('data/db/meli_financial_v4.db')

r = con.execute("""
    SELECT 
        SUM(CASE WHEN detalle = 'A pagar' THEN monto ELSE 0 END) as apagar,
        SUM(CASE WHEN detalle != 'A pagar' THEN monto ELSE 0 END) as rest,
        SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
""").fetchone()
print(f"Total RIPLEY:     ${r[2]:>14,.2f}")
print(f"A pagar:          ${r[0]:>14,.2f} ({r[0]/r[2]*100:.1f}%)")
print(f"Rest (P&L):       ${r[1]:>14,.2f} ({r[1]/r[2]*100:.1f}%)")
print(f"Apagar == abs(Rest): {abs(abs(r[0]) - abs(r[1])) < 0.01}")

r2 = con.execute("""
    SELECT 
        COALESCE(SUM(CASE WHEN lc.financial_group IN ('ingresos','devoluciones','costos_operacionales','costos_comerciales','ajustes') THEN l.monto ELSE 0 END),0) as pl_amount,
        COALESCE(SUM(CASE WHEN lc.financial_group IS NULL THEN l.monto ELSE 0 END),0) as null_fg_amount
    FROM marketplace_ledger_v1 l
    LEFT JOIN marketplace_ledger_clasificado_v1 lc ON l.id_transaccion = lc.id_transaccion
    WHERE l.marketplace = 'RIPLEY'
""").fetchone()
print(f"\nP&L classified:   ${r2[0]:>14,.2f}")
print(f"NULL fg amount:   ${r2[1]:>14,.2f}")
print(f"Match: {abs(r2[1] - r[0]) < 0.01}")

# Verify include_in_operational_pnl
r3 = con.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN detalle = 'A pagar' AND include_in_operational_pnl = false THEN 1 ELSE 0 END) as pagar_not_op,
        SUM(CASE WHEN detalle != 'A pagar' AND include_in_operational_pnl = false THEN 1 ELSE 0 END) as other_not_op
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
""").fetchone()
print(f"\ninclude_in_operational_pnl:")
print(f"  A pagar rows with op=false: {r3[1]}")
print(f"  Other rows with op=false:   {r3[2]}")

con.close()
