---
tags:
  - ripley
  - etl
  - specification
  - p26
---

# RIPLEY ETL TRANSFORMATION SPECIFICATION

## 1. VENTA
- **Fuente origen**: Settlement Ripley.
- **Campo origen**: monto_venta_bruta (o equivalente en raw).
- **Transformación**: Parseo de moneda -> Asignación de fecha -> Limpieza de vacíos.
- **Regla financiera**: Reconocimiento de ingreso bruto en periodo liquidado.
- **Regla tributaria**: N/A (Tributa por ticket cliente, no DTE Ripley).
- **Campo destino**: monto.
- **Tabla destino**: marketplace_ledger_clasificado_v1.
- **Nivel de confianza**: HIGH (CONFIRMED_SOURCE).
- **Evidence Engine**: EV-RIPLEY-SETTLE-XXXX.
- **Explainability**: Origen transaccional directo sin transformación de negocio.
- **Knowledge Object**: KO-RI-ETL-0001.

## 2. COMISION
- **Fuente origen**: Facturación (Seller Center) / Secundario: Settlement.
- **Campo origen**: monto_comision.
- **Transformación**: Normalización monetaria -> Clasificación tributaria (Afecto a IVA).
- **Regla financiera**: Costo directo de venta descontado antes de liquidación.
- **Regla tributaria**: Base imponible afecta según clasificador SII.
- **Campo destino**: monto.
- **Tabla destino**: marketplace_ledger_clasificado_v1 (Con inancial_group = costos_comerciales).
- **Nivel de confianza**: MEDIUM (LIKELY_SOURCE).
- **Evidence Engine**: EV-RIPLEY-DTE-XXXX.
- **Explainability**: Descuento operativo mapeado a cuenta contable de comisiones vía Taxonomía.
- **Knowledge Object**: KO-RI-ETL-0002.

## 3. OPEX (Fulfillment / Bodegaje)
- **Fuente origen**: Facturación (Seller Center) / Secundario: Settlement.
- **Campo origen**: costo_operacional.
- **Transformación**: Agrupación de items logísticos -> Clasificación tributaria.
- **Regla financiera**: Costo operativo de plataforma deducible.
- **Regla tributaria**: Gasto aceptado asociado a Factura.
- **Campo destino**: monto.
- **Tabla destino**: marketplace_ledger_clasificado_v1 (Con inancial_group = costos_operacionales).
- **Nivel de confianza**: MEDIUM (LIKELY_SOURCE).
- **Evidence Engine**: EV-RIPLEY-DTE-XXXX.
- **Explainability**: Descuento por servicios operacionales (despacho/fulfillment) según Taxonomía.
- **Knowledge Object**: KO-RI-ETL-0003.
