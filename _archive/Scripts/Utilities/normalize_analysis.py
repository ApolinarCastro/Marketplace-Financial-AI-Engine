#!/usr/bin/env python3
"""
Analysis of why problematic categories are still visible
"""

def analyze_normalization():
    print("=" * 100)
    print("ANALYSIS: Normalization Mismatch in ML Taxonomy")
    print("=" * 100)
    print()
    
    import json
    import os
    
    # Load ML taxonomy
    tax_path = 'knowledge/taxonomy/ml_v1.json'
    if os.path.exists(tax_path):
        with open(tax_path, encoding='utf-8') as f:
            ml_tax = json.load(f)
        
        print("1. ML TAXONOMY STRUCTURE")
        print("-" * 50)
        print("The 'detalle_classification' keys in ml_v1.json:")
        print()
        
        # Display some sample keys to see their case
        sample_keys = list(ml_tax['detalle_classification'].keys())[:20]
        print("Sample keys:")
        for key in sample_keys:
            print(f"  '{key}'")
        print(f"  ... (and {len(ml_tax['detalle_classification']) - 20} more)")
        print()
        
        # Check for problematic categories
        print("2. SEARCHING FOR PROBLEMATIC CATEGORIES")
        print("-" * 50)
        
        found_categories = []
        for key, value in ml_tax['detalle_classification'].items():
            lower_key = key.lower()
            
            if 'compensated' in lower_key:
                found_categories.append((key, 'Compensated variants', value.get('signal', False)))
            
            if 'missing_invoice' in lower_key:
                found_categories.append((key, 'Missing_invoice variants', value.get('signal', False)))
                
            if 'ajuste' in lower_key and 'poscobro' in lower_key:
                found_categories.append((key, 'Ajuste Poscobro variants', value.get('signal', False)))
        
        if found_categories:
            print("Found problematic categories:")
            for key, desc, signal_value in found_categories:
                print(f"  '{key}' - {desc} - signal={signal_value}")
        else:
            print("  No problematic categories found in taxonomy keys")
        
        print()
        
        # Check for normalized lowercase keys
        print("3. NORMALIZED LOWERCASE KEYS")
        print("-" * 50)
        
        lowercase_keys = [k.lower() for k in ml_tax['detalle_classification'].keys()]
        
        # Check what we're looking for
        targets = ['compensated', 'missing_invoice', 'ajuste poscobro']
        for target in targets:
            if target in lowercase_keys:
                print(f"  ✓ '{target}' exists in lowercase keys")
            else:
                print(f"  ✗ '{target}' NOT found in lowercase keys")
        
        print()
        
        print("4. TAXONOMY NORMALIZATION ANALYSIS")
        print("-" * 50)
        print("The financial_engine.py code uses:")
        print("  matching = [d.lower() for d, info in tax['detalle_classification'].items()]")
        print()
        print("This creates a list of lowercase keys from the taxonomy.")
        print("Then it filters based on signal_mode:")
        print("  if is_signal: only keep keys where info.get('signal') is True")
        print("  if not is_signal: only keep keys where info.get('signal') is False")
        print()
        
        # Show some examples
        print("5. EXAMPLES OF HOW THIS AFFECTS FILTERING")
        print("-" * 50)
        
        print("When signal_mode='SIGNAL' (ML dashboard):")
        print("  - We want: signal=True categories (canonical)")
        print("  - We have: tax['detalle_classification'] with signal values")
        print()
        
        # Count signal true vs false
        signal_true_count = sum(1 for info in ml_tax['detalle_classification'].values() if info.get('signal', False))
        signal_false_count = sum(1 for info in ml_tax['detalle_classification'].values() if not info.get('signal', False))
        
        print(f"  Total ML categories in taxonomy: {signal_true_count + signal_false_count}")
        print(f"  Categories with signal=True (canonical): {signal_true_count}")
        print(f"  Categories with signal=False (noise): {signal_false_count}")
        print()
        
        print("6. THE CRITICAL QUESTION")
        print("-" * 50)
        print("When the frontend requests: /api/v4/ledger?marketplace=ML&signal_mode=SIGNAL")
        print("The financial_engine.py code should:")
        print("  - Load ml_v1.json (✓)")
        print("  - Set is_signal = True (✓)")
        print("  - Create matching = [d.lower() for d, info in tax['detalle_classification'].items() if info.get('signal') is True]")
        print("  - Generate SQL: LOWER(detalle) IN (compensated, missing_invoice, ajuste poscobro, ...)")
        print("  - Filter out NOISE categories (signal=False)")
        print()
        
        # Check if the problematic categories have signal=False
        problematic_with_signal = []
        for key, value in ml_tax['detalle_classification'].items():
            lower_key = key.lower()
            if ('compensated' in lower_key or 'missing_invoice' in lower_key or 
                ('ajuste' in lower_key and 'poscobro' in lower_key)):
                if not value.get('signal', False):
                    problematic_with_signal.append((key, 'NOISE - should be filtered out'))
        
        print("7. PROBLEMATIC CATEGORIES ANALYSIS")
        print("-" * 50)
        if problematic_with_signal:
            print("The problematic categories are NOISE (signal=False):")
            for key, reason in problematic_with_signal:
                print(f"  '{key}' - {reason}")
            print()
            print("Therefore, they SHOULD be filtered out when signal_mode='SIGNAL'")
        else:
            print("No NOISE problematic categories found in taxonomy")
        print()
        
        print("=" * 100)
        print("CONCLUSION")
        print("=" * 100)
        print()
        print("The taxonomy structure is CORRECT.")
        print("If signal filtering is working correctly:")
        print("  - Compensated, Missing_invoice, Ajuste Poscobro should be filtered out")
        print("  - Only signal=True categories should be visible")
        print()
        print("If they're still visible, then:")
        print("  - The signal filtering logic is not being applied correctly")
        print("  - Or signal_mode='SIGNAL' is not being passed to the endpoint")
        print("  - Or there's a different data source being used")
        print()
        
    else:
        print(f"Could not find ML taxonomy file: {tax_path}")

if __name__ == "__main__":
    analyze_normalization()
