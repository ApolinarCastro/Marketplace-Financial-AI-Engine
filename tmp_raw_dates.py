"""Check last RAW file dates per marketplace"""
import duckdb

con = duckdb.connect('data/db/snapshot_pre_poscobro_fix_20260605_155052/meli_financial_v4.db', read_only=True)

# Check file_registry for last loaded files
print("=== FILE REGISTRY (last load) ===")
try:
    q = "SELECT file_name, source, processed_at FROM file_registry ORDER BY processed_at DESC LIMIT 20"
    print(con.execute(q).fetchdf().to_string())
except Exception as e:
    print(f"file_registry: {e}")

# Check last dates per MP per table
print("\n=== LAST DATES PER MP ===")
for tbl in ['marketplace_ledger_v1', 'marketplace_ledger_clasificado_v1']:
    q = f"SELECT LOWER(marketplace) as mp, MAX(fecha) as max_fecha, COUNT(*) as rows FROM {tbl} GROUP BY LOWER(marketplace) ORDER BY mp"
    print(f"\n{tbl}:")
    print(con.execute(q).fetchdf().to_string())

# Check cierre last dates
q = "SELECT LOWER(marketplace) as mp, MAX(periodo_fin) as max_periodo, COUNT(*) as periods FROM marketplace_cierre_financiero_v1 GROUP BY LOWER(marketplace) ORDER BY mp"
print("\ncierre:")
print(con.execute(q).fetchdf().to_string())

# Check auditoria last dates
q = "SELECT LOWER(marketplace) as mp, MAX(detected_at) as max_detected, COUNT(*) as rows FROM marketplace_auditoria_v1 GROUP BY LOWER(marketplace) ORDER BY mp"
print("\nauditoria:")
print(con.execute(q).fetchdf().to_string())

# Check what the last month with ACTUAL revenue is per MP
q = """
SELECT LOWER(marketplace) as mp, strftime(MAX(periodo_fin), '%Y-%m') as last_revenue_month
FROM marketplace_cierre_financiero_v1
WHERE total_ingresos > 0
  AND resultado_neto != 0
  AND strftime(periodo_inicio, '%m') != '01'  -- exclude YTD
GROUP BY LOWER(marketplace)
ORDER BY mp
"""
print("\nlast revenue month (excl YTD):")
print(con.execute(q).fetchdf().to_string())

# Check pipeline_log for last pipeline execution
try:
    print("\n=== PIPELINE LOG ===")
    q = "SELECT * FROM pipeline_log ORDER BY executed_at DESC LIMIT 10"
    print(con.execute(q).fetchdf().to_string())
except Exception as e:
    print(f"pipeline_log: {e}")

con.close()
