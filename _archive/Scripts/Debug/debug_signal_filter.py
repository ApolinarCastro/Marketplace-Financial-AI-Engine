#!/usr/bin/env python3
"""
Debug script to understand why problematic categories are still visible in the UI
"""
import pandas as pd
import json
import os
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

print("=== DEBUGGING: Why are Compensated, Missing_invoice, Ajuste Poscobro still visible? ===")
print()

# Check what the current ledger contains
print("1. Checking marketplace_ledger_v1 for problematic raw details...")
df = db.query("""
    SELECT marketplace, detalle, financial_group, include_in_operational_pnl, COUNT(*) as count, SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE LOWER(detalle) LIKE '%compensated%' 
       OR LOWER(detalle) LIKE '%missing_invoice%' 
       OR LOWER(detalle) LIKE '%ajuste poscobro%'
    GROUP BY marketplace, detalle, financial_group, include_in_operational_pnl
""")

if df.empty:
    print("   No problematic raw details found in marketplace_ledger_v1")
else:
    print("   Found problematic raw details:")
    print(df.to_string(index=False))
print()

# Check what the classified ledger contains
print("2. Checking marketplace_ledger_clasificado_v1 for problematic classified details...")
df_classified = db.query("""
    SELECT marketplace, clasificacion_operativa, financial_group, include_in_operational_pnl, COUNT(*) as count, SUM(monto) as total
    FROM marketplace_ledger_clasificado_v1
    WHERE LOWER(clasificacion_operativa) LIKE '%recuperación%' 
       OR LOWER(clasificacion_operativa) LIKE '%bonificación%'
    GROUP BY marketplace, clasificacion_operativa, financial_group, include_in_operational_pnl
""")

if df_classified.empty:
    print("   No problematic classified details found in marketplace_ledger_clasificado_v1")
else:
    print("   Found problematic classified details:")
    print(df_classified.to_string(index=False))
print()

# Check taxonomy filtering logic
print("3. Checking taxonomy filtering logic...")

# Load ML taxonomy
tax_path = 'knowledge/taxonomy/ml_v1.json'
if os.path.exists(tax_path):
    with open(tax_path, encoding='utf-8') as f:
        ml_tax = json.load(f)
    
    print("   ML Taxonomy structure:")
    print("   - canonical_groups:")
    for group_name, group_info in ml_tax['canonical_groups'].items():
        display_name = group_info['display_name']
        detalles = group_info['detalles']
        signal_count = sum(1 for d in detalles if ml_tax['detalle_classification'].get(d.lower(), {}).get('signal', False))
        noise_count = len(detalles) - signal_count
        print(f"     * {group_name} ({display_name}): {signal_count} SIGNAL, {noise_count} NOISE")
        if len(detalles) <= 10:
            print(f"       Details: {', '.join(detalles)}")
    
    print("   - detalle_classification (signal status for each detalle):")
    problematic_categories = []
    for detalle, info in ml_tax['detalle_classification'].items():
        signal = info.get('signal', False)
        if not signal:
            problematic_categories.append(detalle)
    
    print(f"   Categories with signal=False (NOISE): {len(problematic_categories)}")
    if len(problematic_categories) <= 20:
        print(f"   NOISE categories: {', '.join(problematic_categories)}")
    print()

# Check signal filtering SQL
print("4. Checking SQL signal filtering...")
print("   Signal filtering logic from financial_engine.py:")
print("   - When signal_mode='SIGNAL', only details with signal=True are included")
print("   - When signal_mode='NOISE', only details with signal=False are included")
print("   - When signal_mode='ALL', all details are included")
print()

# Check current endpoint parameters
print("5. Checking what parameters the UI is using...")
print("   From templates/dashboard.html:514-518")
print("   Endpoint: /api/v4/ledger?marketplace=${mp}&periodo=${periodo}&limit=200&offset=${offset || 0}&filter_zero=${fz}&signal_mode=SIGNAL")
print("   signal_mode=SIGNAL should filter out NOISE categories")
print()

print("6. Summary of findings:")
print("   - If compensatory categories are still visible, the signal filtering is not being applied correctly")
print("   - This could be because:")
print("     a) signal_mode parameter is not being passed to the endpoint")
print("     b) The taxonomy filtering logic has a bug")
print("     c) There are multiple data sources being used")
print("     d) The filtering happens after the data is returned to the frontend")
print()
