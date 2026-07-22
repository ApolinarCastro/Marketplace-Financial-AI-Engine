import os
from typing import Dict, Any
from datetime import datetime

class GraphBuilder:
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.graph_schema_version = "1.0"
        self._ensure_directories()
        
    def _ensure_directories(self):
        nodes = ["Marketplace", "TipoDTE", "Folio", "ChainType", "Status", "Gap"]
        for node in nodes:
            os.makedirs(os.path.join(self.vault_path, node), exist_ok=True)
            
    def append_to_indexes(self, payload_dict: Dict[str, Any], evidence_hash: str):
        """
        Strictly Write-Only. Appends the evidence link to all respective index nodes.
        """
        evidence_object = payload_dict.get("evidence_object", {})
        marketplace = payload_dict.get("marketplace_metadata", {}).get("marketplace_id") or payload_dict.get("marketplace", "UNKNOWN")
        doc_type = payload_dict.get("document_type", "UNKNOWN")
        folio = payload_dict.get("folio", "UNKNOWN")
        
        chain_type = evidence_object.get("chain_type", "UNKNOWN")
        certification_status = evidence_object.get("certification_status", "UNKNOWN")
        gaps = evidence_object.get("document_gaps", [])
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        link_str = f"- [[Evidence/{evidence_hash}]] - Generated: {timestamp}\n"
        
        # Define what needs to be appended where
        indexes_to_update = [
            ("Marketplace", marketplace),
            ("TipoDTE", doc_type),
            ("Folio", folio),
            ("ChainType", chain_type),
            ("Status", certification_status)
        ]
        
        for gap in gaps:
            indexes_to_update.append(("Gap", gap))
            
        for folder, file_name in indexes_to_update:
            if not file_name:
                continue
            self._append_to_node(folder, str(file_name), link_str)
            
    def _append_to_node(self, folder: str, file_name: str, link_str: str):
        file_path = os.path.join(self.vault_path, folder, f"{file_name}.md")
        
        # Create header if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"---\ngraph_schema_version: {self.graph_schema_version}\nnode_type: {folder}\nnode_id: {file_name}\n---\n")
                f.write(f"# {folder}: {file_name}\n\n")
                f.write("## Evidence Backlinks\n\n")
                
        # Append
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(link_str)
