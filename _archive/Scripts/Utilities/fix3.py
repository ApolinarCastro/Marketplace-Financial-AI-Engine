with open('generate_costos_evidence.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_breakdown_query = '''
BREAKDOWN_QUERY = """
SELECT 
    c.detalle,
    SUM(c.monto) as total
FROM marketplace_ledger_v1 c
WHERE c.marketplace = 'ML' 
  AND c.fecha BETWEEN '2026-02-01' AND '2026-02-28'
  AND c.financial_group IN ('costos_operacionales', 'costos_comerciales', 'ajustes')
  AND COALESCE(c.include_in_operational_pnl,1)=1
  AND COALESCE(c.clasificacion_operativa, '') NOT LIKE 'Ajuste por%'
GROUP BY 1
"""
'''
import re
content = re.sub(r'BREAKDOWN_QUERY\s*=\s*"""(.*?)"""', new_breakdown_query, content, flags=re.DOTALL)

# Add python side mapping
new_ledger_calc = """
    df_breakdown = conn.execute(BREAKDOWN_QUERY).df()
    from api.api import _map_detalle_to_concept
    ledger_composition = {}
    for _, r in df_breakdown.iterrows():
        concept = _map_detalle_to_concept(str(r['detalle']) if pd.notna(r['detalle']) else "")
        ledger_composition[concept] = ledger_composition.get(concept, 0.0) + float(r['total'])
"""
content = re.sub(r"df_breakdown = conn.execute\(BREAKDOWN_QUERY\)\.df\(\)\n\s+ledger_composition = df_breakdown\.set_index\('concept'\)\['total'\]\.to_dict\(\)", new_ledger_calc.strip(), content, flags=re.DOTALL)

with open('generate_costos_evidence.py', 'w', encoding='utf-8') as f:
    f.write(content)
