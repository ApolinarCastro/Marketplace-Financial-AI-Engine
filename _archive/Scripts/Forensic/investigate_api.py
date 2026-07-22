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

print("--- STEP 1: VALIDATE_REAL_DATA_SOURCE ---")
run_query("SELECT count(*) FROM marketplace_ledger_clasificado_v1", "Total Clasificado rows")

print("\n--- STEP 2: VALIDATE_RIPLEY_CLASSIFICATION ---")
run_query("SELECT COUNT(*) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY'", 'Total Ripley Clasificado')
run_query("SELECT COUNT(*) as has_fin FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' AND financial_group IS NOT NULL", 'Ripley Financial Group IS NOT NULL')
run_query("SELECT COUNT(*) as no_fin FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' AND financial_group IS NULL", 'Ripley Financial Group IS NULL')
run_query("SELECT financial_group, SUM(monto) as total_monto FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' GROUP BY financial_group", 'Ripley SUM amount by financial_group')

print("\n--- STEP 3: VALIDATE_FALABELLA ---")
run_query("SELECT COUNT(*) as total FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'", 'Total Falabella Ledger V1')
run_query("SELECT COUNT(*) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace='FALABELLA'", 'Total Falabella Clasificado')

