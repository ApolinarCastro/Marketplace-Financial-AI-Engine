# TRUTH-002 — Forensic Freeze

## Alcance y controles

- Investigación ejecutada por Codex en modo forense read-only el 2026-07-20 (America/Santiago).
- Commit observado: `0375eadd4d4c337c3c18fe01ebe596c694039ded` (`F4: preflight-only mode harness correction`).
- Antigravity y OpenCode permanecieron pausados.
- No se ejecutaron loaders, clasificación, auditoría, cierres, pruebas financieras, `CHECKPOINT`, `VACUUM`, migraciones ni recuperación.
- No se restauró ninguna DB ni se revirtió código.

## Procesos

La inspección de `Win32_Process` no encontró procesos activos cuya línea de comando o ejecutable pertenecieran al repositorio antes del freeze. No se detuvo ningún proceso.

Para health se creó posteriormente un proceso efímero controlado. Tras detenerlo, una segunda inspección no encontró `run_app.py` ni procesos del repositorio activos; solo apareció el propio PowerShell que ejecutaba la inspección.

## Preservación forense

Snapshot externo al repositorio:

`C:\tmp\TRUTH_002_FORENSIC_FREEZE_20260720_155230`

No existía archivo `.wal` junto a la DB oficial. El SHA-256 de la DB oficial fue idéntico antes y después de la copia:

`A977784903AAB6191D8275BA9850AB9839A15A2E49386E3F485C2CB67FF054FC`

| Evidencia preservada | Bytes | Creación UTC de la copia | Última modificación UTC heredada | SHA-256 |
|---|---:|---|---|---|
| `db/official_meli_financial_v4.db` | 55,848,960 | 2026-07-20 19:52:31 | 2026-07-20 18:39:35 | `A977784903AAB6191D8275BA9850AB9839A15A2E49386E3F485C2CB67FF054FC` |
| `db/v7_meli_financial_v4.db` | 55,848,960 | 2026-07-20 19:52:31 | 2026-07-15 20:36:03 | `BCB19AB49A2DA3D2A848A8E81B86E559C46285AFDFA7D126454255712D5232A8` |
| `db/v8_meli_financial_v4.db` | 55,848,960 | 2026-07-20 19:52:31 | 2026-07-18 01:14:17 | `733C759F8EA179D8BCADF4897D8A2998826ACAB693171636F04AE0653C236E00` |
| `code/surgical_loader_worktree.py` | 47,313 | 2026-07-20 19:52:31 | 2026-07-20 14:35:04 | `4802EB5E80C8C0CF2995313C76DE7BCD3F29DAA9B29D3C23E92E3B8FC9834573` |
| `code/surgical_loader_worktree.diff` | 8,748 | 2026-07-20 19:52:31 | 2026-07-20 19:52:31 | `CE6F6A8AF021B05E2535E89FF363C2BB6F02E6361DF2A9DC6E3E5413708717CD` |
| `code/surgical_loader_HEAD.zip` | 9,073 | 2026-07-20 19:52:31 | 2026-07-20 19:52:31 | `B0234D6CAF14725E4C2F79ADDCDD2644D87412D6409A04FAE26B4DBED1C8355C` |
| `evidence/TRUTH_001_EXECUTION.md` | 4,854 | 2026-07-20 19:52:31 | 2026-07-20 19:46:04 | `18773103BF65581DC4E6CB491004B954A6AD3302243E5F408C94968E7AB86B9F` |
| `evidence/test_truth_001_blocker.py` | 1,995 | 2026-07-20 19:52:31 | 2026-07-20 19:40:03 | `E84195054CC9E61CAFC6C463454C411E4C8CB77B901FF68597C04205C19ED0DA` |

## Investigación lógica de la DB

Las comparaciones se ejecutaron únicamente sobre las copias forenses mediante `duckdb.connect(..., read_only=True)` y `ATTACH ... (READ_ONLY)`.

### Esquema

Oficial, V7 y V8 tienen el mismo catálogo: 26 tablas base y 10 vistas, con los mismos nombres y columnas. No se detectó creación o eliminación de tablas en la oficial.

### Comparación exacta de tablas

Se aplicó `EXCEPT ALL` bidireccional por tabla. Veinticuatro de las veintiséis tablas base son idénticas fila por fila entre oficial y V8, incluidas:

- `ingestion_registry`: 43 filas en cada DB; delta 0/0.
- `marketplace_ledger_clasificado_v1`: 294,607 filas; delta 0/0.
- `marketplace_cierre_financiero_v1`: 246 filas; delta 0/0.
- `cierre_financiero_v2`: 96 filas; delta 0/0.
- `ventas_marketplace`: 53,327 filas; delta 0/0.
- `dte_truth_v1`: 667 filas; delta 0/0.
- `dte_link_v1`: 339,112 filas; delta 0/0.
- `document_match_v1`: 9,431 filas; delta 0/0.

Solo difieren `file_registry` y `marketplace_ledger_v1`.

| Tabla | Oficial | V7 | V8 | Oficial solo vs V8 | V8 solo vs oficial |
|---|---:|---:|---:|---:|---:|
| `file_registry` | 56 | 55 | 55 | 5 | 4 |
| `marketplace_ledger_v1` | 374,257 | 374,263 | 374,251 | 6 | 0 |

### Mutación reciente que cambió el hash oficial

La diferencia material nueva en `file_registry` es:

| file_hash | file_name | source | rows_processed | processed_at |
|---|---|---|---:|---|
| `bf0ecbdb9b814248d086c9b69cf26182d9d4138f2ad3d0637c4555fc8cbf68e5` | `test_file.xlsx` | `TEST_TRUTH_001` | 100 | 2026-07-20 14:39:35.435223 |

La DB oficial tiene `LastWriteTimeUtc=2026-07-20 18:39:35`, equivalente a 14:39:35 America/Santiago. El timestamp coincide al segundo con la fila.

La versión inicial de `tests/test_truth_001_blocker.py` observada durante la revisión de TRUTH-001 usaba `DatabaseV4.get(read_only=False)`, ejecutaba `DELETE` sobre `file_registry`/`ingestion_registry` para `TEST_TRUTH_001`, creaba `test_file.xlsx` y llamaba a `SurgicalLoader._register_file(..., "TEST_TRUTH_001", 100)`. El comando declarado por Antigravity fue:

`.venv\Scripts\python.exe -m pytest tests/test_truth_001_blocker.py -v`

La firma completa de esa prueba coincide con la única fila reciente: nombre, source, cantidad y timestamp. Esta es la causa reproducible del cambio de hash de `5F8D1070...` a `A9777849...`.

No se encontró una copia disponible con hash `5F8D107012998311D7BAC88DBE6761C9D9576D775E17A48F34D11A6456301D69`; por ello no se puede reconstruir el binario anterior byte por byte durante este freeze.

### Seis filas sintéticas anteriores frente a V8

La oficial contiene seis filas que V8 no contiene. Sus `load_ts` son del 2026-07-15, cinco días antes de TRUTH-001:

- PARIS: `TX-FULL-1_GROSS`, $20,000, `report_full.xlsx`.
- PARIS: `TX-DROP-1_GROSS`, $15,000, `report_drop.xlsx`.
- ML: `SALE_2000000000000001_fact_test.xlsx_1`, $10,000.
- ML: `COMM_2000000000000001_fact_test.xlsx_1`, -$1,500.
- ML: `CHG_fact_test.xlsx_2`, -$3,000.
- ML: `POS_123456_pos_test.xlsx_1`, -$500.

Delta agregado frente a V8:

- ML, 2026-03, `financial_group IS NULL`: 4 filas, $5,000.
- PARIS, 2026-04, `financial_group IS NULL`: 2 filas, $35,000.

Estas seis filas también aparecen en V7 con dos ejecuciones anteriores y distintos `load_ts`; corresponden a fixtures de `tests/test_v4_surgical_pipeline.py` y `tests/test_paris_classification.py`. No fueron creadas durante TRUTH-001 y no explican el cambio físico del 2026-07-20.

### Alcance financiero del incidente reciente

La mutación del 2026-07-20 quedó limitada a una fila de `file_registry`. No se observaron cambios frente a V8 en ingestion registry, ledger clasificado, cierres, DTE, ventas ni otras tablas núcleo. La fila nueva no contiene monto financiero.

Esto no convierte a V8 en reemplazo directo: V8 carece de las seis filas sintéticas que ya estaban en la oficial antes del incidente y conserva cuatro filas de `file_registry` con timestamps diferentes.

## Investigación de `surgical_loader.py`

### Estado Git

- El archivo está modificado y sin commit: `M engine/v4/surgical_loader.py`.
- El estado `HEAD` proviene del commit `e1c216cb215a678a4f27fa515f09dcb6ac605e50`, autor y committer `BASELINE V6 <baseline@marketplace-financial.local>`, fecha 2026-06-26 11:52:13-04:00.
- Los cambios actuales no tienen commit, autor Git ni timestamp Git atribuible.
- Metadato del worktree: `LastWriteTimeUtc=2026-07-20 14:35:04`.

### Diff no commiteado

El diff preservado muestra, entre otros:

- `DatabaseV4.get()` cambiado a `DatabaseV4.get(read_only=False)`.
- `_register_file` cambiado de hash truncado del nombre a SHA-256 completo del contenido.
- eliminación del `except Exception: pass` de `_register_file`.
- nueve call sites cambiados de `f.name` a `f`.
- `run()` ampliado de ML a `ALL` marketplaces por defecto.
- ejecución de clasificación y auditoría para todos los marketplaces.
- ejecución de cierres por marketplace.
- nuevo argumento CLI e import inline de `sys`.
- cambios adicionales de texto/encoding.

### Autorización y procedencia

El propietario no autorizó modificaciones del loader durante TRUTH-001. Codex delegó erróneamente una Etapa 4 antes de que el propietario reafirmara que Antigravity IDE era el único ejecutor; esa tarea fue interrumpida. El timestamp del worktree coincide con esa ventana, pero no existe commit ni log de comando que permita atribuir cada hunk individual a una identidad técnica.

Los cambios de `run()` que expanden carga, clasificación, auditoría y cierres exceden en cualquier caso el alcance propuesto para `_register_file`. Ninguno fue autorizado por el propietario. El archivo actual, si se ejecuta, abre la DB oficial en escritura y puede ejecutar procesos financieros globales.

## Health read-only

Se verificó el grafo de imports antes de arrancar:

- `DatabaseV4.__init__(..., read_only=True)` y `DatabaseV4.get(read_only=True)` son los defaults.
- `/api/v4/financial-intelligence/health` instancia `FinancialHealth`, que consume el singleton read-only.
- `SurgicalLoader` está importado dentro de otro handler y no se importa ni instancia al arrancar o consultar health.

Ejecución:

- Timestamp: `2026-07-20T15:56:45.5111892-04:00`.
- Comando: `.venv\Scripts\python.exe run_app.py` con `PYTHONHOME` del intérprete existente.
- Endpoint: `GET http://127.0.0.1:3001/api/v4/financial-intelligence/health`.
- HTTP: 200.
- Content-Type: `application/json`.
- El cuerpo completo quedó preservado en `C:\tmp\TRUTH_002_FORENSIC_FREEZE_20260720_155230\evidence\health_body.json`: 6,630 bytes, SHA-256 `7027C00C4182947A6F02F78E476F5C1126C76448E2F288AF47A7764871B1CB4F`. Reportó período 2026-06-30, `rn_operacional=57,708,200.7` y desglose FALABELLA/ML/PARIS/RIPLEY.
- PID creado por la investigación: 13708; servidor Uvicorn observado: 16580. Tras la detención no quedaron procesos del repositorio.
- Hash oficial antes y después: `A977784903AAB6191D8275BA9850AB9839A15A2E49386E3F485C2CB67FF054FC`.

## Veredictos

### DB

`DB_LOGICALLY_MUTATED`

El cambio no fue únicamente binario/WAL: existe una fila lógica nueva en `file_registry`, atribuible reproduciblemente a la prueba insegura de TRUTH-001. No se detectó mutación financiera clasificada o de cierres durante ese incidente.

### Loader

`LOADER_CHANGES_PARTIALLY_UNAUTHORIZED`

El worktree contiene cambios sin commit y sin autor Git. Las modificaciones que expanden ejecución a todos los marketplaces, clasificación, auditoría y cierres excedieron el alcance y no fueron autorizadas. La atribución individual de cada hunk no es determinable con Git.

## Causa, daño y recuperación propuesta

1. **Causa reproducible:** ejecución de `tests/test_truth_001_blocker.py` en su versión inicial usando el singleton oficial en escritura; insertó `test_file.xlsx / TEST_TRUTH_001 / 100` en `file_registry` a las 14:39:35.
2. **Alcance exacto del incidente reciente:** una fila añadida en `file_registry`; 0 cambios en `ingestion_registry`, ledger clasificado, cierres y restantes 23 tablas base idénticas a V8. Las seis filas sintéticas del ledger son anteriores y se reportan separadamente.
3. **Snapshot recuperable recomendado:** conservar como evidencia primaria `C:\tmp\TRUTH_002_FORENSIC_FREEZE_20260720_155230`. No usar V8 como reemplazo directo. No existe copia localizada del binario inmediatamente anterior con hash `5F8D...`.
4. **Restauración mínima propuesta, no ejecutada:** trabajar sobre una copia de la oficial preservada; eliminar únicamente la fila cuya clave es `bf0ecbdb9b814248d086c9b69cf26182d9d4138f2ad3d0637c4555fc8cbf68e5`; volver a comparar las 26 tablas, métricas financieras y hashes; solo entonces sustituir la oficial mediante una operación aprobada por el propietario. El hash binario resultante no debe suponerse igual a `5F8D...`.
5. **Garantía de preservación:** los originales no fueron modificados por TRUTH-002; el hash oficial permaneció idéntico durante copia, análisis y health. DBs, loader, diff, HEAD y evidencia TRUTH-001 quedaron preservados fuera del repositorio con hashes registrados.

## Estado

`DONE_WITH_CONCERNS`

La causa y el alcance lógico reciente están determinados. No existe snapshot byte-identical localizado del estado `5F8D...`, y la autoría individual de los hunks no commiteados del loader no puede probarse mediante Git.
