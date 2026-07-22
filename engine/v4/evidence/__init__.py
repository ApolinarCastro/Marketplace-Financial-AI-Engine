from engine.v4.evidence.contracts import EvidenceResult, ClosingContribution, CashTraceStatus
from engine.v4.evidence.evidence_link_registry import EvidenceLinkRegistry
from engine.v4.evidence.closing_contribution import ClosingContributionAnalyzer
from engine.v4.evidence.cash_trace import CashTrace
from engine.v4.evidence.coverage_analyzer import CoverageAnalyzer
from engine.v4.evidence.gap_analyzer import GapAnalyzer
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.domain.ledger_engine import LedgerEngine
from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine
from engine.v4.certification.certification_engine import CertificationEngine


class EvidenceOrchestrator:
    def __init__(
        self,
        fe: FinancialEngine | None = None,
        le: LedgerEngine | None = None,
        re: ReconciliationEngine | None = None,
        ce: CertificationEngine | None = None,
    ):
        self.fe = fe or FinancialEngine()
        self.le = le or LedgerEngine(db=self.fe.db)
        self.re = re or ReconciliationEngine(db=self.fe.db)
        self.ce = ce or CertificationEngine(db=self.fe.db)

        self.links = EvidenceLinkRegistry(self.fe)
        self.closing = ClosingContributionAnalyzer(self.fe, self.re, self.ce)
        self.cash = CashTrace()
        self.coverage = CoverageAnalyzer(self.fe, self.le, self.re, self.ce)
        self.gaps = GapAnalyzer(self.coverage, self.fe, self.ce)

    def trace(self, identifier: str, id_type: str = "id_orden") -> list:
        return self.links.resolve(identifier, id_type)

    def get_closing_contribution(self, transaction_id: str) -> ClosingContribution:
        return self.closing.analyze(transaction_id)

    def get_cash_trace(self, order_id: str) -> CashTraceStatus:
        return self.cash.trace(order_id)

    def get_coverage(self, marketplace: str) -> list:
        return self.coverage.analyze(marketplace)

    def get_gaps(self, marketplace: str) -> list:
        return self.gaps.analyze(marketplace)

    def get_full_evidence(self, identifier: str, id_type: str = "id_orden") -> EvidenceResult:
        links = self.trace(identifier, id_type)
        marketplace = links[0].marketplace if links else None
        periodo = links[0].periodo if links else None
        closing = None
        coverage = []
        gaps = []
        cash = None

        if links and marketplace and periodo:
            tx_id = links[0].target_identifier
            closing = self.get_closing_contribution(tx_id)
            coverage = self.get_coverage(marketplace)
            gaps = self.get_gaps(marketplace)
            cash = self.get_cash_trace(identifier)

        return EvidenceResult(
            marketplace=marketplace or "unknown",
            periodo=periodo,
            trace=links,
            closing=closing,
            coverage=coverage,
            gaps=gaps,
            cash_trace=cash,
        )
