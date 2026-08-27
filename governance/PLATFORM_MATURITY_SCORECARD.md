# P27 Platform Maturity Scorecard — Marketplace Financial AI Engine

**Methodology**: 15 dimensions scored 0-10. Evidence-based scoring. Each dimension has 5+ sub-criteria. Final score is arithmetic mean.

---

## 1. Architecture (3.5/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Modularity | 4 | 12 engines but tight coupling via FinancialEngine god object |
| Scalability | 2 | Single DuckDB file is bottleneck. No read replicas, no sharding. |
| Extensibility | 4 | Adding new MP requires changes to 5+ files |
| Separation of concerns | 3 | Engine->Engine imports create layer violations |
| Technology choices | 4 | DuckDB + FastAPI are good choices; JSON exports at root are not |
| **Weighted** | **3.5** | |

## 2. Financial Model (5.5/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Single source of truth | 7 | Cierre reconciliation is legitimate (69/69 periods) |
| Accounting correctness | 6 | Sign convention is consistent. DEC-019 correctly implemented. |
| Traceability | 6 | Lineage engine exists but returns raw DB rows |
| Coverage (4 MPs) | 5 | All 4 MPs present but PARIS/FALABELLA data lags 2 months |
| Concept completeness | 4 | 96 concepts in CONCEPT_REGISTRY_V2 but knowledge/ directory empty |
| Signal/Noise taxonomy | 7 | Well-designed. ML 70/71, RIPLEY 12/32 correct. |
| **Weighted** | **5.5** | |

## 3. Document Model (3/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| DTE parsing | 5 | DTEIndexer works for 4 MP directories |
| XML coverage ML | 7 | 89.4% folio_xml coverage |
| XML coverage RIPLEY | 2 | 407 XMLs found but "NOT certified" |
| XML coverage PARIS | 1 | 68 indexed, 0 linked to ledger |
| XML coverage FALABELLA | 0 | 0% |
| DTE-to-Ledger linking | 1 | 0/68 PARIS/FALABELLA linked |
| **Weighted** | **3** | |

## 4. ETL Pipeline (3.5/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Pipeline automation | 2 | Manual surgical_loader.py execution |
| Idempotency | 3 | `insert_df` with dedup_cols partially handles re-runs |
| Error handling | 3 | Excel auto-header detection is fragile |
| Data validation | 4 | QualityEngine 7 checks are useful |
| Orchestration | 0 | No orchestration. No scheduler. Manual. |
| Portability | 2 | Hardcoded C:\Users\ASUS\... paths everywhere |
| **Weighted** | **3.5** | |

## 5. Data Model (4/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Schema design | 5 | 3 core tables are logical. No formal schema versioning. |
| Indices | 0 | Zero indices defined |
| Referential integrity | 0 | No FKs, no constraints |
| NULL handling | 3 | `COALESCE(include_in_operational_pnl,1)=1` repeated in 11 queries |
| Migration strategy | 0 | None. `_v1` suffix implies intent only. |
| Performance | 4 | DuckDB columnar is fast for aggregates. No query profiling. |
| **Weighted** | **4** | |

## 6. Knowledge Layer (2/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Taxonomy completeness | 4 | YAML + JSON taxonomies exist but in wrong location |
| Concept registry | 0 | CONCEPT_REGISTRY_V2.md referenced but file does not exist |
| Event registry | 0 | EVENT_REGISTRY_V2.md referenced but file does not exist |
| Cash role registry | 0 | CASH_ROLE_REGISTRY_V1.md referenced but file does not exist |
| Knowledge index | 0 | knowledge_index.yaml referenced but file does not exist |
| Documentation accuracy | 1 | CLAUDE.md claims knowledge/ directory; it's empty |
| **Weighted** | **2** | |

## 7. Governance (6.5/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Decision documentation | 8 | 36 DECs documented. Extensive governance reports (50+). |
| Policy enforcement | 4 | POLICY_REGISTRY.json exists but is manual |
| Certification process | 7 | CertificationEngine + automated gate are genuine strengths |
| Audit trail | 5 | Auditor engine exists. 22K alerts but 0 for ML. |
| Regulatory compliance | 0 | No evidence of SII/DTE compliance verification |
| Automated governance | 5 | Certification gate is innovative. Rest is manual. |
| **Weighted** | **6.5** | |

## 8. Code Quality (3.5/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Type hints | 5 | Phase 12+ code uses `from __future__ import annotations`. Legacy code does not. |
| Testing coverage | 4 | 273 tests pass but many are shallow |
| Error handling | 3 | Silent `except: continue` patterns. Bare `except Exception`. |
| Code duplication | 2 | Period calculation logic repeated across 6+ files |
| Documentation strings | 4 | Module docstrings present. Inline comments minimal. |
| Dead code | 2 | JSON export files, _archive scripts, __pycache__ committed |
| **Weighted** | **3.5** | |

## 9. UX (4/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Dashboard completeness | 5 | Two dashboards with convergence effort |
| Data freshness awareness | 2 | No indication to user that data is stale |
| Mobile responsiveness | 2 | Tailwind CDN but no mobile breakpoint testing |
| Loading states | 1 | No loading spinners, no skeleton screens |
| Error states | 2 | Silent failures, no user-visible error handling |
| Navigation | 4 | Links between dashboards. No breadcrumbs. |
| **Weighted** | **4** | |

## 10. Performance (3/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Query optimization | 3 | No query profiling. Repeated COALESCE patterns. |
| Caching | 2 | No caching layer. Every request hits DuckDB. |
| Async architecture | 4 | FastAPI async routes. DuckDB is single-connection. |
| Compression | 0 | No response compression |
| Large dataset handling | 2 | DuckDB handles analytical queries well. No pagination optimization. |
| **Weighted** | **3** | |

## 11. Product Readiness (3.5/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Feature completeness | 4 | Features claimed in documentation exceed implementation |
| Data freshness | 2 | Junio 2026: 0 rows for all MPs |
| User feedback loop | 0 | No user testing, no analytics, no feedback mechanisms |
| Onboarding | 1 | No setup documentation. Hardcoded paths prevent other users. |
| Deployment | 0 | No deployment configuration |
| **Weighted** | **3.5** | |

## 12. Commercial Readiness (5/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Value proposition | 7 | Financial reconciliation is clear, measurable value |
| Market need | 7 | Multi-MP reconciliation solves a real problem |
| Competitive differentiation | 6 | SII DTE integration is a legitimate moat |
| Scalability | 0 | Single-instance, single-developer, no multi-tenant |
| Pricing model | 0 | Not defined |
| Sales materials | 0 | None |
| **Weighted** | **5** | |

## 13. Competitive Analysis (5/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| SII DTE integration | 7 | XML parsing is a genuine differentiator for Chilean market |
| Multi-MP coverage | 6 | ML + PARIS + RIPLEY + FALABELLA is strong coverage |
| Reconciliation accuracy | 0 | $0 delta claimed but not independently verifiable |
| Ease of integration | 1 | Current architecture prevents third-party integration |
| **Weighted** | **5** | |

## 14. Risk Assessment (HIGH)

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Bus factor | HIGH | CATASTROPHIC | Single developer, no documentation, no CI/CD |
| Documentation drift | HIGH | HIGH | CLAUDE.md claims features that don't exist |
| Hardcoded paths | HIGH | HIGH | Every file contains developer-specific path |
| No backup strategy | MEDIUM | HIGH | Manual snapshots only |
| SQL injection | LOW | CRITICAL | Present in production code path |
| **Weighted risk score** | **HIGH** | | |

## 15. Roadmap Maturity (2/10)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Current phase clarity | 5 | "Phase 17" referenced as next. 16 previous phases documented. |
| Dependency tracking | 1 | No dependency mapping between phases |
| Timeline realism | 2 | 14-phase completion in 30 days is aggressive |
| Milestone verification | 1 | "COMPLETED" deliverables with no executable artifacts |
| **Weighted** | **2** | |

---

## Composite Score: 3.7/10

### Score Distribution
```
Architecture       ████████░░ 3.5
Financial Model    ██████████░ 5.5
Document Model     ██████░░░░ 3.0
ETL Pipeline       ███████░░░ 3.5
Data Model         ████████░░ 4.0
Knowledge Layer    ████░░░░░░ 2.0
Governance         █████████░░ 6.5
Code Quality       ███████░░░ 3.5
UX                 ████████░░ 4.0
Performance        ██████░░░░ 3.0
Product Readiness  ███████░░░ 3.5
Commercial Read.   █████████░ 5.0
Competitive        █████████░ 5.0
Risk               ████░░░░░░ (HIGH)
Roadmap            ████░░░░░░ 2.0
```

### Verdict by Layer

| Layer | Score | Verdict |
|-------|-------|---------|
| Foundation (Data/ETL/Documents) | 3.2 | Weak — needs infrastructure investment |
| Core (Financial/Governance) | 6.0 | Strongest layer — good concepts, partial execution |
| Delivery (UX/API/Performance) | 3.5 | Functional but not production-ready |
| Business (Product/Market/Risk) | 3.8 | Real potential but no commercial validation |
| Strategy (Roadmap/Maturity) | 2.0 | Documentation debt masks thin implementation |
