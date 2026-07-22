---
tags:
  - ripley
  - etl
  - mapping
  - p26
---

# RIPLEY FIELD MAPPING

| Origen | Destino | Tipo | Regla | Validación | Responsable |
|---|---|---|---|---|---|
| id_orden_compra (Settle) | id_orden (Ledger) | String | Copia directa | Not Null, Unique per Line | ETL Engine |
| echa_liquidado (Settle) | echa (Ledger) | Date | YYYY-MM-DD | Rango admisible | ETL Engine |
| monto_venta (Settle) | monto (Ledger) | Decimal | Absoluto | > 0 | ETL Engine |
| monto_comision (DTE) | monto (Ledger) | Decimal | Negativo (salida) | < 0, cruce con Settle | ETL Engine |
| monto_despacho (DTE) | monto (Ledger) | Decimal | Negativo (salida) | < 0, cruce con Settle | ETL Engine |
| N/A | inancial_group | String | Taxonomía JSON | Must exist in Taxonomy | Tax Engine |
| olio_dte (XML) | olio_xml (Ledger) | Integer | Extracción XML | Match SII | DocumentGap |
| N/A | id_transaccion | UUID | Hash(Orden+Concepto)| Unique | ETL Engine |
