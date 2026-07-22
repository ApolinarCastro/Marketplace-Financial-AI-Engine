# TECHSPEC MASTER V1

Esta es la especificación técnica y de arquitectura oficial del Marketplace Financial AI Engine.

## Componentes y Principios Fundamentales

* **Single Financial Truth**: Única fuente de verdad financiera. Se declara `marketplace_ledger_clasificado_v1` como única fuente oficial.
* **Marketplace Isolation**: Los marketplaces deben estar aislados en la arquitectura física y lógica. Cada marketplace debe poseer su propio Loader, Parser, Taxonomía, Certificación y Matching. Está prohibido reutilizar reglas económicas, compartir taxonomías o compartir transformaciones financieras.
* **Evidence First**: Todo cambio, decisión o conclusión requiere evidencia. Regla de oro: "Sin evidencia, sin conclusión".
* **No Heuristics**: No se aceptan modelos heurísticos ni reglas adivinables; todo debe estar explícito y documentado.
* **Documentary Truth**: Los documentos oficiales (XML, facturas) validan la transacción.
* **Audit Truth**: Las alertas de auditoría deben reflejar la realidad del sistema y estar debidamente certificadas.
* **Marketplace Lock Policy**: Ver `MARKETPLACE_LOCK_POLICY.md` para reglas de estados DRAFT, CERTIFIED, PRE_LOCK y LOCKED.
* **AI Governance**: Ver `AI_GOVERNANCE_LAYER.md`.
* **Skills Registry**: Ver `SKILLS_REGISTRY.md`.
* **Obsidian Governance**: Ver `OBSIDIAN_GOVERNANCE_MODEL.md`.
* **Regression Guard**: Ver `REGRESSION_GUARD.md`.

## Decisiones Estratégicas

### DEC-050: NO GLOBAL CHANGES
Toda modificación en el sistema debe declarar explícitamente su scope.

Scopes permitidos para modificaciones:
* `scope = ML`
* `scope = PARIS`
* `scope = RIPLEY`
* `scope = FALABELLA`
* `scope = SHOPIFY`

**PROHIBIDO:** El uso de `scope = ALL` queda estrictamente prohibido, salvo en casos de infraestructura certificada y con aprobación explícita.
