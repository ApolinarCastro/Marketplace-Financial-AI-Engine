# P30 — PLATFORM SCORECARD

**Marketplace Financial AI Engine**
**Base**: Exclusivamente evidencia ejecutable

---

## 1. Robustez Técnica: 52/100

| Criterio | Peso | Score | Evidencia |
|----------|------|-------|-----------|
| Clasificación Ledger==Clasificado | 25% | 100 | $0 delta, 402K rows. E-002 |
| Ledger→Cierre convergence | 25% | 10 | Gap $2.07B. E-003, E-004 |
| DTE coverage promedio | 15% | 67 | ML 89%, RIPLEY 97%, PARIS 81%, FALABELLA 0% |
| 268/278 tests PASS | 15% | 96 | 96.4% pass rate |
| Sin SQL injection en código | 10% | 30 | F-006: explainability_engine.py:209 |
| Dependencias declaradas | 10% | 0 | No hay pyproject.toml. F-003 |
| **Ponderado** | **100%** | **52** | |

### Desglose
- **Fortaleza**: Clasificación Ledger==Clasificado es perfecta. Tests PASS rate alto.
- **Debilidad**: Ledger→Cierre no converge. RIPLEY gap masivo. SQL injection en código de producción.

---

## 2. Madurez Funcional: 48/100

| Criterio | Peso | Score | Evidencia |
|----------|------|-------|-----------|
| Multi-MP coverage (4 MPs) | 20% | 100 | ML, RIPLEY, PARIS, FALABELLA en DB |
| Executive endpoints | 20% | 80 | Exec summary, waterfall, structure funcionan |
| DTE certification | 15% | 50 | ML 97.7%, otros MPs no certificados |
| Audit engine | 15% | 50 | 8,362 alerts pero PARIS/FALABELLA 0 |
| Explainability engine | 10% | 70 | 6 KPIs, funciona, pero SQL injection |
| Single Financial Truth | 20% | 5 | NO se cumple (gap $2.07B) |
| **Ponderado** | **100%** | **48** | |

### Desglose
- **Fortaleza**: 4 MPs cubiertos. Executive endpoints funcionales.
- **Debilidad**: Single Financial Truth no certificada. PARIS/FALABELLA sin auditoría.

---

## 3. Estabilidad: 55/100

| Criterio | Peso | Score | Evidencia |
|----------|------|-------|-----------|
| Tests PASS rate | 25% | 96 | 268/278 PASS. 2 FAIL por DB locked (no código) |
| API responde | 25% | 85 | 20+ endpoints 200 OK |
| DB consistency (Ledger==Clasificado) | 25% | 100 | $0 delta |
| DB connection management | 15% | 10 | Singleton + reset cascade. F-007 |
| Error handling | 10% | 30 | No estandarizado. Cierre all retorna $0 |
| **Ponderado** | **100%** | **55** | |

### Desglose
- **Fortaleza**: Tests pasan consistentemente. API responde. DB consistente Ledger==Clasificado.
- **Debilidad**: Singleton DB frágil. Error handling inconsistente.

---

## 4. Consistencia: 35/100

| Criterio | Peso | Score | Evidencia |
|----------|------|-------|-----------|
| Ledger == Clasificado ($0 delta) | 25% | 100 | E-002 |
| Waterfall conservation | 20% | 100 | 4/4 MPs PASS. E-012 |
| Exec == Waterfall | 20% | 100 | 4/4 MPs PASS. E-013 |
| Ledger → Cierre conservation | 25% | 0 | Gap $2.07B. E-004 |
| Cierre PARIS > Ledger | 10% | 0 | Cierre $18M > Ledger. Matemáticamente imposible |
| **Ponderado** | **100%** | **35** | |

### Desglose
- **Fortaleza**: Waterfall conservation perfecta. Ledger==Clasificado perfecto.
- **Debilidad**: Ledger→Cierre no converge. PARIS y FALABELLA tienen cierre > ledger (imposible).

---

## 5. Determinismo: 85/100

| Criterio | Peso | Score | Evidencia |
|----------|------|-------|-----------|
| Misma query → mismo resultado | 40% | 100 | DuckDB es determinista. Sin estado mutable. |
| Tests de regresión SQL=API=UI | 30% | 100 | 8 casos PASS. E-011 |
| Clasificación determinista | 20% | 100 | RAW_TO_CLASSIFICATION_MAP es puro mapping |
| Pipeline re-ejecutable | 10% | 30 | dedup_cols permite re-run. Sin transacciones. |
| **Ponderado** | **100%** | **85** | |

### Desglose
- **Fortaleza**: El motor financiero es determinista. Misma data → mismo resultado siempre.
- **Debilidad**: Pipeline no es totalmente idempotente (sin transacciones).

---

## 6. Auditabilidad: 40/100

| Criterio | Peso | Score | Evidencia |
|----------|------|-------|-----------|
| Auditoría alerts | 25% | 50 | 8,362 alerts. RIPLEY 4,619, ML 3,743 |
| DTE documents | 20% | 50 | 667 indexados. 97.3% linked para RIPLEY. |
| Pipeline log | 15% | 80 | 1,493 eventos. 212 file registrations. |
| ML audit coverage | 15% | 30 | 3,743 alerts para $901.7M — coverage bajo |
| PARIS/FALABELLA audit | 15% | 0 | 0 alerts. Sin cobertura de auditoría |
| Explainability | 10% | 60 | 6 KPIs explicables. SQL injection en código |
| **Ponderado** | **100%** | **40** | |

### Desglose
- **Fortaleza**: Pipeline log y file registry existen. DTE indexing funciona.
- **Debilidad**: PARIS/FALABELLA sin auditoría. Explainability engine tiene SQL injection.

---

## 7. Capacidad Operacional: 30/100

| Criterio | Peso | Score | Evidencia |
|----------|------|-------|-----------|
| Sin rutas absolutas | 20% | 0 | Hardcoded en 3+ archivos. F-004 |
| CI/CD | 20% | 0 | No existe. F-015 |
| Backup automático | 15% | 20 | Snapshots manuales. Sin proceso automático. |
| DB índices | 15% | 0 | No hay índices. F-005 |
| Entorno reproducible | 15% | 0 | Sin pyproject.toml. Sin Dockerfile. |
| Deployment config | 15% | 0 | Sin Docker, sin nginx, sin scripts deploy |
| **Ponderado** | **100%** | **30** | |

### Desglose
- **Fortaleza**: (ninguna sobre 50)
- **Debilidad**: Portabilidad cero. Sin CI/CD. Sin deployment. Sin índices.

---

## 8. Preparación para Producción Interna: 25/100

| Criterio | Peso | Score | Evidencia |
|----------|------|-------|-----------|
| Single Financial Truth | 20% | 5 | Gap $2.07B Ledger→Cierre |
| Portabilidad | 15% | 0 | Hardcoded paths, sin deps, sin CI/CD |
| DTE coverage completa | 15% | 50 | RIPLEY buena, FALABELLA 0%, PARIS sin link |
| Audit trail completo | 15% | 30 | Solo ML+RIPLEY. PARIS/FALABELLA sin auditoría |
| Tests automatizados | 10% | 70 | 268 PASS. Pero sin CI/CD. |
| Manejo de errores | 10% | 30 | No estandarizado |
| Sin SQL injection | 10% | 30 | F-006 presente |
| **Ponderado** | **100%** | **25** | |

---

## Resumen de Scores

| Dimensión | Score | Interpretación |
|-----------|-------|----------------|
| Robustez Técnica | 52/100 | Base sólida, gap Ledger→Cierre la debilita |
| Madurez Funcional | 48/100 | 4 MPs funcionales, Single Financial Truth no certificada |
| Estabilidad | 55/100 | Tests pasan, singleton DB es frágil |
| Consistencia | 35/100 | Perfecta en clasificación, rota en conservación Ledger→Cierre |
| Determinismo | 85/100 | Fuerte — motor es determinista |
| Auditabilidad | 40/100 | ML+RIPLEY cubiertos, PARIS+FALABELLA sin cobertura |
| Capacidad Operacional | 30/100 | Portabilidad cero, sin CI/CD, sin deployment |
| Preparación Producción | 25/100 | **No listo para producción interna** |
| **Promedio General** | **46/100** | **Funcional con deficiencias estructurales graves** |

---

## Conclusión

El motor financiero tiene **bases correctas** en clasificación (Ledger==Clasificado $0 delta), determinismo (85/100), y estabilidad de tests (96.4% PASS). Sin embargo, **no puede declararse preparado para producción** por:

1. **Gap Ledger→Cierre de $2.07B** — la Single Financial Truth no existe en producción
2. **RIPLEY gap masivo** — 54.7% de los datos ($1.8B) no converge
3. **Portabilidad cero** — hardcoded paths, sin dependencias, sin CI/CD
4. **FALABELLA sin DTE** — 0% coverage
5. **SQL injection** en código de producción
6. **PARIS/FALABELLA sin auditoría** — 0 alerts

**Score general: 46/100 — Funcional pero no certificable como estable.**
