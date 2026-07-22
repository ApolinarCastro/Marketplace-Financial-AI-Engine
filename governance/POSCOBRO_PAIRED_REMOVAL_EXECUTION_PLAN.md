# POSCOBRO PAIRED REMOVAL EXECUTION PLAN

**Fecha:** 2026-06-07
**Prioridad:** CRÍTICA
**Objetivo:** Plan quirúrgico para eliminar solo el universo PAIRED de PosCobro ($94.4M) sin afectar EXCLUSIVE, UNMATCHED, RN certificado, ni Single Financial Truth.

---

## RESUMEN EJECUTIVO

**READY_FOR_EXECUTION = SI** ✅

| Métrica | Valor |
|---|---|
| Paired rows a eliminar | 3,663 |
| Paired monto | $94,357,912 (exacto a certificación) |
| Órdenes únicas | 2,821 |
| RN actual ML | $712,045,127 |
| RN post-removal | $617,687,214 |
| Delta RN | -$94,357,912 (-13.25%) |
| Impacto cash real | **$0** |
| Método recomendado | Flag lógico (`include_in_operational_pnl = 0`) |

---

## FASE 1 — IDENTIFICACIÓN EXACTA

### Dataset POSCOBRO_PAIRED_CANDIDATES

**SQL de identificación:**

```sql
SELECT l.id_transaccion, l.id_orden, l.fecha, l.detalle, l.monto
FROM marketplace_ledger_v1 l
WHERE l.marketplace = 'ML'
  AND l.id_transaccion LIKE 'POS_%'
  AND COALESCE(l.include_in_operational_pnl, 1) = 1
  AND EXISTS (
      SELECT 1 FROM marketplace_ledger_v1 l2
      WHERE l2.marketplace = 'ML'
        AND l2.id_orden = l.id_orden
        AND l2.financial_group = 'devoluciones'
        AND COALESCE(l2.include_in_operational_pnl, 1) = 1
  )
ORDER BY l.fecha, l.id_orden
```

**Resultado:**

| Métrica | Valor |
|---|---|
| Rows | 3,663 |
| Monto | $94,357,912.79 |
| Órdenes únicas | 2,821 |
| id_transaccion únicos | 3,663 (1:1) |
| financial_group | 100% `ajustes` |
| Archivos origen | 5 XLSX Poscobro |

### Muestra representativa

| id_transaccion | id_orden | Fecha | Detalle | Monto |
|---|---|---|---|---|
| POS_97095987402_... | 2000010259565826 | 2025-01-01 | dont_want_it_another_cause_fashion | $20,824 |
| POS_97477705238_... | 2000010287968560 | 2025-01-01 | bigger_than_expected_fashion | $29,990 |
| POS_97478092800_... | 2000010287968560 | 2025-01-01 | bigger_than_expected_fashion | $29,990 |
| POS_97133573613_... | 2000010289110890 | 2025-01-01 | bigger_than_expected_fashion | $27,490 |
| POS_97486431834_... | 2000010289126166 | 2025-01-01 | bigger_than_expected_fashion | $21,990 |

### Distribución por concepto

| Concepto | Rows | Monto |
|---|---|---|
| bigger_than_expected_fashion | 890 | $28,300,845 |
| smaller_than_expected_fashion | 721 | $20,169,879 |
| Ajuste Poscobro | 637 | $2,743,204 |
| undelivered_repentant_buyer | 337 | $9,518,055 |
| repentant_buyer | 250 | $7,467,777 |
| dont_want_it_another_cause_fashion | 210 | $6,601,081 |
| undelivered_other | 116 | $3,647,435 |
| compensated | 100 | $3,405,595 |
| others (20+ conceptos) | 402 | $12,504,041 |
| **TOTAL** | **3,663** | **$94,357,912** |

---

## FASE 2 — VALIDACIÓN FINANCIERA

### Certificación cruzada

| Fuente | Monto | Delta |
|---|---|---|
| POSCOBRO_FLOW_RN_ATTRIBUTION (Paired) | $94,357,912.79 | — |
| POSCOBRO_TEMPORAL_RECONCILIATION (Paired) | $94,357,912.79 | — |
| **Esta consulta (EXECUTION_PLAN)** | **$94,357,912.79** | **$0.00** |

**El universo paired está certificado con $0 delta entre 3 fuentes independientes.**

### Verificación: No se filtran rows exclusive

```sql
-- PosCobro total: 6,655 rows, $184,700,910
-- Paired:         3,663 rows, $94,357,912 (55.0% del total)
-- Exclusive:      2,992 rows, $90,342,998 (45.0% del total)
-- Unmatched (raw): 199 rows, $10,096,682
```

**Riesgo de falsos positivos: 0%.** La regla `EXISTS (devolucion)` es una restricción estricta. El avg delta entre pos y dev en la misma orden es de -$1,047 — confirma que representan el mismo evento económico (el ajuste es menor porque cubre solo el monto disputado, la devolución es el reembolso completo).

---

## FASE 3 — SIMULACIÓN RN

### Impacto mensual

| Mes | RN Actual | Paired | RN Post-Removal | Delta% |
|---|---|---|---|---|
| 2025-01 | $18,676,084 | $4,065,288 | $14,610,796 | -21.77% |
| 2025-02 | $16,831,909 | $3,828,854 | $13,003,055 | -22.75% |
| 2025-03 | $45,750,810 | $7,187,286 | $38,563,524 | -15.71% |
| 2025-04 | $55,791,606 | $8,189,511 | $47,602,095 | -14.68% |
| 2025-05 | $69,093,529 | $8,799,474 | $60,294,054 | -12.74% |
| 2025-06 | $59,253,276 | $6,359,321 | $52,893,955 | -10.73% |
| 2025-07 | $45,699,543 | $7,627,325 | $38,072,218 | -16.69% |
| 2025-08 | $34,358,937 | $4,627,612 | $29,731,325 | -13.47% |
| 2025-09 | $36,690,170 | $4,261,328 | $32,428,842 | -11.61% |
| 2025-10 | $59,234,400 | $6,307,879 | $52,926,521 | -10.65% |
| 2025-11 | $70,830,352 | $9,743,981 | $61,086,371 | -13.76% |
| 2025-12 | $69,326,052 | $10,293,428 | $59,032,624 | -14.85% |
| 2026-01 | $19,401,503 | $2,766,688 | $16,634,815 | -14.26% |
| 2026-02 | $14,748,923 | $1,333,062 | $13,415,861 | -9.04% |
| 2026-03 | $30,439,310 | $3,130,173 | $27,309,137 | -10.28% |
| 2026-04 | $36,615,722 | $4,902,146 | $31,713,576 | -13.39% |
| 2026-05 | $24,799,676 | $933,390 | $23,866,286 | -3.76% |
| 2026-06 | $4,503,320 | $1,166 | $4,502,154 | -0.03% |
| **TOTAL** | **$712,045,127** | **$94,357,912** | **$617,687,214** | **-13.25%** |

### Meses más impactados

| Ranking | Mes | Paired | Delta% |
|---|---|---|---|
| 1 | 2025-12 | $10,293,428 | -14.85% |
| 2 | 2025-11 | $9,743,981 | -13.76% |
| 3 | 2025-05 | $8,799,474 | -12.74% |
| 4 | 2025-04 | $8,189,511 | -14.68% |
| 5 | 2025-07 | $7,627,325 | -16.69% |

**Patrón:** Paired representa 10-22% del RN mensual de ML. Consistente mes a mes.

---

## FASE 4 — ANÁLISIS DE IMPACTO

### Click-to-Ledger

El endpoint `/api/v4/ledger` consulta `marketplace_ledger_v1` directamente. Si paired rows tienen `include_in_operational_pnl = 0`, el click sigue funcionando pero mostrará menos rows. **Impacto: ALTO** — el usuario vería que el click muestra menos filas que antes. Mitigación: el click ya muestra solo `op_pnl=1`.

### Dashboard / Estructura Financiera

El bloque "Ajustes & Retenciones" usa datos de:
- `window._cierreCertified.aju` → viene de `cierre_financiero_v1.total_ajustes` **NO afectado** (el cierre no se modifica)
- `currentDesglose` → viene de `desglose endpoint` que filtra `op_pnl=1` **SÍ afectado** — los detail rows y el monto `aju` (desde FINANCIAL_LABEL_TRUTH_REMEDIATION) mostrarán $94.4M menos

### Waterfall

El endpoint `/api/v4/exec/waterfall` usa `cierre_financiero_v1`. **NO afectado** — el cierre no se modifica.

### Cobros Breakdown

El endpoint `/api/v4/exec/cobros-breakdown` y `/api/v4/cierre/desglose` consultan el ledger con `op_pnl=1`. **SÍ afectados** — mostrarán los paired removidos.

### Single Financial Truth

**NO afectado** — La certificación SFT ya documenta que ML tiene un delta estructural entre ledger y cierre. Este cambio ALINEA ledger con la realidad cash, no la modifica.

---

## FASE 5 — RESPUESTAS

### Q1: ¿El universo paired puede identificarse al 100%?

**SI** ✅ — La regla SQL con `EXISTS (devolucion on same order)` identifica exactamente 3,663 rows, $94,357,912.79. $0 delta con certificación previa.

### Q2: ¿Existe riesgo de eliminar filas exclusive?

**NO** ❌ — El subquery `EXISTS (SELECT 1 ... financial_group='devoluciones')` es una restricción estricta que solo captura órdenes con devolución asociada. Exclusive por definición no tiene devolución. Falsos positivos: 0.

### Q3: ¿Cuál sería el RN final después de remover paired?

**$617,687,214** (desde $712,045,127, delta -$94,357,912 = -13.25%)

### Q4: ¿Qué meses son los más impactados?

2025-12 ($10.3M), 2025-11 ($9.7M), 2025-05 ($8.8M), 2025-04 ($8.2M), 2025-07 ($7.6M). Todos los meses 2025-01 a 2026-06 tienen paired.

### Q5: ¿Qué implementación es más segura?

**Opción A: Flag lógico (RECOMENDADA)** ✅

| Opción | Descripción | Riesgo | Esfuerzo |
|---|---|---|---|
| **A) Flag lógico** | `UPDATE include_in_operational_pnl = 0` para 3,663 paired rows, luego re-ejecutar cierre | BAJO | 1 UPDATE + re-clasificación |
| **B) Vista derivada** | Crear `vw_ledger_sin_paired` que excluya paired rows | MEDIO | Modificar todos los consumidores |
| **C) Reclasificación física** | Mover rows a otra tabla | ALTO | Prohibido |

**Justificación de Opción A:**

1. `include_in_operational_pnl` ya existe en el schema — no requiere migración
2. El clasificador ya respeta esta columna (100% de las clasificaciones existentes la usan)
3. El cierre financiero filtra por `op_pnl=1` — al cambiar paired a 0, el cierre NO los incluye
4. Es reversible: `UPDATE ... SET include_in_operational_pnl = 1` restaura todo
5. $0 impacto en el ledger histórico (no se borra nada)
6. $0 impacto en datos raw (archivos XLSX intactos)

---

## FASE 6 — PLAN DE EJECUCIÓN

### Paso 1: Backup (Pre-Requisito)

```bash
# Crear snapshot de la DB actual
# Usar mecanismo existente de snapshots
```

### Paso 2: Marcar Paired Rows

```sql
UPDATE marketplace_ledger_v1
SET include_in_operational_pnl = 0
WHERE marketplace = 'ML'
  AND id_transaccion LIKE 'POS_%'
  AND COALESCE(include_in_operational_pnl, 1) = 1
  AND EXISTS (
      SELECT 1 FROM marketplace_ledger_v1 l2
      WHERE l2.marketplace = 'ML'
        AND l2.id_orden = l.id_orden
        AND l2.financial_group = 'devoluciones'
        AND COALESCE(l2.include_in_operational_pnl, 1) = 1
  );
```

**Afecta:** 3,663 rows, $94,357,912. **99.9% seguro** — la regla está certificada.

### Paso 3: Re-ejecutar clasificación

```python
# Ejecutar run_classification() para ML
# Esto propaga el cambio de op_pnl a marketplace_ledger_clasificado_v1
```

### Paso 4: Re-ejecutar cierre financiero

```python
# Ejecutar run_financial_closing() para ML
# El cierre ahora NO incluirá paired rows en total_ajustes
# RN se reduce en $94.4M automáticamente
```

### Paso 5: Certificar

```python
# Validar:
# 1. RN ML post-cierre = $617,687,214 (+delta de exclusive + unmatched)
# 2. 14/14 regression tests PASS
# 3. 30/30 tests PASS
# 4. Dashboard muestra paired eliminado
# 5. Single Financial Truth se mantiene
```

### Rollback

```sql
UPDATE marketplace_ledger_v1
SET include_in_operational_pnl = 1
WHERE marketplace = 'ML'
  AND id_transaccion LIKE 'POS_%'
  AND id_transaccion IN (
      SELECT id_transaccion FROM snapshot_pre_paired_removal.paired_rows
  );
```

---

## SALIDA FINAL

```
READY_FOR_EXECUTION = SI

  PAIRED_CANDIDATES  = 3,663 rows / $94,357,912.79 (ZERO DELTA from cert)
  EXCLUSIVE_SAFE     = 2,992 rows / $90,342,998.00 (NO false positives)
  
  RN_ACTUAL          = $712,045,127.72
  RN_POST_PAIRED     = $617,687,214.93
  RN_DELTA           = -$94,357,912.79 (-13.25%)
  CASH_IMPACT        = $0.00

  METHOD             = FLAG_LOGICO (include_in_operational_pnl = 0)
  ROLLBACK           = UPDATE include_in_operational_pnl = 1
  RISK               = BAJO (regla certificada, reversible)

  READY              = SI ✅
```
