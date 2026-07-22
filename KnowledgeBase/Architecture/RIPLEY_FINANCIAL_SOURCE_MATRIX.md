---
tags:
  - ripley
  - financial_source
  - p26
---

# RIPLEY FINANCIAL SOURCE MATRIX

| Concepto | Fuente Primaria (Origen) | Fuente Secundaria | Fuente Validación (Documental) | Nivel de Evidencia | Estado |
|---|---|---|---|---|---|
| Venta | Settlement | Ledger | N/A | ALTO | CONFIRMED_SOURCE |
| Comisión | Facturación (Seller Center) | Settlement | DTE (cuando exista) | MEDIO | LIKELY_SOURCE |
| OPEX | Facturación (Seller Center) | Settlement | DTE (cuando exista) | MEDIO | LIKELY_SOURCE |
| Transferencia | Settlement | Banco | N/A | ALTO | CONFIRMED_SOURCE |
| Otros Cobros | Facturación (Seller Center) | Settlement | DTE (cuando exista) | BAJO | UNKNOWN_SOURCE |

## Notas
- **Separación de responsabilidades**: El Settlement es el *origen financiero* de la liquidación y las ventas, pero el DTE es la *fuente de validación* obligatoria de las comisiones y OPEX.
- No se asumirá como un hecho que las retenciones operativas en el Settlement coincidan exactamente con la facturación tributaria hasta que se disponga de XML reales.
