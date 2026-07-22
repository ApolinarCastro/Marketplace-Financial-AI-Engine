from typing import Dict, Any
from datetime import datetime
import json

class MarkdownBuilder:
    def build_evidence_markdown(self, payload_dict: Dict[str, Any]) -> str:
        """
        Builds a deterministic markdown string containing YAML Frontmatter
        and formatted body content based on the ECCPayload (and its embedded evidence_object).
        """
        evidence_object = payload_dict.get("evidence_object", {})
        marketplace = payload_dict.get("marketplace_metadata", {}).get("marketplace_id") or payload_dict.get("marketplace", "UNKNOWN")
        doc_type = payload_dict.get("document_type", "UNKNOWN")
        folio = payload_dict.get("folio", "UNKNOWN")
        
        evidence_hash = evidence_object.get("evidence_hash", "UNKNOWN_HASH")
        evidence_schema_version = evidence_object.get("evidence_schema_version", "1.0")
        chain_type = evidence_object.get("chain_type", "UNKNOWN")
        evidence_level = evidence_object.get("evidence_level", "UNKNOWN")
        certification_status = evidence_object.get("certification_status", "UNKNOWN")
        tags = [f"evidence/{evidence_level.lower()}", f"marketplace/{marketplace.lower()}", f"document/{doc_type}"]
        aliases = [f"Evidence-{folio}-{marketplace}"]

        # 1. Build Frontmatter
        lines = []
        lines.append("---")
        lines.append(f"evidence_hash: {evidence_hash}")
        lines.append(f"evidence_schema_version: {evidence_schema_version}")
        lines.append(f"marketplace: {marketplace}")
        lines.append(f"document_type: {doc_type}")
        lines.append(f"folio: {folio}")
        lines.append(f"chain_type: {chain_type}")
        lines.append(f"evidence_level: {evidence_level}")
        lines.append(f"certification_status: {certification_status}")
        
        lines.append("tags:")
        for t in tags:
            lines.append(f"  - {t}")
            
        lines.append("aliases:")
        for a in aliases:
            lines.append(f"  - {a}")
            
        lines.append("---")
        lines.append("")
        
        # 2. Build Markdown Body
        lines.append(f"# Evidence Report: {folio}")
        lines.append("")
        lines.append(f"**Generated:** {datetime.utcnow().isoformat()}Z")
        lines.append("")
        
        # Gaps Section
        gaps = evidence_object.get("document_gaps", [])
        if gaps:
            lines.append("## > [!WARNING] Document Gaps")
            for gap in gaps:
                lines.append(f"- {gap}")
            lines.append("")
        else:
            lines.append("## > [!SUCCESS] Document Gaps")
            lines.append("No critical gaps detected.")
            lines.append("")

        # Validation Trace Section
        lines.append("## Validation Trace")
        trace = evidence_object.get("validation_trace", [])
        if not trace:
            lines.append("No errors or warnings recorded.")
            lines.append("")
        else:
            for entry in trace:
                entry_type = entry.get("type", "INFO")
                if entry_type == "ERROR":
                    lines.append(f"> [!ERROR] {entry.get('component', 'Unknown')} - {entry.get('code', 'Unknown')}")
                elif entry_type == "WARNING":
                    lines.append(f"> [!WARNING] {entry.get('component', 'Unknown')} - {entry.get('code', 'Unknown')}")
                else:
                    lines.append(f"> [!INFO] {entry.get('component', 'Unknown')} - {entry.get('code', 'Unknown')}")
                lines.append(f"> {entry.get('message', '')}")
                lines.append("")
                
        # Relational Graph Section
        from .backlink_builder import BacklinkBuilder
        builder = BacklinkBuilder()
        relational_links = builder.build_relational_links(payload_dict)
        if relational_links:
            lines.append("## Relational Graph")
            for link in relational_links:
                lines.append(f"- {link}")
            lines.append("")

        # Raw Payload Debug Section
        lines.append("## Embedded ECCPayload")
        lines.append("```json")
        lines.append(json.dumps(payload_dict, indent=2))
        lines.append("```")
        
        return "\n".join(lines)
