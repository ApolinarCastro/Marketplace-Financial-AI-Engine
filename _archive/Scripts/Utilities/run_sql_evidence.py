import duckdb
import pandas as pd

def get_db():
    return duckdb.connect('data/db/meli_financial_v4.db', read_only=True)

conn = get_db()

sql1 = """
SELECT
id_transaccion,
detalle,
monto,
monto_bruto,
comision_marketplace
FROM marketplace_ledger_v1
WHERE marketplace='PARIS'
AND STRFTIME(fecha, '%Y-%m')='2026-01'
LIMIT 20;
"""

sql2 = """
SELECT *
FROM marketplace_ledger_clasificado_v1
WHERE marketplace='PARIS'
AND STRFTIME(fecha, '%Y-%m')='2026-01'
AND (
monto_bruto IS NOT NULL
OR comision_marketplace IS NOT NULL
)
LIMIT 20;
"""

with open('sql_evidence_output.txt', 'w', encoding='utf-8') as f:
    try:
        res1 = conn.execute(sql1).df()
        f.write("--- SQL 1 RESULT ---\n")
        f.write(res1.to_string())
    except Exception as e:
        f.write("SQL 1 Error: " + str(e))

    f.write("\n\n")

    try:
        res2 = conn.execute(sql2).df()
        f.write("--- SQL 2 RESULT ---\n")
        f.write(res2.to_string())
    except Exception as e:
        f.write("SQL 2 Error: " + str(e))

