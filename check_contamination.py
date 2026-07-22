import duckdb
cur = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)

# Check file_registry
print('=== FILE_REGISTRY ===')
try:
    r = cur.execute('SELECT * FROM file_registry ORDER BY processed_at DESC LIMIT 50').fetchall()
    for row in r:
        print(row)
except Exception as e:
    print(f'Error: {e}')

# Check pipeline_log for test executions
print()
print('=== PIPELINE_LOG - test related ===')
try:
    r = cur.execute("SELECT * FROM pipeline_log WHERE message LIKE '%test%' OR message LIKE '%TEST%' ORDER BY timestamp DESC").fetchall()
    for row in r:
        print(row)
except Exception as e:
    print(f'Error: {e}')

cur.close()