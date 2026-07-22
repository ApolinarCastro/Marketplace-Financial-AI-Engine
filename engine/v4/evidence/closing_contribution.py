from engine.v4.evidence.contracts import ClosingContribution
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine
from engine.v4.certification.certification_engine import CertificationEngine


class ClosingContributionAnalyzer:
    def __init__(
        self,
        fe: FinancialEngine,
        re: ReconciliationEngine,
        ce: CertificationEngine,
    ):
        self.fe = fe
        self.re = re
        self.ce = ce

    def analyze(self, transaction_id: str) -> ClosingContribution:
        records = self.fe.query_ledger(order_id=transaction_id, limit=1)
        if not records.get("data"):
            return ClosingContribution(participating=False)

        row = records["data"][0]
        marketplace = row.get("marketplace")
        periodo = row.get("periodo")

        if not marketplace or not periodo:
            return ClosingContribution(
                participating=True,
                financial_group=row.get("financial_group"),
                operational_pnl=bool(row.get("include_in_operational_pnl", 1)),
            )

        cierre = self.fe.query_cierre(marketplace=marketplace, periodo=periodo)
        try:
            recon = self.re.validate_marketplace_consistency(marketplace=marketplace, periodo=periodo)
        except Exception:
            recon = None
        try:
            cert = self.ce.certify(marketplace=marketplace, periodo=periodo)
        except Exception:
            cert = None

        return ClosingContribution(
            participating=True,
            closing_batch=cierre[0].get("batch_id") if cierre else None,
            closing_period=periodo,
            financial_group=row.get("financial_group"),
            operational_pnl=bool(row.get("include_in_operational_pnl", 1)),
            reconciliation_status=recon.certification_status if recon else "NO_VERIFICADO",
            certification_status=cert.status if cert else "NO_VERIFICADO",
        )
