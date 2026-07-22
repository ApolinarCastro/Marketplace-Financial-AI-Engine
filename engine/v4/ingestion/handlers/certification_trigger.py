"""CertificationTrigger — Stage 4 of ingestion pipeline.

Triggers post-ingestion certification checks:
1. Reconciliation run (ledger vs sources)
2. Certification status update
3. DTE coverage recomputation
4. Gap analysis

Zero financial logic. Pure orchestration via public contracts.
"""
from __future__ import annotations
from typing import Any

from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine
from engine.v4.certification.certification_engine import CertificationEngine
from engine.v4.database import DatabaseV4
from engine.v4.certification.document_gap_engine import DocumentGapEngine


class CertificationTrigger:
    def __init__(
        self,
        db: DatabaseV4 | None = None,
        reconciliation_engine: Any = None,
        certification_engine: Any = None,
        gap_engine: Any = None,
    ):
        self.db = db or DatabaseV4.get(read_only=False)
        self.reconciliation = reconciliation_engine or ReconciliationEngine()
        self.certification = certification_engine or CertificationEngine()
        self.gap_engine = gap_engine or DocumentGapEngine()

    def trigger(self, marketplace: str, period: str | None = None) -> dict[str, Any]:
        result: dict[str, Any] = {
            "reconciliation": {"executed": False, "deltas": {}, "status": "PENDING"},
            "certification": {"executed": False, "claims": {}, "status": "PENDING"},
            "coverage": {"executed": False, "dte": {}, "status": "PENDING"},
            "gaps": {"executed": False, "gaps": [], "status": "PENDING"},
            "errors": [],
        }

        try:
            delta = self.reconciliation.reconcile_ledger_vs_cierre(marketplace, period)
            result["reconciliation"]["executed"] = True
            result["reconciliation"]["deltas"] = delta if delta else {}
            result["reconciliation"]["status"] = "PASS" if not delta else "DELTA_FOUND"
        except Exception as e:
            result["reconciliation"]["status"] = "ERROR"
            result["errors"].append(f"Reconciliation failed: {e}")

        try:
            cert = self.certification.certify(marketplace)
            result["certification"]["executed"] = True
            result["certification"]["claims"] = cert if cert else {}
            result["certification"]["status"] = "PASS" if self._all_certified(cert) else "DEGRADED"
        except Exception as e:
            result["certification"]["status"] = "ERROR"
            result["errors"].append(f"Certification failed: {e}")

        try:
            dte = self.db.query(
                "SELECT COUNT(*) as total, SUM(CASE WHEN folio_xml IS NOT NULL AND folio_xml != '' THEN 1 ELSE 0 END) as with_dte FROM marketplace_ledger_v1 WHERE LOWER(marketplace) = LOWER(?)",
                [marketplace],
            )
            result["coverage"]["executed"] = True
            result["coverage"]["dte"] = {"total": int(dte.iloc[0]["total"]), "with_dte": int(dte.iloc[0]["with_dte"])}
            result["coverage"]["status"] = "PASS"
        except Exception as e:
            result["coverage"]["status"] = "ERROR"
            result["errors"].append(f"Coverage failed: {e}")

        try:
            gaps = self.gap_engine.analyze(document_type="all", marketplace=marketplace)
            gaps_list = []
            if hasattr(gaps, "to_dict"):
                gaps_list = gaps.to_dict().get("gaps", []) if hasattr(gaps, "to_dict") else []
            elif isinstance(gaps, list):
                gaps_list = gaps
            result["gaps"]["executed"] = True
            result["gaps"]["gaps"] = gaps_list
            result["gaps"]["status"] = "PASS" if not gaps_list else "GAPS_FOUND"
        except Exception as e:
            result["gaps"]["status"] = "ERROR"
            result["errors"].append(f"Gap analysis failed: {e}")

        overall = all(
            r["status"] in ("PASS", "DELTA_FOUND", "GAPS_FOUND")
            for r in [result["reconciliation"], result["certification"], result["coverage"], result["gaps"]]
        )
        result["overall_status"] = "PASS" if overall else "DEGRADED"
        return result

    def _all_certified(self, cert: Any) -> bool:
        if not cert:
            return False
        if isinstance(cert, dict):
            claims = list(cert.values())
        elif isinstance(cert, list):
            claims = cert
        else:
            return False
        statuses = [c.get("status") if isinstance(c, dict) else str(c) for c in claims]
        return all(s == "CERTIFIED" for s in statuses)
