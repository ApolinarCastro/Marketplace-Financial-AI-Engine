import json

with open("knowledge/taxonomy/ml_v1.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix Different_than_published - move from ajustes to riesgos_y_compensaciones
if 'Different_than_published' in data['detalle_classification']:
    data['detalle_classification']['Different_than_published']['canonical_group'] = 'riesgos_y_compensaciones'
    data['detalle_classification']['Different_than_published']['reason'] = 'ML compensation for product different than published'
    print("Fixed Different_than_published")

# Add missing concepts to classification map
missing_concepts = {
    'Wrong_size': 'ML compensation for wrong size',
    'Wrong_color': 'ML compensation for wrong color',
    'Damaged_or_defective': 'ML compensation for damaged or defective items',
    'Expired_or_past_use_by_date': 'ML compensation for expired products',
    'Other_quality_issue': 'ML compensation for other quality issues',
    'Missing_parts_accessories': 'ML compensation for missing parts/accessories',
    'Wrong_quantity': 'ML compensation for wrong quantity',
    'Wrong_model_version': 'ML compensation for wrong model/version',
    'Wrong_payment_method': 'ML compensation for wrong payment method',
    'Other_payment_issue': 'ML compensation for other payment issues',
    'Other_fashion_related_issue': 'ML compensation for other fashion-related issues',
}

for concept, reason in missing_concepts.items():
    if concept in data['canonical_groups']['riesgos_y_compensaciones']['detalles']:
        data['detalle_classification'][concept] = {
            'signal': True,
            'canonical_group': 'riesgos_y_compensaciones',
            'reason': reason
        }
        print(f"Added {concept} to classification map")

# Save
with open("knowledge/taxonomy/ml_v1.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ Taxonomy fixes applied")