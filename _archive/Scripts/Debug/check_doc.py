import duckdb
conn = duckdb.connect('C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db')
res = conn.execute("SELECT match_status, COUNT(*) FROM document_match_v1 WHERE marketplace='RIPLEY' GROUP BY match_status").fetchall()
print(res)
res2 = conn.execute("SELECT * FROM document_match_v1 WHERE marketplace='RIPLEY' LIMIT 1").df()
print(res2)
