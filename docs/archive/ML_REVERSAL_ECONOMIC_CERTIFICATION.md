# ML REVERSAL ECONOMIC CERTIFICATION

## 1. Evidencia Económica (Order `2000016232845618`)

Al analizar el ledger inmutable (`marketplace_ledger_v1`) y los movimientos RAW subyacentes, se revela la siguiente traza para una orden afectada:

| Fecha | Detalle | Grupo Financiero | Monto (Signo Ledger) | Interpretación Económica |
| :--- | :--- | :--- | :--- | :--- |
| 2026-05-07 | `reserve_for_dispute` | tesoreria | `-63,391.0` | Congelamiento preventivo de fondos |
| 2026-05-07 | `fee_for_divergence_in_package_dimensions` | costos_operacionales | `+63,391.0` | **Cargo (Débito)** al seller por divergencia |
| 2026-05-14 | `fee_for_divergence_in_package_dimensions_cancel` | costos_operacionales | `+16,599.0` | **Cargo adicional (Débito)** |
| 2026-05-14 | `Mediación` | ajustes | `-79,990.0` | **Reversa (Crédito a favor del seller)** |

*Nota sobre signos: En la taxonomía actual de ML, los montos POSITIVOS en la columna de costos representan débitos/descuentos al seller. Los montos NEGATIVOS representan créditos a favor.*

---

## 2. Respuestas a la Directiva

**¿Deben permanecer en costos_operacionales?**
✅ **SÍ**. Ambos conceptos (`fee...` y `fee..._cancel`) operan matemáticamente como **Cargos (Débitos)**. Suman un total de $79.990 descontados al seller. El sufijo `_cancel` en Mercado Libre no indica la anulación del cobro, sino que etiqueta una variante del cargo (por ejemplo, recargo tras perder o cancelar una revisión).

**¿Debe el concepto `_cancel` migrar a devoluciones?**
✅ **NO**. Migrarlo a devoluciones corrompería la Single Financial Truth, ya que no es un ingreso que retorna al seller, es un cobro. La verdadera "reversa" (el crédito que anula el cobro) se ejecutó bajo el concepto **`Mediación`** por el monto exacto de la suma de ambos cargos (-$79.990).

**¿Debe mostrarse neteado en Executive?**
✅ **SÍ**. La vista ejecutiva (P&L y Análisis de Causa Raíz) debe agrupar los eventos a nivel de `id_orden`. Al hacerlo, revelará que el impacto financiero neto para el seller en esta transacción fue **$0** (Cargos Operacionales por $79.990 anulados por un Ingreso por Mediación de $79.990), lo que indica una disputa ganada o un reclamo exitoso, no una fuga real de capital.

---
> **VEREDICTO AUDITORÍA**: La taxonomía actual que clasifica ambos cargos dimensionales como `costos_operacionales` es estrictamente correcta y representa la verdad económica. Modificarlo rompería el balance contable de la orden frente a la `Mediación`.
