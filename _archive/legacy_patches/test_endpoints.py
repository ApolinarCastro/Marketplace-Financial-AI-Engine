import sys
sys.path.append('c:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine')
from api.api import get_marketplace_cierre_desglose, get_exec_summary_v3

print("--- CIERRE DESGLOSE RIPLEY 2025-01 ---")
try:
    desglose = get_marketplace_cierre_desglose("RIPLEY", "2025-01")
    print("Desglose:", desglose)
except Exception as e:
    print("Error:", e)

print("\n--- EXEC SUMMARY V3 RIPLEY 2025-01 ---")
try:
    summary = get_exec_summary_v3("2025-01", "RIPLEY")
    print("Summary:", summary)
except Exception as e:
    print("Error:", e)
