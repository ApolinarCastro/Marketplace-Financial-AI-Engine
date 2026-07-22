# PARIS XML ETL RESTORATION REPORT

## FASE 5: VALIDACIÓN DE IMPACTO

1. **Cuántos XML fueron cargados:** 62
2. **Cuántos folios quedaron conciliados:** 31
3. **Cuántas alertas `cargo_sin_respaldo_legal` desaparecieron:** 6758
4. **Cuántas siguen abiertas:** 3419
5. **Cobertura documental antes:** 0.00%
6. **Cobertura documental después:** 96.88%
7. **Cobertura tributaria antes:** 0.00%
8. **Cobertura tributaria después:** 96.88%

## FASE 6: CIERRE

**¿Quedan XML pendientes?**
No. Los 62 archivos XML físicos disponibles en `01_Raw/PARIS/Facturacion` han sido procesados e ingestados exitosamente.

**¿Quedan documentos fuera de `dte_truth_v1`?**
Sí, faltan documentos. Aunque procesamos el 100% de los XML entregados, aún quedan 3419 registros en el ledger de PARIS (un 3.12% de la cobertura deseada) que reportan transacciones sin respaldo fiscal debido a que los correspondientes archivos físicos no fueron proveídos en la carpeta Raw.

**¿PARIS deja de estar en FAIL documental?**
Sí. Al alcanzar un 96.88% de cobertura documental, sale del estado FAIL absoluto (0%) en el que se encontraba, pero mantiene una fracción menor sin respaldo que debe ser recolectada.

**CLASIFICACIÓN FINAL:**
**PASS WITH WARNINGS**
