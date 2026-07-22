---
tags:
  - certification
  - ko
  - ripley
  - sources
status: draft
---

# KO-RI-SOURCE-0001: Ripley Financial Source Map

## 1. Fuentes Existentes
- **Settlement**: Confirmado y disponible en el Ledger V4. Es la fuente oficial para Ventas y Transferencias (Depósitos Bancarios).

## 2. Fuentes Faltantes
- **Facturación / DTE (XML físicos)**: Requeridos para validar oficialmente Comisiones, OPEX y Otros Cobros tributarios.

## 3. Hipótesis Confirmadas
- El Settlement incluye descuentos totales (Comisiones + OPEX combinados), pero carece del detalle fiscal (folios, IVA, firmas).

## 4. Hipótesis Abiertas (Pendientes de Comprobación)
- *¿Será el DTE la fuente oficial de los montos desglosados de Comisiones y OPEX?* (Actualmente clasificado como LIKELY_SOURCE).
- *¿Cuadrarán centavo a centavo las deducciones del Settlement con la Facturación física?* (Se verificará cuando lleguen los XML).
