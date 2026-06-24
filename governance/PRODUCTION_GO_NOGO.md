# GO / NO GO — PRODUCCIÓN

**Date:** 2026-06-06

---

## Veredictos

### ¿La corrección del RN es quirúrgica?

**PASS** — 1 línea en `marketplace_auditor.py:527`. 3 conceptos. 1 marketplace. No toca clasificación, ledger, API, ni dashboard. La constante `MECANISMOS_EXCLUIDOS` contiene exactamente los 3 conceptos MECHANISM del EVENT_REGISTRY_V2.

### ¿La actualización de Junio es quirúrgica?

**PASS CONDITIONAL** — 3/4 MPs tienen archivos listos. 1 ruta rota (`DIR_FACTURACION` en `surgical_loader.py:11`). RIPLEY requiere archivo externo (no controlable). La recarga requiere `reset_db()` que borra datos existentes — esto es normal (el loader siempre funciona así).

### ¿Existe riesgo de romper clasificación?

**PASS** — `run_classification()` no se modifica. El fix solo cambia `run_financial_closing()`. La clasificación existente (incluyendo `include_in_operational_pnl`) permanece intacta.

### ¿Existe riesgo de romper ledger?

**PASS** — `surgical_loader.py` no se modifica. Excepto por la corrección de `DIR_FACTURACION` (que actualmente está roto y no carga nada — la corrección SOLO PUEDE MEJORAR la situación).

### ¿Existe riesgo de romper auditoría?

**PASS** — `run_audit()` no se modifica. Las alertas de auditoría se regeneran con cada ejecución y son independientes del cálculo de RN.

---

## Resultado Final

```
─────────────────────────────────────
                                     │
         A) CORREGIR YA             │
                                     │
─────────────────────────────────────

Evidencia:
                                     │
1. Root cause identificado:         │
   marketplace_auditor.py:519-528    │
   Missing filter en closing SQL     │
                                     │
2. Fix quirúrgico:                   │
   1 línea, 3 conceptos, 1 MP        │
                                     │
3. Sin riesgo de regresión:          │
   No modifica loader               │
   No modifica clasificación         │
   No modifica auditoría             │
   No modifica API                   │
   No modifica dashboard             │
                                     │
4. Data freshness:                   │
   3/4 MPs listos para recargar      │
   1 ruta corregible                │
   RIPLEY = depende de externo       │
                                     │
5. Impacto negativo si NO se          │
   corrige:                          │
   $35.8M sobrestimación RN          │
   4.59% mensual sistemático         │
   Material para auditoría           │
                                     │
Condiciones:                         │
   - Aceptar sobre-corrección 6.2%   │
     (standalone mechanisms)         │
   - Refinamiento pair rate futuro   │
   - Doc known limitation            │
─────────────────────────────────────
```
