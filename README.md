# Marketplace Conciliacion V4

## Ruta canonica

- Backend FastAPI: `Scripts\run_python.bat run_app.py`
- Frontend React/Vite: `cd src/frontend && npm run dev`
- API base V4: `http://127.0.0.1:3001/api/v4`
- Arranque rapido Windows: `START_APP.bat`
- Frontend oficial: `http://127.0.0.1:3001/app`
- Legacy HTML: `http://127.0.0.1:3001/legacy`
- `START_APP.bat` inicia el backend con el wrapper oficial y abre la UI principal

## Estructura principal

- `01_Raw`: archivos fuente por marketplace y SAP
- `02_Curated/Antigravity_V4_Reports`: reportes exportados por el motor V4
- `04_Conciliaciones`: datasets parquet de salida
- `api/api.py`: contrato API canonico para la app
- `engine/v4`: motor de ingestion, conciliacion, excepciones y reporting
- `src/frontend`: panel operativo React
- `analysis/`: analisis puntuales y generacion de artefactos auxiliares
- `legacy/`: entrypoints y prototipos archivados para referencia
- `tests/test_api_smoke.py`: verificacion minima del contrato API

## Raiz minima

- La raiz operativa debe contener solo entrypoints vigentes, configuracion y documentacion principal.
- El runtime oficial en raiz es `run_app.py`, `START_APP.bat`, `package.json`, `requirements.txt` y documentacion.
- Los prototipos retirados de servicio fueron movidos a `legacy/root_legacy/`.

## CLI de pipeline

- El entrypoint del pipeline operativo es `Scripts/pipeline_cli.py`.
- `npm run pipeline` ejecuta ese CLI con el wrapper oficial.

## Base de datos V4

- La base oficial del motor V4 vive en `data/db/antigravity_v4.db`.
- Si existe una base anterior en `database/antigravity_v4.db`, el motor la migra automaticamente a `data/db/` cuando puede.

## Instalacion

```bash
py -m pip install -r requirements.txt
cd src/frontend
npm install
```

## Ejecucion

1. Backend:

```bash
Scripts\run_python.bat run_app.py
```

2. Frontend:

```bash
cd src/frontend
npm run dev
```

El frontend usa proxy a `127.0.0.1:3001`, por lo que no necesita URLs hardcodeadas. El contrato oficial del panel React es `api/v4`.

Si existe build en `src/frontend/dist`, el backend sirve esa UI en `/app`. El dashboard HTML heredado queda disponible en `/legacy`.

## Runtime oficial

- Toda ejecucion Python soportada pasa por `Scripts\run_python.bat`.
- `run_app.py` es el entrypoint oficial del backend.
- V3 legacy queda fuera del arranque principal y solo debe habilitarse con `ENABLE_LEGACY_V3=1`.
- Los endpoints legacy en `/api/*` se mantienen temporalmente como aliases de compatibilidad.

## Scripts utiles

```bash
npm run server
npm run frontend
npm run build:frontend
npm run check:python
npm run pipeline
npm run smoke
npm run test:engine
npm run test:etl
npm run test:integration
npm run test:all
```

## Validacion recomendada

- `npm run check:python`: confirma que el proyecto esta usando `.venv` y que las dependencias Python criticas estan disponibles.
- `npm run test:all`: ejecuta chequeo de entorno, smoke API, tests del motor, tests ETL, integracion y build del frontend.
- CI: el workflow de `.github/workflows/ci.yml` ejecuta esa misma validacion en Windows.

## Flujo operativo

1. Cargar archivos en `01_Raw`
2. Abrir el panel y ejecutar `Pipeline V4`
3. Revisar KPIs globales, conciliacion por orden, excepciones y reportes exportados

## Regla de orden

- La raiz debe contener solo entrypoints, configuracion y documentacion principal.
- Los scripts manuales nuevos deben entrar en areas auxiliares y no en el flujo productivo por defecto.
- Si un script pasa a ser parte del flujo productivo, debe migrarse a `engine/`, `api/` o `tests/`.
