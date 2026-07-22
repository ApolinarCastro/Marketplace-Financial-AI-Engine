#!/usr/bin/env python3
"""
Analysis of why problematic categories are still visible in the UI
Based on code examination (database locked, so analyzing code logic)
"""

def analyze_signal_filtering():
    print("=" * 80)
    print("ANALYSIS: Why are Compensated, Missing_invoice, Ajuste Poscobro still visible?")
    print("=" * 80)
    print()
    
    print("1. EXPECTED SIGNAL FILTERING LOGIC")
    print("-" * 50)
    print("From financial_engine.py:339-359:")
    print("""
    if signal_mode.upper() != "ALL":
        import json, os
        mp_lower = marketplace.lower()
        tax_files = {
            'ml': 'ml_v1.json', 'paris': 'paris_v1.json',
            'ripley': 'ripley_v1.json', 'falabella': 'falabella_v1.json'
        }
        tax_fname = tax_files.get(mp_lower, 'ripley_v1.json')
        tax_path = os.path.join(os.path.dirname(__file__),
            '..', '..', '..', 'knowledge', 'taxonomy', tax_fname)
        if os.path.exists(tax_path):
            with open(tax_path, encoding='utf-8') as f:
                tax = json.load(f)
            is_signal = signal_mode.upper() == "SIGNAL"
            matching = [d.lower() for d, info in tax['detalle_classification'].items()
                        if (info.get('signal') is True) == is_signal]
            if matching:
                ph = ",".join(["?" for _ in matching])
                conditions.append(f"LOWER(detalle) IN ({ph})")
                params.extend(matching)
    """)
    print("   When signal_mode='SIGNAL', only signal=True categories should be included")
    print("   When signal_mode='NOISE', only signal=False categories should be included")
    print()
    
    print("2. ML TAXONOMY ANALYSIS")
    print("-" * 50)
    print("From knowledge/taxonomy/ml_v1.json:")
    print("   - 'recuperaciones_y_bonificaciones' group contains NOISE categories")
    print("   - These include 'Compensated', 'Missing_invoice', 'Ajuste Poscobro' (in different forms)")
    print("   - All these should have signal=False in taxonomy")
    print("   - Therefore they should be filtered out when signal_mode='SIGNAL'")
    print()
    
    print("3. UI ENDPOINTS AND PARAMETERS")
    print("-" * 50)
    print("From templates/dashboard.html:514-518:")
    print("   Endpoint: /api/v4/ledger?marketplace=${mp}&periodo=${periodo}&signal_mode=SIGNAL")
    print("   signal_mode=SIGNAL should filter out NOISE categories")
    print()
    print("From templates/executive_dashboard.html:332-333:")
    print("   Endpoint: /api/v4/financial-structure?marketplace=ALL&periodo=${period}&signal_mode=SIGNAL")
    print("   signal_mode=SIGNAL should filter out NOISE categories")
    print()
    
    print("4. POTENTIAL ISSUES")
    print("-" * 50)
    print("Issues that could cause NOISE categories to still appear:")
    print()
    print("a) WRONG TAXONOMY LOADING")
    print("   - If wrong taxonomy file is loaded (e.g., ripley_v1.json instead of ml_v1.json)")
    print("   - Then ML categories might not be filtered correctly")
    print()
    print("b) TAXONOMY STRUCTURE ISSUE")
    print("   - If taxonomy structure is wrong or malformed")
    print("   - signal field might not be set correctly")
    print()
    print("c) SQL FILTERING BUG")
    print("   - If the IN clause filtering has a bug")
    print("   - Or if the parameter substitution is wrong")
    print()
    print("d) MULTIPLE DATA SOURCES")
    print("   - If there are multiple endpoints or data sources")
    print("   - And some don't use signal_mode filtering")
    print()
    print("e) CASE SENSITIVITY")
    print("   - If case conversion is not handled correctly")
    print("   - 'Compensated' vs 'compensated' mismatch")
    print()
    print("f) ENDPOINT MISCONFIGURATION")
    print("   - If signal_mode parameter is not passed to endpoint")
    print("   - Default value might be 'ALL' instead of 'SIGNAL'")
    print()
    
    print("5. SPECIFIC INVESTIGATION POINTS")
    print("-" * 50)
    print("a) Check taxonomy loading logic in financial_engine.py")
    print("b) Verify parameter passing in api.py endpoints")
    print("c) Check if there are other data sources bypassing signal filtering")
    print("d) Look for any hardcoded filters that override signal_mode")
    print("e) Examine if the financial_engine.py query_ledger method is being called correctly")
    print()
    
    print("6. LIKELY ROOT CAUSE")
    print("-" * 50)
    print("Based on analysis, the most likely issue is:")
    print()
    print("   The signal filtering in financial_engine.py is working correctly.")
    print("   However, there might be a disconnect between:")
    print("   - The classification system (marketplace_auditor.py)")
    print("   - The signal filtering system (financial_engine.py)")
    print("   - The UI consumption of endpoints")
    print()
    print("   Possible scenarios:")
    print("   1. marketplace_auditor.py classifies categories but financial_engine.py still sees raw details")
    print("   2. Financial engine and marketplace auditor are using different data sources")
    print("   3. There are multiple versions of the same table/views being used")
    print("   4. Signal filtering is applied but then overridden somewhere else")
    print()
    
    print("7. REQUIRED INVESTIGATION")
    print("-" * 50)
    print("a) Check if marketplace_ledger_v1 and marketplace_ledger_clasificado_v1 are synchronized")
    print("b) Verify that the signal filtering in financial_engine.py is being applied correctly")
    print("c) Check if there are any views or synonyms that bypass the filtering")
    print("d) Look for any other places where the ledger data is accessed directly")
    print()
    
    print("=" * 80)
    print("CONCLUSION: The issue is likely a disconnect between the classification")
    print("            system and the signal filtering system, or a data source")
    print("            that bypasses the signal filtering entirely.")
    print("=" * 80)

if __name__ == "__main__":
    analyze_signal_filtering()
