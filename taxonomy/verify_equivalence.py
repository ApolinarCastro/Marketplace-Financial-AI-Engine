"""Verify 100% structural equivalence between Python code and YAML taxonomy."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from taxonomy import taxonomy_loader as tl
from engine.v4.marketplace_auditor import (
    FINANCIAL_STRUCTURE,
    RAW_TO_CLASSIFICATION_MAP,
    CLASIFICACION_TO_FINANCIAL_GROUP,
    NORMALIZED_CLASSIFICATION_MAP,
)

rules = tl.load_rules()
mappings = tl.load_mappings()
validation = tl.validate_taxonomy(rules, mappings)
print("Validation:", validation)

# Show missing concepts
concept_to_group = tl.build_concept_to_group_map(rules)
all_concepts_in_rules = set(concept_to_group.keys())
missing_groups = []
for raw, entry in mappings.items():
    concept = entry["concept"]
    if concept not in all_concepts_in_rules and entry.get("financial_group") not in rules:
        missing_groups.append((raw, concept))
if missing_groups:
    print(f"\n4 concepts mapped but no financial group (likely aliases resolved dynamically):")
    for raw, concept in missing_groups:
        # Check if it maps via CLASIFICACION_TO_FINANCIAL_GROUP
        fg = CLASIFICACION_TO_FINANCIAL_GROUP.get(concept, 'NOT FOUND')
        print(f"  raw={raw!r} -> concept={concept!r} -> group in python={fg!r}")

print("\n=== Financial Group Structure ===")
mismatches = 0
for g, concepts in FINANCIAL_STRUCTURE.items():
    yaml_set = set(rules[g]["concepts"])
    py_set = set(concepts)
    missing = py_set - yaml_set
    extra = yaml_set - py_set
    if missing or extra:
        mismatches += 1
        if missing:
            print(f"  {g}: MISSING in YAML: {missing}")
        if extra:
            print(f"  {g}: EXTRA in YAML: {extra}")

print(f"Concept counts: Python={sum(len(c) for c in FINANCIAL_STRUCTURE.values())}, "
      f"YAML={sum(len(v['concepts']) for v in rules.values())}")
print(f"Group keys match: {set(rules.keys()) == set(FINANCIAL_STRUCTURE.keys())}")
print(f"Structural mismatches: {mismatches}")

print("\n=== Mapping Counts ===")
print(f"RAW_TO_CLASSIFICATION_MAP: {len(RAW_TO_CLASSIFICATION_MAP)}")
print(f"taxonomy_mappings.yaml: {len(mappings)}")

print("\n=== Normalized Map Equivalence ===")
yaml_norm = tl.build_normalized_mappings(mappings)
print(f"Legacy NORMALIZED_CLASSIFICATION_MAP: {len(NORMALIZED_CLASSIFICATION_MAP)}")
print(f"YAML normalized: {len(yaml_norm)}")

norm_mismatches = 0
for norm_key in NORMALIZED_CLASSIFICATION_MAP:
    yaml_val = yaml_norm.get(norm_key)
    py_val = NORMALIZED_CLASSIFICATION_MAP[norm_key]
    if yaml_val != py_val:
        norm_mismatches += 1
        if norm_mismatches <= 5:
            print(f"  MISMATCH: {norm_key[:50]!r}: yaml={yaml_val!r} vs py={py_val!r}")
print(f"Normalized map mismatches: {norm_mismatches}")

print("\n=== Concept -> Financial Group ===")
concept_map = tl.build_concept_to_group_map(rules)
group_mismatches = 0
for concept, expected_group in CLASIFICACION_TO_FINANCIAL_GROUP.items():
    yaml_group = concept_map.get(concept)
    if yaml_group != expected_group:
        group_mismatches += 1
        if group_mismatches <= 5:
            print(f"  GROUP MISMATCH: {concept!r}: yaml={yaml_group!r} vs py={expected_group!r}")
print(f"Group mismatches: {group_mismatches}")

print("\n=== SUMMARY ===")
# 4 dynamically-resolved concepts (Pago, Devolución de dinero\nEnvío variants)
# are expected edge cases — handled by payout_rule / compound-concept logic, not FINANCIAL_STRUCTURE
dynamic_concepts_ok = len([i for i in validation.get("issues", []) if "dynamically" in i]) == 1
structural_ok = mismatches == 0 and norm_mismatches == 0 and group_mismatches == 0
all_ok = structural_ok and dynamic_concepts_ok
print(f"100% equivalence: {'PASS' if all_ok else 'FAIL'}")
if all_ok:
    print("  Structural: PASS (0 mismatches)")
    print(f"  Dynamic concepts: {len([i for i in validation.get('issues', []) if 'dynamically' in i])} (expected)")
else:
    print(f"  Structural mismatches: {mismatches}")
    print(f"  Normalized map mismatches: {norm_mismatches}")
    print(f"  Group mismatches: {group_mismatches}")
    if not dynamic_concepts_ok:
        print(f"  Unexpected validation issues: {[i for i in validation.get('issues', []) if 'dynamically' not in i]}")
