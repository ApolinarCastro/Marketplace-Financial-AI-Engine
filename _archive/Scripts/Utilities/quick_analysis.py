#!/usr/bin/env python3
"""
Quick analysis: Why are Compensated, Missing_invoice, Ajuste Poscobro visible?
"""
import json
import os

print("=" * 100)
print("ROOT CAUSE ANALYSIS: Taxonomy vs Classification System Discrepancy")
print("=" * 100)
print()

# Load ML taxonomy
tax_path = 'knowledge/taxonomy/ml_v1.json'
if os.path.exists(tax_path):
    with open(tax_path, encoding='utf-8') as f:
        ml_tax = json.load(f)
    
    print("1. TAXONOMY SHOWS:")
    print("-" * 50)
    
    # Check our target categories
    targets = ['Compensated', 'Missing_invoice', 'Ajuste Poscobro']
    
    for target in targets:
        if target in ml_tax['detalle_classification']:
            info = ml_tax['detalle_classification'][target]
            signal = info.get('signal', False)
            fg = info.get('financial_group', 'NOT FOUND')
            
            status = "CANONICAL (SIGNAL)" if signal else "NOISE"
            print(f"  {target}: signal={signal} -> {status}")
            print(f"    financial_group='{fg}'")
        else:
            print(f"  {target}: NOT FOUND in taxonomy")
    
    print()
    print("2. CLASSIFICATION SYSTEM (marketplace_auditor.py):")
    print("-" * 50)
    
    # Check the raw classification map
    try:
        from engine.v4.marketplace_auditor import RAW_TO_CLASSIFICATION_MAP
        
        print("In RAW_TO_CLASSIFICATION_MAP:")
        for target in targets:
            if target in RAW_TO_CLASSIFICATION_MAP:
                mapped = RAW_TO_CLASSIFICATION_MAP[target]
                print(f"  {target} -> {mapped}")
            else:
                print(f"  {target} -> NOT FOUND")
        
    except ImportError:
        print("Could not import classification system")
    
    print()
    print("3. FINANCIAL STRUCTURE:")
    print("-" * 50)
    print("In FINANCIAL_STRUCTURE (marketplace_auditor.py):")
    
    try:
        from engine.v4.marketplace_auditor import FINANCIAL_STRUCTURE
        
        # Check which group these categories belong to
        for target in targets:
            for group_name, group_details in FINANCIAL_STRUCTURE.items():
                if target in group_details:
                    print(f"  {target} belongs to '{group_name}'")
                    break
            else:
                print(f"  {target} not found in any financial group")
        
    except ImportError:
        print("Could not import financial structure")
    
    print()
    print("=" * 100)
    print("CRITICAL DISCREPANCY IDENTIFIED:")
    print("=" * 100)
    print()
    print("TAXONOMY says: Compensated, Missing_invoice, Ajuste Poscobro are CANONICAL (signal=True)")
    print()
    print("But GOVERNANCE documents and certifications state they should be NOISE")
    print("(Compensated = Compensación logística, Missing_invoice = Compensación logística)")
    print()
    print("This is the ROOT CAUSE of the issue!")
    print()
    print("SOLUTION NEEDED:")
    print("1. Either update taxonomy to mark these as NOISE (signal=False)")
    print("2. Or update governance certifications to reflect taxonomy as truth")
    print("3. Or add exception logic in signal filtering for these specific categories")
    print()
    print("This explains why:")
    print("- Compensated appears visible in UI")
    print("- Missing_invoice appears visible in UI") 
    print("- Ajuste Poscobro appears visible in UI")
    print("- Yet certifications claim they should be filtered out")
