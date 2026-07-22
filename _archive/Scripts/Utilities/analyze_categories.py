#!/usr/bin/env python3
import pandas as pd
import json
import os
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()
print('=== SEARCHING FOR PROBLEMATIC CATEGORIES IN marketplace_ledger_v1 ===')
print()

# Search for specific problematic categories
problem_categories = ['Compensated', 'Missing_invoice', 'Ajuste Poscobro']

for cat in problem_categories:
    df = db.query('SELECT marketplace, detalle, financial_group, include_in_operational_pnl, COUNT(*) as count, SUM(monto) as total FROM marketplace_ledger_v1 WHERE LOWER(detalle) LIKE ? GROUP BY marketplace, detalle, financial_group, include_in_operational_pnl', [f'%{cat}%'])
    if not df.empty:
        print(f'Categoría problemática: {cat}')
        print(df.to_string(index=False))
        print()
    else:
        print(f'Categoría problemática: {cat} - NO ENCONTRADA')
        print()

print('=== TODAS LAS CATEGORÍAS RIPLEY (senal=NOISE) ===')
# Check what RIPLEY categories are classified as NOISE
tax_path = 'knowledge/taxonomy/ripley_v1.json'
if os.path.exists(tax_path):
    with open(tax_path, encoding='utf-8') as f:
        ripley_tax = json.load(f)
    
    noise_detalles = []
    for detalle, info in ripley_tax['detalle_classification'].items():
        if not info.get('signal', False):
            noise_detalles.append(detalle)
    
    print(f'Total categorías NOISE: {len(noise_detalles)}')
    print('Categorías NOISE RIPLEY:', ', '.join(noise_detalles[:20]))
    if len(noise_detalles) > 20:
        print(f'... y {len(noise_detalles) - 20} más')
    print()

print('=== VERIFICANDO TAXONOMÍA ML: Compensated, Missing_invoice, Ajuste Poscobro ===')
tax_path = 'knowledge/taxonomy/ml_v1.json'
if os.path.exists(tax_path):
    with open(tax_path, encoding='utf-8') as f:
        ml_tax = json.load(f)
    
    for cat in ['Compensated', 'Missing_invoice', 'Ajuste Poscobro']:
        found = False
        for detalle, info in ml_tax.get('detalle_classification', {}).items():
            if cat.lower() in detalle.lower() and not info.get('signal', True):
                print(f'  {detalle}: NOISE (señal={info.get("signal", "UNKNOWN")})')
                found = True
        if not found:
            print(f'  {cat}: NO ENCONTRADO EN TAXONOMÍA o es SIGNAL')
    print()

print('=== VERIFICANDO MONTOS DE CATEGORÍAS PROBLEMÁTICAS (CON include_in_operational_pnl=0) ===')
# Now let's verify the actual monetary amounts
total_amount = 0
for cat in problem_categories:
    df = db.query('SELECT marketplace, detalle, financial_group, include_in_operational_pnl, SUM(monto) as total_amount FROM marketplace_ledger_v1 WHERE LOWER(detalle) LIKE ? GROUP BY marketplace, detalle, financial_group, include_in_operational_pnl', [f'%{cat}%'])
    if not df.empty:
        for _, row in df.iterrows():
            print(f'{cat} ({row["detalle"]}) - Marketplace: {row["marketplace"]}, Financial Group: {row["financial_group"]}, Include in Operational PNL: {row["include_in_operational_pnl"]}, Total Amount: ${row["total_amount"]:.2f}')
            total_amount += float(row['total_amount'])

print(f'Total de todas las categorías problemáticas: ${total_amount:.2f}')
print()

print('=== VERIFICANDO SI settlement_bridge_missing EXISTE EN ledger ===')
df = db.query('SELECT marketplace, detalle, financial_group, include_in_operational_pnl, COUNT(*) as count, SUM(monto) as total FROM marketplace_ledger_v1 WHERE LOWER(detalle) LIKE ? GROUP BY marketplace, detalle, financial_group, include_in_operational_pnl', ['settlement_bridge'])
if not df.empty:
    print('settlement_bridge_missing found in ledger:')
    print(df.to_string(index=False))
else:
    print('settlement_bridge_missing NOT found in ledger')
print()
