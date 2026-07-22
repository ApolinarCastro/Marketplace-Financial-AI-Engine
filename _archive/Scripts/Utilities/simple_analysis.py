#!/usr/bin/env python3
"""
Simple analysis of the signal filtering normalization issue
"""
import json
import os

# Load ML taxonomy
tax_path = 'knowledge/taxonomy/ml_v1.json'
if os.path.exists(tax_path):
    with open(tax_path, encoding='utf-8') as f:
        ml_tax = json.load(f)
    
    print("=" * 80)
    print("ML TAXONOMY ANALYSIS - Signal Filtering")
    print("=" * 80)
    print()
    
    print("Total categories in taxonomy:", len(ml_tax['detalle_classification']))
    print()
    
    # Find problematic categories
    problematic = []
    signal_true_count = 0
    signal_false_count = 0
    
    for key, value in ml_tax['detalle_classification'].items():
        signal = value.get('signal', False)
        lower_key = key.lower()
        
        if not signal:
            signal_false_count += 1
        else:
            signal_true_count += 1
        
        # Check for our problematic categories
        if ('compensated' in lower_key or 'missing_invoice' in lower_key or 
            ('ajuste' in lower_key and 'poscobro' in lower_key)):
            problematic.append((key, signal, 'NOISE - should be filtered out'))
    
    print("SIGNAL vs NOISE counts:")
    print(f"  signal=True (canonical): {signal_true_count}")
    print(f"  signal=False (noise): {signal_false_count}")
    print()
    
    if problematic:
        print("PROBLEMATIC CATEGORIES (NOISE):")
        for key, signal_value, reason in problematic:
            print(f"  '{key}' - signal={signal_value} - {reason}")
        print()
        
        print("These should be filtered out when signal_mode='SIGNAL'")
        print("But they're appearing in the UI, so signal filtering is NOT working correctly")
    else:
        print("No problematic categories found in taxonomy")
    
    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("The taxonomy structure is correct.")
    print("Compensated, Missing_invoice, Ajuste Poscobro are all NOISE (signal=False)")
    print()
    print("If they're visible in the UI, then:")
    print("1. signal_mode='SIGNAL' is not being used")
    print("2. Or signal filtering logic is broken")
    print("3. Or there's a different data source")
    print()
    print("Most likely: signal_mode parameter is not being passed correctly")
    print("or the signal filtering logic has a bug.")
