"""
FORENSE COMPLETO: Click -> Frontend -> API -> SQL -> Resultado

CASO A: Click "Ingresos Brutos"
CASO B: Click "Cargo por venta (Venta)" (subgroup)
Marketplace: ML, Periodo: 2026-04
"""
from __future__ import annotations
import sys, json, textwrap
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from api.api import app
from engine.v4.database import DatabaseV4

client = TestClient(app)
db = DatabaseV4.get()

MP = "ML"
PERIODO = "2026-04"
year, month = PERIODO.split('-')
import calendar
last_day = calendar.monthrange(int(year), int(month))[1]
P_INI = f"{year}-{month}-01"
P_FIN = f"{year}-{month}-{last_day}"

# ============================================================
# 1. GET THE DESGLOSE (panel data) to see available subgroups
# ============================================================
print("=" * 100)
print("CONTEXTO: DESGLOSE PANEL (ML 2026-04)")
print("=" * 100)
desg = client.get(f"/api/v4/cierre/desglose?marketplace={MP}&periodo={PERIODO}")
desg_data = desg.json()
for row in desg_data:
    print(f"  categoria={row['categoria']:25s} clasif_op={str(row['clasificacion_operativa']):45s} detalle={str(row['detalle']):45s} total=${row['total']:>12,.0f}")

# Group by categoria
from collections import defaultdict
by_cat = defaultdict(list)
for r in desg_data:
    by_cat[r['categoria']].append(r)

for cat, items in sorted(by_cat.items()):
    cat_total = sum(i['total'] for i in items)
    print(f"\n  [{cat}] total=${cat_total:>12,.0f}")
    for i in items:
        display = i['clasificacion_operativa'] or i['detalle']
        print(f"    click subgroup sends: subgroup={display}")
        print(f"      (detalle={i['detalle']}, clasif_operativa={i['clasificacion_operativa']}, total=${i['total']:>12,.0f})")

print("\n" + "=" * 100)
print("CADENA DE EJECUCION")
print("=" * 100)

# ============================================================
# CASO A: Ingresos Brutos (category click)
# ============================================================
print("\n" + "-" * 100)
print("CASO A: Click 'Ingresos Brutos'")
print("-" * 100)

# 1. JS function called
print("\n1. FUNCION JS:")
print("   selectFinancialFilter('category', 'ingresos', 'Ingresos Brutos')")
print("   (definida en dashboard.html:487)")

# 2. Parameters
print("\n2. PARAMETROS:")
print("   type = 'category'")
print("   value = 'ingresos'")
print("   label = 'Ingresos Brutos'")
print("   categoryKey = undefined")

# 3. activeFinancialFilter set
print("\n3. activeFinancialFilter:")
print("   { type: 'category', value: 'ingresos', label: 'Ingresos Brutos', category: undefined }")

# 4. URL built
url_a = f"/api/v4/ledger?marketplace={MP}&periodo={PERIODO}&limit=200&offset=0&filter_zero=true&financial_group=ingresos"
print(f"\n4. URL INVOCADA:")
print(f"   {url_a}")

# 5. API endpoint
print(f"\n5. ENDPOINT:")
print(f"   GET /api/v4/ledger")
print(f"   FastAPI function: get_marketplace_ledger()")

# 6. SQL
print(f"\n6. SQL EJECUTADO:")
conditions_a = ["marketplace = '?'"]
params_a = [MP, P_INI, P_FIN, 'ingresos']
sql_a = f"""
    SELECT COUNT(*) as cnt, COALESCE(SUM(monto), 0) as sm
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha >= ? AND fecha <= ?
      AND COALESCE(include_in_operational_pnl, 1) = 1
      AND financial_group = ?
      AND monto != 0
"""
print(f"   COUNT/SUM: {sql_a}")
print(f"   params: {params_a}")
sql_a_data = f"""
    SELECT *
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha >= ? AND fecha <= ?
      AND COALESCE(include_in_operational_pnl, 1) = 1
      AND financial_group = ?
      AND monto != 0
    ORDER BY fecha DESC
    LIMIT ? OFFSET ?
"""
print(f"   DATA: {sql_a_data}")
print(f"   params: {params_a + [200, 0]}")

# 7. financial_group
print(f"\n7. financial_group APLICADO: 'ingresos'")

# 8. clasificacion_operativa
print(f"8. clasificacion_operativa: None (no aplicado)")

# 9. detalle
print(f"9. detalle: None (no aplicado)")

# 10-11. Execute
resp_a = client.get(url_a)
data_a = resp_a.json()
print(f"\n10. total_sum: ${float(data_a['total_sum']):>12,.0f}")
print(f"11. total_count: {data_a['total_count']} rows")
print(f"12. offset: {data_a['offset']}, limit: {data_a['limit']}")
print(f"\n13. PRIMERAS 5 FILAS:")
for i, row in enumerate(data_a['data'][:5]):
    print(f"    [{i+1}] fecha={str(row['fecha'])[:10]} detalle={str(row['detalle'])[:50]} financial_group={row['financial_group']} monto=${float(row['monto']):>12,.0f}")

# ============================================================
# CASO B: Cargo por venta (Venta) (subgroup click)
# ============================================================
print("\n" + "=" * 100)
print("CASO B: Click 'Cargo por venta (Venta)' (subgroup)")
print("=" * 100)

# Determine the category key for this subgroup
subgroup_name = "Cargo por venta (Venta)"
category_key = None
for r in desg_data:
    display = r['clasificacion_operativa'] or r['detalle']
    if display == subgroup_name:
        category_key = r['categoria']
        break

# 1. JS function
print(f"\n1. FUNCION JS:")
print(f"   selectFinancialFilter('subgroup', '{subgroup_name}', '{subgroup_name}', '{category_key}')")
print(f"   (definida en dashboard.html:773)")

# 2. Parameters
print(f"\n2. PARAMETROS:")
print(f"   type = 'subgroup'")
print(f"   value = '{subgroup_name}'")
print(f"   label = '{subgroup_name}'")
print(f"   categoryKey = '{category_key}'")

# 3. activeFinancialFilter
print(f"\n3. activeFinancialFilter:")
print(f"   {{ type: 'subgroup', value: '{subgroup_name}', label: '{subgroup_name}', category: '{category_key}' }}")

# 4. URL built
import urllib.parse
encoded = urllib.parse.quote(subgroup_name)
url_b = f"/api/v4/ledger?marketplace={MP}&periodo={PERIODO}&limit=200&offset=0&filter_zero=true&subgroup={encoded}"
print(f"\n4. URL INVOCADA:")
print(f"   {url_b}")

# 5. What the frontend SENDS vs what the API RECEIVES:
print(f"\n5. PARAMETROS ENVIADOS POR FRONTEND:")
print(f"   - marketplace={MP}")
print(f"   - periodo={PERIODO}")
print(f"   - limit=200")
print(f"   - offset=0")
print(f"   - filter_zero=true")
print(f"   - subgroup={subgroup_name}")
print(f"\n   PARAMETROS ACEPTADOS POR API:")
print(f"   - marketplace (SI)")
print(f"   - periodo (SI)")
print(f"   - financial_group (opcional)")
print(f"   - clasificacion_operativa (opcional)")
print(f"   - detalle (opcional)")
print(f"   - offset (SI)")
print(f"   - limit (SI)")
print(f"   - filter_zero (SI)")
print(f"   - subgroup (NO EXISTE)")
print(f"\n   >>> subgroup NO es un parametro de la API. FastAPI lo ignora silenciosamente.")

# 6. SQL - subgroup filter NOT applied!
print(f"\n6. SQL EJECUTADO:")
print(f"   (SIN filtro subgroup — parametro ignorado)")
print(f"   financial_group = None, clasificacion_operativa = None, detalle = None")
print(f"   Solo se aplican: marketplace + periodo + filter_zero")
conditions_b = [f"marketplace = '{MP}'", f"fecha >= '{P_INI}'", f"fecha <= '{P_FIN}'", "include_in_operational_pnl = 1", "monto != 0"]
sql_b = " AND ".join(conditions_b)
print(f"   WHERE {sql_b}")

# 7. Execute
resp_b = client.get(url_b)
data_b = resp_b.json()
print(f"\n7. total_sum: ${float(data_b['total_sum']):>12,.0f}")
print(f"8. total_count: {data_b['total_count']} rows")

# Print all distinct financial_groups returned
from collections import Counter
fg_counts = Counter()
fg_sums = defaultdict(float)
for row in data_b['data']:
    fg = row.get('financial_group', 'N/A')
    fg_counts[fg] += 1
    fg_sums[fg] += float(row['monto'])

print(f"\n9. financial_groups en respuesta (sin filtro de subgroup):")
for fg, cnt in sorted(fg_counts.items()):
    print(f"    {fg:30s} cnt={cnt:>4d}  sum=${fg_sums[fg]:>12,.0f}")

print(f"\n10. COMPARACION:")
print(f"    CASO A (financial_group=ingresos): total_sum = ${float(data_a['total_sum']):>12,.0f}")
print(f"    CASO B (subgroup ignorado):        total_sum = ${float(data_b['total_sum']):>12,.0f}")
print(f"    Diferencia: ${abs(float(data_b['total_sum']) - float(data_a['total_sum'])):>12,.0f}")

# SQL direct verification
print(f"\n11. VERIFICACION SQL DIRECTA:")
r_a = db.query(
    "SELECT COALESCE(SUM(COALESCE(monto,0)),0) FROM marketplace_ledger_v1 WHERE marketplace=? AND fecha BETWEEN ? AND ? AND COALESCE(include_in_operational_pnl,1)=1 AND financial_group='ingresos' AND monto!=0",
    [MP, P_INI, P_FIN]
)
print(f"    CASO A SQL: ${float(r_a.iloc[0][0]):>12,.0f}")

r_b = db.query(
    "SELECT COALESCE(SUM(COALESCE(monto,0)),0) FROM marketplace_ledger_v1 WHERE marketplace=? AND fecha BETWEEN ? AND ? AND COALESCE(include_in_operational_pnl,1)=1 AND monto!=0",
    [MP, P_INI, P_FIN]
)
print(f"    CASO B SQL: ${float(r_b.iloc[0][0]):>12,.0f}")

print(f"\n12. CONCLUSION:")
print(f"    CASO A: financial_group='ingresos' APLICADO correctamente --> solo filas de ingresos")
print(f"    CASO B: subgroup='{subgroup_name}' IGNORADO (parametro no existe en API --> mismas filas que sin filtro)")
print(f"    Para que 'Cargo por venta (Venta)' filtre correctamente, el frontend debe enviar")
print(f"    'clasificacion_operativa=Cargo%20por%20venta%20(Venta)' o 'detalle=Cargo%20por%20venta%20(Venta)' segun corresponda.")
print(f"    Actualmente el frontend envia 'subgroup=...' que no esta declarado en la API.")
