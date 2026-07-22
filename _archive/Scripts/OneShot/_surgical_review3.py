import sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

# Check "Cargo" ML classification
print("=== ML 'Cargo' classification check ===")
cargo_clasif = db.query("""
    SELECT l.detalle, c.clasificacion_operativa, c.origen_clasificacion, COUNT(*) as cnt
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
    WHERE l.marketplace = 'ML' AND l.detalle = 'Cargo'
    GROUP BY l.detalle, c.clasificacion_operativa, c.origen_clasificacion
""")
for _, r in cargo_clasif.iterrows():
    print(f"  detalle='{r['detalle']}' -> clasif='{r['clasificacion_operativa']}' origen='{r['origen_clasificacion']}' cnt={r['cnt']}")

# Check where 'Cargo' goes in RAW_TO_CLASSIFICATION_MAP
from engine.v4.marketplace_auditor import RAW_TO_CLASSIFICATION_MAP, normalize_detail, NORMALIZED_CLASSIFICATION_MAP
raw_val = RAW_TO_CLASSIFICATION_MAP.get('Cargo', 'NOT_FOUND')
norm_key = normalize_detail('Cargo')
norm_val = NORMALIZED_CLASSIFICATION_MAP.get(norm_key, 'NOT_FOUND')
print(f"\nRAW_TO_CLASSIFICATION_MAP['Cargo'] = '{raw_val}'")
print(f"normalize_detail('Cargo') = '{norm_key}'")
print(f"NORMALIZED_CLASSIFICATION_MAP['{norm_key}'] = '{norm_val}'")

# Check Ripley concepts that should be added to dictionary
print("\n=== CONCEPTS IN RAW MAP BUT NOT IN DICTIONARY ===")
import json
with open('master_marketplace_dictionary_v1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
dict_aliases = set()
for entry in d['dictionary']:
    for alias in entry['aliases']:
        dict_aliases.add(alias)

# All Ripley concepts from ledger
ripley_raw = set()
for r in db.query("SELECT DISTINCT detalle FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY'"):
    ripley_raw.add(str(r[0]))

not_in_dict = ripley_raw - dict_aliases
print(f"Ripley concepts NOT in dictionary ({len(not_in_dict)}):")
for c in sorted(not_in_dict):
    clasif = db.query("SELECT clasificacion_operativa, origen_clasificacion FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' AND detalle=? LIMIT 1", [c])
    if len(clasif) > 0:
        print(f"  '{c}' -> {clasif.iloc[0]['clasificacion_operativa']} ({clasif.iloc[0]['origen_clasificacion']})")

# ML concepts not in dictionary
ml_raw = set()
for r in db.query("SELECT DISTINCT detalle FROM marketplace_ledger_v1 WHERE marketplace = 'ML'"):
    ml_raw.add(str(r[0]))
not_in_dict_ml = ml_raw - dict_aliases
print(f"\nML concepts NOT in dictionary ({len(not_in_dict_ml)}):")
for c in sorted(not_in_dict_ml):
    clasif = db.query("SELECT clasificacion_operativa, origen_clasificacion FROM marketplace_ledger_clasificado_v1 WHERE marketplace='ML' AND detalle=? LIMIT 1", [c])
    if len(clasif) > 0:
        total = db.query("SELECT SUM(monto) as t, COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace='ML' AND detalle=?", [c]).iloc[0]
        if abs(total['t'] or 0) > 1000:
            print(f"  '{c}' -> {clasif.iloc[0]['clasificacion_operativa']} (${total['t']:,.0f}, {total['cnt']} rows)")
