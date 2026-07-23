# CAP-F5-05 SURGICAL FIX

## REGLAS APLICADAS
- Mínima y localizada.
- Reproducible y reversible.
- Cero modificaciones a lógica financiera o cálculos.

## CORRECCIONES REALIZADAS

### 1. Manejo Idempotente de Registro de Archivos
**Archivo:** engine/v4/database.py (Línea 211)
**Cambio:** 
Se reemplazó INSERT INTO file_registry por INSERT OR REPLACE INTO file_registry.
**Motivo:** Esto previene que retries válidos gestionados por el IngestionOrchestrator sufran crashers por Primary Key Violations, permitiendo que el orquestador maneje los duplicados basándose en su estado status = 'COMPLETED'.

### 2. Idempotencia en Inserción del Ledger
**Archivo:** engine/v4/surgical_loader.py (Línea 241)
**Cambio:**
Se agregó la eliminación condicional de los registros asociados al mismo archivo justo antes de la inserción.
`python
self.db.execute("DELETE FROM marketplace_ledger_v1 WHERE archivo_origen = ?", [f.name])
`
**Motivo:** Garantiza que si el loader se ejecuta nuevamente como parte de un proceso de Recovery tras un fallo en las etapas posteriores (Certificación, API o Dashboard), el Ledger no duplique la información, manteniendo la integridad financiera intacta.

## RESULTADO
El pipeline ahora se comporta de manera totalmente transaccional e idempotente, logrando procesar archivos que sufrieron fallos parciales sin contaminar la fuente oficial de verdad financiera.
