# TRUTH-005 — REHABILITACIÓN DEL REGISTRY DE INGESTIÓN

## Veredicto

`REGISTRY_CHAIN_RESTORED`

Cadena demostrada sobre copia temporal de V9:

`RAW controlado → Registry certificado → Ledger`

## Alcance y aislamiento

| Elemento | Ruta | SHA-256 final |
|---|---|---|
| DB oficial | `data/db/meli_financial_v4.db` | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` |
| V9 | `data/db/BASELINE_ESTABLE_V9_TRUTH_RECOVERED/meli_financial_v4.db` | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` |
| Copia V9 antes de la prueba | `C:\tmp\TRUTH_005_CONTROLLED\truth005_v9_working_final.duckdb` | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` |
| Copia después de la prueba | misma ruta temporal | `75A3B79E55896A4D02E75736F77E92BAF1977366BC7999D053B69078F919C1A8` |

La DB oficial y V9 conservaron exactamente su hash. Todas las conexiones de escritura recibieron explícitamente la ruta de la copia temporal. No se ejecutaron clasificación financiera, certificación, auditoría, cierres, DTE, Knowledge ni promoción de DB.

## Limitación histórica obligatoria

La transacción `CHG_Reporte_Facturacion_MercadoLibre_Ene2025.xlsx_1104` conserva:

- estado de procedencia: `LEGACY_PROVENANCE_GAP`;
- evidencia retrospectiva: `RECONSTRUCTED_NOT_ORIGINAL`;
- RAW demostrado;
- ledger demostrado;
- ingestión histórica no demostrada.

No se creó un `execution_id` retroactivo, no se insertó ninguna fila histórica en `ingestion_registry` y no se reemplazó el `file_hash` histórico.

## Esquema antes y después

### `file_registry`

Se conservaron `file_hash`, `file_name`, `source`, `rows_processed` y `processed_at`. Se añadieron únicamente:

- `file_path TEXT`;
- `content_sha256 TEXT`;
- `hash_algorithm TEXT`;
- `file_size_bytes BIGINT`;
- `marketplace TEXT`;
- `document_type TEXT`;
- `period TEXT`;
- `registered_at TIMESTAMP`.

El `file_hash` histórico basado en nombre permanece intacto. Las cargas futuras usan como identidad el SHA-256 físico completo de 64 caracteres y lo persisten también en `content_sha256`.

### `ingestion_registry`

Se reutilizaron las columnas existentes de ejecución, archivo, SHA-256, tiempos, estado, loader, pipeline, conteos, errores y advertencias. Se añadieron:

- `records_read INTEGER`;
- `records_new INTEGER`;
- `records_existing INTEGER`;
- `pipeline_version TEXT`.

Los estados implementados para este flujo son `STARTED`, `COMPLETED`, `FAILED` y `SKIPPED_DUPLICATE`.

### `marketplace_ledger_v1`

Se añadió exclusivamente:

- `execution_id TEXT`.

Las columnas y reglas financieras existentes no fueron modificadas.

## Orden transaccional implementado

1. Lee el archivo físico y calcula SHA-256.
2. Crea un UUID de ejecución.
3. Persiste `STARTED`; si falla, la excepción se propaga antes de invocar el loader.
4. Busca una ejecución `COMPLETED` previa con el mismo SHA-256.
5. Para contenido nuevo, clasifica metadatos y ejecuta `SurgicalLoader.load_file()` sobre el archivo explícito.
6. Inserta las filas ledger con el mismo `execution_id`.
7. Finaliza `COMPLETED`, `FAILED` o `SKIPPED_DUPLICATE` y registra tiempos, conteos y errores.

`load_marketplace()` queda disponible solo para llamadas legacy sin `execution_id`; el Upload Center canónico usa la ruta file-scoped y no resetea ni recarga marketplaces completos.

## Fixture ML controlado

| Campo | Valor |
|---|---|
| Archivo | `C:\tmp\TRUTH_005_CONTROLLED\ML_Facturacion_2026-07_TRUTH005_FINAL.xlsx` |
| Hoja | `REPORT` |
| Tamaño | `5030` bytes en la primera demostración registrada; el fixture final reproducido tiene identidad indicada abajo |
| SHA-256 final | `8B030937040D6BB82B25D51E6C3FAB15EC8FBF85A430CD3BC32FF49DB2FCFCF1` |
| Orden | `TRUTH005-ORDER-1` |
| Cargo | `TRUTH005-CARGO-1` |
| Detalle | `Cargo por envíos de Mercado Libre` |
| Valor del cargo | `3150` |
| Monto ledger esperado | `-3150` |
| Folio | `033-TRUTH005-0001` |

La validación comparó el hash persistido con `hashlib.sha256(archivo.read_bytes()).hexdigest()` y obtuvo igualdad exacta y longitud 64.

## Primera carga

| Campo | Resultado |
|---|---|
| `execution_id` | `09f538db-5471-462f-b520-ee05f067a679` |
| Estado inicial | `STARTED` |
| Estado final | `COMPLETED` |
| Marketplace | `ML` |
| Documento | `facturacion` |
| Periodo | `2026-07` |
| Pipeline | `ml_v4` |
| `records_read` | `1` |
| `records_new` | `1` |
| `records_existing` | `0` |
| Errores | `[]` |

Fila ledger resultante:

| Campo | Valor |
|---|---|
| `id_transaccion` | `CHG_ML_Facturacion_2026-07_TRUTH005_FINAL.xlsx_1` |
| `monto` | `-3150.0` |
| `folio_xml` | `033-TRUTH005-0001` |
| `execution_id` | `09f538db-5471-462f-b520-ee05f067a679` |

## Reingesta idéntica

| Campo | Resultado |
|---|---|
| Nuevo `execution_id` | `e07c2b1c-152c-41ad-ba7e-7ed384e0c895` |
| SHA-256 | igual a la primera carga |
| Estado | `SKIPPED_DUPLICATE` |
| Marketplace / documento / periodo | `ML` / `facturacion` / `2026-07` |
| Pipeline | `ml_v4` |
| `records_read` | `1` |
| `records_new` | `0` |
| `records_existing` | `1` |
| Filas ledger duplicadas | `0` |
| Errores | `[]` |

## Prueba negativa fail-closed

Se sustituyó únicamente `IngestionRegistry.create_record()` en la prueba aislada para lanzar `RuntimeError("STARTED unavailable")`.

Resultado:

- excepción explícita propagada;
- loader no alcanzado;
- conteo de `marketplace_ledger_v1` idéntico antes y después;
- cero falsos positivos.

## Protección financiera

Comparación bidireccional mediante `EXCEPT ALL` entre copia probada y V9:

| Tabla | Diferencia simétrica |
|---|---:|
| `marketplace_ledger_clasificado_v1` | 0 |
| `marketplace_cierre_financiero_v1` | 0 |
| `marketplace_auditoria_v1` | 0 |
| `dte_truth_v1` | 0 |
| Filas ledger legacy, excluyendo la fila controlada | 0 |

Las únicas diferencias lógicas de la copia fueron el esquema indispensable, un archivo controlado en `file_registry`, dos intentos en `ingestion_registry` y una fila ledger controlada.

## Diff de código

- `engine/v4/database.py`: columnas mínimas, conexión read/write explícita y registro de contenido.
- `engine/v4/ingestion/__init__.py`: contrato `STARTED/COMPLETED/FAILED/SKIPPED_DUPLICATE`, conteos y búsqueda idempotente por SHA-256.
- `engine/v4/ingestion/orchestrator.py`: fail-closed, deduplicación previa al loader, enlace `execution_id` y desactivación explícita de etapas posteriores durante TRUTH-005.
- `engine/v4/ingestion/handlers/persistence_engine.py`: persistencia file-scoped con `execution_id`; compatibilidad legacy sin `execution_id`.
- `engine/v4/surgical_loader.py`: inyección explícita de DB, carga de un único archivo ML de facturación y propagación de `execution_id`, sin modificar reglas financieras.
- pruebas focalizadas y contratos existentes actualizados a los estados autorizados.

## Pruebas y comandos

RED inicial:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_truth_005_registry.py -q -p no:cacheprovider
```

Resultado: `3 failed`; causa inicial: `SurgicalLoader.__init__()` no aceptaba DB explícita.

Verificación final focalizada:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_truth_005_registry.py tests/test_ingestion_handlers.py tests/test_orchestrator_wiring.py tests/test_upload_center_e2e.py tests/test_surgical_loader_file_registry.py -q -p no:cacheprovider
```

Resultado: `68 passed in 8.43s`. Pytest emitió después un `PermissionError` al limpiar el enlace temporal `pytest-current` de Windows; ocurrió tras el resultado y no afectó ninguna prueba ni DB.

Verificación adicional:

```powershell
.venv\Scripts\python.exe -m py_compile engine/v4/database.py engine/v4/surgical_loader.py engine/v4/ingestion/__init__.py engine/v4/ingestion/orchestrator.py engine/v4/ingestion/handlers/persistence_engine.py tests/test_truth_005_registry.py
git diff --cached --check
```

Ambos comandos finalizaron con código 0.

## Commit

`d15e94e769b702fe1ca6e97d59bfb1b6333ffce4` — `fix(ingestion): restore content-addressed registry chain`

Commit local; no se hizo push. El cambio DTE preexistente en el working tree fue excluido selectivamente.

## Resultado visible

- Archivo: `ML_Facturacion_2026-07_TRUTH005_FINAL.xlsx`.
- SHA-256 físico: `8B030937040D6BB82B25D51E6C3FAB15EC8FBF85A430CD3BC32FF49DB2FCFCF1`.
- Ejecución válida: `09f538db-5471-462f-b520-ee05f067a679`.
- Registry: `COMPLETED`, 1 leída, 1 nueva, 0 existente.
- Ledger: 1 fila, `-3150`, enlazada por el mismo `execution_id`.
- Reingesta: `SKIPPED_DUPLICATE`, 0 nuevas, 1 existente.
- DB oficial y V9: hashes intactos.

`REGISTRY_CHAIN_RESTORED`
