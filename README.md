# Marketplace Financial AI Engine

## Ruta canonica

- Backend FastAPI: `Scripts\run_python.bat run_app.py`
- API base V4: `http://127.0.0.1:3001/api/v4`
- Arranque rapido Windows: `START_APP.bat`
- Frontend oficial: `http://127.0.0.1:3001/app` (servido server-side desde `templates/`)
- `START_APP.bat` inicia el backend con el wrapper oficial y abre la UI principal

## Estructura principal

- `01_Raw`: archivos fuente por marketplace y SAP (inmutable)
- `data/db/meli_financial_v4.db`: base de datos DuckDB oficial (unica fuente de verdad operacional)
- `api/api.py`: contrato API canonico (FastAPI, ~86 rutas bajo `/api/v4`)
- `engine/v4`: motores de la cadena financiera
- `templates/`: paneles servidos por el backend (`dashboard.html`, `executive_dashboard.html`, `documentary_dashboard.html`, `traceability.html`, `copilot.html`, `upload_center.html`)
- `frontend/shared/`: assets JS compartidos servidos en `/shared` (api_client.js, financial-formatter.js)
- `tests/`: suite de tests activa
- `tools/`: harness y scripts de validacion
- `knowledge/`: taxonomias certificadas y registros de conocimiento
- `evidence/`: evidencia de certificacion y baselines reproducibles

## Arquitectura financiera

```
Ledger
→ Classification
→ Truth
→ Reconciliation
→ Exception Engine
```

Cadena completa: `01_Raw → ETL → Ledger → Classification → Truth → Reconciliation → Exceptions → API → Dashboard`.

## Base de datos

- DB oficial: `data/db/meli_financial_v4.db` (DuckDB, read-only en runtime).
- No existe `antigravity_v4.db`: ya no forma parte del modelo.
- Contrato SQL = API = UI inmutables (regresion 14/14).

## Instalacion

```bash
py -m pip install -r requirements.txt
```

## Ejecucion

1. Backend:

```bash
Scripts\run_python.bat run_app.py
```

2. Abrir: `http://127.0.0.1:3001/app`

Las rutas de UI disponibles:

```text
/app            Marketplace Auditor (dashboard principal)
/exec           Reporte Gerencial Ejecutivo
/documentary  Documentary Dashboard
/traceability   Trazabilidad
/copilot        Copilot
/upload         Upload Center
```

## Runtime oficial

- Toda ejecucion Python soportada pasa por `Scripts\run_python.bat` (usa `.venv`).
- `run_app.py` es el entrypoint oficial del backend (uvicorn, puerto 3001).
- La DB oficial se abre en modo read-only el runtime.

## Scripts utiles

```bash
npm run test:all    # pytest tests/ -v --tb=short
npm run lint        # ruff check .
npm run typecheck   # mypy api/ engine/ --ignore-missing-imports
```

## Validacion

- CI: `.github/workflows/ci.yml` ejecuta lint, typecheck y pytest con `.venv` en Windows.
- `pytest tests/` cubre la suite completa (ver `evidence/production_baseline/tests_before.json`).

## Flujo operativo

1. Cargar archivos en `01_Raw`
2. Abrir el panel `/upload` para registrar ingestiones
3. Revisar KPIs en `/app` y `/exec`, excepciones y conciliaciones

## Certificacion electronica (regla fundamental)

```text
LEDGER_EXISTING  !=  CRYPTOGRAPHIC_CERTIFIED
```

Solo evidencia fiscal real (DTE SII indexado en `dte_truth_v1` con vinculo `dte_linked=1`) puede producir certificacion fiscal.
Las referencias de liquidacion Ripley (settlement) NUNCA se presentan como folio SII.

## Regla de orden

- La raiz debe contener solo entrypoints, configuracion y documentacion principal.
- Los scripts manuales (patch, fix, inject) que no forman parte del runtime se archivan bajo `_archive/` tras consolidacion.
- Todo script que pasa a ser parte del flujo productivo se migra a `engine/`, `api/` o `tests/`.