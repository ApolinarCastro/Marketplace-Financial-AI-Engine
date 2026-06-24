# RN REMEDIATION PLAN

**Status:** PLAN CERTIFIED
**Date:** 2026-06-06
**Scope:** ML only (0% mechanism impact in PARIS, RIPLEY, FALABELLA)

---

## 1. Cambio Exacto Requerido

Agregar filtro de exclusión de mecanismos apareados (BPP, Poscobro Conciliado, Poscobro General) en la query SQL de `run_financial_closing()`.

**NO** usar `include_in_operational_pnl` porque ese flag excluye también ROOT_EVENTS legítimos (Talla/Garantía $98.3M, Arrepentimiento $15.5M, Dañado/Vacío $2.5M) que SÍ deben permanecer en P&L.

---

## 2. SQL Antes

```python
def run_financial_closing(self, marketplace, periodo_inicio, periodo_fin):
    self.db.execute("DELETE FROM marketplace_cierre_financiero_v1 WHERE ...")
    
    def fmt(items): return "'" + "','".join(items) + "'"
    
    sql = f"""
        SELECT 
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ingresos"])}) THEN monto ELSE 0 END) as total_ingresos,
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["devoluciones"])}) THEN monto ELSE 0 END) as total_devoluciones,
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_operacionales"])}) THEN monto ELSE 0 END) as total_costos_op,
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_comerciales"])}) THEN monto ELSE 0 END) as total_costos_com,
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ajustes"])}) THEN monto ELSE 0 END) as total_ajustes
        FROM marketplace_ledger_clasificado_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
    """
```

## 3. SQL Después

```python
MECANISMOS_EXCLUIDOS = [
    "Ajuste por Compra Protegida (BPP)",
    "Ajuste Poscobro Conciliado", 
    "Ajuste Poscobro General"
]

    # En run_financial_closing():
    def fmt(items): return "'" + "','".join(items) + "'"
    
    sql = f"""
        SELECT 
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ingresos"])}) THEN monto ELSE 0 END) as total_ingresos,
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["devoluciones"])}) THEN monto ELSE 0 END) as total_devoluciones,
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_operacionales"])}) THEN monto ELSE 0 END) as total_costos_op,
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_comerciales"])}) THEN monto ELSE 0 END) as total_costos_com,
            SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ajustes"])}) THEN monto ELSE 0 END) as total_ajustes
        FROM marketplace_ledger_clasificado_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND clasificacion_operativa NOT IN ({fmt(MECANISMOS_EXCLUIDOS)})
    """
```

**Location:** `engine/v4/marketplace_auditor.py`, método `run_financial_closing()`, línea 527.

---

## 4. Impacto Esperado

| Escenario | RN ML (all-time) | Delta vs Actual |
|---|---|---|
| Actual (con mecanismos) | $842,250,301 | — |
| Sin mecanismos (BPP + Poscobro) | $699,024,767 | **-$143,225,534** |

**Neto sobre 15 meses certificados (2025-01 a 2026-03):**

| Escenario | RN ML | Delta | Delta % |
|---|---|---|---|
| Actual | ~$775M | — | — |
| Sin mecanismos | ~$642M | **-$133.2M** | **~17.2%** |

**Nota importante:** El impacto neto de $35.8M (certificado en Go-Live Audit) considera que 93.8% de los mecanismos están apareados y se autocancelan en períodos contables. Los $133.2M es el valor bruto de filas de mecanismos. El efecto real en RN al excluir TODAS las filas de mecanismos es de $133.2M, no $35.8M. La certificación previa midió solo el componente apareado.

---

## 5. Riesgo Técnico

| Riesgo | Severidad | Mitigación |
|---|---|---|
| Syntax error en SQL | BAJO | Cambio de 1 línea, validable con `run_financial_closing()` |
| `fmt()` no maneje caracteres Unicode | MEDIO | `MECANISMOS_EXCLUIDOS` usa strings planos ASCII + Unicode. Verificar que `fmt()` escapa correctamente. |
| Constante fuera de método | BAJO | Puede definirse como constante de módulo o dentro del método |

---

## 6. Riesgo Funcional

| Riesgo | Severidad | Mitigación |
|---|---|---|
| Excluir conceptos operacionales equivocados | **CRÍTICO** | `MECANISMOS_EXCLUIDOS` contiene solo 3 conceptos (BPP, Poscobro Conciliado, Poscobro General). Son los únicos clasificados como MECHANISM en EVENT_REGISTRY_V2. 0 riesgo de excluir ROOT_EVENTS. |
| Romper cierre de PARIS/RIPLEY/FALABELLA | NULO | Esos MPs tienen 0 filas con esos conceptos. Impacto $0 en closing. |
| Romper dashboard | NULO | Dashboard consume `marketplace_cierre_financiero_v1` que se recalcula completo con cada `run_financial_closing()`. |

---

## 7. Riesgo de Auditoría

| Riesgo | Severidad | Mitigación |
|---|---|---|
| Paired mechanisms removidos al 100% (no 93.8%) | MEDIO | El fix excluye TODAS las filas de mecanismos, no solo el 93.8% apareado. Esto sobre-corrige en 6.2% ($8.9M all-time). Impacto mensual: ~$0.6M. |
| Standalone mechanisms (6.2%) deben permanecer en P&L | MEDIO | Post-fix, los $8.9M standalone también se excluyen. Esto es una sobre-corrección. Para ser precisos, se necesitaría un filtro más granular (pair rate por período). |

**Recomendación:** Aceptar la sobre-corrección de 6.2% como primer paso quirúrgico, documentar como known limitation, y planificar refinamiento futuro del pair rate dinámico.

---

## Veredicto Técnico

| Pregunta | Respuesta |
|---|---|
| ¿El cambio es quirúrgico? | **SÍ** — 1 línea en 1 método, 3 conceptos, 1 marketplace |
| ¿Riesgo de romper clasificación? | **NO** — no toca `run_classification()` |
| ¿Riesgo de romper ledger? | **NO** — no toca `surgical_loader.py` |
| ¿Riesgo de romper auditoría? | **NO** — no toca `run_audit()` |
| ¿Riesgo de romper dashboard? | **NO** — solo cambia el valor en `cierre_financiero_v1` |
