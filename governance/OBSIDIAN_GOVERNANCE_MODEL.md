# Obsidian Governance Model

## Objetivo
Estructurar Obsidian como la memoria corporativa oficial del proyecto, garantizando un registro histórico, estructurado y auditable de decisiones, problemas y certificaciones.

## Tipos Permitidos
Todo documento o nota en la base de conocimiento de Obsidian debe pertenecer obligatoriamente a uno de los siguientes tipos:

1. **RFC** (Request for Comments): Para proponer cambios o nuevas arquitecturas.
   - *Relación obligatoria:* Componentes afectados.
2. **DEC** (Decision Record): Para registrar decisiones arquitectónicas y técnicas aprobadas.
   - *Relación obligatoria:* Marketplace(s) afectado(s) o Componente.
3. **INCIDENT**: Para documentar incidentes o fallas detectadas en producción/certificación.
   - *Relación obligatoria:* Root Cause.
4. **ROOT_CAUSE**: Para documentar análisis de causa raíz y las soluciones implementadas.
5. **CERTIFICATION**: Para registrar certificaciones de estado o validación de marketplaces (ej. PRE_LOCK, LOCKED).
   - *Relación obligatoria:* Marketplace.
6. **LESSON_LEARNED**: Para registrar aprendizaje organizacional posterior a incidentes o ciclos de desarrollo.

## Relaciones y Estructura
* **PROHIBIDO:** Notas huérfanas. Todas las notas deben estar enlazadas bidireccionalmente según las relaciones obligatorias de su tipo.
* Todo debe estar vinculado al contexto general para asegurar la trazabilidad (ej. RFC -> DEC -> Componente -> Marketplace -> CERTIFICATION).
