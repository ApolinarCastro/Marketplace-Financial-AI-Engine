import json
with open("knowledge/taxonomy/ml_v1.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

classification = data.get('detalle_classification', {})
poscobro_concepts = []
for concept, info in classification.items():
    if info.get('canonical_group') in ['ajustes', 'recuperaciones_y_bonificaciones', 'riesgos_y_compensaciones']:
        poscobro_concepts.append(concept)

print("PosCobro-related concepts (should be excluded from DTE legal audit):")
for c in sorted(poscobro_concepts):
    print(f"  - {c}")