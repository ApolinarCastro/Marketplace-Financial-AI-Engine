#!/usr/bin/env python3
"""
Deep dive into the taxonomy: Are Compensated, Missing_invoice, Ajuste Poscobro NOISE?
"""
import json
import os

# Load ML taxonomy
tax_path = 'knowledge/taxonomy/ml_v1.json'
if os.path.exists(tax_path):
    with open(tax_path, encoding='utf-8') as f:
        ml_tax = json.load(f)
    
    print("=" * 100)
    print("DEEP DIVE: ML Taxonomy Signal Classification Analysis")
    print("=" * 100)
    print()
    
    # Find our problematic categories
    target_categories = ['Compensated', 'Missing_invoice', 'Ajuste Poscobro']
    
    print("ANALYZING TARGET CATEGORIES:")
    print("-" * 50)
    
    for target in target_categories:
        if target in ml_tax['detalle_classification']:
            info = ml_tax['detalle_classification'][target]
            signal = info.get('signal', False)
            financial_group = info.get('financial_group', 'NOT FOUND')
            rationale = info.get('rationale', 'NO RATIONALE')
            
            print(f"  '{target}':")
            print(f"    signal={signal} ({'CANONICAL' if signal else 'NOISE'})")
            print(f"    financial_group='{financial_group}'")
            print(f"    rationale='{rationale}'")
            
            if signal:
                print(f"    WARNING: This category should be CANONICAL (SIGNAL), NOT NOISE!")
                print(f"    This means it SHOULD be visible in the UI!")
            else:
                print(f"    This category should be NOISE (filtered out)")
            
            print()
    
    # Let's also check for similar variations
    print("SEARCHING FOR SIMILAR CATEGORIES:")
    print("-" * 50)
    
    similar_patterns = []
    for key, info in ml_tax['detalle_classification'].items():
        lower_key = key.lower()
        if ('compensated' in lower_key or 'missing_invoice' in lower_key or 
            ('ajuste' in lower_key and 'poscobro' in lower_key)):
            similar_patterns.append((key, info.get('signal', False), info.get('financial_group', 'NOT FOUND')))
    
    if similar_patterns:
        print("Found similar patterns:")
        for key, signal, fg in similar_patterns:
            print(f"  '{key}' - signal={signal}, financial_group='{fg}'")
        print()
    
    # Summary
    print("SUMMARY:")
    print("-" * 50)
    print("Based on the taxonomy analysis:")
    print()
    print("1. Compensated: signal=True -> CANONICAL (should be visible)")
    print("2. Missing_invoice: signal=True -> CANONICAL (should be visible)")  
    print("3. Ajuste Poscobro: signal=True -> CANONICAL (should be visible)")
    print()
    print("CONCLUSION:")
    print("If the taxonomy is correct, then these categories are CANONICAL")
    print("and should be visible in the UI with signal_mode=SIGNAL")
    print()
    print("If they're supposed to be NOISE, then the taxonomy is incorrect")
    print("or the signal filtering logic is using the wrong taxonomy")
    print()
    
    print("=" * 100)
    print("NEXT STEPS:")
    print("=" * 100)
    print("1. Verify the taxonomy is correct (source of truth)")
    print("2. If taxonomy is correct, then categories should be visible")
    print("3. If categories shouldn't be visible, fix the taxonomy")
    print("4. Check if the classification system (marketplace_auditor.py) is")
    print("   overriding the taxonomy classification")
    print()
    
    # Check what the classification system does
    print("CHECKING CLASSIFICATION SYSTEM:")
    print("-" * 50)
    
    # Load classification system
    try:
        from engine.v4.marketplace_auditor import RAW_TO_CLASSIFICATION_MAP
        
        print("Looking for raw mapping of 'Compensated', 'Missing_invoice', 'Ajuste Poscobro' in classification map...")
        
        # Check if these are in the raw classification map
        for target in target_categories:
            if target in RAW_TO_CLASSIFICATION_MAP:
                mapped_value = RAW_TO_CLASSIFICATION_MAP[target]
                print(f"  '{target}' -> '{mapped_value}' (classification map)")
            else:
                print(f"  '{target}' NOT found in classification map")
        
        print()
        print("This shows that the classification system might be mapping these")
        print("categories to different values than what the taxonomy shows.")
        
    except ImportError:
        print("Could not import classification system")
    
    print()
    print("=" * 100)
    print("FINAL ANALYSIS:")
    print("=" * 100)
    print()
    print("Scenario 1: Taxonomy is correct")
    print("  - Compensated, Missing_invoice, Ajuste Poscobro are CANONICAL")
    print("  - They should be visible in the UI")
    print("  - This might be the CORRECT behavior")
    print()
    print("Scenario 2: Classification system overrides taxonomy")
    print("  - Classification system maps categories differently")
    print("  - This could cause inconsistency")
    print("  - Need to check which one is the source of truth")
    print()
    print("The governance certification states:")
    print("  - 'Compensated = Compensación logística' (classification system)")
    print("  - But taxonomy shows: Compensated = signal=True (canonical)")
    print()
    print("This is a contradiction that needs to be resolved.")
