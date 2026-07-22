import pandas as pd
import os
import sys

# Change to the correct working directory
os.chdir('C:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine')

# Try to import and use the database
try:
    from engine.v4.database import DatabaseV4
    
    print("Attempting to access database...")
    
    # First, let's just check if the tables exist
    db = DatabaseV4.get()
    
    # Simple query to test connection
    result = db.query("SELECT name FROM sqlite_master WHERE type='table' LIMIT 10")
    print("Available tables:")
    print(result.to_string())
    
    # Query for specific problematic ML concepts
    print("\n=== Checking for specific ML concepts from Phase 16C ===")
    specific_concepts = [
        'Bigger_than_expected_fashion',
        'Not_match_size_guide_fashion', 
        'Different_than_published',
        'Undelivered_repentant_buyer'
    ]
    
    for concept in specific_concepts:
        result = db.query("SELECT COUNT(*) as cnt, financial_group FROM marketplace_ledger_v1 WHERE marketplace='ML' AND detalle = ?", [concept])
        print(f"{concept}: {result.iloc[0]['cnt']} rows, financial_group={result.iloc[0]['financial_group']}")
        
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()