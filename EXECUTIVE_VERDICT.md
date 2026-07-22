# P30 — EXECUTIVE VERDICT

**Marketplace Financial AI Engine**
**Fecha**: 6 Julio 2026
**Tipo**: Certificación Técnica Independiente
**Base**: Exclusivamente evidencia ejecutable (código, DB, API, tests, frontend)

---

## Respuestas

### 1. ¿El Marketplace Financial AI Engine es técnicamente sólido?

**SÍ, PARCIALMENTE.** El motor financiero tiene bases sólidas:
- Ledger == Clasificado con delta $0 (402,089 rows, $3.38B). `tests/test_financial_engine.py`, `marketplace_ledger_v1` vs `marketplace_ledger_clasificado_v1`
- 268/278 tests PASS. `pytest tests/ -v --tb=short`
- API responde correctamente para 20+ endpoints. `api/api.py`, smoke test.
- 8 endpoints de Executive Summary funcionan para todos los MPs. `test_financial_engine.py`
- Waterfall conservation se cumple por MP. `test_certification_gate.py:test_gate_waterfall_conservation`

**Limitaciones severas**:
- Conservation Ledger vs Cierre tiene gap de $2.07B. Ver `marketplace_ledger_v1` (total $3.38B) vs `marketplace_cierre_financiero_v1` (total $1.31B).
- RIPLEY: ledger $2.14B vs cierre $337M — gap de $1.8B. Ver evidence collector.
- DTE coverage: FALABELLA 0%, PARIS 81.2% pero 68 DTE indexados no vinculados a ledger. `dte_truth_v1` (667 docs) vs `folio_xml` en ledger (219 distinct).
- Single Financial Truth no está certificada en producción. Cierre vs Ledger no convergen.

### 2. ¿Puede operar de forma confiable con datos reales?

**SÍ, CON RESTRICCIONES.**
- 402,089 transacciones reales cargadas y clasificadas. `marketplace_ledger_v1`, `marketplace_ledger_clasificado_v1`
- ML: 107,482 rows, 89.4% DTE coverage. Funciona con datos reales.
- RIPLEY: 219,901 rows, 97.3% DTE coverage. Períodos 2025-01 a 2026-06.
- PARIS: 74,028 rows, 81.2% DTE coverage.
- FALABELLA: 678 rows, 0% DTE coverage.

**Problemas**:
- RIPLEY P&L operacional: solo $93.9M ingresos de $2.14B total — 95.6% del valor es NO operacional (tesorería/señal ruido). `financial-structure?marketplace=RIPLEY&signal_mode=SIGNAL`
- FALABELLA tiene 0% DTE coverage y solo 678 rows.
- 2 tests FAIL por DB locked (no es bug de código pero es problema operacional).
- Rutas absolutas hardcoded: `engine/v4/database.py:12`, `dte_indexer.py:13-19`, `surgical_loader.py:12-15`.

### 3. ¿La arquitectura soporta crecimiento controlado?

**NO.** Evidencia:
- Sin índices en DuckDB. Toda consulta escanea tabla completa. No hay `CREATE INDEX` en `database.py`.
- Singleton `DatabaseV4.get()` — una conexión para todo. `engine/v4/database.py:41-51`
- Sin migraciones de esquema. `_v1` en nombres de tabla pero sin versionado.
- God object `FinancialEngine` con 10+ responsabilidades. `engine/v4/domain/financial_engine.py`
- Sin CI/CD. `.github/workflows/` vacío.
- DuckDB es colunar, usado como OLTP — desajuste arquitectónico.

### 4. ¿La Single Financial Truth permanece íntegra?

**NO.** Evidence:
- Ledger total: $3,381,794,665.45 vs Cierre total: $1,311,453,028.12 = gap de $2,070,341,637.33
- RIPLEY: ledger $2,139,918,844.00 vs cierre $337,005,407.00
- ML: ledger $901,712,441.45 vs cierre $610,179,330.12
- PARIS: ledger $337,594,474.00 vs cierre $355,671,316.00 (cierre > ledger)
- FALABELLA: ledger $2,568,906.00 vs cierre $8,596,975.00 (cierre > ledger)

La clasificación Ledger==Clasificado es correcta, pero la integración Ledger→Cierre NO converge. RIPLEY tiene el gap más grave.

### 5. ¿Existen riesgos críticos que comprometan el motor financiero?

**SÍ.**

| Riesgo | Evidencia | Severidad |
|--------|-----------|-----------|
| RIPLEY conservation gap | Ledger $2.14B vs Cierre $337M | CRÍTICO |
| Cierre vs Ledger no convergen | 4/4 MPs tienen gap | ALTO |
| Sin índices DB | `database.py` no crea índices | ALTO |
| Singleton connection | `database.py:41` reset afecta todas las queries | ALTO |
| SQL injection | `explainability_engine.py:209` f-string en SQL | ALTO |
| No backup automático | Solo snapshots manuales | ALTO |
| ML audit trail incompleto | 3,743 alerts vs RIPLEY 4,619; ML es 27% del valor pero solo 45% de alerts | MEDIO |
| FALABELLA sin DTE | 0/678 rows con folio_xml | MEDIO |

### 6. ¿El sistema puede declararse técnicamente estable?

**NO.** El motor financiero tiene bases correctas (Ledger==Clasificado, clasificación por MP, exec endpoints funcionan) pero el gap Ledger→Cierre y la falta de conservación hacen imposible declarar estabilidad. RIPLEY específicamente tiene $1.8B sin explicación en el cierre.

---

## Veredicto Final

```
Estado General:      FUNCIONAL CON DEFICIENCIAS ESTRUCTURALES
Single Financial Truth: RECHAZADO (gap $2.07B entre Ledger y Cierre)
RIPLEY:              OPERACIONAL con gap $1.8B no explicado
ML:                  SÓLIDO (mejor cobertura, mejor audit trail)
PARIS:               ACEPTABLE (cierre > ledger, DTE parcial)
FALABELLA:           DÉBIL (solo 678 rows, 0% DTE)
Producción:          NO LISTO
```

El motor es correcto en clasificación (Ledger==Clasificado con $0 delta), pero la cadena completa Ledger→Cierre→Resultado Neto NO está certificada. RIPLEY es el principal riesgo con $1.8B de diferencia.
