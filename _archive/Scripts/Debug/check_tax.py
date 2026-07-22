import duckdb
db=duckdb.connect('data/db/meli_financial_v4.db')
print(db.execute("SELECT DISTINCT financial_group, detalle FROM marketplace_ledger_v1 WHERE detalle LIKE '%Comisi%' OR detalle LIKE '%comisi%'").df())
