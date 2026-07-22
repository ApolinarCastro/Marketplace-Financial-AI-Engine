# RIPLEY Automation Blueprint

## Objetivo

Automatizar la trazabilidad punta a punta entre:

1. `TH` como libro mayor granular de transacciones.
2. `CICLOS` como consolidado por orden y factura/ciclo.
3. `SELLER` como liquidación comercial a pagar.
4. `FF` como capa complementaria de fulfillment y descuentos.
5. `XML` como certificación tributaria DTE.

## Flujo recomendado

1. Ingesta diaria o por lote.
2. Normalización de encoding, fechas, montos y encabezados.
3. Estandarización de llaves:
   - `order_id`
   - `order_line_id`
   - `invoice_number`
   - `cycle_date`
   - `seller_liquidation_number`
   - `xml_folio`
4. Construcción de tablas canónicas:
   - `raw_th_transactions`
   - `raw_cycle_orders`
   - `raw_seller_liquidations`
   - `raw_ff_orders`
   - `raw_ff_adjustments`
   - `raw_tax_dte`
5. Reglas de conciliación:
   - `TH -> CICLOS` por `invoice_number` y `order_id`
   - `CICLOS -> SELLER` por `order_id`
   - `FF -> SELLER` sólo cuando exista coincidencia temporal o mapping adicional
   - `SELLER -> XML` requiere tabla puente externa o metadata adicional
6. Certificación:
   - estado `CERTIFIED` si todos los tramos obligatorios cierran
   - estado `PARTIAL` si llega hasta `SELLER` pero no existe puente fiscal
   - estado `BROKEN` si no cierra `TH -> CICLOS` o `CICLOS -> SELLER`

## Diseño mínimo ejecutable

### Etapa 1

Programar `traceability_analysis.py` como job recurrente y guardar:

- `traceability_report.json`
- `traceability_report.md`

### Etapa 2

Persistir resultados en SQLite o Postgres con estas tablas:

- `ripley_trace_order_status`
- `ripley_trace_invoice_status`
- `ripley_tax_document_status`
- `ripley_trace_gaps`

### Etapa 3

Agregar alertas automáticas cuando ocurra cualquiera de estos casos:

- orden en `TH` sin match en `CICLOS`
- orden en `CICLOS` sin match en `SELLER`
- orden fulfillment en `FF` sin puente documental
- liquidación seller sin soporte tributario vinculable
- cambio de estructura de columnas o encoding

## Brecha crítica

Hoy no existe en esta carpeta una llave directa que una:

- `SELLER.Número documento liquidación`
- con `XML.Folio`

Sin esa tabla puente, la certificación tributaria completa no puede declararse como determinística. La automatización correcta debe marcar esa ausencia como excepción formal y no forzar un match heurístico.
