# FAILURE LIBRARY

## FAIL-001: EXECUTION_TRANSPORT_FAILURE

**Fecha**: 2026-10-06
**Status**: RESOLVED

### Task State
```
STATUS = FAIL
FAILURE_CLASS = EXECUTION_TRANSPORT_FAILURE
ROOT_CAUSE_CANDIDATE = POWERSHELL_COMMAND_STRING_INTERPRETATION
REPEATED_ATTEMPTS_WITHOUT_NEW_EVIDENCE = TRUE
```

### Contexto
- **Objetivo**: Agregar `"DESTRUCTIVE_GIT"` a `GATE_TYPES` en `engine/loop_control/constants.py`
- **Método fallido**: Intentar crear archivos `.py` vía PowerShell (here-strings, base64, `python -c`)
- **Causa raíz**: PowerShell no interpreta correctamente los comandos con caracteres especiales, comillas anidadas, y saltos de línea dentro de strings

### Solución aplicada
- **Método**: Usar herramienta nativa `edit` de OpenCode directamente sobre el archivo físico
- **Archivo**: `engine/loop_control/constants.py` (línea 89)
- **Cambio**: Agregar `"DESTRUCTIVE_GIT",` a la tupla `GATE_TYPES`
- **Verificación**: Lectura posterior confirmó contenido correcto
- **Tests**: 53/55 PASS (2 failures pre-existing, 0 regresiones)

### Criterio PASS
```
FILE_CREATED = TRUE (editado exitosamente)
FILE_CONTENT_VERIFIED = TRUE (lectura posterior correcta)
PYTHON_EXIT_CODE = 1 (2 tests pre-existing fallan, no relacionados)
EXPECTED_OUTPUT = ACTUAL_OUTPUT (53/55 PASS, 0 regresiones por el cambio)
```

### Lección aprendida
> **Nunca transportar código Python dentro de comandos PowerShell.**
> Usar siempre las herramientas nativas de OpenCode (`write`, `edit`) para crear/modificar archivos.
