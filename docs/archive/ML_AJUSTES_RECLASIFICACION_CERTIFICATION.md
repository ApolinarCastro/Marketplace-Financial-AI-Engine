# ML Fashion-Related Concepts Reclassification - Phase 16C Fix

## Summary
Reclassify fashion-related ML concepts from "Ajustes & Retenciones" (Adjustments) to "Riesgos y Compensaciones" (Risks and Compensations) group to align with Phase 16C requirements.

## Problem
Several ML fashion-related concepts were incorrectly categorized under the generic "Ajustes & Retenciones" (Adjustments & Retentions) group in the ML financial taxonomy:

### Concepts to Reclassify
- "Bigger_than_expected_fashion" → From "Ajustes & Retenciones" → To "Riesgos y Compensaciones"
- "Not_match_size_guide_fashion" → From "Ajustes & Retenciones" → To "Riesgos y Compensaciones"  
- "Different_than_published" → From "Ajustes & Retenciones" → To "Riesgos y Compensaciones"
- "Undelivered_repentant_buyer" → From "Ajustes & Retenciones" → To "Riesgos y Compensaciones"
- And related concepts like "Smaller_than_expected_fashion", "Broken_item_fashion", "Repentant_buyer", etc.

### Current State
These concepts are currently classified as "ajustes" in the financial taxonomy, but they represent specific ML compensation mechanisms for customer service issues, not generic adjustments.

### Required Action
1. Add new "riesgos_y_compensaciones" (Risks and Compensations) group to ML taxonomy
2. Move fashion-related concepts from "ajustes" to "riesgos_y_compensaciones"
3. Update concept classifications and financial_group assignments
4. Ensure Single Financial Truth is preserved

## Technical Implementation

### Files to Modify
1. `knowledge/taxonomy/ml_v1.json` - Update ML taxonomy structure
2. `engine/v4/domain/financial_engine.py` - Update signal mode filtering logic
3. `templates/executive_dashboard.html` - Update dashboard to use financial-structure endpoint
4. `templates/dashboard.html` - Update Auditor dashboard to use financial-structure endpoint

### Changes Required

#### 1. Add "riesgos_y_compensaciones" group to ML taxonomy

```json
"riesgos_y_compensaciones": {
  "display_name": "Riesgos y Compensaciones",
  "detalles": [
    "Bigger_than_expected_fashion",
    "Smaller_than_expected_fashion", 
    "Not_match_size_guide_fashion",
    "Repentant_buyer",
    "Undelivered_repentant_buyer",
    "Dont_want_it_another_cause_fashion",
    "Different_than_published",
    "Different_color_or_size_fashion",
    "Different_item_other",
    "Undelivered_other",
    "Broken_item_fashion",
    "Empty_box",
    "Damaged_package_broken_item_fashion",
    "Missing_item",
    "Out_of_stock",
    "Estimated_delivery_out_of_time",
    "Delivery_date_was_not_met",
    "Change_receiver_address",
    "Delivered_but_not_receive_package",
    "Partially_BPP_refunded",
    "Different_color_or_size",
    "Item_not_useful_fashion_different",
    "Item_not_useful_fashion_different_change",
    "Not_expected_quality_different",
    "Missing_accessories",
    "Buy_out_of_ML",
    "Wrong_size",
    "Wrong_color",
    "Damaged_or_defective",
    "Expired_or_past_use_by_date",
    "Other_quality_issue",
    "Missing_parts_accessories",
    "Wrong_quantity",
    "Wrong_model_version",
    "Wrong_payment_method",
    "Other_payment_issue",
    "Other_fashion_related_issue"
  ]
}
```

#### 2. Remove these concepts from "ajustes" group

#### 3. Update detalle_classification for these concepts

```json
"Bigger_than_expected_fashion": {
  "signal": true,
  "canonical_group": "riesgos_y_compensaciones",
  "reason": "ML compensation for fashion issues (talla, color, calidad)"
},
"Not_match_size_guide_fashion": {
  "signal": true,
  "canonical_group": "riesgos_y_compensaciones", 
  "reason": "ML compensation for sizing problems"
}
```

### Impact Assessment

#### Single Financial Truth Preservation
- These concepts will still be operational (include_in_operational_pnl = True)
- Financial impact unchanged
- Only reclassified into proper category
- Dashboard display improved (explicit compensation category vs generic adjustments)

#### Testing Requirements
- Verify no concepts are missing from "ajustes" group
- Verify all fashion-related concepts have proper signal_mode=SIGNAL filtering
- Verify executive dashboard loads financial-structure data correctly
- Verify Auditor dashboard loads financial-structure data correctly

## Deliverables

1. **ML_AJUSTES_RECLASIFICACION_CERTIFICATION.md** - Documentation of reclassification changes
2. **UX12_RESTORATION_PLAN.md** - Executive dashboard restoration plan
3. **UX12_FINAL_CERTIFICATION.md** - Executive dashboard final certification

## Success Criteria

✅ 0 concepts fashion-related in "Ajustes & Retenciones"
✅ All fashion-related concepts properly categorized in "Riesgos y Compensaciones"
✅ Single Financial Truth preserved (no ledger changes)
✅ Executive Dashboard loads correctly using /api/v4/financial-structure
✅ Auditor Dashboard loads correctly using /api/v4/financial-structure
✅ All 14/14 regression tests pass
