import logging
from engine.v4.evidence.contracts import CoverageMetric
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.domain.ledger_engine import LedgerEngine
from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine
from engine.v4.certification.certification_engine import CertificationEngine

logger = logging.getLogger("meli.evidence.coverage")


class CoverageAnalyzer:
    def __init__(
        self,
        fe: FinancialEngine,
        le: LedgerEngine,
        re: ReconciliationEngine,
        ce: CertificationEngine,
    ):
        self.fe = fe
        self.le = le
        self.re = re
        self.ce = ce

    def analyze(self, marketplace: str) -> list[CoverageMetric]:
        metrics = []

        ledger_count = self.fe.query_ledger(
            marketplace=marketplace, limit=1, filter_zero=False, operational_only=False,
        )
        total_ledger = ledger_count.get("total_count", 0)

        classified = self.fe.get_financial_records_count(marketplace=marketplace, periodo=None)
        cov_pct = (classified / total_ledger * 100) if total_ledger > 0 else 0.0
        metrics.append(CoverageMetric(
            source="RAW",
            target="Ledger",
            coverage_pct=round(cov_pct, 2),
            source_total=float(total_ledger),
            matched=float(classified),
            method="FinancialEngine.query_ledger().total_count + get_financial_records_count()",
            engine_used="FinancialEngine",
            method_used="get_financial_records_count()",
            details={"classification_coverage": f"{classified}/{total_ledger}"},
        ))

        folio_count = 0
        if total_ledger > 0:
            folio_result = self.fe.query_ledger(
                marketplace=marketplace, limit=10000, filter_zero=False, operational_only=False,
            )
            folio_count = sum(1 for r in folio_result.get("data", []) if r.get("folio_xml"))
        folio_cov = (folio_count / total_ledger * 100) if total_ledger > 0 else 0.0
        metrics.append(CoverageMetric(
            source="Ledger",
            target="XML/DTE",
            coverage_pct=round(folio_cov, 2),
            source_total=float(total_ledger),
            matched=float(folio_count),
            method="FinancialEngine.query_ledger() — folio_xml presence",
            engine_used="FinancialEngine",
            method_used="query_ledger()",
            details={"records_with_folio": folio_count, "total_records": total_ledger},
        ))

        try:
            recon = self.re.validate_marketplace_consistency(marketplace=marketplace)
            metrics.append(CoverageMetric(
                source="Ledger",
                target="Cierre",
                coverage_pct=round(recon.taxonomy_coverage, 2),
                source_total=float(recon.total_records),
                matched=float(recon.total_records - recon.orphan_records),
                method="ReconciliationEngine.validate_marketplace_consistency()",
                engine_used="ReconciliationEngine",
                method_used="validate_marketplace_consistency()",
                details={
                    "orphans": recon.orphan_records,
                    "reconciliation_delta": recon.delta,
                    "certification_status": recon.certification_status,
                },
            ))

            metrics.append(CoverageMetric(
                source="Cierre",
                target="Documentos",
                coverage_pct=round(recon.document_coverage, 2),
                source_total=100.0,
                matched=recon.document_coverage,
                method="ReconciliationEngine.validate_marketplace_consistency().document_coverage",
                engine_used="ReconciliationEngine",
                method_used="validate_marketplace_consistency()",
                details={"document_coverage": recon.document_coverage},
            ))
        except Exception as e:
            logger.warning(f"Reconciliation consistency check failed for {marketplace}: {e}")

        try:
            cert = self.ce.certify(marketplace=marketplace)
            for claim in getattr(cert, "claims", []):
                status = claim.status if hasattr(claim, "status") else "UNKNOWN"
                metrics.append(CoverageMetric(
                    source=claim.kpi,
                    target="Certificación",
                    coverage_pct=100.0 if status == "PASS" else 0.0,
                    source_total=1.0,
                    matched=1.0 if status == "PASS" else 0.0,
                    method="CertificationEngine.certify()",
                    engine_used="CertificationEngine",
                    method_used="certify()",
                    details={"status": status, "description": getattr(claim, "description", "")},
                ))
        except Exception as e:
            logger.warning(f"Certification check failed for {marketplace}: {e}")

        return metrics
