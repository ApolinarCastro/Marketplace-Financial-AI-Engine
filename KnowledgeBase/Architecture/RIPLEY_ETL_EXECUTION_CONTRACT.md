---
tags:
  - ripley
  - etl
  - execution_contract
  - p26
---

# RIPLEY ETL EXECUTION CONTRACT

## 1. OBJETIVO
Este documento puente traduce de manera exacta las definiciones establecidas en RIPLEY_ETL_TRANSFORMATION_SPEC.md y RIPLEY_FIELD_MAPPING.md en tareas de implementación técnicas. No se introducen nuevas reglas de negocio.

## 2. IMPLEMENTATION MATRIX

| ID | Nombre | Archivo ETL | Tabla Origen | Campo Origen | Tabla Destino | Campo Destino | Tipo Transformación | Validación | Rollback | Prueba Asociada | KO Asociado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ETL-RI-01 | Ventas a Ledger | engine/v4/etl/ripley_loader.py | aw_ripley_settlement | monto_venta | marketplace_ledger_clasificado_v1 | monto | Numérico Directo | >0, Unique Line | Delete by ID | 	est_ripley_venta_etl.py | KO-RI-ETL-0001 |
| ETL-RI-02 | Comisiones a Ledger | engine/v4/etl/ripley_loader.py | aw_ripley_settlement / aw_ripley_dte | monto_comision | marketplace_ledger_clasificado_v1 | monto | Negativo (monto * -1) | <0, Not Null | Delete by ID | 	est_ripley_comision_etl.py | KO-RI-ETL-0002 |
| ETL-RI-03 | OPEX a Ledger | engine/v4/etl/ripley_loader.py | aw_ripley_settlement / aw_ripley_dte | costo_operacional | marketplace_ledger_clasificado_v1 | monto | Negativo (monto * -1) | <0, Group Sum | Delete by ID | 	est_ripley_opex_etl.py | KO-RI-ETL-0003 |

## 3. PRUEBAS OBLIGATORIAS (Test Driven Data)
Antes de insertar un solo byte en el Ledger V4, se crearán suites de unit tests en 	ests/etl/ripley/:
- 	est_comisiones(): Verifica asignación costos_comerciales.
- 	est_opex(): Verifica asignación costos_operacionales.
- 	est_otros_cobros(): Verifica casos borde.
- 	est_ausencia_facturacion(): Simula BLOCKED_BY_SOURCE_DATA.
- 	est_ausencia_settlement(): Simula Data Missing.
- 	est_diferencias(): Tolerancia de centavos vs reglas rígidas.

## 4. REGRESIÓN
La fase de código concluirá obligatoriamente corriendo la suite completa de pruebas para confirmar:
1. Zero Regression Financiera (Ledger intocado para ML/Paris/Falabella).
2. Zero Regression Documental (Drawer/Engine de los demás intactos).
3. Regression Ripley Promotions (Garantiza que el nuevo flujo promocional no altere Settlement ni a otros Marketplaces).

