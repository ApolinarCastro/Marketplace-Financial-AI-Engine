#!/usr/bin/env python3
"""
DEEP DIVE: Understanding the signal filtering disconnect

Based on code analysis, let me trace through the exact flow to identify the root cause
"""

def trace_signal_filtering_flow():
    print("=" * 100)
    print("DEEP DIVE: Signal Filtering Flow Analysis")
    print("=" * 100)
    print()
    
    print("STEP 1: API ENDPOINT CALL")
    print("-" * 50)
    print("User frontend calls: /api/v4/ledger?marketplace=ML&periodo=2026-01&signal_mode=SIGNAL")
    print()
    print("This calls api.py:54-75:")
    print("""
@app.get("/api/v4/ledger")
def get_marketplace_ledger(...):
    marketplace: str = "ML"
    periodo: str | None = None
    ...
    signal_mode: str = "SIGNAL"  # ← PASSED FROM UI
    
    fe = FinancialEngine()
    return fe.query_ledger(
        marketplace=marketplace, 
        periodo=periodo,
        signal_mode=signal_mode,  // ← PASSED TO FINANCIAL ENGINE
    )
""")
    print("✓ API correctly passes signal_mode=SIGNAL to FinancialEngine")
    print()
    
    print("STEP 2: FINANCIAL ENGINE QUERY")
    print("-" * 50)
    print("FinancialEngine.query_ledger() method:")
    print("""
    def query_ledger(self, ..., signal_mode="ALL"):
        ...
        
        # Signal/noise filtering using taxonomy
        if signal_mode.upper() != "ALL":
            import json, os
            mp_lower = marketplace.lower()  # marketplace = "ML"
            tax_files = {
                'ml': 'ml_v1.json', 'paris': 'paris_v1.json',
                'ripley': 'ripley_v1.json', 'falabella': 'falabella_v1.json'
            }
            tax_fname = tax_files.get(mp_lower, 'ripley_v1.json')  # tax_fname = 'ml_v1.json'
            tax_path = os.path.join(os.path.dirname(__file__), 
                '..', '..', '..', 'knowledge', 'taxonomy', tax_fname)
            if os.path.exists(tax_path):
                with open(tax_path, encoding='utf-8') as f:
                    tax = json.load(f)
                is_signal = signal_mode.upper() == "SIGNAL"  # is_signal = True
                matching = [d.lower() for d, info in tax['detalle_classification'].items()
                            if (info.get('signal') is True) == is_signal]
                if matching:
                    ph = ",".join(["?" for _ in matching])
                    conditions.append(f"LOWER(detalle) IN ({ph})")
                    params.extend(matching)
    """)
    print("✓ FinancialEngine loads 'ml_v1.json' taxonomy")
    print("✓ signal_mode=SIGNAL is 'SIGNAL' (not 'ALL')")
    print("✓ is_signal = True (looking for signal=True categories)")
    print()
    
    print("STEP 3: TAXONOMY STRUCTURE")
    print("-" * 50)
    print("Looking at ml_v1.json 'detalle_classification':")
    print("""
    "detalle_classification": {
        "Compensated": {
            "signal": false,  // ← NOISE
            "financial_group": "recuperaciones_y_bonificaciones",
            "rationale": "INCLUDED IN recupeaciones_y_bonificaciones"
        },
        "Missing_invoice": {
            "signal": false,  // ← NOISE
            "financial_group": "recuperaciones_y_bonificaciones",
            "rationale": "INCLUDED IN recupeaciones_y_bonificaciones"
        },
        "Cargo por venta (Venta)": {
            "signal": true,   // ← SIGNAL
            "financial_group": "ingresos",
            "rationale": "CANONICAL revenue"
        },
        ...
    }
    """)
    print("✓ ML taxonomy has signal=False for Compensated, Missing_invoice")
    print("✓ These should be filtered out when is_signal=True")
    print("✓ But wait... the tax['detalle_classification'] lookup uses d.lower()")
    print("✓ So we need to check: 'compensated' vs 'Compensated'")
    print()
    
    print("STEP 4: THE CRITICAL BUG")
    print("-" * 50)
    print("Look at the taxonomy key structure:")
    print("""
    In ml_v1.json, the keys in 'detalle_classification' are normalized!
    
    From the classification process in marketplace_auditor.py:
    """
    print("""
    # From marketplace_auditor.py:396-398
    NORMALIZED_CLASSIFICATION_MAP = {
        normalize_detail(k): v for k, v in RAW_TO_CLASSIFICATION_MAP.items() if k
    }
    """)
    print("    The normalize_detail() function converts to lowercase and removes accents")
    print("    So 'Compensated' becomes 'compensated'")
    print()
    print("    But the taxonomy files use different normalization!")
    print("    Let me check ml_v1.json 'detalle_classification' keys:")
    
    # Let's actually examine this
    import json
    import os
    
    tax_path = 'knowledge/taxonomy/ml_v1.json'
    if os.path.exists(tax_path):
        with open(tax_path, encoding='utf-8') as f:
            ml_tax = json.load(f)
        
        print(f"    Total keys in taxonomy: {len(ml_tax['detalle_classification'])}")
        
        # Check for specific problematic categories
        problematic_keys = []
        for key, value in ml_tax['detalle_classification'].items():
            if 'compensated' in key.lower():
                problematic_keys.append(key)
            if 'missing_invoice' in key.lower():
                problematic_keys.append(key)
            if 'ajuste' in key.lower() and 'poscobro' in key.lower():
                problematic_keys.append(key)
        
        if problematic_keys:
            print(f"    Found potentially problematic keys: {', '.join(problematic_keys[:10])}")
            if len(problematic_keys) > 10:
                print(f"    ... and {len(problematic_keys) - 10} more")
        
        # Check for case variations
        compensations = []
        for key in ml_tax['detalle_classification'].keys():
            if 'compensated' in key.lower():
                compensations.append(key)
        
        if compensations:
            print(f"    Compensation-related keys: {', '.join(compensations[:5])}")
            if len(compensations) > 5:
                print(f"    ... and {len(compensations) - 5} more")
        
        # Check what lowercase keys exist
        lowercase_keys = [k.lower() for k in ml_tax['detalle_classification'].keys()]
        if 'compensated' in lowercase_keys:
            print("    ✓ 'compensated' exists in lowercase keys")
        else:
            print("    ✗ 'compensated' NOT found in lowercase keys")
            
        if 'missing_invoice' in lowercase_keys:
            print("    ✓ 'missing_invoice' exists in lowercase keys")
        else:
            print("    ✗ 'missing_invoice' NOT found in lowercase keys")
    else:
        print("    Could not find ML taxonomy file")
    
    print()
    
    print("STEP 5: CONCLUSION")
    print("-" * 50)
    print("Based on this analysis, here's what could be wrong:")
    print()
    print("POSSIBLE ISSUE 1: TAXONOMY STRUCTURE MISMATCH")
    print("  - FinancialEngine looks for taxonomy keys as stored (potentially mixed case)")
    print("  - Classification normalizes keys to lowercase (e.g., 'Compensated' → 'compensated')")
    print("  - Signal filtering might be looking for 'Compensated' but taxonomy has 'compensated'")
    print()
    print("POSSIBLE ISSUE 2: TAXONOMY LOADING ERROR")
    print("  - Wrong taxonomy file might be loaded")
    print("  - Or the tax_path might be incorrect")
    print()
    print("POSSIBLE ISSUE 3: NORMALIZATION MISMATCH")
    print("  - FinancialEngine uses d.lower() from tax['detalle_classification']")
    print("  - But the matching might be comparing against differently normalized keys")
    print()
    print("STEP 6: CRITICAL FIX NEEDED")
    print("-" * 50)
    print("The fix needs to ensure consistent key normalization:")
    print("  1. Taxonomy files should use consistent case (lowercase)")
    print("  2. FinancialEngine should normalize lookup keys the same way")
    print("  3. Both taxonomy loading and signal filtering should use the same normalization")
    print()
    
    print("=" * 100)
    print("SUMMARY: The root cause is likely a key normalization mismatch")
    print("         between the taxonomy structure and the signal filtering logic.")
    print("=" * 100)

if __name__ == "__main__":
    trace_signal_filtering_flow()
