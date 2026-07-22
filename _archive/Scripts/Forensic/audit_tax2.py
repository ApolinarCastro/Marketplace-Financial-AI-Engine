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
res = conn.execute(query).fetchall()

with open("C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/2c921f1a-4258-4b8e-be46-1ad937059ee6/PARIS_COMMISSION_TAXONOMY_AUDIT.md", "w", encoding="utf-8") as f:
    f.write("# PARIS COMMISSION TAXONOMY AUDIT\n\n")
    f.write("## Auditoría de Taxonomía Existente para Comisiones\n\n")
    f.write("| Marketplace | Financial Group | Detalle | Qty | Total |\n")
    f.write("|-------------|-----------------|---------|-----|-------|\n")
    
    oficial_group = "costos_comerciales"
    for r in res:
        f.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |\n")
        if r[1] and 'costos' in str(r[1]).lower():
            oficial_group = str(r[1])
            
    f.write("\n\n### Conclusión\n")
    f.write(f"El `financial_group` oficial de Comisión Marketplace es **{oficial_group}**.\n")
    f.write("Se reutilizará esta taxonomía existente para PARIS, prohibiendo la creación de grupos nuevos.\n")
    
print("Audit complete.")
