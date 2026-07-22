# Contracts, Observability, Intelligence & Certification Design

## Context

Phases 1-3 established FinancialEngine, Taxonomy YAML, and ReconciliationEngine.
Phases 4-10 complete the consolidation pattern: extract → encapsulate → certify.

## Design Principles (unchanged)

- **Backend Decides**: API is thin orchestrator, zero financial logic
- **Single Financial Truth**: all data traceable to `marketplace_ledger_clasificado_v1`
- **Audit Ready**: every alert includes SQL evidence, row count, financial impact
- **Deterministic**: queries are 100% reproducible, no state, no LLM

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                       api.py (thin)                     │
│  /health/* → ObservabilityEngine                        │
│  /intelligence/* → IntelligenceEngine                    │
│  /certify/* → CertificationEngine                        │
└──────────┬──────────────────────────────────────────┬────┘
           │                                          │
     ┌─────▼──────────┐               ┌──────────────▼──┐
     │  Observability  │               │  Intelligence   │
     │  - metrics      │               │  - insights     │
     │  - health score │               │  - returns      │
     │  - alerts       │               │  - anomalies    │
     └────────┬───────-┘               └────────┬─────────┘
              │                                 │
              └────────────┬────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ Certification│
                    │ - 6 claims  │
                    │ - status    │
                    └────────────-┘
                           │
                    ┌──────▼──────┐
                    │Reconciliation│
                    │ - 5 levels  │
                    │ - contracts │
                    └────────────-┘
```

## Component Contracts

### ObservabilityEngine (Phase 5)
- `FinancialMetricsCollector.collect(mp, periodo)` → 10 metrics (coverage, health, etc.)
- `FinancialHealthScore.evaluate(mp, periodo)` → 0-100 score with explanation
- `FinancialAlertAggregator.aggregate(mp, periodo)` → reconciliation alerts → API response

### IntelligenceEngine (Phase 7)
- `OperationalInsights.analyze(mp, periodo)` → trends, period changes, tax impact, return rate
- `ReturnReasonAnalyzer.analyze(mp, periodo)` → devoluciones decomposition by detalle
- `FinancialAnomalyDetector.detect(mp, periodo)` → CRITICAL_DELTA, UNCLASSIFIED, ORPHANS, ZERO_REVENUE

### CertificationEngine (Phase 9)
- `CertificationEngine.certify(mp, periodo)` → 6 KPI claims, status (CERTIFIED/DEGRADED/FAILED), pass rate
- Each claim = KPI + description + delta + status + evidence_sql + record_count + impact_amount

## API Endpoints (new)

| Endpoint | Engine | Purpose |
|---|---|---|
| `GET /api/v4/health/financial` | HealthScore | Dashboard health card |
| `GET /api/v4/health/metrics` | MetricsCollector | Raw metrics |
| `GET /api/v4/intelligence/insights` | OperationalInsights | Trend/cost analysis |
| `GET /api/v4/intelligence/returns` | ReturnReasonAnalyzer | Return decomposition |
| `GET /api/v4/intelligence/anomalies` | AnomalyDetector | Anomaly detection |
| `GET /api/v4/certify` | CertificationEngine | Full certification |

## Key Constraints
- Zero `if/else` financial logic in api.py (max 5 lines per endpoint)
- All SQL queries are parameterized and deterministic
- Every anomaly/alert includes `evidence_sql` for traceability
- No modification to existing certified tables or endpoints

## Rollback
- Each phase is independently removable
- API endpoints can be commented out without affecting other routes
- All new files under `engine/v4/{observability,intelligence,certification}/` — isolated from core engine
