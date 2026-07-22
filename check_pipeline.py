import duckdb
cur = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
print('=== PIPELINE_LOG - test related ===')
try:
    r = cur.execute("SELECT * FROM pipeline_log WHERE details LIKE '%test%' OR details LIKE '%TEST%' ORDER BY timestamp DESC").fetchall()
    for row in r:
        print(row)
except Exception as e:
    print(f'Error: {e}')
cur.close()