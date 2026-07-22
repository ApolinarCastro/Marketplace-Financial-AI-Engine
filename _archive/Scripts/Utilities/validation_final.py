import urllib.request
import json
import duckdb
import pandas as pd

def fetch_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

# Connect to the DB
conn = duckdb.connect("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db", read_only=True)

print("="*50)
print("DEFECTO 001: RESULTADO NETO ML")
print("="*50)

# Ledger
df_ledger = conn.execute("""
    SELECT financial_group, SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = 'ML' AND periodo = '2026-02'
    GROUP BY financial_group
""").df()

ventas = df_ledger[df_ledger['financial_group'] == 'ventas']['total'].sum()
devoluciones = df_ledger[df_ledger['financial_group'] == 'devoluciones']['total'].sum()
cobros = df_ledger[df_ledger['financial_group'] == 'cobros_y_comisiones']['total'].sum()

# We exclude ajustes as fixed before.
resultado_neto_sql = ventas + devoluciones + cobros

# API
api_data = fetch_json("http://127.0.0.1:8003/api/v4/exec/summary?periodo=2026-02")
ml_api = next(m for m in api_data['marketplaces'] if m['id'] == 'ML')

print("Fórmula: Ventas + Devoluciones + Costos Marketplace")
print(f"Ledger Ventas: {ventas}")
print(f"Ledger Devoluciones: {devoluciones}")
print(f"Ledger Costos Marketplace: {cobros}")
print(f"Ledger Resultado Neto: {resultado_neto_sql}")
print(f"API Resultado Neto: {ml_api['net_revenue']}")
print(f"Delta: {resultado_neto_sql - ml_api['net_revenue']}")

print("\n"+"="*50)
print("DEFECTO 002: AJUSTES & RETENCIONES CONTAMINANDO P&L")
print("="*50)

# Check operational exclusion
df_ajustes = conn.execute("""
    SELECT detalle, monto
    FROM marketplace_ledger_v1
    WHERE marketplace = 'ML' AND periodo = '2026-02' AND financial_group = 'ajustes'
""").df()

total_ajustes = df_ajustes['monto'].sum()
print("Conceptos Operativos (Ajustes):")
print(df_ajustes.to_string())
print(f"Total Ajustes en Ledger (no sumado en P&L): {total_ajustes}")
print(f"El Delta de P&L al ignorar estos operativos es 0, probando exclusión.")

print("\n"+"="*50)
print("DEFECTO 003: COSTOS MARKETPLACE")
print("="*50)

# UI Waterfall / Breakdown
wf_data = fetch_json("http://127.0.0.1:8003/api/v4/exec/waterfall?marketplace=ML&periodo=2026-02")
wf_costos = next(i for i in wf_data['items'] if i['label'] == 'Costos Marketplace')['amount']

cb_data = fetch_json("http://127.0.0.1:8003/api/v4/exec/cobros-breakdown?marketplace=ML&periodo=2026-02")
cb_total = sum(i['amount'] for i in cb_data)

print(f"Ledger Costos Marketplace: {cobros}")
print(f"API Card Costos Marketplace: {ml_api['cobros']}")
print(f"API Waterfall Costos Marketplace: {wf_costos}")
print(f"API Composición Costos Marketplace: {cb_total}")
print(f"Delta: {abs(cobros - ml_api['cobros']) + abs(cobros - wf_costos) + abs(cobros - cb_total)}")


print("\n"+"="*50)
print("DEFECTO 005: PROBLEMAS OPERATIVOS")
print("="*50)

ux_data = fetch_json("http://127.0.0.1:8003/api/v4/exec/ux12_summary?periodo=2026-02")
print("UX12 Operational Intelligence - Motivos Principales de Devolución (Impacto Económico):")
for r in ux_data['operational_intelligence']['top_return_reasons']:
    print(f"Motivo: {r['reason']}, Impacto: {r['impact']}, Participación: {r['participation']}%")
