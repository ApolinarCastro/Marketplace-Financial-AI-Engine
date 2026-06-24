import duckdb, json, time, os
os.chdir(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')

con = duckdb.connect('data/db/meli_financial_v4.db')

# Check what the issue is with the table
print("=== CHECKING TABLE ===")
tables = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchdf()
print("Tables:", list(tables['table_name']))

# Backup old table data first
old = con.execute("SELECT * FROM marketplace_ledger_clasificado_v1").fetchdf()
print(f"Old clasificado rows: {len(old)}")

# Drop and recreate
con.execute("DROP TABLE IF EXISTS marketplace_ledger_clasificado_v1")

con.execute("""
    CREATE TABLE marketplace_ledger_clasificado_v1 (
        marketplace VARCHAR,
        id_transaccion VARCHAR,
        id_orden VARCHAR,
        detalle VARCHAR,
        tipo_movimiento VARCHAR,
        monto DOUBLE,
        fecha DATE,
        clasificacion_operativa VARCHAR,
        confianza_clasificacion DOUBLE,
        origen_clasificacion VARCHAR,
        include_in_operational_pnl BOOLEAN,
        financial_group VARCHAR,
        financial_subgroup VARCHAR
    )
""")
print("Table recreated successfully")

# Verify it works
con.execute("SELECT COUNT(*) FROM marketplace_ledger_clasificado_v1").fetchone()
print("DELETE test: ok")

con.close()
print("\nReady for FASE 1")
