# PRODUCTION DECISION

**Date:** 2026-06-06

---

1. **¿Qué debe corregirse?** — Agregar `AND include_in_operational_pnl = TRUE` a la query SQL de `run_financial_closing()` en `marketplace_auditor.py:519-528`. Esto excluye los mecanismos apareados (BPP, Poscobro Conciliado, Poscobro General) del cálculo de RN.

2. **¿Dónde debe corregirse?** — Únicamente en `engine/v4/marketplace_auditor.py`, método `run_financial_closing()`, línea 527, en la cláusula WHERE de la query de cierre financiero.

3. **¿Qué NO debe tocarse?** — No modificar `run_classification()`, no modificar `include_in_operational_pnl`, no modificar `FINANCIAL_STRUCTURE`, no modificar `RAW_TO_CLASSIFICATION_MAP`, no modificar loaders, no modificar DB, no modificar API, no modificar dashboard.

4. **¿Cuál es el riesgo de corregir?** — Bajo. El flag `include_in_operational_pnl` ya está correctamente asignado para ~8,426 filas ML. El riesgo es excluir conceptos operacionales legítimos si algún concepto incorrectamente tiene flag = FALSE. Verificar post-fix que PARIS, RIPLEY, FALABELLA no pierdan filas operacionales (0 mechanisms en esos MPs → 0 impacto).

5. **¿Cuál es el riesgo de NO corregir?** — $35.8M (4.59%) de sobreestimación de RN continúa. Material para auditoría financiera. Riesgo de inexactitud en reportes gerenciales y toma de decisiones.
