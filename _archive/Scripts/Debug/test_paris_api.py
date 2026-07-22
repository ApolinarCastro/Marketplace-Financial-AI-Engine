import sys
sys.path.insert(0, '.')
from api.api import get_marketplace_cierre_desglose, get_exec_summary

print("=== DESGLOSE PARIS ENE 2025 ===")
res_desglose = get_marketplace_cierre_desglose("PARIS", "2025-01")
for r in res_desglose:
    if r['categoria'] == 'ingresos':
        print(f"[{r['categoria']}] {r['detalle']}: {r['total']}")

print("\n=== EXEC SUMMARY PARIS ENE 2025 ===")
res_exec = get_exec_summary("2025-01")
for mp in res_exec['marketplaces']:
    if mp['id'] == 'PARIS':
        print(f"Venta Bruta: {mp['venta_bruta']}")
        print(f"Comision: {mp['comision_marketplace']}")
