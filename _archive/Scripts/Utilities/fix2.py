with open('generate_costos_evidence.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'conn = duckdb.connect("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db", read_only=True)',
    'import engine.v4.database as db_module\n    conn = db_module.DatabaseV4.get().conn'
)

with open('generate_costos_evidence.py', 'w', encoding='utf-8') as f:
    f.write(content)
