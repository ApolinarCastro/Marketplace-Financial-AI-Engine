# TRUTH-004 — TRAZABILIDAD Y DESBLOQUEO DE TRANSACCIÓN ML

## Resultado

**Veredicto: `FIRST_BREAK_REGISTRY`**

La transacción `CHG_Reporte_Facturacion_MercadoLibre_Ene2025.xlsx_1104` puede reproducirse desde el archivo RAW y existe en `marketplace_ledger_v1`, pero no existe una ejecución correspondiente en `ingestion_registry`. La cadena se detiene en Registry conforme a la regla de detención de TRUTH-004. No se ejecutaron las etapas de clasificación, API ni evidencia documental.

## Contexto reproducido

| Campo | Valor |
|---|---|
| Fecha de ejecución | `2026-07-20T17:54:17.5569615-04:00` |
| Commit | `c52755ab285f4aeb7a9f37b441ffa782aae06827` |
| Branch | `f4-clean-code` |
| DB oficial | `data/db/meli_financial_v4.db` |
| Hash DB antes | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` |
| Hash DB después | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` |
| Hash V9 antes | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` |
| Hash V9 después | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` |
| Modo DB | DuckDB `read_only=True` |

## Cadena observada

| Enlace | Estado | Evidencia |
|---|---|---|
| RAW | DEMOSTRADO | Archivo existente; hoja `REPORT`; fila DataFrame 1104 / fila Excel 1105; SHA-256 físico registrado abajo. |
| Registry | ROTO | Existe una entrada nominal en `file_registry`, pero su `file_hash` no es hash del contenido y no existe ninguna fila correspondiente en `ingestion_registry`. |
| Ledger | OBSERVADO, NO ENCADENADO POR REGISTRY | Existe exactamente una fila con el identificador objetivo y coincide con el RAW. No subsana la ausencia del registro de ingestión. |
| Clasificación | NO EJECUTADO | Detención obligatoria en Registry. |
| DTE | NO EJECUTADO | Detención obligatoria en Registry. |
| API | NO EJECUTADO | Detención obligatoria en Registry. |

Cadena conseguida:

`RAW (DEMOSTRADO) → Registry (ROTO) ⛔ → Ledger (OBSERVADO, SIN ENLACE REGISTRAL) → Clasificación (NO EJECUTADO) → DTE (NO EJECUTADO) → API (NO EJECUTADO)`

## Etapa 1 — RAW

| Campo | Evidencia |
|---|---|
| Archivo | `Reporte_Facturacion_MercadoLibre_Ene2025.xlsx` |
| Ruta absoluta | `C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\ML\Facturacion\Reporte_Facturacion_MercadoLibre_Ene2025.xlsx` |
| Existencia | Sí |
| Tamaño | `802844` bytes |
| SHA-256 físico | `49F6F4AFAD6182F97D3C6A411B46069A79770233B816D195CD4844D73CB62492` |
| MD5 físico auxiliar | `6545CB39A9BDA394C792BB735806A901` |
| Hoja | `REPORT` |
| Encabezado | fila Excel 1 |
| Fila fuente | índice DataFrame `1104`; fila Excel `1105` |
| Detalle | `Cargo por envíos de Mercado Libre` |
| Valor del cargo | `3150` |
| Monto ledger derivado | `-3150` |
| Número del cargo | `40129569770` |
| Número de venta | `2000010334239382` |
| Pago | `98056222184` |
| Folio | `033-0006491256` |
| Fecha del cargo | `2025-01-01` |

La construcción retrospectiva del identificador está demostrada por el contrato del loader preservado: para cargos distintos de venta y anulación usa `CHG_{nombre_archivo}_{índice}` y transforma `Valor del cargo` mediante `monto = -valor_cargo`. Para esta fila produce exactamente `CHG_Reporte_Facturacion_MercadoLibre_Ene2025.xlsx_1104` y `-3150`.

## Etapa 1 — Registry

### `file_registry`

Existe una fila:

| Campo | Valor observado |
|---|---|
| `file_hash` | `9fb68c83357d8ae377f6649d56087a22` |
| `file_name` | `Reporte_Facturacion_MercadoLibre_Ene2025.xlsx` |
| `source` | `ML` |
| `rows_processed` | `1425` |
| `processed_at` | `2026-07-13 11:39:52.533087` |

El valor `9fb68c83357d8ae377f6649d56087a22` coincide con los primeros 32 caracteres de SHA-256 del **nombre UTF-8** del archivo (`9fb68c83357d8ae377f6649d56087a224a06417761278d4902204ab84ee27a99`), no con el SHA-256 del contenido (`49F6F4AF...`). Por tanto, esta fila demuestra procesamiento nominal por nombre, pero no identidad criptográfica del RAW actual.

### `ingestion_registry`

La búsqueda por:

- nombre exacto;
- ruta absoluta;
- SHA-256 físico;
- MD5 físico;

retornó **0 filas**.

No existen para este archivo `execution_id`, `status`, tiempos de inicio/fin, `marketplace`, `document_type`, `period`, `loader_executed`, `pipeline` ni `records_inserted`. El enlace Registry no puede demostrarse.

## Ledger observado

Aunque la regla exige detener la progresión en Registry, se registró la fila ya consultada para delimitar el alcance del quiebre:

| Campo | Valor |
|---|---|
| `marketplace` | `ML` |
| `id_transaccion` | `CHG_Reporte_Facturacion_MercadoLibre_Ene2025.xlsx_1104` |
| `id_orden` | `2000010334239382` |
| `fecha` | `2025-01-01` |
| `periodo` | derivado de `fecha`: `2025-01` |
| `detalle` | `Cargo por envíos de Mercado Libre` |
| `monto` | `-3150.0` |
| `tipo_movimiento` | `CARGO` |
| `archivo_origen` | `Reporte_Facturacion_MercadoLibre_Ene2025.xlsx` |
| `folio_xml` | `033-0006491256` |
| `financial_group` | `NULL` |
| `include_in_operational_pnl` | `NULL` |
| `load_ts` | `2026-07-13 11:39:52.521926` |

La tabla no posee una columna física `periodo`; el periodo reportado se deriva de `fecha` sin alterar datos.

## Primer quiebre reproducible

El primer quiebre es `RAW → Registry`:

1. El RAW existe y su fila exacta es reproducible.
2. `file_registry` conserva solo una referencia nominal cuyo hash representa el nombre, no el contenido.
3. `ingestion_registry` carece completamente de la ejecución del archivo.
4. Por ello no existe evidencia registral ejecutable que conecte criptográficamente el RAW con la carga que produjo el ledger.

## Corrección

No se aplicó corrección. Reparar retrospectivamente el enlace requeriría crear o inferir evidencia histórica de ingestión, lo que violaría el modo read-only y no puede hacerse sin inventar un `execution_id` ni hechos de ejecución inexistentes. No se ejecutó `SurgicalLoader`, clasificación, auditoría, cierres, pruebas financieras ni escrituras sobre la DB oficial o V9.

## Comandos reproducibles

```powershell
Get-FileHash 'data\db\meli_financial_v4.db' -Algorithm SHA256
Get-FileHash 'data\db\BASELINE_ESTABLE_V9_TRUTH_RECOVERED\meli_financial_v4.db' -Algorithm SHA256
git rev-parse HEAD
git branch --show-current
```

La inspección estructurada se ejecutó con el Python aislado del repositorio, `pandas`/`calamine` para el XLSX y `duckdb.connect(path, read_only=True)` para consultas parametrizadas a `file_registry`, `ingestion_registry` y la fila objetivo de `marketplace_ledger_v1`.

## Veredicto final

`FIRST_BREAK_REGISTRY`
