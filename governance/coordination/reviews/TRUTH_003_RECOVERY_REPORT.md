# TRUTH-003 — Recuperación integral

## Veredicto

`TRUTH_BASELINE_RECOVERED`

## Evidencia forense

| Artefacto | SHA-256 esperado | SHA-256 observado |
|---|---|---|
| Loader no autorizado preservado | `4802EB5E80C8C0CF2995313C76DE7BCD3F29DAA9B29D3C23E92E3B8FC9834573` | Igual |
| Prueba insegura preservada | `E84195054CC9E61CAFC6C463454C411E4C8CB77B901FF68597C04205C19ED0DA` | Igual |
| DB forense congelada | `A977784903AAB6191D8275BA9850AB9839A15A2E49386E3F485C2CB67FF054FC` | Igual |

## Loader neutralizado

`engine/v4/surgical_loader.py` fue restaurado completo desde `e1c216cb215a678a4f27fa515f09dcb6ac605e50`:

- blob restaurado: `e78452a3f1c986aa1b784409f6cfc59675165969`;
- SHA-256 restaurado: `D6D13E56A8D55EC92F23582FF36E451BE88226297598B53B43E919C88D72ED68`.

Se modificó exclusivamente `SurgicalLoader.run()`:

```python
def run(self):
    self.load_marketplace("ML")
```

Diff quirúrgico: 1 inserción y 8 eliminaciones. Se retiraron de `run()` el import de `MarketplaceAuditorEngine`, clasificación, auditoría, cierre y sus mensajes/resultados.

Validación AST sin importar el loader:

- llamadas encontradas en `run()`: `load_marketplace`;
- argumento: `ML`;
- `run_classification`: ausente;
- `run_audit`: ausente;
- `run_financial_closing`: ausente;
- `MarketplaceAuditorEngine`: ausente;
- compilación sintáctica estática: exitosa.

Estado final:

- SHA-256: `4DB43D77731BF05B9CA5433C1FD33D764F8C1BE6F4EBDD619E3AA6C8BC560808`;
- blob Git: `e1812d3af5faef9f798742617db5498d9f1c4ce9`;
- commit local exclusivo: `c52755a`;
- mensaje: `fix(loader): separate ingestion from classification audit and closing`;
- push: no ejecutado.

## Prueba insegura

`tests/test_truth_001_blocker.py` era untracked. Fue retirada después de verificar la copia forense. No se ejecutó nuevamente y no se modificaron otros tests.

## Recuperación transaccional

Fuente única:

`C:\tmp\TRUTH_002_FORENSIC_FREEZE_20260720_155230\db\official_meli_financial_v4.db`

Se creó una copia nueva con hash inicial `A9777849...`. Dentro de una transacción se validó exactamente esta fila:

| file_hash | file_name | source | rows_processed |
|---|---|---|---:|
| `bf0ecbdb9b814248d086c9b69cf26182d9d4138f2ad3d0637c4555fc8cbf68e5` | `test_file.xlsx` | `TEST_TRUTH_001` | 100 |

- filas antes: 1;
- filas después: 0;
- filas afectadas: 1;
- transacción: commit;
- nuevo SHA-256 candidato: `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE`.

No se ejecutó otra sentencia de modificación.

## Validación lógica

Comparación `EXCEPT ALL` bidireccional entre la copia forense y la candidata:

- 26 tablas base presentes;
- 10 vistas presentes;
- esquemas y columnas idénticos;
- 25 tablas idénticas fila por fila;
- `file_registry`: original 56, recuperada 55;
- diferencia original→recuperada: exactamente la fila `TEST_TRUTH_001`;
- diferencia recuperada→original: 0;
- `marketplace_ledger_v1`: 374,257 filas, delta 0/0;
- `marketplace_ledger_clasificado_v1`: 294,607 filas, delta 0/0;
- `marketplace_cierre_financiero_v1`: 246 filas, delta 0/0;
- `cierre_financiero_v2`: 96 filas, delta 0/0;
- `ingestion_registry`: 43 filas, delta 0/0;
- `dte_truth_v1`: 667 filas, delta 0/0;
- `dte_link_v1`: 339,112 filas, delta 0/0;
- `document_match_v1`: 9,431 filas, delta 0/0.

Invariancia exacta mediante `EXCEPT ALL`:

- filas y sumas por marketplace: 0/0;
- filas y sumas por periodo: 0/0;
- filas y sumas por `financial_group`: 0/0;
- clasificación: 0/0;
- cierres V1/V2: 0/0;
- DTE: 0/0;
- ingestion registry: 0/0.

Las seis filas sintéticas anteriores permanecen sin cambios.

## Sustitución recuperable

Precondiciones cumplidas:

- ningún proceso del repositorio activo;
- ningún WAL presente;
- hash oficial previo todavía `A9777849...`.

Se usó reemplazo atómico en el mismo volumen. Respaldo preservado:

`data/db/meli_financial_v4_pre_truth003_20260720_173842_A9777849.db`

- hash del respaldo: `A977784903AAB6191D8275BA9850AB9839A15A2E49386E3F485C2CB67FF054FC`;
- nuevo hash oficial: `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE`;
- apertura read-only: exitosa;
- hash antes/después de validación read-only: idéntico;
- WAL posterior: ausente;
- filas `TEST_TRUTH_001`: 0.

## Baseline V9

Creado:

`data/db/BASELINE_ESTABLE_V9_TRUTH_RECOVERED/`

Contenido:

- `meli_financial_v4.db`, 55,848,960 bytes;
- SHA-256: `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE`;
- `MANIFEST_V9.json` con fingerprints de 26 tablas, 10 vistas, métricas financieras, loader, respaldo, fila eliminada, health y comandos reproducibles.

El manifiesto declara que V9 no reproduce byte por byte `5F8D...`, recupera el estado lógico anterior al incidente, conserva las seis filas sintéticas previas y no modifica cifras financieras.

## Comprobación funcional read-only

Comando: `.venv\Scripts\python.exe run_app.py`.

Timestamp: `2026-07-20T17:40:26.3354732-04:00`.

Health:

- endpoint: `/api/v4/financial-intelligence/health`;
- HTTP: 200;
- Content-Type: `application/json`;
- cuerpo: 6,630 bytes;
- SHA-256 del cuerpo: `7027C00C4182947A6F02F78E476F5C1126C76448E2F288AF47A7764871B1CB4F`;
- evidencia completa: `C:\tmp\TRUTH_002_FORENSIC_FREEZE_20260720_155230\evidence\truth003\health_body.json`;
- hash DB antes/después: `C76C3FEE...`, idéntico.

Consulta transaccional:

- `id_transaccion`: `CHG_Reporte_Facturacion_MercadoLibre_Ene2025.xlsx_1104`;
- marketplace: ML;
- periodo: 2025-01;
- ledger: 1 fila, monto -3,150;
- clasificación: 0 filas;
- folio XML: `033-0006491256`;
- API `/api/v4/ledger`: HTTP 200, 0 filas;
- cuerpo API: `{"data":[],"total_count":0,"total_sum":0.0,"offset":0,"limit":200,"detalles":[]}`;
- SHA-256 cuerpo API: `2BE2312ACB99E7DC8F9BB3F943D03F5245853AFB3BF8A208DCA007DFF8F7ACC2`;
- hash DB antes/después: idéntico.

## Estado Git y limitaciones

- Loader neutralizado en commit local `c52755a`.
- Informe actualizado como único informe TRUTH-003.
- V9 y su manifiesto creados conforme a la autorización.
- No se ejecutaron loader, clasificación, auditoría, cierres ni suite financiera.

El HOLD de recuperación se levanta. La comprobación funcional deja dos hechos pendientes para la siguiente tarea: la transacción existe en `marketplace_ledger_v1`, no tiene fila clasificada y la API retorna cero filas. Esto no se declara todavía como el primer quiebre de la cadena, porque `RAW → Registry → Ledger` deberá demostrarse secuencialmente antes de avanzar. Su corrección no forma parte de TRUTH-003.
