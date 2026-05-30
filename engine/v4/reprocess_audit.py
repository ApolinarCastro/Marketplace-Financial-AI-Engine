import sys
from pathlib import Path

ROOT = Path("c:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine")
sys.path.append(str(ROOT))

from engine.v4.meli_auditor import MeliAuditorEngine

if __name__ == "__main__":
    e = MeliAuditorEngine()
    n = e.run_classification()
    print(f"Clasificadas: {n}")
    
    stats = e.run_financial_closing('2026-03-01', '2026-03-31')
    print(f"Cierre Marzo 2026: {stats}")
    
    a = e.run_audit()
    print(f"Hallazgos Audit: {a}")
