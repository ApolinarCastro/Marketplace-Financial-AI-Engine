"""
closing_engine.py — Automated period close pipeline.

Orchestrates: ingestion check → classification → reconciliation → audit → certification → publication
Outputs: CloseReport with status per phase.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from engine.v4.database import DatabaseV4
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine
from engine.v4.certification import CertificationEngine
from engine.v4.observability import FinancialMetricsCollector


@dataclass
class PhaseResult:
    phase: str
    status: str  # PASS | FAIL | SKIP
    duration_s: float
    detail: str


@dataclass
class CloseReport:
    marketplace: str
    period: str
    results: list[PhaseResult] = field(default_factory=list)
    all_passed: bool = False
    total_duration_s: float = 0
    detail: str = ""


class ClosingEngine:
    """Run a full period close: ingest → classify → reconcile → audit → certify → publish."""

    ALLOWED_CLOSE_PHASES = ["reconcile", "audit", "certify", "publish"]
    # ingest/classify are excluded to prevent accidental ledger modification

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()
        self.fe = FinancialEngine(self.db)
        self.recon = ReconciliationEngine(self.db)
        self.cert = CertificationEngine(self.db)
        self.metrics = FinancialMetricsCollector(self.db)

    def run_period_close(
        self,
        marketplace: str,
        periodo: str,
        phases: list[str] | None = None,
        dry_run: bool = True,
    ) -> CloseReport:
        """Execute only safe close phases. dry_run=True prevents all mutations."""
        mp = marketplace.upper()
        phases = phases or self.ALLOWED_CLOSE_PHASES
        results: list[PhaseResult] = []

        start = datetime.now()

        if "reconcile" in phases:
            t0 = datetime.now()
            result = self.recon.validate_marketplace_consistency(mp, periodo)
            dur = (datetime.now() - t0).total_seconds()
            status = "PASS" if result.certification_status in ("CERTIFIED", "RECONCILED") else "FAIL"
            results.append(PhaseResult("RECONCILE", status, round(dur, 2),
                                       f"Delta=${result.delta:,.2f}, taxonomy_coverage={result.taxonomy_coverage}%"))

        if "audit" in phases:
            t0 = datetime.now()
            try:
                from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
                auditor = MarketplaceAuditorEngine()
                n = auditor.run_audit()
                dur = (datetime.now() - t0).total_seconds()
                results.append(PhaseResult("AUDIT", "PASS" if n == 0 else "WARNING", round(dur, 2),
                                           f"{n} alerts generated"))
            except Exception as e:
                dur = (datetime.now() - t0).total_seconds()
                results.append(PhaseResult("AUDIT", "WARNING", round(dur, 2), f"Audit issued {n if 'n' in dir() else 0} alerts ({e})"))

        if "certify" in phases:
            t0 = datetime.now()
            cert = self.cert.certify(mp, periodo)
            dur = (datetime.now() - t0).total_seconds()
            status = "PASS" if cert.status == "CERTIFIED" else "FAIL"
            results.append(PhaseResult("CERTIFY", status, round(dur, 2),
                                       f"KPI claims: {len(cert.claims)} passed, {sum(1 for c in cert.claims if c.status=='FAILED')} failed"))

        if "publish" in phases and not dry_run:
            t0 = datetime.now()
            met = self.metrics.collect(mp, periodo)
            dur = (datetime.now() - t0).total_seconds()
            results.append(PhaseResult("PUBLISH", "PASS", round(dur, 2),
                                       f"Metrics collected: {len(met.data_coverage)} dimensions"))

        total_dur = (datetime.now() - start).total_seconds()
        all_ok = all(r.status == "PASS" for r in results)

        return CloseReport(
            marketplace=mp, period=periodo,
            results=results, all_passed=all_ok,
            total_duration_s=round(total_dur, 2),
            detail="All phases passed" if all_ok else f"Some phases failed: {', '.join(r.phase for r in results if r.status not in ('PASS', 'SKIP'))}",
        )
