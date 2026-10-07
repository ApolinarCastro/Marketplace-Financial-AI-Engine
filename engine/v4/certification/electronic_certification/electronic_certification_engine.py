"""Electronic Certification Engine Orchestrator"""
from typing import Dict, Any

from .xml_validator import XmlValidator
from .xsd_validator import XsdValidator
from .signature_validator import SignatureValidator
from .caf_validator import CafValidator
from .vat_validator import VatValidator


def can_claim_electronic_certification(result: Dict[str, Any] | None) -> bool:
    """Gate: TRUE only when electronic certification actually executed and passed.

    Requires overall_status == "PASS", which the engine emits solely when
    every mandatory stage executed with PASS/WARNING and none returned
    NOT_IMPLEMENTED (→ PARTIAL) or a hard failure (→ FAIL). Missing
    dependencies, missing XSD, or unexecuted crypto validation can never
    satisfy this gate.
    """
    if not isinstance(result, dict):
        return False
    return result.get("overall_status") == "PASS"

class ElectronicCertificationEngine:
    def __init__(self):
        self.xml_validator = XmlValidator()
        self.xsd_validator = XsdValidator()
        self.signature_validator = SignatureValidator()
        self.caf_validator = CafValidator()
        self.vat_validator = VatValidator()

    def certify(self, xml_content: str) -> Dict[str, Any]:
        """
        Executes the full electronic certification pipeline on a DTE XML.
        """
        result = {
            "overall_status": "PASS",
            "electronic_certificate": {
                "xml": None,
                "xsd": None,
                "signature": None,
                "caf": None,
                "vat": None
            },
            "metadata": {},
            "errors": [],
            "warnings": []
        }

        has_partial = False

        def _handle_stage(stage_name, stage_result):
            nonlocal has_partial
            result["electronic_certificate"][stage_name] = stage_result
            
            if stage_result.get("warnings"):
                result["warnings"].extend(stage_result["warnings"])
                
            status = stage_result.get("status")
            
            if status == "NOT_IMPLEMENTED":
                has_partial = True
                return "CONTINUE"
            
            if status == "PASS" or status == "WARNING":
                return "CONTINUE"
                
            # Anything else is a hard FAIL (FAIL, INVALID_*, EXPIRED_*, ROUNDING_ERROR)
            result["overall_status"] = "FAIL"
            if stage_result.get("errors"):
                result["errors"].extend(stage_result["errors"])
            return "STOP"

        # 1. XML Structure
        xml_res = self.xml_validator.validate(xml_content)
        if _handle_stage("xml", xml_res) == "STOP":
            return result
            
        # Extract metadata to pass downstream
        metadata = xml_res.get("metadata", {})
        result["metadata"] = metadata

        # 2. XSD
        xsd_res = self.xsd_validator.validate(xml_content)
        if _handle_stage("xsd", xsd_res) == "STOP":
            return result

        # 3 & 4. Signature (Structure & Crypto handled internally)
        sig_res = self.signature_validator.validate(xml_content)
        if _handle_stage("signature", sig_res) == "STOP":
            return result
            
        # Merge cert metadata
        if sig_res.get("certificate"):
            result["metadata"]["certificate"] = sig_res["certificate"]

        # 5. CAF
        caf_res = self.caf_validator.validate(xml_content, metadata)
        if _handle_stage("caf", caf_res) == "STOP":
            return result
            
        # Merge CAF metadata
        if caf_res.get("caf_metadata"):
            result["metadata"]["caf"] = caf_res["caf_metadata"]

        # 6. VAT
        vat_res = self.vat_validator.validate(xml_content, metadata)
        if _handle_stage("vat", vat_res) == "STOP":
            return result
            
        # Merge Tax metadata
        if vat_res.get("tax_metadata"):
            result["metadata"]["tax"] = vat_res["tax_metadata"]

        # Finalize Overall Status
        if result["overall_status"] != "FAIL":
            if has_partial:
                result["overall_status"] = "PARTIAL"
            else:
                result["overall_status"] = "PASS"

        return result
