---
tags:
  - ripley
  - promotions
  - domain_model
  - p26
---

# RIPLEY COMMERCIAL PROMOTIONS MODEL

## 1. Dominio
Este modelo funcional define el flujo de facturación cruzada originado por campañas promocionales, descuentos asimilados y compensaciones comerciales otorgadas por Tarjeta Ripley u otros mecanismos de retención donde la plataforma actúa como recaudador y luego reembolsa al vendedor (seller).

## 2. Actores
- **Empresa**: IMPORTADORA Y COMERCIALIZADORA NANDA SPA (Seller).
- **Marketplace**: COMERCIAL ECCSA S.A. (Ripley).

## 3. Documentos Físicos (Evidencia)
- **Factura Electrónica (Tipo 33)**: Emitida por NANDA SPA hacia ECCSA para cobrar las compensaciones por descuentos de la plataforma.
- **Nota de Crédito (Tipo 61)**: Emitida para reversar, anular o corregir cobros de comisiones, OPEX u otras penalidades previas.

## 4. Conceptos y Clasificación Financiera

| Concepto | Naturaleza Financiera | Financial Group Destino | Evidencia Documental | Fuente Primaria (Origen) | Fuente Validación |
|---|---|---|---|---|---|
| Recuperación Promocional | Recuperación / Ingreso | promociones_y_reembolsos | Factura Tipo 33 | Seller (Facturación propia) | DTE (SII) |
| Descuentos Asumidos Ripley | Compensación | promociones_y_reembolsos | Factura Tipo 33 | Seller (Facturación propia) | DTE (SII) |
| Reversos Comisiones | Reembolso (Costo Negativo)| costos_comerciales | Nota Crédito Tipo 61 | Facturación (Seller Center) | DTE (SII) |
| Reversos OPEX | Reembolso (Gasto Negativo)| costos_operacionales | Nota Crédito Tipo 61 | Facturación (Seller Center) | DTE (SII) |

## 5. Validación Objetiva
- **Recuperación Promocional**: Corresponde estrictamente a un **Ingreso** (cuenta por cobrar del seller hacia Ripley por un descuento asumido por la tarjeta/marketplace).
- **Notas de Crédito**: Corresponden estrictamente a un **Reembolso** o disminución de un costo/gasto previamente reconocido. No son ingresos brutos por venta.
