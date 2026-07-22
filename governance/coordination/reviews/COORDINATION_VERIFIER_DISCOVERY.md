# Coordination Verifier Discovery

Tarea: `GOV-R001`  
Modo: `READ-ONLY` (única escritura autorizada: este informe)  
Fecha: `2026-07-14`

## 1. Archivos inspeccionados

Se leyeron íntegramente los ocho archivos exigidos:

- `tools/verify_coordination_interface.py`
- `tests/test_coordination_interface.py`
- `tools/install_coordination_hook.ps1`
- `.claude/commands/agents/agent-coordination.md`
- `.claude/helpers/swarm-hooks.sh`
- `governance/coordination/COORDINATION_CONTRACT.md`
- `governance/coordination/coordination_registry.json`
- `governance/coordination/coordination_state.json`

Para determinar activación y referencias también se inspeccionaron, sin modificarlos: `.claude/settings.json`, `.claude/helpers/hook-handler.cjs`, `.claude/helpers/swarm-comms.sh`, `.claude-flow/config.yaml`, `.claude-flow/swarm/swarm-state.json`, `.mcp.json`, `.githooks/pre-commit`, `.github/workflows/ci.yml`, `AGENTS.md`, `CLAUDE.md` y los índices de `.claude/commands/agents/`.

Reproducción observada:

- `python tools/verify_coordination_interface.py`: `FAIL`, reproducible en 115.5 segundos.
- `pytest tests/test_coordination_interface.py`: `6 passed in 0.34s`, usando un directorio temporal fuera del repositorio.

## 2. Clasificación por archivo

| Archivo | Clasificación | Evidencia | Riesgo | Decisión propuesta |
|---|---|---|---|---|
| `governance/coordination/COORDINATION_CONTRACT.md` | CANONICAL_INTERFACE | Declara `governance/coordination/` como única interfaz y define fuentes canónicas. | Bajo | Conservar como autoridad contractual. |
| `governance/coordination/coordination_registry.json` | CANONICAL_INTERFACE | Define raíz única, inventario canónico, rutas protegidas y comando de verificación. | Bajo | Conservar como registro canónico. |
| `governance/coordination/coordination_state.json` | CANONICAL_INTERFACE | Contiene propietario, objetivo, handoff, bloqueos y estado operacional activo. | Bajo | Conservar como única ubicación de estado activo. |
| `tools/verify_coordination_interface.py` | AUTHORIZED_SUPPORT | Valida registry, state, board, referencias y rutas protegidas; no persiste estado de coordinación. Se auto-detecta porque contiene las expresiones que busca. | Medio | Autorizar por ruta y función; no excluirlo de controles estructurales propios. |
| `tests/test_coordination_interface.py` | AUTHORIZED_SUPPORT | Usa repositorio temporal y fixtures para pruebas positivas y negativas. El texto `CURRENT_TASK` y las claves de state son datos de prueba, no estado activo. | Bajo | Autorizar como soporte de prueba y mantener aislamiento temporal. |
| `tools/install_coordination_hook.ps1` | AUTHORIZED_SUPPORT | Solo configura explícita e idempotentemente `core.hooksPath=.githooks`; no almacena tareas ni handoffs. La configuración local está actualmente ausente, por lo que el hook no está instalado. | Bajo | Autorizar por ruta; mantener instalación explícita. |
| `.claude/commands/agents/agent-coordination.md` | PARALLEL_COORDINATION_CHANNEL | Es un comando invocable que prescribe `npx claude-flow swarm init` con topologías jerárquica, mesh y adaptativa. Está indexado por tres documentos de comandos y el entorno habilita Claude Flow y equipos. | Alto | No convertirlo en allowlist. Requiere decisión formal de desactivar, retirar o subordinar el mecanismo al contrato canónico. |
| `.claude/helpers/swarm-hooks.sh` | PARALLEL_COORDINATION_CHANNEL | Escribe mensajes, agentes, consensos y handoffs en `.claude-flow/swarm/`; transmite decisiones, bloqueos, próximos pasos y contexto entre agentes; puede autoasignar continuidad mediante `pre-task`/`post-task`. | Crítico | Mantener el FAIL semántico. Requiere decisión formal antes de remediar el verificador. |
| `tests/__pycache__/test_coordination_interface*.pyc` | GENERATED_ARTIFACT | Bytecode derivado de pytest/Python; coincide solo por nombre. | Nulo | Excluir `__pycache__` del recorrido común. |
| `tools/__pycache__/verify_coordination_interface*.pyc` | GENERATED_ARTIFACT | Bytecode derivado del verificador; coincide solo por nombre. | Nulo | Excluir `__pycache__` del recorrido común. |
| `.claude-flow/swarm/swarm-state.json` | GENERATED_ARTIFACT | Registra una ejecución histórica de swarm con estado `terminated`, sin agentes ni tareas actuales. Demuestra uso previo del mecanismo, no actividad presente. | Alto como evidencia | No tratarlo como estado canónico ni ignorar su existencia al decidir sobre el canal paralelo. |

No se encontró base suficiente para clasificar los dos mecanismos `.claude` como `LEGACY_NON_OPERATIONAL`: la configuración que los rodea sigue habilitada. Tampoco queda un hallazgo principal en `INSUFFICIENT_EVIDENCE`.

## 3. Falsos positivos demostrados

### Búsqueda por nombre

`find_duplicate_coordination_channels()` recorre `root.rglob('*')` sin excluir artefactos generados y marca cualquier nombre que contenga `coordination`. Esto produce falsos positivos exactos sobre:

- `tests/test_coordination_interface.py`
- `tools/install_coordination_hook.ps1`
- `tests/__pycache__/test_coordination_interface.cpython-314-pytest-9.0.3.pyc`
- `tests/__pycache__/test_coordination_interface.cpython-314.pyc`
- `tools/__pycache__/verify_coordination_interface.cpython-314.pyc`

La coincidencia de `.claude/commands/agents/agent-coordination.md` no es un falso positivo demostrado: contiene instrucciones operacionales para iniciar coordinación paralela.

### Búsqueda de texto y autoescaneo

`find_forbidden_state_markers()` busca tokens aislados, sin distinguir declaración, fixture, prueba negativa o persistencia operacional. Esto marca falsamente:

- `tools/verify_coordination_interface.py`, porque define y usa los propios patrones `CURRENT_TASK`, `"handoff"`, `"next_actor"` y `"current_owner"`.
- `tests/test_coordination_interface.py`, porque construye un state temporal y contiene la prueba negativa `CURRENT_TASK = do something`.

La coincidencia de `.claude/helpers/swarm-hooks.sh` no es falsa: el archivo crea mensajes con tipo `handoff` y persiste handoffs, agentes, decisiones y próximos pasos fuera del canal canónico.

### Artefactos generados

El escaneo de contenido sí declara exclusiones, pero el escaneo por nombre no reutiliza esa política. Deben excluirse de ambos recorridos: `__pycache__`, `.pytest_cache`, `.mypy_cache`, `node_modules`, `.venv` y `.git`. El recorrido también debe evitar enlaces o rutas inaccesibles de forma determinística.

## 4. Canales paralelos reales

### `.claude/commands/agents/agent-coordination.md`

Sí contiene instrucciones operacionales activas para coordinar agentes. No guarda por sí mismo el estado, pero ordena inicializar swarms por comandos ejecutables y está ubicado en el árbol de comandos de Claude. Está referenciado por `README.md`, `agent-capabilities.md` y `agent-types.md`. Además, `.claude/settings.json` habilita Claude Flow, equipos, lista de tareas, buzón, autoasignación y memoria compartida.

### `.claude/helpers/swarm-hooks.sh`

Lee, escribe o transmite:

- tareas y sus resultados mediante `pre_task_swarm_context()` y `post_task_swarm_update()`;
- handoffs mediante `initiate_handoff()`, `accept_handoff()`, `complete_handoff()` y `get_pending_handoffs()`;
- agentes/propietarios operativos mediante `AGENT_ID`, `AGENT_NAME` y `agents.json`;
- próximo actor mediante `toAgent` en cada handoff;
- estado operacional mediante `status`, `blocked`, `nextSteps`, estadísticas y mensajes;
- decisiones entre agentes mediante `context.decisions` y consensos persistidos.

Todo se almacena fuera de `governance/coordination/`, principalmente en `.claude-flow/swarm/`. Por definición contractual, es un canal paralelo real aunque el único swarm observado esté terminado y vacío.

También existe `.claude/helpers/swarm-comms.sh`, no reportado por el verificador actual, que implementa colas, buzones, broadcast y consenso en la misma raíz paralela. Es evidencia adicional de que el detector actual tiene falsos negativos semánticos además de falsos positivos.

## 5. Referencias activas encontradas

- `.githooks/pre-commit` ejecuta el verificador y sus tests. `core.hooksPath` no está configurado localmente, por lo que hoy no está instalado.
- `.github/workflows/ci.yml` ejecuta el verificador, los tests de coordinación y luego la suite. Es configuración versionada de CI, aunque no se verificó ejecución remota.
- `.claude/commands/agents/{README.md,agent-capabilities.md,agent-types.md}` enlaza `agent-coordination.md`.
- `.claude/settings.json` tiene `CLAUDE_FLOW_HOOKS_ENABLED=true`, `claudeFlow.enabled=true`, equipos, task list, mailbox, autoasignación y namespace compartido habilitados.
- `.claude-flow/config.yaml` configura topología `hierarchical-mesh`, consenso y hooks con `autoExecute=true`; el MCP conserva `autoStart=false`.
- `.mcp.json` registra Ruflo/Claude Flow con `autoStart=false`.
- `AGENTS.md` y `CLAUDE.md` ordenan usar `hooks_route`, `swarm_init` y `agent_spawn` para trabajo complejo.
- No se encontró una referencia directa desde `.claude/settings.json`, `hook-handler.cjs`, `.mcp.json`, `AGENTS.md` o `CLAUDE.md` al nombre `swarm-hooks.sh`. Sin embargo, la configuración general de swarm está activa y existe estado histórico persistido.

## 6. Causa raíz del verificador

La causa raíz es una mezcla de tres modelos incompatibles en dos búsquedas sintácticas globales:

1. Identidad por nombre: interpreta cualquier archivo con `coordination` como canal, incluso tests, instaladores y bytecode.
2. Identidad por token: interpreta cualquier aparición de claves canónicas como estado activo, incluso el código del detector y pruebas negativas.
3. Identidad operacional no modelada: no analiza si un archivo persiste, transmite, asigna o restaura estado entre agentes. Por eso detecta `swarm-hooks.sh` casi por accidente y no detecta `swarm-comms.sh`.

La ausencia de un iterador común de archivos también explica el tiempo de 115.5 segundos y que `__pycache__` se excluya en una función pero no en la otra.

## 7. Corrección mínima propuesta

No implementar hasta resolver formalmente los canales paralelos reales.

1. Crear un único iterador de archivos escaneables usado por ambas validaciones, con exclusión exacta de los seis directorios generados y manejo determinístico de rutas inaccesibles.
2. Declarar un conjunto exacto de soporte autorizado: verificador, test e instalador. La autorización debe cubrir su función técnica, no permitirles persistir estado activo.
3. Separar `duplicate_name_findings` de `operational_channel_findings`; no usar la mera subcadena `coordination` como prueba suficiente.
4. Sustituir la búsqueda de tokens aislados por una regla operacional: bloquear archivos externos que escriban o transmitan tarea actual, propietario, próximo actor, handoff, decisiones o estado persistente.
5. Mantener como fallos explícitos `agent-coordination.md`, `swarm-hooks.sh` y cualquier mecanismo equivalente mientras no exista una decisión de gobierno que los desactive o los subordine al canal canónico.
6. Añadir diagnóstico por categoría para que el resultado distinga soporte autorizado, artefactos ignorados y canales paralelos bloqueantes.

Esta propuesta no convierte hallazgos reales en allowlist. Un cambio mínimo al verificador puede eliminar falsos positivos, pero no debe producir `PASS` mientras existan los canales paralelos identificados.

## 8. Archivos que requerirían modificación

Después de aprobación y decisión sobre los canales paralelos:

- `tools/verify_coordination_interface.py`: iterador común, clasificación por rol y detector operacional.
- `tests/test_coordination_interface.py`: pruebas positivas/negativas de la nueva semántica.

Posibles cambios separados, no autorizados por `GOV-R001` y sujetos a decisión formal:

- `.claude/commands/agents/agent-coordination.md`
- `.claude/helpers/swarm-hooks.sh`
- `.claude/helpers/swarm-comms.sh`
- `.claude/settings.json`
- `.claude-flow/config.yaml`
- `AGENTS.md` y `CLAUDE.md`

No se propone modificar registry, state, DB, `engine/rc1`, `engine/v4` ni el Execution Board como parte de la remediación del verificador.

## 9. Pruebas positivas necesarias

- Repositorio canónico mínimo válido produce `PASS`.
- Verificador, test e instalador existen fuera de la raíz canónica y no se clasifican como canales.
- Fixtures con claves `handoff`, `next_actor`, `current_owner` y una prueba negativa con `CURRENT_TASK` no se interpretan como estado activo.
- Cada directorio generado exigido puede contener nombres coincidentes sin afectar el resultado.
- Referencias canónicas existentes, versiones, owners y state coherentes siguen validándose.
- El escaneo termina en tiempo acotado y produce orden estable de hallazgos.

## 10. Pruebas negativas necesarias

- Un registry o contrato alternativo fuera de `governance/coordination/` falla.
- Una referencia canónica inexistente falla.
- State que contradice versión, raíz, owners o next actor del registry falla.
- Cambio en ruta protegida sin RFC falla.
- Archivo externo que persiste tarea actual, owner, next actor o handoff falla aunque su nombre no contenga `coordination`.
- Script externo que escribe mensajes, decisiones o estados de agentes en `.claude-flow/swarm` falla.
- Comando que inicializa un canal de coordinación paralelo falla.
- Un archivo autorizado de soporte que empiece a escribir estado operacional fuera del canal canónico falla.

## 11. Riesgos

- Una allowlist amplia por directorio ocultaría canales reales dentro de `tools/`, `tests/` o `.claude/`.
- Excluir todos los archivos `.claude` eliminaría evidencia crítica de coordinación paralela.
- Mantener búsquedas por palabras comunes seguirá generando ruido y alentará excepciones inseguras.
- Detectar solo nombres conocidos dejará pasar variantes como `swarm-comms.sh`.
- El estado actual de `.claude-flow/swarm` está terminado, pero la configuración permite reactivación; confundir inactividad puntual con desactivación sería incorrecto.
- El hook versionado no está instalado localmente y su ejecución efectiva no fue certificada en esta tarea.

## 12. Veredicto

`PARALLEL_CHANNEL_REQUIRES_DECISION`

La remediación de falsos positivos es técnicamente segura solo si conserva el bloqueo de los canales paralelos reales. Antes de implementar, se requiere una decisión explícita sobre Claude Flow/Ruflo, `agent-coordination.md`, `swarm-hooks.sh`, `swarm-comms.sh` y el estado persistido en `.claude-flow/`.
