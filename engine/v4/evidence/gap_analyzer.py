import logging
from engine.v4.evidence.contracts import GapReport
from engine.v4.evidence.coverage_analyzer import CoverageAnalyzer
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.certification.certification_engine import CertificationEngine

logger = logging.getLogger("meli.evidence.gap")


class GapAnalyzer:
    def __init__(
        self,
        coverage: CoverageAnalyzer,
        fe: FinancialEngine,
        ce: CertificationEngine,
    ):
        self.coverage = coverage
        self.fe = fe
        self.ce = ce

    def analyze(self, marketplace: str) -> list[GapReport]:
        gaps = []
        mc = marketplace.upper()

        coverage_metrics = self.coverage.analyze(marketplace)

        for m in coverage_metrics:
            if m.coverage_pct < 100.0:
                gaps.append(GapReport(
                    gap_id=f"COV-{m.source}-{m.target}",
                    marketplace=mc,
                    description=f"Coverage gap: {m.source} -> {m.target} = {m.coverage_pct:.1f}%",
                    root_cause=f"Only {m.matched:.0f} of {m.source_total:.0f} records covered",
                    impact=f"Missing {m.source_total - m.matched:.0f} records in {m.target}",
                    priority="ALTA" if m.coverage_pct < 50 else "MEDIA",
                ))

        if mc == "ML":
            gaps.append(GapReport(
                gap_id="POSCOBRO",
                marketplace=mc,
                description="PosCobro paired mechanisms still in P&L (DEC-019 applied but not fully removed from cierre)",
                root_cause="Classification re-run needed to propagate include_in_operational_pnl=0",
                impact="~$94.4M RN overstatement if not excluded",
                priority="ALTA",
            ))

        if mc in ("PARIS", "FALABELLA"):
            cov_p = next((m.coverage_pct for m in coverage_metrics if m.target == "XML/DTE"), 100.0)
            if cov_p < 5:
                gaps.append(GapReport(
                    gap_id="DTE_LINK",
                    marketplace=mc,
                    description=f"{mc} DTE/XML coverage is {cov_p:.1f}% — no folio_xml linkage",
                    root_cause="DTEIndexer heuristic limitation: no order_id matcher implemented",
                    impact="Cannot certify XML-to-Ledger traceability",
                    priority="ALTA",
                ))

        try:
            alerts = self.fe.query_audit(marketplace=mc, limit=50)
            for alert in alerts.get("data", []):
                gaps.append(GapReport(
                    gap_id=f"AUDIT-{alert.get('id', 'unknown')}",
                    marketplace=mc,
                    description=alert.get("descripcion", alert.get("check_name", "Unknown alert")),
                    root_cause=alert.get("detalle", "Verifiable through query_audit()"),
                    impact="Audit alert active",
                    priority="MEDIA",
                ))
        except Exception as e:
            logger.warning(f"Audit query failed for {marketplace}: {e}")

        try:
            cert = self.ce.certify(marketplace=mc)
            if hasattr(cert, "status") and cert.status != "CERTIFIED":
                gaps.append(GapReport(
                    gap_id=f"CERT-{cert.status}",
                    marketplace=mc,
                    description=f"Certification status: {cert.status}",
                    root_cause=f"Pass rate: {cert.pass_rate:.1f}%",
                    impact="Marketplace not fully certified",
                    priority="ALTA" if cert.status == "FAILED" else "MEDIA",
                ))
        except Exception as e:
            logger.warning(f"Certification check failed for {marketplace}: {e}")

        return gaps
