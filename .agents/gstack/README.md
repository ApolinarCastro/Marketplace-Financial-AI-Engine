# gstack — Instalado en este repositorio

52 skills de [gstack](https://github.com/garrytan/gstack) (Garry Tan, Y Combinator) instalados en `.agents/skills/gstack-*`.

## Skills prioritarios para este proyecto

| Skill | Para qué |
|-------|----------|
| `/gstack-investigate` | Debug de ledger vacío, tests rotos, pipeline de datos |
| `/gstack-review` | Code review antes de cada PR |
| `/gstack-cso` | Auditoría OWASP + STRIDE (crítico para motor financiero) |
| `/gstack-ship` | Release engineering: tests → PR → merge |
| `/gstack-qa` | QA con navegador real (frontend financiero) |
| `/gstack-plan-eng-review` | Revisión de arquitectura (separación capas Auditor/360) |
| `/gstack-plan-ceo-review` | Decisiones estratégicas de scope |
| `/gstack-office-hours` | Reframing de producto antes de codificar |
| `/gstack-health` | Dashboard de calidad de código |
| `/gstack-document-release` | Mantener docs sincronizados con el código |
| `/gstack-context-save` / `context-restore` | Persistencia de sesión |

## Flujo recomendado (gstack sprint)

```
/gstack-office-hours → /gstack-plan-ceo-review → /gstack-plan-eng-review
→ implementar → /gstack-review → /gstack-qa → /gstack-ship
```
