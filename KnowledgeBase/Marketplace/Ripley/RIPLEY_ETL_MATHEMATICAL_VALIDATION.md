---
tags:
  - ripley
  - validation
  - p26
---
# RIPLEY ETL MATHEMATICAL VALIDATION

- **Ventas**: Valor origen = monto_venta -> Regla: Passthrough -> Valor destino = monto_venta -> Cuenta: Ingresos por Venta -> P&L: Positivo -> Caja: Positivo.
- **Comisiones**: Valor origen = monto_comision -> Regla: monto * -1 -> Valor destino = Negativo -> Cuenta: Costos Comerciales -> P&L: Negativo -> Caja: Negativo.
- **OPEX**: Valor origen = monto_opex -> Regla: monto * -1 -> Valor destino = Negativo -> Cuenta: Costos Operacionales -> P&L: Negativo -> Caja: Negativo.
- **Promociones (DTE 33)**: Valor origen = monto_promocion -> Regla: Passthrough -> Valor destino = Positivo -> Cuenta: Promociones y Reembolsos -> P&L: Positivo.
- **Notas Crédito (DTE 61)**: Valor origen = monto_reverso -> Regla: Passthrough -> Valor destino = Positivo -> Cuenta: (Disminución de Costo) -> P&L: Positivo.
