# Skills Registry

Este documento registra las skills oficiales mínimas requeridas y validadas para el funcionamiento y auditoría del Marketplace Financial AI Engine.

## Evidence First
**Regla Absoluta:**
> # Sin evidencia
> Sin conclusión

## Skills Mínimas Registradas

1. `financial_root_cause`: Para análisis profundo de la causa raíz de discrepancias o anomalías financieras.
2. `marketplace_reconciliation`: Para tareas de conciliación financiera específicas entre los datos del marketplace y la contabilidad/bancos.
3. `waterfall_validator`: Para validación de los flujos de cascada de pagos y descuentos (gross to net).
4. `financial_invariant_checker`: Para validación constante de invariantes financieros y ecuaciones de equilibrio.
5. `delta_explainer`: Para analizar, desglosar y explicar cualquier delta o diferencia detectada (> 0).
6. `audit_alert_classifier`: Para clasificar y priorizar las alertas de auditoría y determinar si son falsos positivos, bugs o errores reales.
7. `documentary_certification`: Para asegurar la consistencia y presencia de la documentación requerida (XMLs, boletas, notas de crédito).
8. `dte_match_validator`: Para validar el cruce entre los Documentos Tributarios Electrónicos (DTE) y los registros de venta.
9. `tax_consistency_checker`: Para validaciones de consistencia tributaria (IVA, retenciones, etc.).
10. `single_truth_guardian`: Para proteger la integridad de `marketplace_ledger_clasificado_v1` como única fuente de verdad.
11. `regression_detector`: Para análisis de impactos y prevención de regresiones ante nuevos cambios o integraciones.
12. `trust_score_analysis`: Para la métrica de confianza (Trust Score) basada en la consistencia de los datos.
13. `executive_summary_generator`: Para sintetizar hallazgos técnicos en resúmenes ejecutivos accionables.
