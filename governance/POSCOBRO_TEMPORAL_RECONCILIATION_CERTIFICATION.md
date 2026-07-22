# POSCOBRO_TEMPORAL_RECONCILIATION_CERTIFICATION

**Misión:** POSCOBRO_TEMPORAL_RECONCILIATION_CERTIFICATION
**Prioridad:** CRÍTICA
**Fecha:** 2026-06-07

Se ejecutó un análisis temporal sobre el total de registros de `PosCobro` vigentes en el P&L Operacional (`include_in_operational_pnl = TRUE`, Total: $184.7M). Se cruzaron los `id_orden` con los eventos de `Devoluciones` y `Liberaciones` (Cargo por venta) para determinar los tiempos exactos de compensación.

---

## FASE 3: ATRIBUCIÓN FINANCIERA

| Categoría | Rows | Orders | Monto PosCobro | % del Total |
| :--- | :--- | :--- | :--- | :--- |
| **SAME_MONTH** | 2,344 | 2,344 | $ 76,554,159.00 | 41.45% |
| **NEXT_MONTH** | 476 | 476 | $ 17,305,264.00 | 9.37% |
| **LONG_TAIL** | 1 | 1 | $ 498,489.79 | 0.27% |
| **NEVER_MATCHED** | 2,629 | 2,629 | $ 90,342,998.00 | 48.91% |

*(Nota: La suma de SAME_MONTH + NEXT_MONTH + LONG_TAIL representa la porción de órdenes identificadas con una transacción compensatoria, es decir, el segmento "Paired").*

---

## FASE 4: VALIDACIÓN CASH

Se verificó el "Cash real en Liberaciones" (montos cobrados originalmente de la venta asociada al `id_orden`) para cada categoría:

| Categoría | Monto PosCobro (Ajuste) | Monto Liberado (Cash Real) | Ratio Cash |
| :--- | :--- | :--- | :--- |
| **SAME_MONTH** | $ 76,554,159.00 | $ 70,853,416.00 | 92.55% |
| **NEXT_MONTH** | $ 17,305,264.00 | $ 15,952,843.00 | 92.18% |
| **LONG_TAIL** | $ 498,489.79 | $ 0.00 | 0.00% |
| **NEVER_MATCHED** | $ 90,342,998.00 | $ 71,089,735.00 | 78.68% |

---

## PREGUNTAS OBLIGATORIAS

**1. ¿Cuánto de los $90.7M paired se compensa el mismo mes?**
Exactamente **$ 76,554,159.00** se compensan dentro del mismo período financiero (mismo año y mes).

**2. ¿Cuánto se compensa en meses posteriores?**
Un total de **$ 17,803,753.79** se compensa en meses posteriores.
(Desglose: $ 17,305,264.00 dentro de los 90 días `NEXT_MONTH` + $ 498,489.79 pasando los 90 días `LONG_TAIL`).

**3. ¿Cuánto nunca se compensa?**
Un total de **$ 90,342,998.00** (`NEVER_MATCHED`) no encuentra una devolución compensatoria asociada en el histórico del ledger.

**4. ¿Cuánto cash real existe en cada categoría?**
Detallado en la Fase 4: `SAME_MONTH` posee ~$70.8M; `NEXT_MONTH` ~$15.9M; `NEVER_MATCHED` ~$71.0M. Las categorías de compensación rápida (<= 90 días) tienen una tasa de respaldo de cash (Ratio Cash) altísima superior al 92%.

**5. Si se elimina SOLO SAME_MONTH ¿Cuál sería el impacto RN?**
Eliminar la retención de `SAME_MONTH` aumentaría (recuperaría) el Resultado Neto en **$ 76,554,159.00**.

**6. Si se elimina SAME_MONTH + NEXT_MONTH ¿Cuál sería el impacto RN?**
Eliminar ambos grupos aumentaría (recuperaría) el Resultado Neto en **$ 93,859,423.00**.

---

## SALIDA FINAL

### PAIRED_BREAKDOWN

*   **SAME_MONTH** = $ 76,554,159.00
*   **NEXT_MONTH** = $ 17,305,264.00
*   **LONG_TAIL** = $ 498,489.79
*   **NEVER_MATCHED** = $ 90,342,998.00

### RECOMMENDED_ACTION

**Acción Recomendada:** `ELIMINAR SAME_MONTH + AVALUAR NEXT_MONTH`

**Evidencia Cuantificada:**
1.  **SAME_MONTH ($76.5M)**: Son provisiones que se cancelan / compensan de forma íntegra dentro del mismo período fiscal. Al afectar el mismo P&L donde ocurre la devolución, su inclusión genera ruido artificial y destruye el RN. Es un **candidato fuerte a eliminación inmediata** del P&L Operacional.
2.  **NEXT_MONTH ($17.3M)**: Tienen un comportamiento virtualmente idéntico a `SAME_MONTH` (Ratio Cash >92%), pero cruzan la barrera del mes. Deberían eliminarse si el P&L se mira a trimestre (YTD/QTD), pero requieren un ajuste de provisiones cruzadas mes a mes.
3.  **NEVER_MATCHED ($90.3M) y LONG_TAIL ($0.5M)**: Su eliminación es arriesgada. Al no tener compensación demostrable, si se eliminan, se sobreestimará la ganancia neta. Estas deben preservarse hasta encontrar qué proceso las devengó o por qué no cruzaron.
