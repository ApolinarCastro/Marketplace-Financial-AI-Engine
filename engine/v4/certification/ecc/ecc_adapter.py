"""ECC Orchestrator Adapter"""
from typing import Dict, Any

from engine.v4.certification.electronic_certification.electronic_certification_engine import ElectronicCertificationEngine
from .ecc_mapping import ECCMapping
from .ecc_normalizer import ECCNormalizer
from .ecc_payload import ECCPayload
from .marketplaces.marketplace_registry import MarketplaceRegistry
from .evidence.evidence_engine import EvidenceEngine

class ECCAdapter:
    def __init__(self):
        self.validator = ElectronicCertificationEngine()
        self.mapper = ECCMapping()
        self.normalizer = ECCNormalizer()
        self.marketplace_registry = MarketplaceRegistry()
        self.evidence_engine = EvidenceEngine()

    def process(self, xml_content: str, marketplace: str = None) -> ECCPayload:
        """
        Orchestrates the validation and extraction of an electronic document.
        Returns an ECCPayload containing normalized data and the certification result.
        """
        # 1. Validation
        cert_result = self.validator.certify(xml_content)
        
        # We always extract data, even if validation fails, because the DocumentaryEngine
        # might need to log the invalid document's metadata (e.g. for anomaly detection).
        # However, the evidence_level will clearly state it's invalid.
        
        # 2. Raw Extraction
        raw_data = self.mapper.extract(xml_content)
        
        # 3. Normalization
        norm_data = self.normalizer.normalize(raw_data)
        
        # 4. Payload Assembly
        payload = ECCPayload(
            document_type=norm_data.get("document_type"),
            marketplace=marketplace,
            issuer_tax_id=norm_data.get("issuer_tax_id"),
            receiver_tax_id=norm_data.get("receiver_tax_id"),
            folio=norm_data.get("folio"),
            issue_date=norm_data.get("issue_date"),
            net_amount=norm_data.get("net_amount"),
            vat_amount=norm_data.get("vat_amount"),
            exempt_amount=norm_data.get("exempt_amount"),
            total_amount=norm_data.get("total_amount"),
            references=norm_data.get("references", []),
            items=norm_data.get("items", []),
            electronic_certificate=cert_result
        )
        
        # 5. Marketplace Enrichment
        marketplace_plugin = self.marketplace_registry.get_plugin(marketplace)
        payload = marketplace_plugin.enrich_payload(payload)
        
        # 6. Evidence Consolidation
        evidence = self.evidence_engine.consolidate(payload, cert_result)
        payload.evidence_object = evidence.to_dict()
        
        return payload
