from typing import Dict, Any
from .markdown_builder import MarkdownBuilder
from .vault_exporter import VaultExporter
from .graph_builder import GraphBuilder
from .dashboard_builder import DashboardBuilder

class ObsidianAdapter:
    def __init__(self, vault_path: str = "./vault"):
        self.markdown_builder = MarkdownBuilder()
        self.vault_exporter = VaultExporter(vault_path)
        self.graph_builder = GraphBuilder(vault_path)
        self.dashboard_builder = DashboardBuilder(vault_path)
        
    def export_evidence(self, payload_dict: Dict[str, Any]):
        """
        Orchestrates the export of an ECCPayload containing an EvidenceObject
        to the Obsidian Vault.
        """
        # Ensure there is an evidence object to export
        evidence_object = payload_dict.get("evidence_object")
        if not evidence_object:
            raise ValueError("Payload does not contain an evidence_object")
            
        evidence_hash = evidence_object.get("evidence_hash")
        if not evidence_hash:
            raise ValueError("EvidenceObject must have an evidence_hash")
            
        # 1. Build Markdown
        markdown_content = self.markdown_builder.build_evidence_markdown(payload_dict)
        
        # 2. Export to Vault
        filename = f"{evidence_hash}.md"
        self.vault_exporter.write_evidence(filename, markdown_content)
        
        # 3. Update Indexes (Graph Nodes)
        self.graph_builder.append_to_indexes(payload_dict, evidence_hash)

    def deploy_dashboards(self):
        """
        Deploys the static Dataview dashboards into the Vault.
        """
        self.dashboard_builder.deploy_dashboards()
