import pandas as pd
import duckdb
import json
import sys
import os
os.chdir(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')

sys.path.insert(0, '.')

# Import the exact same functions used by run_classification()
from engine.v4.marketplace_auditor import normalize_detail, NORMALIZED_CLASSIFICATION_MAP, FINANCIAL_STRUCTURE, CLASIFICACION_TO_FINANCIAL_GROUP

con = duckdb.connect('data/db/meli_financial_v4.db')

# Step 1: Read ONLY RIPLEY rows from ledger
source = con.execute("""
    SELECT id_transaccion, id_orden, detalle, fecha, monto, tipo_movimiento, folio_xml
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
    ORDER BY fecha
""").fetchdf()

total_rows = len(source)
total_amount = float(source['monto'].sum())
print(f"RIPLEY rows loaded: {total_rows}")
print(f"RIPLEY total amount: ${total_amount:,.2f}")

# Step 2: Replicate EXACTLY the classification logic from run_classification()

details = source['detalle'].astype(str).str.strip()

# Handle blank/null/0/nan raw details
blank_mask = details.isna() | details.str.lower().isin(['', '0', '0.0', 'nan', 'none', 'null'])
details[blank_mask] = "Ajuste Poscobro"

# Apply normalization and map
norm_details = details.apply(normalize_detail)
clean_names = norm_details.map(NORMALIZED_CLASSIFICATION_MAP)

clasif = clean_names.copy()
conf = pd.Series(1.0, index=source.index)
origen = pd.Series("atomic_match", index=source.index)

# Identify missing matches
unmatched_mask = clean_names.isna()

# 1. REGLA DINAMICA DE TESORERIA
payout_mask = unmatched_mask & (
    details.str.lower().str.contains('pre_payout_', na=False) |
    details.str.lower().str.contains('post_payout_', na=False) |
    details.str.lower().str.contains('withdraw', na=False) |
    details.str.lower().str.contains('retiro de dinero', na=False) |
    details.str.lower().str.contains('reserve_for_dispute', na=False)
)
clasif[payout_mask] = "Retiro de dinero"
conf[payout_mask] = 1.0
origen[payout_mask] = "payout_rule"

unmatched_mask = unmatched_mask & ~payout_mask

# 2. Historic pre-2026 rule
fechas = source['fecha'].astype(str).str[:10]
ids = source['id_transaccion'].astype(str)

historic_mask = unmatched_mask & (
    ((fechas != 'nan') & (fechas != 'NaT') & (fechas != 'None') & (fechas <= '2025-12-31')) |
    (ids.str.contains('2023') | ids.str.contains('2024') | ids.str.contains('2025'))
)

clasif[historic_mask] = "Ajuste histórico (pre-2026)"
conf[historic_mask] = 1.0
origen[historic_mask] = "auto_history"

# 3. Unrecognized rows
unrecognized_mask = unmatched_mask & ~historic_mask
clasif[unrecognized_mask] = "NO_CLASIFICADO"
conf[unrecognized_mask] = 0.0
origen[unrecognized_mask] = "unrecognized"

# Step 3: Map to financial_group
financial_group = clasif.map(CLASIFICACION_TO_FINANCIAL_GROUP)

# Step 4: Statistics

classified_rows = int((clasif != "NO_CLASIFICADO").sum())
unclassified_rows = int((clasif == "NO_CLASIFICADO").sum())
classified_amount = float(source.loc[clasif != "NO_CLASIFICADO", 'monto'].sum())
unclassified_amount = float(source.loc[clasif == "NO_CLASIFICADO", 'monto'].sum())

coverage_pct = (classified_rows / total_rows * 100) if total_rows else 0
amount_coverage_pct = (classified_amount / total_amount * 100) if total_amount else 0

# financial_group distribution
fg_dist = source.copy()
fg_dist['financial_group'] = financial_group
fg_dist['clasificacion_operativa'] = clasif
fg_dist['confianza'] = conf
fg_dist['origen'] = origen

fg_grouped = fg_dist.groupby('financial_group').agg(rows=('monto', 'count'), amount=('monto', 'sum')).reset_index()
fg_grouped = fg_grouped.sort_values('amount', ascending=False)

# clasificacion_operativa distribution
co_grouped = fg_dist.groupby(['financial_group', 'clasificacion_operativa']).agg(rows=('monto', 'count'), amount=('monto', 'sum')).reset_index()
co_grouped = co_grouped.sort_values('amount', ascending=False)

# Unmapped concepts
unmapped = fg_dist[fg_dist['clasificacion_operativa'] == 'NO_CLASIFICADO']
unmapped_concepts = unmapped.groupby('detalle').agg(rows=('monto', 'count'), amount=('monto', 'sum')).reset_index()
unmapped_concepts = unmapped_concepts.sort_values('amount', ascending=False)

# Expected Dashboard categories after propagation
# Dashboard shows: ingresos, devoluciones, costos_operacionales, costos_comerciales, ajustes
dashboard_categories = fg_dist[fg_dist['financial_group'].isin(['ingresos', 'devoluciones', 'costos_operacionales', 'costos_comerciales', 'ajustes'])]
dash_grouped = dashboard_categories.groupby('financial_group').agg(rows=('monto', 'count'), amount=('monto', 'sum')).reset_index()
dash_grouped = dash_grouped.sort_values('amount', ascending=False)

# Build results
results = {
    "total_rows": total_rows,
    "total_amount": total_amount,
    "classified_rows": classified_rows,
    "unclassified_rows": unclassified_rows,
    "classified_amount": classified_amount,
    "unclassified_amount": unclassified_amount,
    "coverage_pct": round(coverage_pct, 2),
    "amount_coverage_pct": round(amount_coverage_pct, 2),
    "coverage_pass": coverage_pct >= 99.0,
    "amount_coverage_pass": amount_coverage_pct >= 99.0,
    "financial_group_distribution": fg_grouped.to_dict('records'),
    "clasificacion_operativa_distribution": co_grouped.to_dict('records'),
    "unmapped_concepts": unmapped_concepts.to_dict('records'),
    "expected_dashboard_categories": dash_grouped.to_dict('records'),
    "dashboard_total_neto": float(dash_grouped['amount'].sum()),
}

print("\n=== DRY RUN RESULTS ===")
print(f"Total rows: {total_rows}")
print(f"Total amount: ${total_amount:,.2f}")
print(f"Classified rows: {classified_rows} ({coverage_pct:.2f}%)")
print(f"Unclassified rows: {unclassified_rows}")
print(f"Classified amount: ${classified_amount:,.2f} ({amount_coverage_pct:.2f}%)")
print(f"Unclassified amount: ${unclassified_amount:,.2f}")
print(f"Coverage >= 99%: {coverage_pct >= 99.0}")
print(f"Amount coverage >= 99%: {amount_coverage_pct >= 99.0}")

print("\n--- Financial Group Distribution ---")
for r in fg_grouped.to_dict('records'):
    print(f"  {str(r['financial_group']):25s} | rows={r['rows']:>6d} | amount=${r['amount']:>14,.2f}")

print("\n--- Clasificacion Operativa Distribution ---")
for r in co_grouped.to_dict('records'):
    print(f"  {str(r['clasificacion_operativa']):45s} | {str(r['financial_group']):25s} | rows={r['rows']:>6d} | amount=${r['amount']:>14,.2f}")

print("\n--- Unmapped Concepts ---")
for r in unmapped_concepts.to_dict('records'):
    print(f"  '{r['detalle']:60s}' | rows={r['rows']:>4d} | amount=${r['amount']:>14,.2f}")

print("\n--- Expected Dashboard Categories ---")
for r in dash_grouped.to_dict('records'):
    print(f"  {r['financial_group']:25s} | rows={r['rows']:>6d} | amount=${r['amount']:>14,.2f}")
  
# Save to JSON for report generation
with open('_dry_run_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str, ensure_ascii=False)

con.close()
print("\nResults saved to _dry_run_results.json")
