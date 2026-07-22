---
tags:
  - ripley
  - p26
  - promotion
---
# RIPLEY CONTROLLED PROMOTION

## 1. Muestra Representativa (Mocked from Real Patterns)
Se ejecutó un lote controlado usando patrones reales del ledger Ripley (órdenes 2026-X).

- **Venta Simple (Settle_1)**: -> VALIDATED. Inserción monto_venta en entas.
- **Venta con Comisión (Settle_2)**: Settle existe, DTE falta -> BLOCKED_BY_SOURCE_DATA. NO promovido.
- **Venta con OPEX (Settle_3)**: Settle existe, DTE falta -> BLOCKED_BY_SOURCE_DATA. NO promovido.
- **Promoción ECCSA (Factura 33_A)**: Físico ausente -> BLOCKED_BY_SOURCE_DATA.
- **Nota Crédito 61 (NC_61_A)**: Físico ausente -> BLOCKED_BY_SOURCE_DATA.
- **Caso DIFFERENCE_REJECTED**: Prueba en memoria con  de diferencia forzada -> No promovido.
- **Caso MISSING_SETTLEMENT**: Prueba en memoria con DTE sin orden -> No promovido.

## 2. API / Drawer / Executive
Los registros promovidos exitosamente (Ventas puras) fluyen a la API bajo estado_documental="VENTA".
Los bloqueados muestran document_certification.status = "BLOCKED_BY_SOURCE_DATA" en el JSON, visible en el Drawer.
