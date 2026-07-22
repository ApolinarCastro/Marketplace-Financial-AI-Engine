from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
res = db.query("SELECT id_transaccion, include_in_operational_pnl, clasificacion_operativa FROM marketplace_ledger_clasificado_v1 WHERE clasificacion_operativa LIKE '%repentant%' OR clasificacion_operativa LIKE '%Arrepentimiento%' OR clasificacion_operativa LIKE '%arrepentimiento%'").to_dict(orient='records')
for r in res:
    print(r)