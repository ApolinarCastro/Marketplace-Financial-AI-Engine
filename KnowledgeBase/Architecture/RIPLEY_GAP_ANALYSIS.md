---
tags:
  - ripley
  - gaps
  - p26
---

# RIPLEY GAP ANALYSIS

## 1. Valores que existen SOLAMENTE en Settlement
- Descuentos operativos (penalidades), fecha exacta de liquidación bancaria, ID de transferencia.

## 2. Valores que existen SOLAMENTE en Facturación (XML)
- Folio DTE fiscal, IVA de las comisiones, Hash del SII, firma digital.

## 3. Valores a Reconstruir
- Las comisiones brutas deben calcularse a partir del XML y cruzarse con los montos netos descontados en el Settlement.
