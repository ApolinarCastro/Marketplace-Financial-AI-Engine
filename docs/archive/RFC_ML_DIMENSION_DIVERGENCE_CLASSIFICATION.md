# RFC: ML_DIMENSION_DIVERGENCE_CLASSIFICATION

## 1. Contexto y Origen
Se ha detectado mediante auditoría forense que los conceptos crudos:
- `fee_for_divergence_in_package_dimensions`
- `fee_for_divergence_in_package_dimensions_cancel`

Provienen de forma nativa de los archivos de Liquidación y Liberaciones de **Mercado Libre**, específicamente a partir de marzo 2026. Al no estar el concepto `cancel` debidamente mapeado, esto generó fallbacks y clasificaciones parciales (`costos_operacionales` vs `NULL`).

## 2. Naturaleza Económica e Impacto
Ambos conceptos corresponden a la misma naturaleza económica:
- **Cargo / Cancelación de Cargo** aplicado por Mercado Libre cuando las dimensiones reales (peso o volumen) del paquete difieren de las declaradas en la publicación (envíos Fulfillment o Mercado Envíos).
- Es estrictamente un costo operativo vinculado a la logística.
- No hay sangrado o contaminación cross-marketplace, estos strings son exclusivos del ecosistema ML.

## 3. Resolución Propuesta
Para eliminar la existencia de clasificaciones parciales o nulas, y de acuerdo con el principio de **Mismo Concepto = Misma Clasificación**, se propone la siguiente normalización determinística en el motor central (`marketplace_auditor.py`):

1. **Mapeo Limpio (`CLEAN_CONCEPTS_MAP`)**:
   - `"fee_for_divergence_in_package_dimensions": "Cargo por diferencias en las medidas y el peso del paquete"`
   - `"fee_for_divergence_in_package_dimensions_cancel": "Cancelación del cargo por diferencias en las medidas y el peso del paquete"`

2. **Taxonomía Financiera (`FINANCIAL_STRUCTURE`)**:
   Ambos conceptos normalizados se asociarán explícitamente a la clasificación oficial:
   `costos_operacionales`

Esta resolución no requiere crear nuevos grupos, reutiliza la taxonomía existente, y asegura una cobertura del 100% sobre las filas detectadas.
