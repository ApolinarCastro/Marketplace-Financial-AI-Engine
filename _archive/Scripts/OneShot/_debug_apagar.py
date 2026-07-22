import sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import normalize_detail, NORMALIZED_CLASSIFICATION_MAP, RAW_TO_CLASSIFICATION_MAP

db = DatabaseV4.get()

# Check 'A pagar'
raw_val = RAW_TO_CLASSIFICATION_MAP.get('A pagar', 'NOT_IN_MAP')
norm = normalize_detail('A pagar')
norm_val = NORMALIZED_CLASSIFICATION_MAP.get(norm, 'NOT_IN_NORM_MAP')
print("RAW_MAP['A pagar'] = '%s'" % raw_val)
print("normalize('A pagar') = '%s'" % norm)
print("NORM_MAP['%s'] = '%s'" % (norm, norm_val))

# Check actual Ripley 'A pagar' values
rows = db.query("SELECT DISTINCT detalle FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND detalle LIKE '%paga%'")
for r in rows:
    val = str(r[0])
    print("DB value: '%s'" % repr(val))
    print("  norm: '%s'" % normalize_detail(val))

# Check if 'a pagar' collides with any other normalized key
all_norm_keys = sorted(NORMALIZED_CLASSIFICATION_MAP.keys())
print("\nAll normalized keys containing 'pagar':")
for k in all_norm_keys:
    if 'pagar' in k:
        print("  '%s' -> '%s'" % (k, NORMALIZED_CLASSIFICATION_MAP[k]))
