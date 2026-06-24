import sys, warnings; sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine'); warnings.filterwarnings('ignore')
import duckdb

con = duckdb.connect(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\meli_financial_v4.db', read_only=True)

def q(sql):
    return con.execute(sql).fetchdf()

# FASE 4: ML audit deep dive
print("=== FASE 4: ML AUDIT DEEP DIVE ===\n")

# Why legal check returns 0 for ML
print("1. ML folio_xml coverage:")
r = q("""
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN folio_xml IS NULL THEN 1 ELSE 0 END) as null_folio,
  SUM(CASE WHEN folio_xml = 'None' THEN 1 ELSE 0 END) as none_folio,
  SUM(CASE WHEN folio_xml IS NOT NULL AND folio_xml != 'None' AND folio_xml NOT LIKE '%disponible%' AND folio_xml NOT LIKE 'A%n%' THEN 1 ELSE 0 END) as valid_folio
FROM marketplace_ledger_v1 WHERE marketplace='ML'
""")
print(r.to_string(index=False))

print("\n2. ML valid folios matching dte_truth:")
r = q("""
SELECT 
  COUNT(*) as valid_folios,
  SUM(CASE WHEN EXISTS (SELECT 1 FROM dte_truth_v1 t WHERE l.folio_xml LIKE '%' || t.folio) THEN 1 ELSE 0 END) as matched_dte,
  SUM(CASE WHEN NOT EXISTS (SELECT 1 FROM dte_truth_v1 t WHERE l.folio_xml LIKE '%' || t.folio) THEN 1 ELSE 0 END) as unmatched_dte
FROM marketplace_ledger_v1 l 
WHERE l.marketplace='ML' AND l.folio_xml IS NOT NULL AND l.folio_xml != 'None' 
  AND l.folio_xml NOT LIKE '%disponible%' AND l.folio_xml NOT LIKE 'A%n%'
""")
print(r.to_string(index=False))

print("\n3. ML audit_ml_misclassification check:")
# Check what records exist
r = q("SELECT * FROM marketplace_auditoria_v1 WHERE marketplace='ML' ORDER BY detected_at DESC LIMIT 10")
print(f"Any ML audit rows: {len(r)}")
if len(r) > 0: print(r.to_string(index=False))

print("\n4. Check if audit_ml module inserts rows:")
try:
    from engine.v4.marketplace_auditor_ml import audit_ml_misclassifications
    import inspect
    src = inspect.getsource(audit_ml_misclassifications)
    # Just check if it inserts into auditoria
    if 'marketplace_auditoria_v1' in src:
        print("audit_ml_misclassifications DOES insert into marketplace_auditoria_v1")
    else:
        print("audit_ml_misclassifications does NOT insert into marketplace_auditoria_v1")
    # Check the logic briefly
    print(f"Source lines: {len(src.splitlines())}")
except Exception as e:
    print(f"Error inspecting audit_ml: {e}")

# FASE 3: Dashboard check
print("\n\n=== FASE 3: DASHBOARD CONSUMPTION ===\n")

# Check if dashboard templates reference cierre table
import os
dash_dir = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\templates'
dash_files = [f for f in os.listdir(dash_dir) if f.endswith('.html')]
print(f"Dashboard templates: {dash_files}")

for fname in dash_files:
    fpath = os.path.join(dash_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check references
    checks = {
        'cierre_financiero_v1': 'cierre_financiero_v1' in content,
        'resultado_neto': 'resultado_neto' in content,
        '/api/v4/': '/api/v4/' in content,
        '/exec/': '/exec/' in content,
        'cache': 'cache' in content.lower(),
    }
    print(f"  {fname}: {checks}")

# Check API routes
api_path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\api\api.py'
with open(api_path, 'r', encoding='utf-8') as f:
    api_content = f.read()

# Find cierre endpoints
import re
endpoints = re.findall(r'@router\.(get|post)\([\'"]([^\'"]+)[\'"]\)', api_content)
cierre_eps = [e for e in endpoints if 'cierre' in e[1] or 'exec' in e[1]]
print(f"\nCierre/Exec API endpoints: {len(cierre_eps)}")
for m, ep in cierre_eps:
    print(f"  {m.upper()} {ep}")

# Check if endpoints query direct DB or cached
print("\nAPI query sources:")
for ep_match in re.finditer(r'@router\.(get|post)\([\'"]([^\'"]+)[\'"]\)\s*\n(?:async )?def \w+\([^)]*\):\s*\n(.*?)(?=\n@router|\Z)', api_content, re.DOTALL):
    ep_path = ep_match.group(2)
    body = ep_match.group(3)
    is_cache = 'cache' in body.lower()
    is_db = 'db.' in body or 'database' in body.lower()
    is_memory = 'memory' in body.lower() or 'cache' in body.lower()
    print(f"  {ep_path}: direct_db={is_db}, caching={is_cache}")

con.close()
