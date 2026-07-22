from typing import Dict, Any, List
from .evidence_models import EvidenceObject
from ..ecc_payload import ECCPayload

class EvidenceEngine:
    def _find_document_gaps(self, payload: ECCPayload) -> List[str]:
        gaps = []
        if not payload.issuer_tax_id:
            gaps.append("MISSING_ISSUER_TAX_ID")
        if not payload.receiver_tax_id:
            gaps.append("MISSING_RECEIVER_TAX_ID")
        if not payload.folio:
            gaps.append("MISSING_FOLIO")
        if not payload.issue_date:
            gaps.append("MISSING_ISSUE_DATE")
        if payload.total_amount is None:
            gaps.append("MISSING_TOTAL_AMOUNT")
        return gaps

    def consolidate(self, payload: ECCPayload, cert_result: Dict[str, Any]) -> EvidenceObject:
        """
        Consolidates payload gaps and certification trace into a single frozen EvidenceObject.
        """
        certification_status = cert_result.get("overall_status", "UNKNOWN")
        evidence_level = certification_status
        chain_type = payload.chain_type or "UNKNOWN_CHAIN"
        
        # Build validation trace from the certificate
        validation_trace = []
        for error in cert_result.get("errors", []):
            if isinstance(error, dict):
                validation_trace.append({
                    "type": "ERROR",
                    "component": error.get("validator", "UNKNOWN"),
                    "code": error.get("code", "UNKNOWN_ERROR"),
                    "message": error.get("message", str(error))
                })
            else:
                validation_trace.append({
                    "type": "ERROR",
                    "component": "ElectronicCertificationEngine",
                    "code": "VALIDATION_ERROR",
                    "message": str(error)
                })
            
        for warning in cert_result.get("warnings", []):
            if isinstance(warning, dict):
                validation_trace.append({
                    "type": "WARNING",
                    "component": warning.get("validator", "UNKNOWN"),
                    "code": warning.get("code", "UNKNOWN_WARNING"),
                    "message": warning.get("message", str(warning))
                })
            else:
                validation_trace.append({
                    "type": "WARNING",
                    "component": "ElectronicCertificationEngine",
                    "code": "VALIDATION_WARNING",
                    "message": str(warning)
                })

        document_gaps = self._find_document_gaps(payload)
        
        evidence = EvidenceObject(
            evidence_level=evidence_level,
            chain_type=chain_type,
            certification_status=certification_status,
            validation_trace=validation_trace,
            document_gaps=document_gaps
        )
        
        return evidence
