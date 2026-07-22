import pandas as pd
import os
from engine.v4.database import DatabaseV4

db_path = 'data/db/meli_financial_v4.db'
print('Database exists:', os.path.exists(db_path))
print('File size:', os.path.getsize(db_path) if os.path.exists(db_path) else 'N/A')

db = DatabaseV4.get()
print('\n=== ML ledger problematic concepts (fashion-related) ===')
result = db.query("""
    SELECT detalle, COUNT(*) as cnt, financial_group 
    FROM marketplace_ledger_v1 
    WHERE marketplace='ML' 
    AND (LOWER(detalle) LIKE '%bigger%' OR LOWER(detalle) LIKE '%not_match%' OR LOWER(detalle) LIKE '%different%' OR LOWER(detalle) LIKE '%repentant%' OR LOWER(detalle) LIKE '%undelivered%')
    GROUP BY detalle, financial_group
    ORDER BY cnt DESC
    LIMIT 20
""")
print(result.to_string())

print('\n=== Specific ML concepts from Phase 16C ===')
specific_concepts = [
    'Bigger_than_expected_fashion',
    'Not_match_size_guide_fashion', 
    'Different_than_published',
    'Undelivered_repentant_buyer'
]
for concept in specific_concepts:
    result = db.query("SELECT COUNT(*) as cnt, financial_group FROM marketplace_ledger_v1 WHERE marketplace='ML' AND detalle = ?", [concept])
    print(f'{concept}: {result.iloc[0]["cnt"]} rows, financial_group={result.iloc[0]["financial_group"]}')