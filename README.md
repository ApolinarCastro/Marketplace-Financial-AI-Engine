# Marketplace Conciliacion V6

## Ruta canonica

- Backend FastAPI: `Scripts\run_python.bat run_app.py`
- API base V4 (frozen): `http://127.0.0.1:8004/api/v4`
- Arranque rapido Windows: `START_APP.bat`
- Dashboard: `http://127.0.0.1:8004/`
- `START_APP.bat` inicia el backend con el wrapper oficial y abre la UI principal

## Estructura principal

- `api/api.py`: contrato API canonico (FastAPI, endpoints /api/v4/*)
- `engine/v4`: motor de ingestion, clasificacion financiera, cierres y auditoria
- `tests/`: test suite (14 regression tests, smoke, ML audit, classification)
- `governance/`: freeze, baseline, estrategia git, matriz de remediacion
- `01_Raw`: archivos fuente por marketplace y XML DTE
- `data/db/`: base de datos DuckDB + snapshots de baseline

## Raiz minima

- La raiz operativa debe contener solo entrypoints vigentes, configuracion y documentacion principal.
- El runtime oficial en raiz es `run_app.py`, `START_APP.bat`, `config.py`, `requirements.txt`.
- Scratch code y prototipos retirados estan excluidos via .gitignore.

## CLI de pipeline

- El entrypoint del pipeline operativo es `Scripts/pipeline_cli.py`.

## Base de datos V6

- Base oficial: `data/db/meli_financial_v4.db` (DuckDB)
- Snapshot oficial: `data/db/snapshot_baseline_v6_20260529_105928/`
- SHA256: `e1e341ef44e0a61c4e846d34e05d14a4c291dcd904869f20fdf6e9a37fef1c29`
- Rows: 414,314 | SUM: $1,507,835,610

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

El dashboard HTML se sirve en `/` desde `templates/dashboard.html`. No hay frontend React en V6.

## Runtime oficial

- `run_app.py` es el entrypoint oficial del backend (FastAPI + uvicorn).
- Puerto: 8004 (configurado en `config.py`).
- Legacy endpoints V3 desactivados.

## Comandos

```bash
python run_app.py                  # Iniciar API
START_APP.bat                      # Inicio rapido Windows
pytest tests/ -v --tb=short        # Ejecutar tests (14 regression)
.\.venv\Scripts\python.exe -m pytest tests/ -v --tb=short
```

## Baseline V6 — Estado

- **Baseline**: BASELINE_ESTABLE_V6 (CURRENT_STABLE)
- **Freeze**: ACTIVO — ver `governance/FREEZE_ACTIVO.txt`
- **Git**: Inicializado con tag `BASELINE_V6`
- **CI/CD**: `.github/workflows/ci.yml` — requiere DB snapshot para CI (trabajo en progreso)
- **Tests**: 14/14 regression tests PASS

### Baseline anteriores
- V5 (SUPERSEDED, 2026-05-29) — snapshot en `data/db/snapshot_baseline_v5_20260529_094539/`
- V4-V1 (SUPERSEDED) — snapshots preservados en `data/db/`

## Contratos inmutables (FREEZE)

DB clasifica → API expone → UI renderiza.
Nadie más interpreta.

Ver `governance/FREEZE_ACTIVO.txt` — Regla 3 para detalle completo.

## Baseline historica

| Baseline | Fecha | Rows | SUM | Estado |
|---|---|---|---|---|
| V6 | 2026-05-29 | 414,314 | $1,507,835,610 | CURRENT_STABLE |
| V5 | 2026-05-29 | 414,183 | $1,505,252,594 | SUPERSEDED |
| V4 | 2026-05-28 | — | — | SUPERSEDED |
| V3 | 2026-05-28 | — | — | SUPERSEDED |
| V2 | 2026-05-28 | — | — | SUPERSEDED |
