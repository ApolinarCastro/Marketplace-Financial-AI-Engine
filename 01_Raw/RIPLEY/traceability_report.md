# RIPLEY Traceability Report

- Generated at: 2026-07-02T13:02:33
- Files: {"TH_files": 8, "CICLOS_files": 49, "FF_files": 62, "SELLER_files": 48, "XML_files": 407}
- Rows: {"TH_rows": 127586, "CICLOS_rows": 19384, "FF_rows": 1584, "FF_adjustment_rows": 214, "SELLER_rows": 17913}

## End-to-End Lineage
- 1. TH: Libro mayor granular por evento | Join: order_id, invoice_number, order_line_id, cycle_date
- 2. CICLOS: Resumen por orden dentro del ciclo/factura | Join: invoice_number y order_id
- 3. SELLER: Liquidación comercial consolidada a pagar | Join: order_id; document number sólo interno en estos datos
- 4. FF: Órdenes fulfillment y descuentos operacionales | Join: order_id y order_line_id
- 5. XML: Certificación tributaria SII (DTE 33, 43, 52, 61) | Join: folio fiscal; no aparece un puente directo a SELLER

## Traceability Coverage
- {"th_to_ciclos_by_invoice_matches": 49, "th_to_ciclos_by_order_matches": 13646, "ciclos_to_seller_by_order_matches": 11974, "ff_to_seller_by_order_matches": 0, "ff_adjustments_to_seller_by_order_matches": 0, "seller_to_xml_by_document_matches": 0}

## XML Tax Documents
- {"document_count_by_type": {"33": 253, "61": 19, "43": 105, "52": 30}, "document_total_by_type": {"33": 121453338.0, "61": 2062851.0, "43": 52179469.0, "52": 11009493.0}}

## Main Gaps
- No existe llave directa entre `SELLER.Número documento liquidación` y `XML.Folio` en los archivos disponibles.
- Los CSV de `TH` y `CICLOS` presentan encabezados con codificación inconsistente; la normalización es obligatoria antes de conciliar.
- La cobertura temporal no es uniforme: `TH` tiene 8 archivos mensuales, `SELLER` 48 libros, `CICLOS` 49 cierres y `XML` 407 DTE.

## TH Top Transaction Types
- Importe del pedido: 16271
- Importe del envÃ­o del pedido: 16271
- Gastos de envÃ­o pagados por el operador: 16271
- Comisiones: 16271
- Impuesto sobre las comisiones: 16271
- Factura manual: 12466
- Impuesto de la factura manual: 12466
- Importe del pedido reembolsado: 4238
- Importe del envÃ­o del pedido reembolsado: 4238
- Gastos de envÃ­o reembolsados pagados por el operador: 4238
- ComisiÃ³n de reembolso: 4238
- Impuesto sobre la comisiÃ³n de reembolso: 4238