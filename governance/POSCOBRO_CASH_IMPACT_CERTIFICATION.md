# POSCOBRO — Cash Impact Certification

**Pregunta única**: ¿PosCobro modifica realmente el dinero final que recibe el seller?

**Fuente de cash**: Liberaciones (18 archivos, 2025-01 a 2026-06)

**Prohibido**: P&L, Ledger, Dashboard, Clasificaciones, reason_detail, status_detail, ROOT_EVENT, MECHANISM, EVENT_ROLE

---

## FASE 1 — Universo PosCobro

| FLOW | Rows | Órdenes | Monto |
|------|------|---------|-------|
| **claim** | 6,158 | 5,325 | $183,063,202 |
| **refund** | 5,749 | 5,370 | $154,945,450 |
| **chargeback** | 7 | 7 | $212,930 |
| **TOTAL** | **11,914** | **6,219** | **$338,221,582** |

6,219 órdenes únicas. 5,325 tienen flow=claim, 5,370 tienen flow=refund, 7 tienen flow=chargeback. Las órdenes pueden tener múltiples FLOWs (dual-flow).

---

## FASE 2 — Trazabilidad a Liberaciones

Método de matching: `ID DE LA ORDEN` (float64) → `np.int64` → `str`

| Métrica | Valor |
|---------|-------|
| Órdenes PosCobro | 6,219 |
| Encontradas en Liberaciones | 5,383 (86.6%) |
| NO en Liberaciones | 836 (13.4%) |
| Monto PosCobro en Lib | $330,483,673 (97.7%) |
| Monto PosCobro NO en Lib | $7,737,909 (2.3%) |

97.7% del monto de PosCobro corresponde a órdenes que existen en Liberaciones. Solo 2.3% no tiene registro de liberación (órdenes sin venta asociada en el período cubierto).

---

## FASE 3+4 — Prueba de Caja y Matriz de Impacto

### claim ($183.1M)

| Concepto | Monto |
|----------|-------|
| PosCobro (órdenes en Liberaciones) | $181,397,454 |
| Liberacion NET de esas mismas órdenes | **$13,054,567** |
| **Cash conversion** | **7.20%** |
| Órdenes sin Liberación | 69 ($1.7M) |

### refund ($154.9M)

| Concepto | Monto |
|----------|-------|
| PosCobro (órdenes en Liberaciones) | $148,873,289 |
| Liberacion NET de esas mismas órdenes | **$71,086** |
| **Cash conversion** | **0.05%** |
| Órdenes sin Liberación | 803 ($6.1M) |

### chargeback ($0.2M)

| Concepto | Monto |
|----------|-------|
| PosCobro (órdenes en Liberaciones) | $212,930 |
| Liberacion NET de esas mismas órdenes | **$118,245** |
| **Cash conversion** | **55.53%** |
| Órdenes sin Liberación | 0 |

### Matriz completa

| FLOW | PosCobro $ | Liberación $ | Delta $ | Conversión |
|------|-----------|-------------|---------|-----------|
| claim | $181,397,454 | $13,054,567 | -$168,342,887 | 7.20% |
| refund | $148,873,289 | $71,086 | -$148,802,203 | 0.05% |
| chargeback | $212,930 | $118,245 | -$94,685 | 55.53% |
| **TOTAL** | **$330,483,673** | **$13,243,898** | **-$317,239,775** | **4.01%** |

---

## FASE 5 — Dictamen

### 1. claim → ¿caja real?

**NO — impacta parcialmente (C).** Solo 7.20% del monto de claim se convierte en cash real en Liberaciones. El 92.8% restante son entradas pareadas (paired mechanisms) que aparecen en P&L pero no modifican el dinero que recibe el seller.

### 2. refund → ¿caja real?

**NO — no impacta caja (B).** Solo 0.05% de conversión. Virtualmente cero. Los refunds en PosCobro son reversiones contables (paired con claims) que no generan movimiento de efectivo. El cash real de la devolución ya se registró en el ciclo de liberación original.

### 3. chargeback → ¿caja real?

**NO — impacta parcialmente (C).** 55.53% de conversión. La muestra es pequeña (7 órdenes, $213K), pero sugiere que chargeback tiene el mayor impacto cash de los tres flows. Sin embargo, incluso aquí, ~44% no se convierte.

### 4. % de conversión total

| Métrica | Valor |
|---------|-------|
| PosCobro total | $338,221,582 |
| Cash real en Liberaciones | $13,441,859 |
| **Conversión global** | **3.97%** |
| **96.03% no impacta cash** | **$324,779,723** |

### 5. Dictamen final

**PosCobro NO modifica materialmente el dinero final que recibe el seller.**

De $338.2M registrados en PosCobro, solo **$13.4M (4.0%)** termina como variación de cash en Liberaciones. El 96% restante es ruido contable — asientos pareados que inflan el P&L pero no tocan el disponible del seller.

La respuesta a la pregunta única:

> **$338,221,582 en PosCobro → genera $13,441,859 reales en Liberaciones**
>
> **= 3.97% de conversión**

| Clasificación | FLOW | Justificación |
|---------------|------|--------------|
| B — No impacta caja | **refund** | 0.05% conversión |
| C — Impacta parcialmente | **claim** | 7.20% conversión |
| C — Impacta parcialmente | **chargeback** | 55.53% conversión (muestra pequeña) |
| **GLOBAL** | **TODOS** | **3.97% — NO impacta caja** |

**PASS.** La respuesta se sostiene exclusivamente en Liberaciones. Sin P&L, sin Ledger, sin Dashboard, sin Clasificaciones.

---

*Fuentes: `01_Raw/ML/Poscobro/` (5 archivos, 11,914 rows), `01_Raw/ML/Liberaciones/` (18 archivos, 2025-01 a 2026-06)*
