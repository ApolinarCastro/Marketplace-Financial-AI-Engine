# POST-DEC-019 Stabilization
**Fecha:** 2026-06-07
**Meta:** Corregir los 3 hallazgos abiertos post DEC-019 sin alterar la verdad financiera certificada.

---

## Resumen de cambios

| Archivo | Cambio | Riesgo |
|---|---|---|
| `api/api.py:573-638` | Waterfall endpoint: unified operational query (op_pnl=1) | Bajo — solo SELECT |
| `api/api.py:769-799` | Audit endpoint: solo `run_audit()`, sin classification/closing | Bajo — código muerto removido |
| `templates/dashboard.html:728` | `aju` desde `window._cierreCertified.aju` (waterfall operacional) | Bajo — misma fuente que otros KPIs |
| `templates/dashboard.html:868` | Desglose siempre `exclude_non_operational=true` (incl. ML) | Bajo — filtro adicional solo |

---

## FASE 1 — RN Operacional

**Antes:**
- RN visible = `cierre_financiero_v1.resultado_neto` (ALL-rows, incluye paired PosCobro)
- Waterfall: universo mixto (ing/cop/ccm/aju desde cierre ALL-rows, dev desde ledger op_pnl=1)
- Dashboard aju desde `currentDesglose` (ALL-rows para ML)

**Después:**
- Waterfall: query unificado desde `marketplace_ledger_v1` con `COALESCE(include_in_operational_pnl,1)=1`
- Dashboard aju desde waterfall (misma fuente, mismo filtro)
- Desglose siempre filtrado por op_pnl=1 (todos los MPs)

**Resultado: RN operacional = Ing + Dev + Cop + Ccm + Aju (op_pnl=1)**

| ML 2026-01 | Valor |
|---|---|
| RN Operacional | $19,487,868.00 |
| RN Full (cierre) | $24,101,867.50 |
| Delta (paired PosCobro) | $4,613,999.50 |

**Veredicto: PASS** ✅ — Delta esperado = DEC-019 rows excluidas.

---

## FASE 2 — Ajustes & Retenciones (Sign Analysis)

### Data (ML, ALL ajustes rows):

| Distribución | Rows | Total | Significado |
|---|---|---|---|
| POSITIVE | 11,384 | $327,166,567.93 | Ingreso para ML |
| NEGATIVE | 85 | -$405,701.00 | Costo para ML |
| **Net** | **11,469** | **$326,760,866.93** | **Neto positivo** |

Único concepto NEGATIVE: "Cargo" (85 rows, -$405,701 = créditos a vendedores).

### Análisis semántico

Los ajustes en el ledger representan **ingreso para ML** (recuperación de vendedores por claims, devoluciones, BPP, etc.). Desde la perspectiva del vendedor, son descuentos/cargos. Pero el dashboard muestra el **P&L de ML**, no del vendedor.

El signo POSITIVO en ajustes es correcto para ML P&L:
- Ingresos (+) = ML recibe dinero
- Devoluciones (-) = ML paga devoluciones
- Costos (-) = ML paga costos
- Ajustes (+) = ML recupera dinero de vendedores

**NO hay inversión de signo.**

### Recomendación: Opción A — Mantener signo actual

| Opción | Descripción | Veredicto |
|---|---|---|
| **A)** Mantener signo actual | Valores positivos = ingreso para ML | ✅ **RECOMENDADO** |
| B) Mostrar como "Descuentos y Retenciones" negativo | Invertir signo visualmente | ❌ Rompe consistencia P&L |
| C) Separar Recuperaciones vs Retenciones | Dividir en dos categorías | ❌ No hay distinción natural (todos son recuperaciones) |

**Razones:**
1. Los ajustes representan INGRESO para ML, no gasto
2. El signo POSITIVO es correcto en el P&L de ML (aumenta RN)
3. Invertir el signo crearía una anomalía: RN ≠ Ing + Dev + Cop + Ccm + Aju
4. La visualización actual es consistente con todas las certificaciones previas

**Mejora sugerida (sin implementar):** Cambiar label "Ajustes & Retenciones" → "Recuperaciones ML" para comunicar que es ingreso para ML.

---

## FASE 3 — Audit Button Safe Mode

**Antes:** `POST /api/v4/run-audit` ejecutaba `run_classification()` → `run_financial_closing()` x48 → `run_audit()`. La classification re-run deshacía DEC-019.

**Después:** Solo ejecuta `run_audit()`. Classification y closing removidos.

| Métrica | Valor |
|---|---|
| Tiempo | 7.33s (vs 35-45s antes) |
| Alertas generadas | 22,401 |
| DEC-019 preservado | ✅ |
| Cierres preservados | ✅ |
| Single Financial Truth | ✅ |

**Veredicto: PASS** ✅

---

## FASE 4 — Regresión

| Suite | Resultado |
|---|---|
| 30/30 tests | **PASS** ✅ |
| Single Financial Truth | **PASS** ✅ ($0 delta) |
| DEC-019 Preserved | **PASS** ✅ (4,729 rows op_pnl=0 intactas) |
| Dashboard Consistency | **PASS** ✅ (aju desde waterfall operacional) |
| Visual = Click | **PASS** ✅ (financial_group='ajustes' unificado) |
| RN = Operacional | **PASS** ✅ ($19.5M operacional vs $24.1M full, delta explicado) |

---

## Output Final

| Indicador | Resultado |
|---|---|
| **RN_OPERATIONAL** | **PASS** ✅ |
| **AUDIT_BUTTON_SAFE_MODE** | **PASS** ✅ |
| **DEC019_PRESERVED** | **PASS** ✅ |
| **SINGLE_FINANCIAL_TRUTH** | **PASS** ✅ |

---

## Entregables

- `governance/POST_DEC019_STABILIZATION.md` (este archivo)
- `governance/RN_OPERATIONAL_CERTIFICATION.md`
- `governance/AUDIT_BUTTON_SAFE_MODE_CERTIFICATION.md`
- `api/api.py` (waterfall unificado + audit seguro)
- `templates/dashboard.html` (aju consistente + desglose operacional para todos)
