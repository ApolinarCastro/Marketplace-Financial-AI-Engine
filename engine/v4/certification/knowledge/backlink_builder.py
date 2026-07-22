from typing import Dict, Any, List

class BacklinkBuilder:
    def build_relational_links(self, payload_dict: Dict[str, Any]) -> List[str]:
        """
        Builds a deterministic, sorted, and deduplicated list of WikiLinks 
        from the ECCPayload.
        """
        evidence_object = payload_dict.get("evidence_object", {})
        marketplace = payload_dict.get("marketplace_metadata", {}).get("marketplace_id") or payload_dict.get("marketplace", "UNKNOWN")
        doc_type = payload_dict.get("document_type", "UNKNOWN")
        folio = payload_dict.get("folio", "UNKNOWN")
        
        chain_type = evidence_object.get("chain_type", "UNKNOWN")
        certification_status = evidence_object.get("certification_status", "UNKNOWN")
        
        links = set()
        
        # Add primary dimension links
        links.add(f"[[Marketplace/{marketplace}]]")
        links.add(f"[[TipoDTE/{doc_type}]]")
        links.add(f"[[Folio/{folio}]]")
        links.add(f"[[ChainType/{chain_type}]]")
        links.add(f"[[Status/{certification_status}]]")
        
        # Add gaps
        for gap in evidence_object.get("document_gaps", []):
            links.add(f"[[Gap/{gap}]]")
            
        # Return sorted list for deterministic ordering
        return sorted(list(links))
