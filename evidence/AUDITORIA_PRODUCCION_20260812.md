# Auditoría Quirúrgica de Cuellos de Botella — Pase a Producción

## Marketplace Financial AI Engine
**Fecha:** 2026-08-12
**Objetivo:** Determinar los cuellos de botella que impiden la madurez y el pase a producción, y definir la vía más expedita y tecnológicamente resolutiva.
**Método:** Inspección quirúrgica de estructura, schema DB, tests, CI, frontend, y capa de certificación.

---

## 1. Veredicto Ejecutivo

La aplicación lleva un ciclo de "avances y retrocesos" porque arrastra **tres deudas estructurales no resueltas**:

1. **Certificación electrónica ilusoria** — la capa de certificación se auto-valida sin tocar jamás un documento fiscal real.
2. **Deriva de documentación** — el README describe una arquitectura que no existe.
3. **Cultura de parcheo** — ~20 scripts one-off (`fix_*.py`, `inject*.py`, `patch_*.py`) en lugar de consolidar correcciones en el motor.

El pase a producción está bloqueado **no por falta de código, sino por un objetivo no alcanzable con los datos disponibles**: se intenta certificar tributariamente transacciones cuya llave fiscal no está en los archivos.

---

## 2. Estado Real vs. Estado Declarado

### 2.1 Deriva de documentación (HECHO)

| README declara | Realidad | Impacto |
|----------------|----------|---------|
| Frontend React/Vite en `src/frontend` | No existe `src/`; solo `frontend/shared/` | README mintiendo sobre el stack |
| DB oficial `data/db/antigravity_v4.db` | DB real es `meli_financial_v4.db` | Falsa referencia a DB inexistente |
| `Scripts/pipeline_cli.py` como entrypoint | Existe pero rodeado de 20 scripts de parcheo | Entrypoint ahogado en basura |
| Build en `src/frontend/dist` | No existe `frontend/dist` | No hay build frontend |

**Hallazgo:** El README describe un "refactor limpio" que nunca se completó. La UI real son 6 archivos HTML monolíticos en `templates/` (dashboard.html 83KB, documentary_dashboard.html 80KB, executive_dashboard.html 60KB).

### 2.2 Cultura de parcheo (HECHO)

`Scripts/` contiene estos artefactos de firefighting sin consolidar:
`fix_js.py`, `fix_orch.py`, `fix_paths.py`, `fix_syntax.py`, `inject2.py` → `inject5.py`, `inject_api.py`, `patch_api_validation.py`, `patch_dashboard.py`, `patch_dashboard_2.py`, `patch_ripley.py`, `refactor_frontend.py`, `refactor_frontend_v2.py`, `create_tests.py` → `create_tests_3.py`, `f5_*_certify.py`.

Estos scripts **no son parte del flujo productivo** (`engine/`, `api/`, `tests/`) — son parches aplicados manualmente y abandonados. Cada "retroceso" probablemente corresponde a un parche que se perdió o que rompió algo que otro parche había arreglado.

### 2.3 Inestabilidad de datos (HECHO)

`data/db/` contiene 15+ archivos DB: snapshots corruptos (`corrupt_snapshot`), backups fechados, `pre_fix`, `pre_nan_fix`, `pre_truth003`, `pre_future_fix`, etc. Esto es señal de una base de datos tratada como archivo de trabajo, sin control de versión ni migración formal.

---

## 3. El Cuello de Botella Central: Certificación Electrónica Ilusoria

### 3.1 Evidencia de DB (verificada esta sesión)

| Métrica | Valor |
|---------|-------|
| Links en `dte_link_v1` (Ripley) | 210,232 |
| `cert_type` | `LEDGER_EXISTING` (todos) |
| Folios en `dte_truth_v1` (DTE reales) | 407 |
| Folios en `dte_link_v1` | 160 |
| **Intersección real (DTE ↔ link)** | **0** |

La tabla `dte_link_v1` para Ripley tiene 210,232 links con `cert_type = LEDGER_EXISTING`, que significa "este folio existe en el propio ledger". Es una **auto-certificación circular**: el ledger valida al ledger. Ninguno de esos 210,232 links toca un folio fiscal real del SII.

### 3.2 Por qué los tests "pasan" (INFERENCIA)

El gate de certificación `test_gate_dte_coverage` mide la columna `folio_xml` del ledger como si fuera cobertura DTE. Pero `folio_xml` en Ripley contiene **números de liquidación interna** (505930, 517031, etc.), no folios SII (108927, 26794, etc.). La cobertura "97.9%" reportada para Ripley mide cuántas filas tienen settlement_ref, no cuántas tienen documento fiscal.

**El test pasa porque valida la métrica equivocada.**

### 3.3 La llave documental real existe, pero no se implementó

En la auditoría del 06-08-2026 se confirmó que Ripley sí tiene una llave documental: la columna `Número de factura` en `transaction-logs.csv`, que conecta `Número de pedido → Número de factura → Identificador del ciclo de facturación`, y que referencia el DTE oficial en el portal del SII (factura de Comisión + factura de Despachos por ciclo).

La tabla recomendada `ripley_invoice_map` **nunca fue creada** (verificado: no existe en el schema, que tiene 37 tablas).

---

## 4. Inventario de Cuellos de Botella (Priorizados)

| # | Cuello de botella | Severidad | Bloquea producción | Evidencia |
|---|-------------------|-----------|--------------------|-----------|
| B1 | Certificación DTE circular (`LEDGER_EXISTING`) | CRÍTICO | Sí — el claim central es falso | Intersección dte_truth ∩ dte_link = 0 |
| B2 | Falta tabla `ripley_invoice_map` (llave fiscal) | CRÍTICO | Sí — sin puente no hay cert | Tabla no existe en 37 tablas |
| B3 | Deriva README vs realidad (src/frontend, antigravity_v4.db) | ALTO | Sí — onboarding/CI rotos | README vs estructura real |
| B4 | Sin build frontend (`frontend/dist` no existe) | ALTO | Sí — no hay UI desplegable | `frontend/` solo tiene `shared/` |
| B5 | ~20 scripts de parcheo en `Scripts/` sin consolidar | ALTO | Sí — deuda técnica viva | Listado de Scripts/ |
| B6 | Inestabilidad de DB (15+ archivos, snapshots corruptos) | ALTO | Sí — riesgo de pérdida | Listado de data/db/ |
| B7 | Test suite lento/inestable (1082 tests >30 min, se colgó) | MEDIO | Parcial | Ejecución esta sesión |
| B8 | Paths hardcodeados (`C:\Users\ASUS Zenbook\...`) | MEDIO | Sí — no portable | database.py, surgical_loader.py |
| B9 | 37 tablas con 6+ tablas Ripley superpuestas | MEDIO | No — deuda | dte_link_v1, dte_ledger_link, document_match_v1, ripley_* |

---

## 5. La Vía Más Expedita y Tecnológicamente Resolutiva

### Decisión de alcance primero (lo que nadie ha decidido)

El bloqueo raíz no es técnico, es de **alcance del claim**. La app intenta vender "certificación electrónica" cuando lo que realmente tiene es "conciliación financiera + tracking documental". Hasta que no se decida el alcance honesto, ningún refactor terminará en "final feliz".

### Ruta recomendada (3 fases, la más corta al valor)

**FASE 0 — Congelar y declarar la verdad (1-2 días)**
- Congelar el código: integrar los `fix_*/inject_*/patch_*` de `Scripts/` que realmente estén en uso, y archivar el resto a `_archive/`.
- Cambiar el `cert_type` de Ripley de `LEDGER_EXISTING` a `SETTLEMENT_REF` (verdad: son refs de liquidación, no DTE).
- Corregir el README para que refleje la realidad (HTML en `templates/`, `meli_financial_v4.db`).
- **Resultado:** elimina la ilusión de certificación y detiene el ciclo de "retrocesos" por parches perdidos.

**FASE 1 — Rebaseline de la capa de datos (3-5 días)**
- Elegir **una** DB canónica (`meli_financial_v4.db`) y archivar los 14 archivos restantes a `_archive/db_history/`.
- Consolidar las 6+ tablas Ripley en una sola cadena documental: `ripley_settlement_chain` (ya tiene 287K filas con `settlement_stage`) como fuente única, y desactivar `dte_link_v1`/`dte_ledger_link`/`document_match_v1` para Ripley.
- Corregir el gate de certificación para que mida **cobertura documental real** (folio SII presente), no `folio_xml`.
- **Resultado:** tests que pasan por razones correctas, datos con fuente única.

**FASE 2 — Puente fiscal real (la llave que ya se encontró) (1-2 semanas)**
- Ingerir los `transaction-logs.csv` (bitácoras con `Número de factura`) de todos los períodos a `01_Raw/RIPLEY/`.
- Crear `ripley_invoice_map` (Número de factura → Número de pedido → ciclo → folio SII).
- Poblar el folio SII cruzando con el portal del SII (RUT ECCSA + fecha + monto) o mapeo manual.
- **Resultado:** certificación electrónica real, punta a punta, para las facturas que tengan DTE.

### Lo que NO se debe hacer (anti-patrones detectados)

- ❌ No refactorizar el frontend a React/Vite "para quedar bien con el README" — es la vía más lenta al valor, y el README ya mintió una vez.
- ❌ No agregar más tablas Ripley — ya hay 6+ superpuestas; cada una nueva multiplica la deuda.
- ❌ No seguir parcheando `api.py` con scripts `inject*.py` — cada parche es un retroceso futuro.

---

## 6. Conclusión

La vía más expedita es **detener la ilusión de certificación y redefinir el alcance honesto** (conciliación financiera + tracking documental), para luego construir el puente fiscal real con la llave ya identificada (`Número de factura`). El resto del código —motor, ledger, cierre, trazabilidad interna TH→CICLOS→SELLER→Ledger— está sólido y verificado. El "final feliz" llega cuando el producto prometa lo que los datos pueden respaldar, no cuando se agregue más código.
