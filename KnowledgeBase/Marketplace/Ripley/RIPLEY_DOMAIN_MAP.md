---
tags:
  - ripley
  - domain
  - p26
---

# RIPLEY DOMAIN MAP

## 1. Entidades del Dominio
- **Venta**: Orden original realizada por el cliente en Ripley.com.
- **Settlement**: Archivo Excel/CSV oficial provisto por Ripley detallando liquidaciones a vendedores.
- **Facturación**: DTE emitido por Ripley al vendedor por concepto de comisiones y otros servicios.
- **XML**: Archivo físico del DTE.
- **Comisiones**: Porcentaje o monto fijo cobrado por Ripley sobre la venta.
- **OPEX**: Costos operacionales (logística, fulfillment, bodegaje).
- **Otros Cobros**: Penalidades, publicidad, etc.
- **Bancos**: Cuentas donde Ripley deposita el Settlement líquido.

## 2. Flujo Financiero
Venta -> Descuento Comisión -> Descuento OPEX -> Liquidación (Settlement) -> Depósito Bancario.
Paralelamente: Emisión DTE (Facturación) por Comisiones + OPEX.
