# P40R2B ARCHITECTURE — Pure Orchestration (CORRECCIÓN FINAL)

## El Orchestrator NO depende del Copilot

El Copilot es una capa de **presentación**.

Debe consumir al Orchestrator, no ser consumido por él.

---

## 1. ARQUITECTURA FINAL

```
                UI
                 │
                 ▼
          CopilotEngine            ← capa de presentación
                 │
                 ▼
      Evidence Orchestrator        ← capa de coordinación
           │        │
           ▼        ▼
    FinancialEngine  LedgerEngine   ← capa de producción de conocimiento
           │        │
           ▼        ▼
ReconciliationEngine  CertificationEngine
```

### Flujo correcto

1. **UI** pregunta → **CopilotEngine** recibe
2. **CopilotEngine** delega → **Evidence Orchestrator** coordina
3. **Evidence Orchestrator** consulta → **FinancialEngine + LedgerEngine + ReconciliationEngine + CertificationEngine**
4. **FinancialEngine** produce datos → **Orchestrator** relaciona
5. **Orchestrator** devuelve JSON estructurado → **CopilotEngine** genera explicación
6. **CopilotEngine** responde → **UI** muestra

### Prohibido

```
❌ Evidence Orchestrator → CopilotEngine.ask()   ← el Orchestrator nunca consume al Copilot
❌ Evidence Orchestrator → SQL directo            ← RULE-001
❌ Evidence Orchestrator → copilot_queries.py     ← RULE-001
❌ Evidence Orchestrator → DuckDB                 ← RULE-001
```

---

## 2. DEPENDENCIAS DEL ORCHESTRATOR

### Permitido

| Engine | Métodos públicos |
|--------|-----------------|
| FinancialEngine | `query_ledger()`, `query_cierre()`, `query_cierre_all()`, `query_desglose()`, `query_exec_summary()`, `query_waterfall()`, `query_cobros_breakdown()`, `list_periods()`, `resolve_period_range()`, `query_audit()`, `query_audit_types()`, `get_financial_records_count()`, `is_financial_structure_ready()`, `query_operational_intelligence()` |
| LedgerEngine | `get_ledger_records_count()` |
| ReconciliationEngine | `validate_marketplace_consistency()`, `validate_all_marketplaces()` |
| CertificationEngine | `certify()` |

### Prohibido

| Engine | Razón |
|--------|-------|
| CopilotEngine | Capa de presentación. El Orchestrator no consume al Copilot. |
| DuckDB | RULE-001 — el Orchestrator no conoce tablas físicas |
| SQL directo | RULE-001 — el Orchestrator no ejecuta SQL |
| copilot_queries.py | RULE-001 — el Orchestrator no conoce SQL interno |

---

## 3. COMPONENTES

### 3.1 EvidenceLinkRegistry

**Responsabilidad:** Construir relaciones entre identificadores.

**Fuente exclusiva:** `FinancialEngine.query_ledger()` — datos estructurados.

```
Entrada: id_orden = "ORD-12345"

  1. FinancialEngine.query_ledger(order_id="ORD-12345")
     → id_transaccion: "ML-SALE-202601-XXXXX"
     → folio_xml: "033-123456789"
     → archivo_origen: "ML/Facturacion/Ene2025.xlsx"
     → marketplace: "ML"
     → periodo: "2026-01"
     → financial_group: "ingresos"
     → detalle: "Venta"
     → monto: 18261.00

  2. FinancialEngine.query_ledger(id_transaccion="ML-SALE-202601-XXXXX")
     → misma transacción, confirmación de consistencia

Resultado: lista de EvidenceLink con id_transaccion ↔ id_orden ↔ folio_xml ↔ archivo_origen ↔ marketplace ↔ periodo
```

**SQL nuevo:** 0. **Dependencias:** FinancialEngine solamente.

### 3.2 ClosingContribution

**Responsabilidad:** Responder "¿Esta transacción participa en este cierre?"

```
Entrada: id_transaccion = "ML-SALE-202601-XXXXX"

  1. FinancialEngine.query_ledger(id_transaccion="ML-SALE-202601-XXXXX")
     → periodo="2026-01", marketplace="ML", include_in_operational_pnl=1

  2. FinancialEngine.query_cierre(marketplace="ML", periodo="2026-01")
     → resultado_neto, total_ingresos, batch_id

  3. ReconciliationEngine.validate_marketplace_consistency(marketplace="ML", periodo="2026-01")
     → Level1: $0 delta, status=CERTIFICADO

  4. CertificationEngine.certify(marketplace="ML", periodo="2026-01")
     → 6 claims, pass_rate=100%, status=CERTIFIED

Resultado: ClosingContribution { participating: true, closing_batch, ... }
```

**SQL nuevo:** 0. **Dependencias:** FinancialEngine + ReconciliationEngine + CertificationEngine.

### 3.3 CashTrace

**Responsabilidad:** Diseñar la cadena XML → Settlement → Pago → Banco → Cobro.

**No se implementa.** Solo contratos. CashTrace es el gap #1 del sistema.

**Dependencias:** 0 (diseño solamente).

### 3.4 CoverageAnalyzer

**Responsabilidad:** Calcular % de cobertura entre eslabones.

**Fuente exclusiva:** FinancialEngine + LedgerEngine + ReconciliationEngine + CertificationEngine.

```
Entrada: marketplace = "ML"

  1. LedgerEngine.get_ledger_records_count(marketplace="ML")
     → 107,542 total rows

  2. FinancialEngine.get_financial_records_count(marketplace="ML")
     → 107,542 classified rows (100%)

  3. FinancialEngine.query_exec_summary(marketplace="ML")
     → gross, returns, costs, net (KPIs certificados)

  4. ReconciliationEngine.validate_marketplace_consistency(marketplace="ML")
     → taxonomy coverage, document coverage, alerts

Resultado:
  - RAW→Ledger: 100% (107,542 rows)
  - Ledger→XML: 89.4% (desde query_exec_summary + query_ledger)
  - Clasificación: 100% (desde get_financial_records_count)
  - Cierre: 100% (desde validate_marketplace_consistency)
```

**SQL nuevo:** 0. **Dependencias:** FinancialEngine + LedgerEngine + ReconciliationEngine.

### 3.5 GapAnalyzer

**Responsabilidad:** Reportar qué eslabones faltan.

```
Entrada: marketplace = "RIPLEY"

  1. CoverageAnalyzer.run(marketplace="RIPLEY")
     → cobertura por eslabón

  2. FinancialEngine.query_audit(marketplace="RIPLEY")
     → alertas activas

  3. CertificationEngine.certify(marketplace="RIPLEY")
     → claims + pass_rate

  4. ReconciliationEngine.validate_marketplace_consistency(marketplace="RIPLEY")
     → taxonomy coverage, document coverage

  5. Comparar contra cadena universal
     → gaps detectados

Resultado:
  - XML→SII: 0% (G3: folios incompatibles)
  - Cash: 0% (G1: sin fuente de cash)
  - Gaps: [G1, G3, G5, G7, G9]
```

**SQL nuevo:** 0. **Dependencias:** CoverageAnalyzer + FinancialEngine + CertificationEngine + ReconciliationEngine.

---

## 4. GAPS ARQUITECTÓNICOS (P40R2B)

| Gap | Capacidad faltante | Dónde debe exponerse |
|-----|-------------------|---------------------|
| GAP-DTE | DTE/XML lookup por folio_xml (tipo_dte, monto_total, emisor) | FinancialEngine — nuevo método público `get_dte_info(folios)` |
| GAP-EVIDENCE | Validación de existencia de evidencia (Ledger + RAW + XML) | CertificationEngine — nuevo método público `validate_evidence(marketplace, periodo)` |

Actualmente, `folio_xml` existe como columna en `marketplace_ledger_v1` pero no hay método público que retorne los datos del DTE asociado. Los datos están en `dte_truth_v1` pero solo accesibles mediante `CopilotEngine._xml_info()` (privado).

**Solución:** Agregar método público en FinancialEngine:
```python
def get_dte_info(self, folios: list[str]) -> list[dict]:
    """Retorna info DTE para una lista de folios. SQL encapsulado."""
```

---

## 5. MATRIZ DE RESPONSABILIDAD (FINAL)

| Capa | Produce datos | Coordina | Explica | Accede SQL |
|-------|-------------|----------|---------|------------|
| FinancialEngine | ✅ | ❌ | ❌ | ✅ interno |
| LedgerEngine | ✅ | ❌ | ❌ | ✅ interno |
| ReconciliationEngine | ✅ | ✅ | ❌ | ✅ interno |
| CertificationEngine | ✅ | ✅ | ❌ | ✅ interno |
| Evidence Orchestrator | ❌ | ✅ | ❌ | ❌ |
| CopilotEngine | ❌ | ❌ | ✅ | ❌ |

Los Engines **producen** conocimiento.
El Orchestrator **coordina** conocimiento.
El Copilot **explica** conocimiento.

Ninguno invade la responsabilidad del otro.

---

## 6. CONTRATOS

```python
@dataclass
class EvidenceLink:
    source_identifier: str
    source_type: str
    target_identifier: str
    target_type: str
    engine_used: str       # "FinancialEngine" | "LedgerEngine" | etc.
    method_used: str       # "query_ledger()" | etc.
    confidence: str        # "CERTIFICADO" | "PARCIAL" | "NO_DISPONIBLE"

@dataclass
class ClosingContribution:
    participating: bool
    closing_batch: str | None
    closing_period: str | None
    financial_group: str | None
    operational_pnl: bool
    reconciliation_status: str
    certification_status: str

@dataclass
class CashTraceStatus:
    settlement_id: str | None
    settlement_amount: float | None
    settlement_date: str | None
    payment_id: str | None
    bank_deposit_id: str | None
    cash_status: str

@dataclass
class CoverageMetric:
    source: str
    target: str
    coverage_pct: float
    source_total: float
    matched: float
    method: str
    engine_used: str
    method_used: str

@dataclass
class GapReport:
    gap_id: str
    marketplace: str
    description: str
    root_cause: str
    impact: str
    priority: str
```

---

## 7. API ENDPOINTS

```yaml
evidence_orchestrator:
  endpoints:
    - path: /api/v4/evidence/links
      contracts: [FinancialEngine.query_ledger()]
      params: [id_orden]
      response: list[EvidenceLink]

    - path: /api/v4/evidence/closing-contribution
      contracts: [FinancialEngine.query_cierre(),
                  ReconciliationEngine.validate_marketplace_consistency(),
                  CertificationEngine.certify()]
      params: [id_transaccion]
      response: ClosingContribution

    - path: /api/v4/evidence/coverage
      contracts: [LedgerEngine.get_ledger_records_count(),
                  FinancialEngine.query_exec_summary(),
                  ReconciliationEngine.validate_marketplace_consistency()]
      params: [marketplace]
      response: list[CoverageMetric]

    - path: /api/v4/evidence/gaps
      contracts: [CoverageAnalyzer.run(),
                  FinancialEngine.query_audit(),
                  CertificationEngine.certify()]
      params: [marketplace]
      response: list[GapReport]

    - path: /api/v4/evidence/cash-trace
      contracts: []  # diseño futuro
      params: [id_orden]
      response: CashTraceStatus
```

---

## 8. EVIDENCIA DE EJECUCIÓN

| Paso | Acción ejecutada | Reutilizado | Código nuevo | Estado |
|------|-----------------|-------------|-------------|--------|
| 1 | Dependencias del Orchestrator: solo 4 engines (sin Copilot) | ✅ | 0 LOC | PASS |
| 2 | EvidenceLinkRegistry → solo FinancialEngine.query_ledger() | ✅ | 0 LOC | PASS |
| 3 | ClosingContribution → FinancialEngine + ReconciliationEngine + CertificationEngine | ✅ | 0 LOC | PASS |
| 4 | CoverageAnalyzer → FinancialEngine + LedgerEngine + ReconciliationEngine | ✅ | 0 LOC | PASS |
| 5 | GapAnalyzer → CoverageAnalyzer + FinancialEngine + CertificationEngine + ReconciliationEngine | ✅ | 0 LOC | PASS |
| 6 | CashTrace → diseño (0 dependencias) | ✅ | 0 LOC | PASS |
| 7 | GAP-DTE documentado (necesita método público en FinancialEngine) | ✅ | 0 LOC | PASS |
| 8 | GAP-EVIDENCE documentado (necesita método público en CertificationEngine) | ✅ | 0 LOC | PASS |
| 9 | Validación DEC-019 | ✅ | 0 LOC | PASS |
| 10 | Validación Single Financial Truth | ✅ | 0 LOC | PASS |

**Total: 0 SQL. 0 cálculos. 0 dependencias de presentación. Solo orquestación pura.**

---

## 9. UBICACIÓN

```
engine/v4/evidence/
    __init__.py                  ← EvidenceOrchestrator
    evidence_link_registry.py    ← FinancialEngine.query_ledger()
    closing_contribution.py      ← FinancialEngine + ReconciliationEngine + CertificationEngine
    cash_trace.py                ← contratos (diseño)
    coverage_analyzer.py         ← FinancialEngine + LedgerEngine + ReconciliationEngine
    gap_analyzer.py              ← CoverageAnalyzer + FinancialEngine + CertificationEngine + ReconciliationEngine
    contracts.py                 ← dataclasses
```

7 archivos. 0 dependencias al Copilot. 0 SQL. 0 tablas.

---

## 10. CHECKLIST FINAL

```
[✅] El Orchestrator no importa DuckDB
[✅] El Orchestrator no ejecuta SQL
[✅] El Orchestrator no usa execute_query()
[✅] El Orchestrator no importa copilot_queries.py
[✅] El Orchestrator no depende de CopilotEngine (solo al revés)
[✅] EvidenceLinkRegistry no parsea texto generado (solo datos estructurados)
[✅] CoverageAnalyzer no depende de CopilotEngine
[✅] Toda información proviene de métodos públicos en FinancialEngine/LedgerEngine/ReconciliationEngine/CertificationEngine
[✅] Gaps arquitectónicos documentados (GAP-DTE, GAP-EVIDENCE)
[✅] DEC-019 preservada
[✅] Single Financial Truth preservada
```

---

## 11. PRINCIPIO FINAL

**Los Engines producen conocimiento.**
**El Orchestrator coordina conocimiento.**
**El Copilot explica conocimiento.**

Ninguno invade la responsabilidad del otro.
