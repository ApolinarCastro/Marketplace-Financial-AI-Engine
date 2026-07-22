# Legal Alert RCA: Cargo Sin Respaldo Legal

## Hallazgo Principal
La alerta masiva de `cargo_sin_respaldo_legal` es un falso negativo originado en la validación de `engine/v4/marketplace_auditor.py` (línea ~737).

## Causa Raíz
Se implementó un `JOIN` estricto `l.folio_xml = t.folio`. Mercado Libre envía sus folios fiscales con formato estructurado (ej. `033-0013380337`), pero en la tabla de verdad `dte_truth_v1` se almacenan los folios en su forma natural o parcialmente normalizada (`13380337`). El cruce estricto omite estas diferencias y clasifica transacciones legítimas como faltantes de respaldo legal.

## Plan de Remediación
Modificar la consulta SQL en el `marketplace_auditor.py` para aplicar una limpieza en tiempo de ejecución o cruce (ej. `regexp_replace(l.folio_xml, '^[0-9]+-0*', '') = t.folio`) garantizando así que los folios hagan match correctamente con la tabla de verdad del SII.
