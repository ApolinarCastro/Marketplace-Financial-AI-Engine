import duckdb

db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db"
conn = duckdb.connect(db_path, read_only=True)

query = """
    SELECT marketplace, financial_group, detalle, COUNT(*) as qty, SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE detalle LIKE '%omisi%' OR detalle LIKE '%Comis%' OR detalle LIKE '%comis%' OR clasificacion_operativa LIKE '%omisi%'
    GROUP BY marketplace, financial_group, detalle
    ORDER BY marketplace, financial_group
"""
df = conn.execute(query).df()
print(df.to_markdown())

with open("C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/2c921f1a-4258-4b8e-be46-1ad937059ee6/PARIS_COMMISSION_TAXONOMY_AUDIT.md", "w", encoding="utf-8") as f:
    f.write("# PARIS COMMISSION TAXONOMY AUDIT\n\n")
    f.write("## Auditoría de Taxonomía Existente para Comisiones\n\n")
    f.write(df.to_markdown(index=False))
    f.write("\n\n### Conclusión\n")
    # I will fill the conclusion manually based on the output.
