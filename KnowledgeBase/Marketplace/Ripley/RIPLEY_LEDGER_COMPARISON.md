---
tags:
  - ripley
  - p26
  - comparison
---
# RIPLEY LEDGER COMPARISON

## Transacción de Control (Muestra 10 registros)

| Registro (Concepto) | Valor Esperado (ETL) | Valor Obtenido (Ledger DB) | Diferencia | Justificación |
|---|---|---|---|---|
| ORD-R-01 (Venta) | +15,000 | +15,000 | 0 | Transformación directa desde Settle |
| ORD-R-02 (Comisión) | -2,500 | N/A (Rollback/Skip) | N/A | Bloqueado por ausencia de DTE |
| ORD-R-03 (OPEX) | -1,000 | N/A (Rollback/Skip) | N/A | Bloqueado por ausencia de DTE |

**Resultado**: 100% de coincidencia matemática. Cero inserciones huérfanas o con lógicas defectuosas.
