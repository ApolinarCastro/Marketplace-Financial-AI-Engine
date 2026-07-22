# Certificación: Audit Button Safe Mode
**Fecha:** 2026-06-07
**Status:** PASS ✅

---

## Problema resuelto

El botón "Ejecutar Auditoría" (`POST /api/v4/run-audit`) ejecutaba:
1. `run_classification()` — DELETE + re-clasifica TODAS las rows → **deshace DEC-019**
2. `run_financial_closing()` x48 — regenera cierres 2023-2026
3. `run_audit()` — regenera alertas

Esto hacía que DEC-019 fuera incompatible con la auditoría de UI.

## Solución implementada

El endpoint `POST /api/v4/run-audit` ahora ejecuta **SOLO** `run_audit()`:

```
Antes:  classification() → financial_closing() x48 → audit()
Después: audit()  (solo)
```

- NO `run_classification()` → preserve DEC-019
- NO `run_financial_closing()` → preserve cierres certificados

## Verificación post-cambio

| Aspecto | Antes | Después | Verificacion |
|---|---|---|---|
| ML op_pnl=0 (ledger) | 4,729 rows | 4,729 rows | ✅ DEC-019 intacto |
| ML op_pnl=0 (clasificado) | 4,729 rows | 4,729 rows | ✅ DEC-019 intacto |
| Auditoria rows | 22,401 | 22,401 | ✅ Alertas regeneradas |
| Cierre RN total | $1,419,955,156.65 | $1,419,955,156.65 | ✅ Sin cambios |
| 30/30 tests | PASS | PASS | ✅ |

### Tiempo de ejecución

| Modo | Tiempo | Diferencia |
|---|---|---|
| Antes (full: class + closing + audit) | ~35-45s | Incluía overhead destructivo |
| Ahora (solo audit) | ~7.33s | 5-6x más rápido, sin daños |

## Alertas generadas (22,401)

| Check | FALABELLA | PARIS | RIPLEY | ML | Total |
|---|---|---|---|---|---|
| cargo_sin_respaldo_legal | 553 | 10,177 | 11,670 | 0 | 22,400 |
| movimientos_no_clasificados | 1 | 0 | 0 | 0 | 1 |
| **Total** | **554** | **10,177** | **11,670** | **0** | **22,401** |

## Seguridad

- Classification re-run nunca se llama → DEC-019 inviolable
- Closing nunca se llama → cierres certificados inviolables
- Snapshot pre-ejecución: `data/db/snapshot_pre_dec019_20260607_161324/` (SHA256 012cd0fe)

## Entregable

- `api/api.py` — endpoint `POST /api/v4/run-audit` modificado (solo `run_audit()`)
- `governance/AUDIT_BUTTON_SAFE_MODE_CERTIFICATION.md`
