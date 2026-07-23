# CAP-F5-05 ROOT CAUSE ANALYSIS

## ESCENARIOS AFECTADOS
R4, R5, R6, R7 resultaron en FALLA durante el proceso de Recovery.

## COMPARACIÓN ANTES VS DESPUÉS DE RECOVERY (CASO R5)
| Componente | Antes del Fallo | Después del Recovery (Antes del Fix) | Status |
|------------|-----------------|--------------------------------------|--------|
| Registry | Hash Válido | FAILED (por Duplicate File) | FALLA |
| Ledger | Hash Válido (Datos en tabla) | Ledger con datos duplicados o estancados | FALLA |
| Classification | N/A (Fallo posterior) | No ejecutada | FALLA |
| Certification | N/A | No ejecutada | FALLA |

## IDENTIFICACIÓN DE LA CAUSA RAÍZ
Se detectaron dos problemas estructurales complementarios que rompían la idempotencia y la capacidad de recuperación del sistema:

1. **Bloqueo prematuro por Primary Key (ile_registry)**: 
   PersistenceEngine escribía el hash del archivo en la tabla ile_registry antes de insertar los datos en el ledger usando un INSERT INTO directo. Si el pipeline fallaba posteriormente (ej: R5, R6, R7), este registro impedía cualquier reintento porque producía una violación de constraint de Primary Key, forzando a que el orquestador marcara el retry inmediatamente como FAILED.
   
2. **Duplicación de registros en Ledger por falta de Idempotencia**:
   Para aquellos escenarios donde el loader lograba ejecutarse en el retry (si no se bloqueaba por el error anterior), el método load_facturacion del SurgicalLoader realizaba un insert_df directo a marketplace_ledger_v1 sin antes purgar los registros previos pertenecientes a dicho archivo (rchivo_origen). Esto producía duplicación de registros financieros exactos para los escenarios que fallaron post-persistencia.

## CONCLUSIÓN
La falla no reside en el Financial Engine ni en la lógica contable, sino exclusivamente en el **tracking operacional de duplicados** y la falta de **idempotencia local a nivel de archivo** en la capa de persistencia del SurgicalLoader.
