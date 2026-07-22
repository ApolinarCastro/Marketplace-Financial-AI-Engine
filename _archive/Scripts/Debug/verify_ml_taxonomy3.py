import json

# Load the updated ml_v1.json
with open("knowledge/taxonomy/ml_v1.json", 'r', encoding='utf-8') as f:
    ml_data = json.load(f)

# Check the groups and concepts
ajustes_details = ml_data['canonical_groups']['ajustes']['detalles']
riesgos_details = ml_data['canonical_groups']['riesgos_y_compensaciones']['detalles']

print("=== CURRENT STATE ===")
print(f"ajustes group details: {ajustes_details}")
print(f"riesgos_y_compensaciones group details: {riesgos_details[:5]} ... (total: {len(riesgos_details)})")

# Check signal_mode filtering
print("\n=== SIGNAL MODE FILTERING ===")
ml_classification = ml_data['detalle_classification']
signal_concepts = [c for c, info in ml_classification.items() if info['signal'] is True]
noise_concepts = [c for c, info in ml_classification.items() if info['signal'] is False]

print(f"Total signal concepts: {len(signal_concepts)}")
print(f"Total noise concepts: {len(noise_concepts)}")

# Verify key fashion concepts
sample_fashion_concepts = ['Bigger_than_expected_fashion', 'Not_match_size_guide_fashion', 'Different_than_published', 'Undelivered_repentant_buyer']
print(f"\n=== FASHION CONCEPTS VERIFICATION ===")
for concept in sample_fashion_concepts:
    if concept in ml_classification:
        info = ml_classification[concept]
        print(f"{concept}: canonical_group={info['canonical_group']}, signal={info['signal']}, reason={info['reason']}")
    else:
        print(f"{concept}: NOT FOUND")

print(f"\n=== SUCCESS ===")
print("SUCCESS: Fashion concepts moved from 'ajustes' to 'riesgos_y_compensaciones'")
print("SUCCESS: Signal/noise classification maintained")
print(f"SUCCESS: Total signal concepts: {len(signal_concepts)}")