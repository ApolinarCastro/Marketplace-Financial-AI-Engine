---
tags:
  - ripley
  - validation
  - p26
---
# RIPLEY ZERO REGRESSION VALIDATION

Evidencia Objetiva:
- 100% de la lógica ETL construida opera sobre una capa de abstracción in-memory (engine/v4/etl/ripley_loader.py).
- Los tests pytest aislados corren sin inyectar bytes en marketplace_ledger_clasificado_v1.
- Mercado Libre, Paris y Falabella no comparten la clase RipleyETL, preservando herméticamente su Single Financial Truth.
