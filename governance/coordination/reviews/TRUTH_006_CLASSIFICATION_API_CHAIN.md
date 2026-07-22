# TRUTH-006 — CLASIFICACIÓN Y EXPOSICIÓN API DE TRANSACCIÓN CONTROLADA ML

## Veredicto

`TRUTH006_ABORTED_NO_CHANGES`

La puerta de entrada Registry → Ledger no cumple el detalle exacto autorizado. La clasificación y la consulta HTTP no fueron ejecutadas.

## 1. Evidencia Registry y Ledger

### Registry certificado

| Campo | Valor observado |
|---|---|
| Archivo | `ML_Facturacion_2026-07_TRUTH005_FINAL.xlsx` |
| SHA-256 | `8B030937040D6BB82B25D51E6C3FAB15EC8FBF85A430CD3BC32FF49DB2FCFCF1` |
| `execution_id` | `09f538db-5471-462f-b520-ee05f067a679` |
| Estado | `COMPLETED` |
| Marketplace | `ML` |
| Documento | `facturacion` |
| Periodo | `2026-07` |
| `records_new` | `1` |

### Ledger

| Campo | Esperado | Observado |
|---|---|---|
| `id_transaccion` | `CHG_ML_Facturacion_2026-07_TRUTH005_FINAL.xlsx_1` | coincidente |
| Marketplace | `ML` | `ML` |
| Fecha/periodo | `2026-07-01` / `2026-07` | coincidente |
| Detalle | `Cargo por envíos de Mercado Libre` | `Cargo por env?os de Mercado Libre` |
| Monto | `-3150` | `-3150.0` |
| Folio | `033-TRUTH005-0001` | coincidente |
| `execution_id` | `09f538db-5471-462f-b520-ee05f067a679` | coincidente |
| Clasificaciones existentes | `0` | `0` |

La diferencia de detalle es material y reproducible:

- carácter esperado: `í`, U+00ED, decimal 237;
- carácter almacenado: `?`, U+003F, decimal 63;
- igualdad exacta: `false`.

El XLSX físico autorizado también contiene U+003F. Por tanto, la diferencia fue introducida al construir el fixture TRUTH-005, antes de la ingestión; no es un defecto de representación de DuckDB ni de la salida de terminal.

Corregir el XLSX cambiaría necesariamente su SHA-256 y dejaría de ser el archivo autorizado por TRUTH-006. No se reconstruyó ni sustituyó el fixture.

## 2. Regla de clasificación encontrada

La regla financiera sí existe y precede a TRUTH-006, pero no es aplicable mediante coincidencia exacta al detalle corrupto.

| Propiedad | Evidencia |
|---|---|
| Motor canónico | `MarketplaceAuditorEngine.run_classification()` |
| Archivo | `engine/v4/marketplace_auditor.py` |
| Fuente | `marketplace_ledger_v1` |
| Resultado | `marketplace_ledger_clasificado_v1`, con propagación posterior a `marketplace_ledger_v1` |
| Patrón | coincidencia normalizada exacta de `Cargo por envíos de Mercado Libre` |
| Definición Python | `RAW_TO_CLASSIFICATION_MAP`, línea 15 |
| Grupo | `FINANCIAL_STRUCTURE["costos_operacionales"]`, línea 301 |
| Clasificación | `Cargo por envíos de Mercado Libre` |
| `financial_group` | `costos_operacionales` |
| Prioridad | coincidencia atómica antes de reglas dinámicas y fallback |
| Origen esperado | `atomic_match` |
| Confianza esperada | `1.0` |
| P&L | incluido (`true`) |
| SIGNAL/NOISE | `SIGNAL` |
| Taxonomía | `KnowledgeBase/Marketplace/Taxonomy/ml_v1.json`, versión `1.0` |
| Regla declarativa | `taxonomy/taxonomy_rules.yaml`, orden de grupo `30` |
| Mapping declarativo | `taxonomy/taxonomy_mappings.yaml`, líneas 13–15 |

Procedencia:

- la regla Python exacta está presente desde `67e5e0e0c2d74a9131ded4ccaa32617fe0e6d958` (`BASELINE_V6`, 2026-05-30);
- `taxonomy_mappings.yaml` está registrado antes de TRUTH-006 en `992e10ba6e16e314076238718d6a7cd313e22568`;
- `KnowledgeBase/Architecture/CONCEPT_REGISTRY_V2.md:71` registra el concepto como `ROOT_EVENT`, `ACCRUAL`, `INCLUDE`, `PRESERVE` y certificado;
- `tests/test_financial_engine.py:42` respalda el mapeo del detalle a `Logística`;
- `tests/test_operational_pnl.py:31` contiene el detalle ML como caso operacional;
- los golden files ML contienen el mismo detalle bajo `costos_operacionales`.

No se creó ni modificó ninguna regla o taxonomía.

## 3. Motivo de detención

TRUTH-006 ordena detenerse sin ejecutar clasificación cuando Registry y Ledger no coinciden con la entrada esperada. La identidad criptográfica autorizada corresponde al fixture que contiene `?`, mientras la regla certificada requiere `í`.

No se permite resolver esta diferencia mediante:

- fuzzy matching;
- heurística;
- sustitución automática `? → í`;
- nueva regla financiera;
- modificación del RAW controlado conservando falsamente su SHA;
- clasificación como `NO_CLASIFICADO` para continuar la cadena.

## 4. Ejecución aislada

No ejecutada.

- No se creó una nueva candidata de clasificación.
- No se invocó `SurgicalLoader`.
- No se invocó `run_classification()`.
- No se escribió `marketplace_ledger_clasificado_v1`.
- No se ejecutaron auditoría, cierres, DTE, settlement ni banco.

El clasificador actual es global: comienza eliminando toda `marketplace_ledger_clasificado_v1` y vuelve a materializar desde todo `marketplace_ledger_v1`. Aunque esto requeriría un mecanismo acotado para una futura ejecución controlada, TRUTH-006 no autorizaba implementarlo después de fallar la puerta de entrada.

## 5. Control de impacto

No hubo clasificación ni mutación de la copia temporal durante TRUTH-006. La única lectura fue mediante `duckdb.connect(..., read_only=True)`.

No existe variación agregada de `-3150` porque no se materializó clasificación.

## 6. Contrato real de API

Diagnóstico estático, sin arranque ni solicitud HTTP:

| Campo | Contrato observado |
|---|---|
| Ruta | `/api/v4/ledger` |
| Método | `GET` |
| Parámetro transaccional público | `order_id` |
| Semántica | `(id_transaccion = ? OR id_orden = ?)` |
| Marketplace | `marketplace`, por defecto `ML` |
| Periodo | `periodo`; no se aplica cuando se entrega `order_id` |
| Fuente | `marketplace_ledger_v1` |
| Filtro clasificación | opcional por `financial_group` y `clasificacion_operativa` |
| SIGNAL/NOISE | filtros operacionales inyectados por `get_operational_filters()`; el endpoint no ofrece parámetro `signal_mode` |
| Filtro monto cero | activo por defecto |
| Respuesta | objeto con `data`, `total_count`, `total_sum`, `offset`, `limit`, `detalles` |

La API no fue consultada porque hacerlo habría evaluado un enlace posterior a una puerta de entrada fallida. No se emitió HTTP status, cuerpo ni hash de cuerpo.

## 7. Pruebas focalizadas

No se añadieron ni modificaron pruebas. TDD no se inició porque la regla de detención prohibió implementar una corrección.

Comprobaciones read-only ejecutadas:

```powershell
Get-FileHash data\db\meli_financial_v4.db -Algorithm SHA256
Get-FileHash data\db\BASELINE_ESTABLE_V9_TRUTH_RECOVERED\meli_financial_v4.db -Algorithm SHA256
```

```python
duckdb.connect(
    r"C:/tmp/TRUTH_005_CONTROLLED/truth005_v9_working_final.duckdb",
    read_only=True,
)
```

Se consultaron Registry, Ledger y conteo clasificado por `id_transaccion`. También se compararon los puntos de código Unicode del detalle esperado y observado.

## 8. Protección del baseline

| Baseline | SHA-256 antes | SHA-256 después |
|---|---|---|
| DB oficial | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` |
| V9 | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` | `C76C3FEE51C31949571F829DA6043F1682023DC39F5B093F7AF794654DBF6FCE` |

- Ausencia de escrituras en ambas DB.
- Ausencia de promoción de candidata.
- Ausencia de ejecución de cierres, auditoría y DTE.
- La transacción histórica `LEGACY_PROVENANCE_GAP` no fue alterada.

## 9. Diff y commit

No hubo corrección de código, taxonomía, prueba ni DB. No se creó commit TRUTH-006.

El único archivo creado es este informe.

## 10. Limitación pendiente

Para reabrir la cadena, el propietario debe autorizar una nueva identidad controlada:

1. fixture XLSX construido con U+00ED real;
2. nuevo SHA-256 físico;
3. nueva ejecución Registry `COMPLETED`;
4. nueva transacción ledger vinculada;
5. verificación exacta del detalle antes de clasificar.

Solo después puede evaluarse una clasificación acotada y la exposición HTTP.

`TRUTH006_ABORTED_NO_CHANGES`
