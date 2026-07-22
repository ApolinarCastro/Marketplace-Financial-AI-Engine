import duckdb
con = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
df = con.execute("SELECT detalle, tipo_movimiento, id_transaccion FROM marketplace_ledger_v1 WHERE id_transaccion IN ('145404934728', '144623804641', '144390458215', '144667518268')").df()
print(df)
df2 = con.execute("SELECT detalle, clasificacion_operativa FROM marketplace_ledger_clasificado_v1 WHERE clasificacion_operativa LIKE '%Poscobro%' LIMIT 10").df()
print(df2)
