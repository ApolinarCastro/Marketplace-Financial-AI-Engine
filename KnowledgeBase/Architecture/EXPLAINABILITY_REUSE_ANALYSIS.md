---
tags:
  - reuse_analysis
  - explainability
  - p26
status: active
---

# EXPLAINABILITY REUSE ANALYSIS

## ¿Puede construirse la explicación reutilizando endpoints y motores existentes?
**Sí.** Queda absolutamente prohibido crear un endpoint nuevo (GET /api/v4/explain/{tx_id}).

## Componentes Reutilizables a Extender
1. **Drawer Endpoint**: GET /api/v4/electronic_certification/status/{transaction_id} ya orquesta la recolección del certificado electrónico, la evidencia y los datos base de la transacción.
2. **Evidence Engine**: Ya entrega el evidence_level, confidence_score y el hash.
3. **Marketplace Intelligence**: Podemos leer dinámicamente KnowledgeBase/Marketplace/Taxonomy/ml_v1.json para extraer la regla tributaria exacta o regla operativa aplicada.
4. **Knowledge Objects**: Se mapeará en el resultado el enlace directo al DEC correspondiente (ej. DEC-019_POSCOBRO).

## Formato Estricto (Data, no texto libre)
La extensión del payload del Drawer incluirá un nodo estructurado:
`json
"explainability": {
    "que_ocurrio": "[Mapeado de Ledger V4 transaction_type]",
    "por_que_ocurrio": "[Mapeado de rule_description en Taxonomía JSON]",
    "evidencia_hash": "[Reutilizado de Evidence Engine]",
    "regla_aplicada": "[Taxonomy Rule ID]",
    "dec_interviniente": "[Taxonomy DEC link]",
    "accion_requerida": "[Mapeado de Executive / Document Gap]"
}
`

**Conclusión**: La explicabilidad será una extensión del Drawer (ElectronicCertificationEngine), consumiendo el Knowledge Graph y el Marketplace Ledger.
