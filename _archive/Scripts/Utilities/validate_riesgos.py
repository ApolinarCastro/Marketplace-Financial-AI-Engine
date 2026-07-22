import json

with open("knowledge/taxonomy/ml_v1.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check riesgos_y_compensaciones group
riesgos = data['canonical_groups'].get('riesgos_y_compensaciones', {})
ajustes = data['canonical_groups'].get('ajustes', {})

print("=== RIESGOS Y COMPENSACIONES ===")
print(f"Display name: {riesgos.get('display_name')}")
print(f"Detalles count: {len(riesgos.get('detalles', []))}")
for d in riesgos.get('detalles', []):
    print(f"  - {d}")

print(f"\n=== AJUSTES ===")
print(f"Display name: {ajustes.get('display_name')}")
print(f"Detalles count: {len(ajustes.get('detalles', []))}")
for d in ajustes.get('detalles', []):
    print(f"  - {d}")

# Check for duplicates
riesgos_set = set(riesgos.get('detalles', []))
ajustes_set = set(ajustes.get('detalles', []))
duplicates = riesgos_set & ajustes_set
print(f"\n=== DUPLICATES BETWEEN RIESGOS AND AJUSTES: {len(duplicates)} ===")
for d in duplicates:
    print(f"  DUPLICATE: {d}")

# Check classification mapping
classification = data.get('detalle_classification', {})
print(f"\n=== CLASSIFICATION MAPPING FOR RIESGOS ===")
for d in riesgos.get('detalles', []):
    if d in classification:
        cg = classification[d].get('canonical_group')
        signal = classification[d].get('signal')
        print(f"  {d}: canonical_group={cg}, signal={signal}")
    else:
        print(f"  {d}: NOT IN CLASSIFICATION MAP!")