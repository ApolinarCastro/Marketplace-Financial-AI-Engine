# F5-06: Production Hardening

Este plan aborda los seis puntos solicitados para preparar el sistema para operación segura y continua en producción, sin modificar la lógica financiera.

## User Review Required
> [!WARNING]
> La modificación de cómo se instancia DatabaseV4 en pi.py (usando ead_only=True) es fundamental dado que DuckDB solo permite un escritor concurrente. Esto garantizará que la API nunca bloquee procesos de ingesta.

## Proposed Changes

---
### 1. Configuración (Limpieza de Rutas Absolutas)
Se eliminarán las rutas absolutas (C:\Users\ASUS Zenbook\...) que atan el código al entorno de desarrollo local. Se usarán rutas relativas al PROJECT_ROOT o Path(__file__).

#### [MODIFY] engine/v4/surgical_loader.py
Reemplazar ROOT = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine") por rutas relativas.

#### [MODIFY] engine/v4/surgical_xml_justifier.py
Reemplazar ROOT = Path(r"...") por resolución relativa basada en el directorio del script.

#### [MODIFY] engine/v4/xml_matcher.py y engine/v4/dte_indexer.py
Reemplazar cadenas hardcodeadas absolutas por construcciones con Path.

---
### 2. Seguridad Operativa (DB Read-Only para API)
La API debe funcionar estrictamente en modo lectura para proteger la base de datos oficial y permitir concurrencia con los workers de ingesta.

#### [MODIFY] pi/api.py
Ajustar la instanciación de la base de datos de V4:
`python
db = DatabaseV4(db_path=Path("data/db/meli_financial_v4.db"), read_only=True)
DatabaseV4._instance = db
`

---
### 3. Manejo de Errores y Salud del Sistema
Se incorporarán 	ry...except estructurados en los endpoints y en el orquestador para registrar el contexto real del fallo (trazas de pila) en lugar de silenciarlos, y devolver respuestas HTTP estandarizadas en caso de degradación (e.g. 503).

#### [MODIFY] engine/v4/ingestion/orchestrator.py
Añadir logger.error("Exception in orchestrator", exc_info=True) en el bloque catch principal para garantizar trazabilidad de los fallos (punto 5).

#### [MODIFY] pi/api.py
Crear un manejador global de excepciones o envolver endpoints clave para retornar HTTPException(status_code=500) y loguear el error con contexto, asegurando que el Dashboard maneje respuestas no-200.

---
### 4. Observabilidad y Trazabilidad
Validar que Marketplace Auditor v3.5 y Reporte Gerencial UX1.2 utilicen datos en tiempo real de V4.
Añadir validaciones menores en pi.py para asegurar consistencia del estado de reportes, incluyendo validación del estado del motor en GET /api/v4/health (si no existe, crearlo) para chequeos de readiness/liveness.

## Verification Plan

### Automated Tests
- Se correrán las suites existentes (127/127) para garantizar cero regresiones funcionales:
  python -m pytest tests/ -p no:cacheprovider
  
### Manual Verification
- Validar inicialización de pi.py para confirmar que DuckDB arranca en modo ead_only=True.
- Intentar procesar un archivo inválido y confirmar que el log ahora contiene la traza completa (exc_info).
