# Paris Revenue Certification V2

## Objetivo de Validación
Evitar la reintroducción de la regresión visual y financiera que provoca que la Venta Bruta asuma el valor neto (monto a pagar) y la comisión operativa se muestre en $0.

## Verificación Continua Requerida
1. `gross` = monto_transaccion bruto sin descontar comisión.
2. `commission` = costo_separado (diferencia entre bruto y neto en el reporte de liquidación).
3. `available` = neto (lo que Paris finalmente transfiere).
4. La integridad del Pipeline (`Dashboard UI == Auditor Stats == Ledger`).

## Conclusión del RCA
Cualquier alteración al `load_paris` en `surgical_loader.py` que mezcle las columnas `monto` y `monto a pagar` corrompe las métricas operacionales. La corrección se auditará antes del lanzamiento definitivo de la Fase 16.
