# ML PosCobro Traceability

## Hallazgo Principal
Los conceptos fashion provenientes del Poscobro Técnico en Inglés (ej. `Bigger_than_expected_fashion`, `Repentant_buyer`) están desapareciendo de la capa visual o colapsando bajo "Ajustes & Retenciones".

## Causa Raíz
Aunque la taxonomía `knowledge/taxonomy/ml_v1.json` define explícitamente el bucket canonical `riesgos_y_compensaciones` para estos conceptos de ajustes técnicos, el script del motor `engine/v4/marketplace_auditor.py` ignora el JSON y hardcodea un mapeo manual en `RAW_TO_CLASSIFICATION_MAP` hacia `Ajuste por Talla/Garantía`, ubicando luego este valor directamente en `FINANCIAL_STRUCTURE["ajustes"]`. Esto colapsa toda la estructura impidiendo que el frontend distinga entre Riesgos/Compensaciones y Ajustes tradicionales.

## Plan de Remediación
Refactorizar `engine/v4/marketplace_auditor.py` separando los ajustes operativos (fashion, protección al vendedor) hacia el grupo contable `riesgos_y_compensaciones` para mantener coherencia con `ml_v1.json`.
