# POST-FIX DASHBOARD CERTIFICATION

**Fecha:** 2026-06-06  
**Auditor:** Sistema

---

## Arquitectura Dashboard → API → DB

```
Dashboard (HTML/JS)
    │
    │  HTTP GET /api/v4/cierre/*
    │  HTTP GET /api/v4/exec/*
    ▼
API (FastAPI Router)
    │
    │  SQL direct → marketplace_cierre_financiero_v1
    │  SQL direct → marketplace_ledger_clasificado_v1
    ▼
DB (DuckDB) — data/db/meli_financial_v4.db
```

---

## Preguntas de certificación

### 1. ¿El dashboard consume los cierres regenerados?

**SÍ.** Ambos dashboards consumen API endpoints que consultan directamente `marketplace_cierre_financiero_v1`:

- `templates/dashboard.html` → `/api/v4/cierre/*`
- `templates/executive_dashboard.html` → `/api/v4/cierre/*` + `/api/v4/exec/*`

Los endpoints no tienen referencia a tablas intermedias ni vistas materializadas. La consulta es directa a la tabla de cierre.

### 2. ¿Existe caché?

**NO.** No se detecta caché en ninguno de los dashboards ni en los endpoints de API:
- Los templates HTML no contienen lógica de caché
- Los endpoints API no tienen decoradores de caché ni almacenamiento intermedio
- No hay Redis, memcached, ni archivos de caché en el proyecto
- Cada request ejecuta SQL contra DuckDB

### 3. ¿Existe tabla intermedia?

**NO.** El flujo es directo:

```
marketplace_cierre_financiero_v1
    ↓ (SQL query)
API response (JSON)
    ↓ (HTTP)
Dashboard (Chart.js / HTML)
```

No hay ETL intermedio entre el cierre y la presentación.

### 4. ¿Existe riesgo de mostrar datos antiguos?

**BAJO.** Sin caché ni tabla intermedia:
- Cada request refleja el estado actual de la DB
- Si la DB fue regenerada (como en este post-fix), el dashboard refleja inmediatamente los nuevos datos
- No hay ventana de inconsistencias

**Riesgo identificado:** Si la aplicación se ejecuta con hot-reload desactivado, el servidor puede mantener una conexión DuckDB que apunte a un snapshot anterior. Sin embargo, esto es propio del ciclo de vida del servidor, no del dashboard.

---

## Archivos verificados

| Archivo | ¿Consume cierre? | Cache | Tabla intermedia | Riesgo |
|---|---|---|---|---|
| `templates/dashboard.html` | ✅ Vía API | No | No | Bajo |
| `templates/executive_dashboard.html` | ✅ Vía API | No | No | Bajo |
| `api/api.py` | ✅ SQL directo | No | No | Bajo |

---

## VEREDICTO: PASS

- Dashboard consume cierre regenerado: **SÍ**
- Riesgo de datos antiguos: **BAJO** (sin caché, sin tabla intermedia)
- Reflejo inmediato del fix en la UI
- Sin cambios requeridos en frontend
