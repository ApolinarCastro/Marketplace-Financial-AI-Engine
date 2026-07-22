---
tags:
  - ripley
  - validation
  - p26
---
# RIPLEY MULTI-DOCUMENT VALIDATION

- ¿Puede una orden poseer **múltiples Settlement**? Sí, reliquidaciones.
- ¿Puede poseer **múltiples Facturas**? No, suele consolidarse mensual, pero una orden pertenece a 1 factura.
- ¿Múltiples **DTE**? No, salvo NC (61).
- ¿Múltiples **Notas Crédito**? Sí.
- Relación: Muchas-a-Uno (Órdenes a Factura) o Uno-a-Muchos (Orden a Múltiples NC por reversos parciales).
