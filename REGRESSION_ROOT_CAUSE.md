# REGRESSION ROOT CAUSE

La regresión se produjo por la introducción no probada de dos alteraciones críticas posteriores al commit `0f71cc4`:

1. **Interrupción Intencional de Certificación (Mocking Invasivo)**:
   Se añadió en `api/api.py` el endpoint `/api/v4/electronic_certification/status/{transaction_id}` que contenía:
   ```python
   if doc.get("estado_xml") in ("CONCILIADO", "DOCUMENTADO"):
       response.status_code = 409
       return {"status": "BLOCKED", "reason": "BACKEND_CONTRACT_INCOMPLETE"}
   ```
   Esto rompía por diseño cualquier intento del frontend de mostrar certificaciones exitosas, en un aparente intento de pausar el desarrollo, lo cual derivó en una regresión sistémica.

2. **Mutilación del Frontend HTML**:
   En el archivo `templates/dashboard.html`, la lógica de renderizado asíncrono y resolución de dependencias del Drawer (apertura/cierre y pintado de Evidencias) fue alterada severamente, resultando en `undefined` errors que detenían la ejecución de JavaScript de renderización (Skeletons/Loading Infinito).

**Solución**: Los bloques problemáticos han sido removidos restaurando la versión `CERTIFIED_BASELINE_V1`.
