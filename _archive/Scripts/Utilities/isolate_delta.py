import duckdb

db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db"
conn = duckdb.connect(db_path, read_only=True)

query = """
    SELECT 
        SUM(COALESCE(monto_bruto, 0)) as vb,
        SUM(COALESCE(comision_marketplace, 0)) as com,
        SUM(COALESCE(monto, 0)) as neto,
        SUM(COALESCE(monto_bruto, 0)) - SUM(COALESCE(comision_marketplace, 0)) - SUM(COALESCE(monto, 0)) as delta
    FROM marketplace_ledger_v1
    WHERE marketplace='PARIS' AND fecha BETWEEN '2026-06-01' AND '2026-06-30' AND detalle='Venta'
"""
res = conn.execute(query).fetchone()

with open("C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/2c921f1a-4258-4b8e-be46-1ad937059ee6/PARIS_DELTA_161720_ISOLATION.md", "w", encoding="utf-8") as f:
    f.write("# PARIS DELTA 161720 ISOLATION\n\n")
    f.write("## 2026-06\n\n")
    f.write(f"- SUM(monto_bruto): {res[0]}\n")
    f.write(f"- SUM(comision_marketplace): {res[1]}\n")
    f.write(f"- SUM(monto): {res[2]}\n")
    f.write(f"- DELTA (monto_bruto - comision_marketplace - monto): {res[3]}\n")

# Phase 2: Transaction Trace
trace_query = """
    SELECT 
        id_transaccion, id_orden, fecha, archivo_origen, monto, monto_bruto, comision_marketplace,
        (COALESCE(monto_bruto, 0) - COALESCE(comision_marketplace, 0) - COALESCE(monto, 0)) as dif
    FROM marketplace_ledger_v1
    WHERE marketplace='PARIS' AND fecha BETWEEN '2026-06-01' AND '2026-06-30' AND detalle='Venta'
      AND ABS((COALESCE(monto_bruto, 0) - COALESCE(comision_marketplace, 0) - COALESCE(monto, 0))) > 0.01
"""
res_trace = conn.execute(trace_query).fetchall()
col_names = [d[0] for d in conn.execute(trace_query).description]

with open("C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/2c921f1a-4258-4b8e-be46-1ad937059ee6/PARIS_DELTA_161720_TRANSACTION_TRACE.md", "w", encoding="utf-8") as f:
    f.write("# PARIS DELTA 161720 TRANSACTION TRACE\n\n")
    f.write("Filas que generan el delta:\n\n")
    f.write("| " + " | ".join(col_names) + " |\n")
    f.write("|" + "|".join(["---"] * len(col_names)) + "|\n")
    for r in res_trace:
        f.write("| " + " | ".join([str(x) for x in r]) + " |\n")

print("Isolations done.")
