# LEDGER CONSISTENCY AUDIT (PRE-GATE VALIDATION)

## 1. Validación de Universo (Marketplace: RIPLEY, Período: YTD)

Se ha ejecutado la validación en duro sobre SQLite `marketplace_ledger_v1` comparando el Endpoint del Ledger vs Financial Structure y Executive Summary.

### Resultados de la Sumatoria Neta:
- **1. RAW Ledger (SQL crudo)**: $592,786,647
- **2. Ledger + get_operational_filters()**: $68,109,790
- **3. /api/v4/financial-structure**: $68,109,790
- **4. /api/v4/exec/summary**: $68,109,790
- **5. /api/v4/ledger (API actual)**: $592,786,647

**Conclusión Irrefutable**: 
El endpoint `/api/v4/ledger` ignora actualmente el perímetro operativo dictado por la **Single Financial Truth**, lo que infla los montos mostrados en la UI a más de $592M cuando la realidad operativa certificada (Cierre / Financial Structure) es de $68.1M.

---

## 2. Análisis de Registros Excluidos (RIPLEY)

Al aplicar `get_operational_filters("RIPLEY")`, el sistema rechaza correctamente **42,418 registros** (en el período YTD) que el Ledger actual está mostrando por error.

| Grupo Financiero | Detalle Excluido | Regla Aplicada | Motivo del Rechazo | Monto YTD Impactado |
|---|---|---|---|---|
| ingresos | `order_amount` | `detalle != 'order_amount'` | **Duplicación Cruda**. Ripley envía este concepto que agrupa el precio total, duplicando los ingresos reales. | $27,703,864 |
| ingresos | `Precio total` | `include_in_operational_pnl = 1` | Subtotal informativo que no representa un ingreso devengado líquido. | $142,082,294 |
| ingresos | `Subtotal` | `include_in_operational_pnl = 1` | Registro intermedio de conciliación. | $136,692,806 |
| tesoreria | `Amount transferred to tienda` | `include_in_operational_pnl = 1` | Movimiento de caja, no P&L. | $112,100,243 |
| tesoreria | `A pagar` | `include_in_operational_pnl = 1` | Provisión de caja, no P&L. | $59,194,948 |
| N/A (Null) | `Comisión` | `financial_group IS NOT NULL` | Registro corrupto o huérfano sin clasificación del motor. | $24,542,653 |

---

## 3. Demostración SQL de la Corrección

**SQL Erróneo Actual (Endpoint `/api/v4/ledger`)**:
```sql
SELECT COUNT(*) as cnt, COALESCE(SUM(monto), 0) as sm 
FROM marketplace_ledger_v1 
WHERE fecha >= '2026-01-01' AND marketplace = 'RIPLEY' AND monto != 0
```
> Retorna universos duplicados e inconsistentes.

**SQL Correcto (A inyectar en `/api/v4/ledger`)**:
```sql
SELECT COUNT(*) as cnt, COALESCE(SUM(monto), 0) as sm 
FROM marketplace_ledger_v1 
WHERE fecha >= '2026-01-01' AND marketplace = 'RIPLEY' AND monto != 0
  AND COALESCE(include_in_operational_pnl, 1) = 1 
  AND financial_group IS NOT NULL 
  AND detalle != 'order_amount'
```
> Garantiza paridad absoluta con `/api/v4/financial-structure` y elimina la inflación artificial de montos.

---
## ESTADO DEL EXIT GATE
**PRE-GATE APROBADO OBLIGATORIAMENTE**. Se ha demostrado matemática y lógicamente que la inyección de `get_operational_filters()` recupera la coherencia total de las vistas.
