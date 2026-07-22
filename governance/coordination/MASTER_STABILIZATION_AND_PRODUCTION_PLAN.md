# MARKETPLACE FINANCIAL OPERATING SYSTEM
# PLAN MAESTRO DE ESTABILIZACIÓN Y PUESTA EN MARCHA

Versión: 1.0

Estado:
PROPUESTO PARA ACTIVACIÓN

Documento rector:
FOUNDATION RESET versión 1.0

---

# 1. PROPÓSITO

Estabilizar, completar y poner en marcha Marketplace Financial Operating System garantizando:

- costo monetario adicional cero
- una sola verdad financiera
- cero duplicidad financiera
- trazabilidad desde RAW hasta banco
- conciliación por marketplace
- evidencia reproducible
- respuestas certificadas del Financial Copilot
- cambios controlados y reversibles
- protección del núcleo certificado

El proyecto avanzará mediante capacidades verificables y no mediante cantidad de archivos, endpoints o funcionalidades declaradas.

---

# 2. RESULTADO ESPERADO

El sistema debe demostrar:

RAW

↓

Registry

↓

ETL

↓

Ledger

↓

Clasificación

↓

Cierre

↓

XML

↓

Settlement

↓

Banco

↓

Dashboard

↓

Copilot

Cada eslabón deberá identificar:

- fuente
- registro
- regla
- versión
- resultado
- evidencia
- cobertura
- excepción
- estado de certificación

---

# 3. ORDEN DE AUTORIDAD

El orden obligatorio de autoridad es:

1. FOUNDATION RESET
2. DEC y RFC aprobados
3. MARKETPLACE_AUDITOR_V3_5_RC1
4. contratos públicos certificados
5. governance/coordination/
6. este Plan Maestro
7. execution_board.json
8. evidence/

Si dos instrucciones se contradicen, prevalece la de mayor autoridad.

---

# 4. CANAL ÚNICO DE COORDINACIÓN

El único canal permitido entre Codex y OpenCode es:

governance/coordination/

Los archivos JSON existentes continuarán funcionando como registros técnicos para lectura automática.

Las instrucciones, planes, tareas, informes y veredictos dirigidos al usuario se expresarán en Markdown.

No se utilizarán como canales operacionales paralelos:

- AGENTS.md
- comentarios aislados
- documentos temporales
- conversaciones no registradas
- archivos fuera de governance/coordination/

---

# 5. RESPONSABILIDADES

## 5.1 APOLINAR CASTRO — PROPIETARIO DEL PRODUCTO

Responsabilidades:

- aprobar el Plan Maestro
- definir prioridades del negocio
- confirmar el significado económico de las reglas
- autorizar cambios sobre componentes protegidos
- aprobar el inicio de cada fase
- aprobar o rechazar el paso a producción

## 5.2 CODEX — DIRECCIÓN TÉCNICA Y SUPERVISIÓN

Responsabilidades:

- convertir cada fase en tareas concretas
- autorizar una sola tarea activa
- revisar los cambios de OpenCode
- controlar el cumplimiento de Foundation Reset
- inspeccionar diffs, pruebas y evidencias
- detectar modificaciones no autorizadas
- proteger RC1
- determinar el estado real de cada capacidad
- emitir el veredicto de cada gate
- mantener actualizado el Execution Board

Codex no aprobará una capacidad sin evidencia reproducible.

## 5.3 OPENCODE — EJECUTOR CONTROLADO

Responsabilidades:

- leer primero los documentos de coordinación
- ejecutar únicamente la tarea autorizada
- no ampliar el alcance
- realizar cambios pequeños y reversibles
- ejecutar las pruebas requeridas
- generar evidencia
- informar todos los archivos modificados
- detenerse cuando encuentre una contradicción
- no inventar estados, reglas, tablas o contratos

OpenCode no puede declarar unilateralmente una capacidad terminada o certificada.

## 5.4 ANTIGRAVITY — APOYO SECUNDARIO

Puede utilizarse para:

- segunda revisión
- prototipos aislados
- diseño visual
- documentación
- análisis sin escritura

No puede modificar autónomamente:

- RC1
- Ledger
- DuckDB oficial
- taxonomías
- motores financieros
- conciliación productiva
- exportaciones SAP

---

# 6. MODELO OFICIAL DE ESTADOS

Los únicos estados permitidos son:

NOT_STARTED

↓

IMPLEMENTED

↓

VALIDATED

↓

VERIFIED

↓

CERTIFIED

## IMPLEMENTED

El código o componente existe.

## VALIDATED

Las pruebas específicas pasan y existe evidencia reproducible.

## VERIFIED

Codex confirmó:

- consistencia de la evidencia
- aislamiento de las pruebas
- ausencia de contaminación
- cumplimiento de gobernanza
- regresión comparada contra baseline

## CERTIFIED

Se completaron tres ejecuciones limpias consecutivas desde un entorno controlado.

No se utilizarán:

- DONE
- COMPLETE
- PASS como estado operacional
- cero regresiones sin comparación reproducible

---

# 7. REGLAS NO NEGOCIABLES

- No modificar RC1 sin RFC aprobado.
- No duplicar lógica financiera.
- No duplicar SQL financiero.
- No calcular cifras financieras en frontend.
- No modificar el Ledger desde conciliación.
- No utilizar RAW como base operacional después de la ingesta.
- No eliminar RAW como evidencia.
- No inventar relaciones entre transacciones.
- No convertir observaciones en reglas automáticas.
- No avanzar con gates pendientes.
- No utilizar APIs pagadas.
- No introducir servicios cloud obligatorios.
- No declarar resultados sin evidencia.
- No ejecutar cambios globales.
- No trabajar simultáneamente en dos capacidades.
- No declarar una capacidad certificada por la sola existencia de pruebas.

---

# 8. COMPONENTES PROTEGIDOS

Se consideran protegidos:

- engine/rc1/
- engine/v4/
- DB oficial
- Ledger certificado
- clasificación financiera certificada
- cierre financiero certificado
- DocumentCertificationEngine
- DocumentGapEngine
- contratos API certificados
- dashboards certificados
- tablas núcleo

Todo cambio protegido requiere:

1. bug reproducible
2. evidencia antes del cambio
3. RFC o autorización expresa
4. análisis de impacto
5. plan de rollback
6. prueba negativa
7. implementación quirúrgica
8. regresión
9. recertificación proporcional

---

# 9. MODELO DE EJECUCIÓN

Toda tarea seguirá este orden:

1. Apolinar aprueba el objetivo.
2. Codex define alcance y gate.
3. Codex registra una única tarea activa.
4. OpenCode ejecuta la tarea.
5. OpenCode entrega diff, pruebas y evidencia.
6. Codex revisa el repositorio real.
7. Codex emite un veredicto.
8. Se actualiza el canal de coordinación.
9. Se regenera el Execution Board.
10. Apolinar autoriza el siguiente paso.

Veredictos permitidos:

- APPROVED_TO_CONTINUE
- REQUIRES_REMEDIATION
- BLOCKED_BY_EVIDENCE
- REJECTED
- CERTIFIED

---

# 10. FASE 0 — CONTENCIÓN Y ESTABILIZACIÓN

## Objetivo

Establecer el estado real del proyecto antes de continuar.

## Acciones

1. Congelar CAP-002 y nuevos desarrollos.
2. Auditar los cambios relacionados con CAP-001.
3. Eliminar el uso no autorizado del estado DONE.
4. Comparar los 56 fallos contra un baseline reproducible.
5. Revisar la modificación de engine/v4/ingestion/__init__.py.
6. Revisar la modificación de tools/generate_execution_board.py.
7. Verificar contaminación de DuckDB y data/uploads/.
8. Verificar si los tests utilizan componentes reales o mocks.
9. Confirmar la integridad de RC1.
10. Establecer el estado correcto de CAP-001.

## Entregables

- CAP001_CORRECTIVE_REVIEW.md
- REGRESSION_BASELINE.md
- PROTECTED_PATH_DIFF_REPORT.md
- evidencia de ejecución

## Gate de salida

- Los 56 fallos están clasificados.
- Se conoce si existen regresiones nuevas.
- Se conoce si la DB fue modificada.
- Se conoce si RC1 fue afectado.
- CAP-001 tiene un estado justificable.
- No quedan cambios sin explicar.

---

# 11. FASE 1 — ENDURECIMIENTO DE LA GOBERNANZA

## Objetivo

Convertir las reglas de coordinación en controles ejecutables.

## Acciones

1. Integrar verify_coordination_interface.py en pytest.
2. Crear prueba de referencias inexistentes.
3. Crear prueba de rutas protegidas.
4. Crear prueba de canal paralelo.
5. Crear hook local pre-commit.
6. Crear instalación explícita e idempotente del hook.
7. Mantener CI cloud como control opcional.
8. No depender de servicios pagados.

## Gate de salida

- El verificador pasa.
- Los casos inválidos fallan como se espera.
- No existe otro canal de coordinación.
- El costo monetario adicional permanece en cero.
- RC1 permanece intacto.

---

# 12. FASE 2 — VERDAD DEL RUNTIME

## Objetivo

Determinar qué componentes se ejecutan realmente.

## Acciones

1. Inventariar rutas y endpoints activos.
2. Identificar motores canónicos.
3. Detectar módulos huérfanos.
4. Identificar código duplicado.
5. Comprobar tablas y vistas reales.
6. Relacionar pruebas con capacidades.
7. Comparar documentación contra runtime.
8. Actualizar el Execution Board con evidencia real.

## Entregables

- RUNTIME_TRUTH_MAP.md
- ACTIVE_COMPONENT_REGISTRY.md
- DUPLICATION_REGISTER.md
- Execution Board regenerado

## Gate de salida

Cada capacidad debe tener:

- código activo
- contrato
- fuente de datos
- prueba
- evidencia
- estado justificable

---

# 13. FASE 3 — UPLOAD CENTER E INGESTA

## Objetivo

Certificar el flujo:

Upload

↓

Detect

↓

Validate

↓

Classify

↓

Persist

↓

Certify

↓

Knowledge

## Acciones

1. Aislar tests mediante DB temporal.
2. Utilizar directorios temporales.
3. Ejecutar tres cargas controladas.
4. Validar SHA-256.
5. Probar archivos duplicados.
6. Probar cuarentena.
7. Probar archivos inválidos.
8. Verificar metadata completa.
9. Verificar las seis etapas reales.
10. Limpiar los recursos temporales.
11. Generar evidencia por ejecución.

## Gate de salida

- Tres cargas limpias consecutivas.
- Cero contaminación.
- Cero duplicados no detectados.
- Metadata completa.
- CAP-001 y CAP-002 verificadas.

---

# 14. FASE 4 — TRAZABILIDAD FINANCIERA

## Objetivo

Demostrar:

RAW

↓

Registry

↓

ETL

↓

Ledger

↓

Clasificación

↓

Cierre

## Acciones

1. Relacionar archivo con registro.
2. Relacionar fila RAW con transacción.
3. Registrar versión de transformación.
4. Registrar regla de clasificación.
5. Validar participación única en P&L.
6. Separar P&L y tesorería.
7. Crear EvidenceObject.
8. Probar reproducción desde RAW.

## Gate de salida

- Delta financiero igual a cero.
- Cada cifra tiene origen.
- Cada evento participa una sola vez.
- No existe duplicidad de lógica.
- Ledger permanece intacto.

---

# 15. FASE 5 — MOTOR DE CONCILIACIÓN

## Objetivo

Incorporar el conocimiento legacy RTU como motor satélite.

## Orden

1. Mercado Libre
2. Paris
3. Falabella
4. Ripley

Cada marketplace se certificará por separado.

## Acciones

1. Inventariar scripts legacy.
2. Identificar entradas y salidas.
3. Crear fixtures históricos.
4. Identificar tolerancias reales.
5. Extraer funciones puras.
6. Ejecutar el motor nuevo en modo sombra.
7. Comparar legacy versus nuevo.
8. Explicar cada diferencia.
9. Implementar tablas satélite append-only.
10. Versionar reglas y ejecuciones.
11. Conectar evidencias mediante contratos públicos.
12. No modificar Ledger ni clasificación.

## Clasificación de reglas

Cada regla legacy será clasificada como:

- ADOPTAR
- ADAPTAR
- RECHAZAR
- EVIDENCIA INSUFICIENTE

## Gate de salida

- 100% de equivalencia en casos certificados.
- Delta igual a cero.
- Cero consumo duplicado.
- Tolerancias aprobadas.
- Ledger intacto.
- Evidencia reproducible.

---

# 16. FASE 6 — EXPORTACIÓN SAP ONE

## Objetivo

Generar archivos SAP únicamente desde conciliaciones certificadas.

## Flujo

Conciliación certificada

↓

Selección

↓

Preview

↓

Validación

↓

Aprobación humana

↓

Exportación

↓

Manifiesto

## Reglas

- No guardar salidas en 01_Raw.
- Utilizar una carpeta exports/.
- No hardcodear cuentas SAP.
- No cargar automáticamente a SAP.
- Generar hash y manifiesto.
- Mantener archivo de control.
- Requerir aprobación humana.

## Gate de salida

- Archivos técnicamente válidos.
- Totales reconciliados.
- Trazabilidad completa.
- Exportación reversible.
- Cero carga automática.

---

# 17. FASE 7 — EVIDENCE ORCHESTRATOR Y FINANCIAL COPILOT

## Objetivo

Responder preguntas financieras utilizando evidencia certificada.

## Acciones

1. Crear Question Registry.
2. Asignar ID canónico a cada pregunta.
3. Mapear cada pregunta a motores autorizados.
4. Definir evidencia mínima.
5. Mapear cada pregunta a un handler.
6. Utilizar contratos públicos.
7. No incorporar SQL financiero en el orquestador.
8. Crear golden tests.
9. Crear pruebas de falta de evidencia.
10. Ejecutar benchmarks.
11. Generar EvidenceObject por respuesta.
12. Certificar pregunta por pregunta.

## Estados de respuesta

- ANSWERED_CERTIFIED
- ANSWERED_WITH_GAPS
- INSUFFICIENT_EVIDENCE
- NOT_SUPPORTED

## Gate de salida

- Cero respuestas inventadas.
- Cero SQL financiero duplicado.
- Cada respuesta muestra evidencia.
- Las preguntas sin soporte se rechazan correctamente.

---

# 18. FASE 8 — INTELIGENCIA EJECUTIVA

## Objetivo

Transformar el Dashboard en una explicación financiera.

Debe explicar:

- qué pasó
- por qué pasó
- dónde ocurrió
- qué impacto tuvo
- cómo demostrarlo
- qué acción requiere

No se incorporarán cálculos financieros en frontend.

---

# 19. FASE 9 — PREPARACIÓN PARA PRODUCCIÓN

## Acciones

1. Ejecutar el ciclo completo.
2. Probar backup.
3. Probar restauración.
4. Validar secretos.
5. Validar permisos.
6. Medir rendimiento.
7. Ejecutar tres ciclos limpios.
8. Preparar rollback.
9. Ejecutar operación paralela.
10. Emitir decisión GO o NO-GO.

## Criterios obligatorios

- RC1 íntegro.
- Suite oficial controlada.
- Cero hallazgos P0.
- Cero hallazgos P1.
- Tres ejecuciones limpias.
- Delta financiero igual a cero.
- Cero duplicidad financiera.
- Restauración probada.
- Preguntas prioritarias certificadas.
- Aprobación del propietario del producto.

---

# 20. INCORPORACIÓN DE EXPERIENCIAS EXTERNAS

Las experiencias externas se incorporarán mediante principios y patrones. No se copiará código sin evaluación.

## ESCALAFY

Aportes:

- preguntas de rentabilidad
- cashflow explicable
- margen por SKU, canal y campaña
- conocimiento estructurado para LLM

## AGENTFACTORY BUSINESS PLUGINS

Aportes:

- skills modulares
- guardrails
- routing
- evals
- golden tests

No se incorporarán reglas financieras ajenas al dominio.

## PONYTAIL BENCHMARKS

Aportes:

- baseline A/B
- medición por mediana
- corrección como gate
- costo
- latencia
- declaración de limitaciones

## OPENCLAW PERSONAS

Aportes:

- SOP
- outputs estructurados
- reglas anti-alucinación

No se duplicará TUKE Master.

## CECOMMERCE

Aportes:

- alertas
- misiones
- priorización ejecutiva

No se incorporarán:

- cálculos financieros en frontend
- LocalStorage como persistencia financiera

## QWED FINANCE GUARD

Estado:

PENDIENTE DE EVALUACIÓN TÉCNICA

Condiciones:

- costo cero
- sin envío de datos sensibles
- sin duplicar Regression Guard
- compatible con DEC-019

---

# 21. POLÍTICA DE COSTO CERO

El proyecto no dependerá de:

- APIs pagadas
- modelos pagados
- bases cloud pagadas
- CI pagado
- hosting pagado durante desarrollo
- observabilidad SaaS
- servicios vectoriales pagados

Herramientas principales:

- OpenCode
- Ollama
- Python
- DuckDB
- FastAPI
- pytest
- Git
- Obsidian local

OpenCode será el ejecutor principal.

Antigravity será una herramienta secundaria y no una dependencia operacional.

---

# 22. CRITERIO DE PUESTA EN MARCHA

La salida se realizará progresivamente:

1. piloto interno
2. operación paralela
3. producción controlada
4. expansión por marketplace

El proyecto no se considerará terminado únicamente porque el Dashboard funcione.

Debe demostrar las preguntas establecidas en Foundation Reset con evidencia reproducible.

---

# 23. PRIMERA FASE PROPUESTA

La primera fase que podrá activarse será:

FASE 0 — CONTENCIÓN Y ESTABILIZACIÓN

La primera tarea será:

REVISIÓN CORRECTIVA DE CAP-001

No se autoriza CAP-002 hasta cerrar el gate de la Fase 0.

---

# 24. ESTADO DEL PLAN

Este Plan Maestro queda:

PROPUESTO PARA ACTIVACIÓN

Su incorporación en el repositorio no significa ejecución automática.

La ejecución comenzará únicamente después de:

1. validación de incorporación
2. verificación de coherencia
3. aprobación expresa del propietario del producto
4. activación formal de la Fase 0
