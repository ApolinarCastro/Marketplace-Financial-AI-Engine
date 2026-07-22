import json
import os

# Load the ml_v1.json file
ml_path = "knowledge/taxonomy/ml_v1.json"
with open(ml_path, 'r', encoding='utf-8') as f:
    ml_data = json.load(f)

# List of fashion-related concepts to update
fashion_concepts = [
    "Bigger_than_expected_fashion",
    "Smaller_than_expected_fashion",
    "Not_match_size_guide_fashion", 
    "Repentant_buyer",
    "Undelivered_repentant_buyer",
    "Dont_want_it_another_cause_fashion",
    "Different_color_or_size_fashion",
    "Different_item_other",
    "Undelivered_other",
    "Broken_item_fashion",
    "Empty_box",
    "Damaged_package_broken_item_fashion",
    "Missing_item",
    "Out_of_stock",
    "Estimated_delivery_out_of_time",
    "Different_color_or_size",
    "Item_not_useful_fashion_different",
    "Item_not_useful_fashion_different_change",
    "Not_expected_quality_different",
    "Missing_accessories",
    "Buy_out_of_ML",
    "Different_color_or_size_fashion_change",
    "BPP_covered",
    "Unauthorized_purchase",
    "Change_receiver_address",
    "Delivered_but_not_receive_package",
    "Partially_BPP_refunded",
    "Delivery_date_was_not_met"
]

# Update the classification for these concepts
updated_count = 0
for concept in fashion_concepts:
    if concept in ml_data.get('detalle_classification', {}):
        ml_data['detalle_classification'][concept]['canonical_group'] = "riesgos_y_compensaciones"
        ml_data['detalle_classification'][concept]['reason'] = f"ML compensation for {concept.replace('_', ' ')}"
        updated_count += 1
        print(f"Updated {concept}: {ml_data['detalle_classification'][concept]}")

# Save the updated file
with open(ml_path, 'w', encoding='utf-8') as f:
    json.dump(ml_data, f, ensure_ascii=False, indent=2)

print(f"\nUpdated {updated_count} fashion-related concepts")
print("Current 'ajustes' group details:", ml_data['canonical_groups']['ajustes']['detalles'])
print("Current 'riesgos_y_compensaciones' group details:", ml_data['canonical_groups']['riesgos_y_compensaciones']['detalles'][:5], "...")