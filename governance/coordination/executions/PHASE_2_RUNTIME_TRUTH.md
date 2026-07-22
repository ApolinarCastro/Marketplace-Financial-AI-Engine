# PHASE 2 - RUNTIME TRUTH (CORRECTED)

Fecha de correccion: 2026-07-17  
Commit inspeccionado: `795124b77b036f970149bf298f59f14391af9041`  
Estado operativo: `PASS_WITH_OBSERVATIONS`  
Estado de certificacion: `NOT_CERTIFIED`

## Alcance

Correccion deterministica de los conteos y clasificaciones de Fase 2. No se modificaron la DB oficial, `BASELINE_ESTABLE_V7`, modulos legacy ni codigo financiero.

## 1. Rutas API

Comando reproducible:

```powershell
@'
import ast
from pathlib import Path
for name in ('api/api.py', 'api/knowledge_api.py'):
    tree = ast.parse(Path(name).read_text(encoding='utf-8'))
    routes = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for d in n.decorator_list if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr in {'get','post','put','patch','delete'}]
    print(name, len(routes))
'@ | .\.venv\Scripts\python.exe -
```

Resultado:

| Archivo | Rutas declaradas |
|---|---:|
| `api/api.py` | 29 |
| `api/knowledge_api.py` | 8 |
| **Total** | **37** |

Las ocho rutas del router de conocimiento son: `POST /consolidate`, `GET /status`, `GET /coverage-gaps`, `GET /audit-coverage`, `GET /retention-recs`, `GET ""`, `POST /export` y `GET /{knowledge_id}`. El prefijo efectivo es `/api/v4/knowledge`.

## 2. Pruebas

Comando reproducible:

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

Resultado observado el 2026-07-17:

```text
731 tests collected in 2.80s
```

Este es el unico total de pruebas vigente en el informe: **731 pruebas unicas recolectadas**. El resultado previamente registrado de la ejecucion de Fase 2, `700 passed, 21 skipped, 10 errors`, tambien suma 731. Se eliminan como invalidos los totales manuales 685 y 845. Los 10 errores corresponden a CAP-001 y fueron reproducidos de forma aislada como `fixture 'isolated_app' not found`; no constituyen pruebas ejecutadas del pipeline.

## 3. Modulos de `engine/v4`

Comando base reproducible:

```powershell
(Get-ChildItem engine\v4 -Directory | Where-Object Name -ne '__pycache__').Count
```

Resultado: **19 subdirectorios fuente**. `__pycache__` es un artefacto generado y no se cuenta.

La clasificacion se obtuvo buscando imports o referencias desde `api/`, `engine/` y `tools/`, excluyendo autorreferencias del propio subdirectorio y pruebas:

| Clasificacion | Cantidad | Subdirectorios |
|---|---:|---|
| ACTIVE | 10 | `certification`, `copilot`, `domain`, `evidence`, `ingestion`, `intelligence`, `knowledge`, `reconciliation`, `security`, `sql` |
| LEGACY | 0 | Ninguno demostrado en el arbol actual |
| ORPHAN | 9 | `benchmarks`, `closing`, `contracts`, `etl`, `explainability`, `golden`, `lineage`, `observability`, `registry` |
| **Total** | **19** | **19** |

`data_quality`, `production` y `scorecard`, citados en la version anterior, no existen como subdirectorios actuales de `engine/v4`; por tanto no pueden contarse como LEGACY.

## 4. ClosingEngine

Comando reproducible:

```powershell
rg -n "ClosingEngine|engine\.v4\.closing" api engine tools tests
```

Consumidores encontrados: export interno en `engine/v4/closing/__init__.py` y pruebas en `tests/test_closing.py`. No existe consumidor de produccion en `api/`, otro motor activo o `tools/`. En consecuencia, `ClosingEngine` se clasifica **solo como ORPHAN**, no como ACTIVE.

## 5. Evidence Orchestrator y SQL

Comandos reproducibles:

```powershell
rg -n -i "select|insert|update|delete|execute\(|query\(|duckdb|sql" engine\v4\evidence
rg -n -C 5 "evidence/coverage|evidence/gaps" api\api.py
```

Resultado:

- Los endpoints `/api/v4/evidence/coverage` y `/api/v4/evidence/gaps` no contienen SQL inline; construyen `EvidenceOrchestrator` y delegan a `get_coverage()` y `get_gaps()`.
- `EvidenceOrchestrator` no define SQL ni formulas financieras propias.
- Sus dependencias `FinancialEngine`, `LedgerEngine`, `ReconciliationEngine` y `CertificationEngine` si realizan consultas de lectura para obtener ledger, cierres, auditoria y cobertura.
- Esas lecturas no equivalen a calculos financieros duplicados en el orquestador.

Por tanto, la afirmacion corregida es: **cero SQL inline y cero calculo financiero en Evidence Orchestrator; existen consultas de lectura delegadas a motores canonicos**.

## 6. Registry

`governance/coordination/coordination_registry.json` conserva estructura, permisos y contenido funcional. Solo se actualizo `generated_at` para reflejar esta correccion.

## 7. Gate de Fase 2

| Criterio | Resultado |
|---|---|
| Rutas API | 37, conteo AST reproducible |
| Pruebas | 731 recolectadas; 700 PASS + 21 SKIP + 10 ERROR registrados |
| Modulos | 19 clasificados sin doble conteo |
| ClosingEngine | ORPHAN exclusivamente |
| Evidence Orchestrator | Sin SQL inline; lecturas delegadas distinguidas de calculos |
| DB oficial | No modificada durante la correccion |

**PHASE_2_CORRECTED**  
**PHASE_3_AUTHORIZED**

La autorizacion de Fase 3 no certifica CAP-001. CAP-001 requiere 10/10 PASS en entorno aislado, pipeline real verificable y hash identico de la DB oficial antes y despues.


## 8. Ejecucion inicial de Fase 3 - CAP-001

Comando reproducible ejecutado fuera del sandbox por restricciones ACL del basetemp de pytest:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_upload_center_e2e.py -q -p no:cacheprovider --basetemp "tests\.pytest-tmp-cap001-<execution>"
```

Resultado:

```text
..........                                                               [100%]
10 passed in 8.77s
```

Aislamiento verificado:

- DatabaseV4 se redirige a una DuckDB nueva bajo tmp_path.
- api.api.UPLOAD_DIR se redirige a tmp_path/uploads.
- KnowledgeIndexer.DEFAULT_PATH se redirige a tmp_path/knowledge_index.yaml.
- Los directorios temporales de pytest fueron eliminados despues de la ejecucion.
- Hash SHA-256 de data/db/meli_financial_v4.db antes y despues: 804B5B822940EF6EB637DFDBA1814AB4EB78C38572AC3ACEFE9CE99FF8F1F06B.

Limitacion de evidencia: SurgicalLoader fue simulado deliberadamente para no ejecutar loaders ni logica financiera protegida. El orquestador y los handlers de las seis etapas se ejecutaron contra la DB temporal, pero la persistencia financiera real no fue ejecutada. Por ello CAP-001 queda **VALIDATED / NOT_CERTIFIED**, no VERIFIED ni CERTIFIED.
