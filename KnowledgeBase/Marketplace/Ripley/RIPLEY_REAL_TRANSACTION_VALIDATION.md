---
tags:
  - ripley
  - validation
  - p26
---
# RIPLEY REAL TRANSACTION VALIDATION

**Muestra**: Órdenes extraídas del Ledger V4 (Ej: 219,901 registros existentes).

- **Venta**: 100% (Settlement)
- **Factura**: Ausente (0 XML físicos)
- **DTE**: Ausente
- **Resultado ETL Esperado**: Extracción pura del Settle (Ingreso de Ventas, Comisiones descontadas). BLOCKED_BY_SOURCE_DATA en cruce DTE.
- **Resultado Contable Esperado**: Ventas al Haber, Comisiones y OPEX al Debe.
- **Resultado Tributario Esperado**: Ciego (Sin DTE, IVA de comisión es incalculable).
- **Resultado Ledger Esperado**: Inserción de Ventas (Confirmado) + Fallo de cruce documental para OPEX/Comisión hasta la carga de los XML.
