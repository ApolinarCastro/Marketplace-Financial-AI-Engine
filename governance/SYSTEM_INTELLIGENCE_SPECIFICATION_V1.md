---
id: SYSTEM_INTELLIGENCE_SPECIFICATION_V1
version: 1.0.0
fecha: 2026-07-27
estado: ESPECIFICADO
owner: AI & Copilot Architect / Lead System Intelligence Engineer
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - ARCHITECTURE_REGISTRY_V1
  - DATA_CONTRACT_REGISTRY_V1
  - EVIDENCE_REGISTRY_V1
  - DUAL_GRAPH_ARCHITECTURE_MODEL_V1
relacionado_con:
  - FINANCIAL_COPILOT_QUESTION_REGISTRY_V1
  - KNOWLEDGE_OS_SPECIFICATION
---

# ESPECIFICACIÓN MAESTRA DE LA CAPA SYSTEM INTELLIGENCE V1

## Propósito y Principio Supremo de Seguridad
Establecer la especificación formal de la capa **System Intelligence**, responsable de convertir evidencia certificada, conocimiento canónico y relaciones de grafos duales en respuestas financieras $0 delta, explicables y sin alucinaciones para el **Financial Copilot**.

---

## Principio Supremo de Aislamiento de Seguridad (9.2)

> [!CAUTION]
> ### PROHIBICIÓN ABSOLUTA DE CONSULTA DIRECTA
> Queda estrictamente prohibido que el Financial Copilot o cualquier modelo de lenguaje consulte directamente:
> 1. Archivos RAW de marketplace sin registrar (`01_Raw/`).
> 2. Documentos no certificados o en borrador (`00_Inbox/`).
> 3. Documentos aislados en cuarentena (`99_Quarantine/`).
> 4. Tablas o base de datos DuckDB sin contrato de datos explícito (`CTR-001` a `CTR-011`).
> 5. Evidencias sin hash SHA-256 verificado.
> 6. Referencias externas no adoptadas.
>
> Toda interacción, consulta o razonamiento DEBE pasar obligatoriamente a través de los componentes de la capa **System Intelligence**.

---

## Componentes Conceptuales Obligatorios (23 Componentes - Section 9.3)

### 1. `Query Interpreter`
- **Propósito**: Analizar sintáctica y semánticamente la pregunta del usuario.
- **Entradas**: Texto libre en lenguaje natural.
- **Salidas**: Estructura de consulta normalizada (parámetros, períodos, marketplace).
- **Owner**: NLP Specialist | **Criticidad**: ALTA | **Madurez**: Nivel 1 (Especificado).

### 2. `Intent Classifier`
- **Propósito**: Clasificar la intención del usuario dentro de las 10 Preguntas Financieras Estratégicas.
- **Entradas**: Consulta normalizada.
- **Salidas**: Intent ID (e.g. `INTENT_VENTAS_REALES`, `INTENT_DESCUENTO_OCULTO`).
- **Owner**: AI Engineer | **Criticidad**: CRÍTICA | **Madurez**: Nivel 1 (Especificado).

### 3. `Financial Question Router`
- **Propósito**: Enrutar la pregunta hacia la cadena de contratos y evidencia correspondiente.
- **Entradas**: Intent ID.
- **Salidas**: Ruta de consulta en el Dual Graph (`CTR-001` .. `CTR-011`).
- **Owner**: Solution Architect | **Criticidad**: CRÍTICA | **Madurez**: Nivel 1 (Especificado).

### 4. `Contract Validator`
- **Propósito**: Comprobar que todos los contratos de datos requeridos estén en estado `CERTIFICADO`.
- **Entradas**: IDs de contratos requeridos.
- **Salidas**: Estatus de validación de contrato (`PASS` | `FAIL`).
- **Owner**: Data Architect | **Criticidad**: CRÍTICA MAXIMA | **Madurez**: Nivel 1 (Especificado).

### 5. `Evidence Resolver`
- **Propósito**: Recuperar los hashes SHA-256 y rutas de evidencia registradas en `EVIDENCE_REGISTRY_V1.md`.
- **Entradas**: Capacidad o concepto financiero consultado.
- **Salidas**: Lista de registros `EVID-[ID]` verificados.
- **Owner**: Evidence Guardian | **Criticidad**: CRÍTICA MAXIMA | **Madurez**: Nivel 1 (Especificado).

### 6. `Knowledge Retriever`
- **Propósito**: Extraer fragmentos canónicos desde `KnowledgeOS/01_Canonical/` y `02_Governance/`.
- **Entradas**: Nodos del Knowledge Graph.
- **Salidas**: Contexto canónico en Markdown inmutable.
- **Owner**: Knowledge Engineer | **Criticidad**: ALTA | **Madurez**: Nivel 1 (Especificado).

### 7. `Graph Reasoning Engine`
- **Propósito**: Ejecutar traversals en el Dual Graph para reconstruir linaje y causa raíz.
- **Entradas**: Nodos de origen (RAW / Registro) y nodos de destino (Copilot / Respuesta).
- **Salidas**: Grafo de trazabilidad y aristas de impacto.
- **Owner**: Graph Architect | **Criticidad**: ALTA | **Madurez**: Nivel 1 (Especificado).

### 8. `Semantic Search Engine`
- **Propósito**: Búsqueda semántica sobre índices de conocimiento canónico.
- **Entradas**: Vectores de consulta.
- **Salidas**: Documentos canónicos más afines con puntaje de similitud.
- **Owner**: RAG Specialist | **Criticidad**: MEDIA | **Madurez**: Nivel 1 (Especificado).

### 9. `RAG Orchestrator`
- **Propósito**: Orquestar la recuperación aumentada de generación sin permitir fuentes no verificadas.
- **Entradas**: Contexto canónico y evidencias resueltas.
- **Salidas**: Prompt empaquetado para el modelo.
- **Owner**: RAG Specialist | **Criticidad**: CRÍTICA | **Madurez**: Nivel 1 (Especificado).

### 10. `Embedding Manager`
- **Propósito**: Generar y gestionar representaciones vectoriales del conocimiento canónico.
- **Entradas**: Documentos Markdown de `01_Canonical/` y `02_Governance/`.
- **Salidas**: Vectores densos indexados.
- **Owner**: AI Data Engineer | **Criticidad**: MEDIA | **Madurez**: Nivel 1 (Especificado).

### 11. `Model Router`
- **Propósito**: Seleccionar la ruta de ejecución óptima conforme a la política de routing.
- **Entradas**: Nivel de complejidad de la consulta.
- **Salidas**: Destino de ejecución (Determinista SQL → Grafo → RAG → LLM).
- **Owner**: AI Architect | **Criticidad**: ALTA | **Madurez**: Nivel 1 (Especificado).

### 12. `Local Model Adapter`
- **Propósito**: Conector para ejecución local privada de LLMs (Ollama / Qwen / Llama).
- **Entradas**: Prompt certificado.
- **Salidas**: Texto generado localmente.
- **Owner**: Infrastructure AI Engineer | **Criticidad**: MEDIA | **Madurez**: Nivel 1 (Especificado).

### 13. `Cloud Model Adapter`
- **Propósito**: Conector seguro con transporte cifrado hacia APIs cloud de alta capacidad.
- **Entradas**: Prompt certificado redactado de PII.
- **Salidas**: Texto generado cloud.
- **Owner**: Cloud Security Engineer | **Criticidad**: MEDIA | **Madurez**: Nivel 1 (Especificado).

### 14. `MCP Adapter`
- **Propósito**: Proveer herramientas estandarizadas mediante Model Context Protocol para subagentes.
- **Entradas**: Invocación de herramientas MCP.
- **Salidas**: Respuestas de herramientas estructuradas.
- **Owner**: Agent Architect | **Criticidad**: ALTA | **Madurez**: Nivel 1 (Especificado).

### 15. `Agent Orchestrator`
- **Propósito**: Coordinar subagentes especializados (Data Auditor, Financial Specialist, Reconciliation Agent).
- **Entradas**: Tarea multi-dominio compleja.
- **Salidas**: Plan de ejecución subagente consolidado.
- **Owner**: Multi-Agent Designer | **Criticidad**: ALTA | **Madurez**: Nivel 1 (Especificado).

### 16. `Citation Builder`
- **Propósito**: Adjuntar citas bidireccionales explícitas (rutas `file://`, hashes SHA-256, `execution_id`).
- **Entradas**: Payload de respuesta preliminar.
- **Salidas**: Respuesta enriquecida con referencias probatorias.
- **Owner**: Quality Reviewer | **Criticidad**: CRÍTICA | **Madurez**: Nivel 1 (Especificado).

### 17. `Confidence Evaluator`
- **Propósito**: Calcular el nivel de confianza de la respuesta (0% a 100%) basado en completitud de evidencias.
- **Entradas**: Cadena de contratos y evidencias verificadas.
- **Salidas**: Score de confianza y estatus.
- **Owner**: Decision Analyst | **Criticidad**: CRÍTICA | **Madurez**: Nivel 1 (Especificado).

### 18. `Hallucination Guard`
- **Propósito**: Validar que ninguna cifra o afirmación producida por el modelo carezca de respaldo directo en la evidencia.
- **Entradas**: Respuesta del modelo vs Payload de la base de datos DuckDB.
- **Salidas**: Aprobación (`PASS`) o Rechazo por alucinación (`REJECT`).
- **Owner**: AI Safety Reviewer | **Criticidad**: CRÍTICA MAXIMA | **Madurez**: Nivel 1 (Especificado).

### 19. `Policy Engine`
- **Propósito**: Aplicar políticas de acceso, restricciones de gobernanza y normas del Master Plan.
- **Entradas**: Identidad de usuario y consulta.
- **Salidas**: Permiso o Denegación de consulta.
- **Owner**: Chief Security Officer | **Criticidad**: CRÍTICA | **Madurez**: Nivel 1 (Especificado).

### 20. `Audit Logger`
- **Propósito**: Registrar de manera inmutable cada interacción y consulta procesada por el Copilot.
- **Entradas**: Evento completo de consulta/respuesta.
- **Salidas**: Registro en log de auditoría con `query_id`.
- **Owner**: Security Auditor | **Criticidad**: CRÍTICA | **Madurez**: Nivel 1 (Especificado).

### 21. `Response Composer`
- **Propósito**: Formatear la respuesta final en Markdown compatible con UI y Obsidian.
- **Entradas**: Payload validado, citas, tablas y métricas.
- **Salidas**: Documento de respuesta final.
- **Owner**: UX / Frontend Engineer | **Criticidad**: ALTA | **Madurez**: Nivel 1 (Especificado).

### 22. `Certification Gate`
- **Propósito**: Bloqueador final que detiene cualquier respuesta que no cumpla la Regla de Oro del Proyecto.
- **Entradas**: Respuesta empaquetada.
- **Salidas**: Emisión final o activación de Fallback Handler.
- **Owner**: Single Financial Truth Guardian | **Criticidad**: CRÍTICA MAXIMA | **Madurez**: Nivel 1 (Especificado).

### 23. `Fallback Handler`
- **Propósito**: Emitir la respuesta estandarizada obligatoria cuando falta evidencia o falla la certificación.
- **Entradas**: Señal de fallo o rechazo del Hallucination Guard / Certification Gate.
- **Salidas**: Mensaje formal de evidencia insuficiente con detalle de bloqueadores.
- **Owner**: Fallback Specialist | **Criticidad**: CRÍTICA | **Madurez**: Nivel 1 (Especificado).

---

## Reserva Tecnológica de IA/ML (Section 9.4)

Se reserva formalmente la ubicación arquitectónica para futuras integraciones:
- **Motores de Inferencia Local**: Ollama (ejecución de modelos Qwen 2.5 Finance, Llama 3.1).
- **Inferencia Cloud & Acceleration**: NVIDIA NIM Microservices / Cloud LLM APIs.
- **Protocolo de Contexto**: Model Context Protocol (MCP) para comunicación entre agentes.
- **Vector Stores & Caching**: Vector Databases (ChromaDB / Qdrant) y Semantic Cache.
- **Frameworks de Agentes**: Multi-agent framework orchestrators.

---

## Jerarquía Obligatoria de Fuentes de Confianza (Section 9.5)

```text
1. Evidencia Certificada (EVIDENCE_REGISTRY_V1.md + Hashes SHA-256) [CONFIANZA 100%]
        ↓
2. Registro Canónico (KnowledgeOS/01_Canonical/) [CONFIANZA 99%]
        ↓
3. Contrato de Datos Validado (DATA_CONTRACT_REGISTRY_V1.md) [CONFIANZA 98%]
        ↓
4. Data Lineage Certificado (DATA_LINEAGE_REGISTRY_V1.md) [CONFIANZA 95%]
        ↓
5. Knowledge Graph (Nodos y Aristas Normativas) [CONFIANZA 90%]
        ↓
6. Execution Graph (Nodos y Aristas de Código/Tests) [CONFIANZA 85%]
        ↓
7. Referencia Externa Adoptada (EXTERNAL_REFERENCE_ADOPTION_MATRIX_V1) [CONFIANZA 80%]
        ↓
8. Modelo de Lenguaje Generativo (LLM Inference Output) [CONFIANZA AUXILIAR]
```

> **REGLA INVIOLABLE**: El Modelo de Lenguaje NUNCA prevalecerá sobre evidencias certificadas o registros canónicos.

---

## Tipos de Respuesta Permitidos (Section 9.6)

| Tipo | Descripción | Condición |
| :--- | :--- | :--- |
| `RESPUESTA_CERTIFICADA` | Cifra $0 delta respaldada en evidencia inmutable | 100% Contratos y Evidencias `PASS` |
| `RESPUESTA_VALIDADA` | Resultado verificado por tests sin certificación final | Pruebas PASS, evidencia parcial |
| `RESPUESTA_PARCIAL` | Información completa solo para un subconjunto de MPs | 1 MP sin contrato certificado |
| `EVIDENCIA_INSUFICIENTE` | Activación del Fallback Handler obligatorio | Falta hash SHA-256 o archivo fuente |
| `DATOS_NO_DISPONIBLES` | Datos no ingeridos para el período solicitado | Período fuera de alcance |
| `CONTRATO_INCUMPLIDO` | Contrato de datos en estado no validado | `CTR-[ID]` en revisión o fallado |
| `LINEAGE_INCOMPLETO` | Cadena de trazabilidad con eslabón roto | Cadena < 11 pasos |
| `CONFLICTO_DE_EVIDENCIA` | Dos evidencias arrojan montos divergentes | Alerta a Cuarentena activa |
| `CAPACIDAD_NO_IMPLEMENTADA` | Función solicitada programada para fase futura | Nivel de madurez < 2 |
| `RESPUESTA_BLOQUEADA` | Bloqueo por política de seguridad o permisos | Policy Engine Deny |

---

## Regla Explícita de No Alucinación (Section 9.7)

Cuando la evidencia probatoria sea insuficiente, el sistema emitirá **OBLIGATORIAMENTE** el siguiente mensaje de fallback:

> **"No se puede responder con evidencia suficiente."**

Seguido del desglose auditado:
1. **Evidencia Faltante**: ID y tipo de evidencia no encontrada.
2. **Contrato Incumplido**: ID de contrato que no se satisface (`CTR-[ID]`).
3. **Lineage Incompleto**: Eslabón de la cadena de 11 pasos donde se pierde la trazabilidad.
4. **Capacidad No Certificada**: Nivel de madurez actual de la capacidad involucrada.
5. **Acción Futura**: Fase del Master Plan donde se resolverá el bloqueo.

---

## Política de Routing de Modelos (Section 9.8)

```text
Determinismo SQL / DuckDB (Prioridad 1 - Sin LLM)
        ↓
Consulta Estructurada API (Prioridad 2 - Sin LLM)
        ↓
Traversal de Grafos Duales (Prioridad 3 - Algorítmico)
        ↓
RAG Canónico (Prioridad 4 - Recuperación Estricta)
        ↓
Modelo de Lenguaje (Prioridad 5 - Último Recurso de Formateo)
```

---

## Especificación del Log de Auditoría (Section 9.9)

Cada interacción registrara de manera inmutable los siguientes campos:

```yaml
query_id: "Q-YYYYMMDD-UUID"
usuario: "user_id / system_id"
fecha: "YYYY-MM-DDTHH:MM:SSZ"
pregunta_original: "Texto enviado por el usuario"
intencion_detectada: "INTENT_ID"
fuentes_consultadas: ["01_Canonical/...", "DATA_CONTRACT..."]
contratos_evaluados: ["CTR-001", "CTR-008"]
evidencia_hash_utilizada: ["311c78e2b7..."]
consultas_sql_ejecutadas: ["SELECT sum(monto)..."]
modelo_utilizado: "Determinist / Ollama / Cloud"
prompt_utilizado_hash: "SHA256 of prompt"
respuesta_generada: "Texto Markdown emitido"
nivel_confianza: "100%"
advertencias: []
latencia_ms: 120
errores: None
resultado_final: "RESPUESTA_CERTIFICADA"
certificacion_gate: "PASS"
```

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:SYSTEM_INTELLIGENCE_SPECIFICATION_V1` (Tipo: `Especificacion_System_Intelligence`)
- `Node:HALLUCINATION_GUARD_POLICY` (Tipo: `Regla_Seguridad`)

### Execution Graph Nodes
- `ExecNode:VERIFY_SYSTEM_INTELLIGENCE_GATE` (Process: Auditar cumplimiento del aislamientos de seguridad y fallback en CI/CD)

---

## Trazabilidad y Relaciones
- **ESTABLECE**: La especificación de la capa de inteligencia intermedia.
- **PROTEGE**: Al Financial Copilot contra alucinaciones y consultas no verificadas.
- **AFECTA**: [FINANCIAL_COPILOT_QUESTION_REGISTRY_V1](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/FINANCIAL_COPILOT_QUESTION_REGISTRY_V1.md).

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[SYSTEM_INTELLIGENCE_SPECIFICATION_V1]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md`
