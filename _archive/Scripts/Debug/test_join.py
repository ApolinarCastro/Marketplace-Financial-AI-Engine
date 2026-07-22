import requests
import json

URL = "http://127.0.0.1:8003/api/v4/debug/sql"

def run_query(query, title):
    print(f"\n=== {title} ===")
    res = requests.post(URL, json={"query": query})
    data = res.json()
    if data["status"] == "success":
        for row in data["data"]:
            print(row)
    else:
        print("ERROR:", data["message"])

q = """
SELECT 
    COALESCE(c.financial_group, 'sin_clasificar') as financial_group,
    COUNT(*) as cantidad,
    SUM(COALESCE(l.monto, 0)) as total
FROM marketplace_ledger_v1 l
LEFT JOIN marketplace_ledger_clasificado_v1 c
    ON l.marketplace = c.marketplace 
    AND l.id_transaccion = c.id_transaccion
WHERE l.marketplace = 'RIPLEY'
GROUP BY 1
"""
run_query(q, "Join Result for Ripley")

q2 = """
SELECT 
    COUNT(*) as total_l
FROM marketplace_ledger_v1 l
WHERE l.marketplace = 'RIPLEY'
"""
run_query(q2, "Total L")

q3 = """
SELECT 
    COUNT(*) as total_c
FROM marketplace_ledger_clasificado_v1 c
WHERE c.marketplace = 'RIPLEY'
"""
run_query(q3, "Total C")

q4 = """
SELECT count(*) FROM marketplace_ledger_v1 l
INNER JOIN marketplace_ledger_clasificado_v1 c
ON l.id_transaccion = c.id_transaccion
WHERE l.marketplace = 'RIPLEY'
"""
run_query(q4, "Total Inner Join")
