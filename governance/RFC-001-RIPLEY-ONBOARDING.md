# RFC-001: RIPLEY ONBOARDING

**Scope:** `scope = RIPLEY`
**Estado:** DRAFT / PENDIENTE DE EVIDENCIA

## Contexto y Restricciones
Este RFC establece el proceso de onboarding para el marketplace de RIPLEY, asegurando absoluto cumplimiento con las reglas de negocio del sistema:
- **Marketplace Isolation:** Prohibido reutilizar reglas, taxonomías o lógicas de Mercado Libre (ML) o PARIS.
- **Single Financial Truth:** Única fuente oficial será `marketplace_ledger_clasificado_v1`.
- **DEC-050 NO GLOBAL CHANGES:** Todo desarrollo estará encapsulado bajo `scope = RIPLEY`.

---

## 1. Fuentes oficiales RAW
> **[EVIDENCIA REQUERIDA]**
> Por favor, confirmar y proveer los canales oficiales de los cuales se extraerá la data cruda (RAW) financiera y transaccional de Ripley.

## 2. Archivos disponibles
> **[EVIDENCIA REQUERIDA]**
> Solicitamos proporcionar ejemplos reales (muestras) de archivos RAW descargables o reportes provenientes del portal oficial de Ripley.

## 3. APIs disponibles
> **[EVIDENCIA REQUERIDA]**
> Proveer documentación oficial de las APIs de Ripley utilizadas para liquidaciones, ventas, cobros y devoluciones.

## 4. Diccionario de campos
> **[EVIDENCIA REQUERIDA]**
> Proveer listado de columnas de los reportes y su definición oficial explícita.
> *Nota: Por regla de No Heuristics, está estrictamente prohibido inferir el significado de las columnas financieras.*

## 5. Flujo económico observado
> **[EVIDENCIA REQUERIDA]**
> Proveer ejemplos reales de ciclos transaccionales para modelar el diagrama de flujo económico (venta, comisiones, impuestos, envíos, devoluciones, liquidación final).

## 6. Riesgos identificados
> **[PENDIENTE]**
> A la espera de las evidencias de los puntos 1-5 para identificar brechas de información o ambigüedades en el modelo de Ripley.

## 7. Invariantes financieras candidatas
> **[PENDIENTE]**
> Las ecuaciones matemáticas de equilibrio se derivarán exclusivamente una vez comprendido el flujo económico soportado por evidencia. No se asumirán ecuaciones de ML o PARIS.

## 8. Estrategia PRE_LOCK
Para que RIPLEY alcance el estado de pre-certificación (`PRE_LOCK`), debe demostrar en su propio dominio aislado:
* Delta financiero preliminar = 0.
* Construcción y validación de su propio Loader, Parser, Taxonomía y Matching.
* `UI = API = SQL` operando y validado en entorno de pruebas.
* Alertas debidamente justificadas.

## 9. Estrategia LOCKED
Para que RIPLEY alcance el estado final y seguro (`LOCKED`), debe cumplir la directiva de Regression Guard:
* `UI = API = SQL` verificado en producción.
* `SQL = Ledger Clasificado` sin desviaciones.
* `XML = Document Match` perfecto.
* Delta financiero permanente = 0.
* Certificación ejecutiva final.

## 10. Artefactos Esperados
`RIPLEY/`
 ├── `loader/`
 ├── `parser/`
 ├── `taxonomy/`
 ├── `matching/`
 ├── `certification/`
 └── `reconciliation/`

*Nota: Todos estos artefactos serán exclusivos de RIPLEY y no compartirán lógica ni componentes con ML o PARIS.*
