import urllib.request
import json

print("--- /api/v4/exec/summary ---")
try:
    r1 = urllib.request.urlopen("http://127.0.0.1:8003/api/v4/exec/summary?periodo=2026-02")
    print("Status:", r1.status)
except Exception as e:
    print("Error:", e)

print("\n--- /api/v4/exec/ux12_summary ---")
try:
    r2 = urllib.request.urlopen("http://127.0.0.1:8003/api/v4/exec/ux12_summary?periodo=2026-02")
    print("Status:", r2.status)
    print("Response:", r2.read().decode())
except urllib.error.HTTPError as e:
    print("Status:", e.code)
    print("Response:", e.read().decode())

print("\n--- /api/v4/exec/operational_intelligence ---")
try:
    r3 = urllib.request.urlopen("http://127.0.0.1:8003/api/v4/exec/operational_intelligence?periodo=2026-02")
    print("Status:", r3.status)
    print("Response:", r3.read().decode())
except urllib.error.HTTPError as e:
    print("Status:", e.code)
    print("Response:", e.read().decode())
