import os
from datetime import datetime

class VaultExporter:
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self._ensure_directories()
        
    def _ensure_directories(self):
        os.makedirs(os.path.join(self.vault_path, "Evidence"), exist_ok=True)
        
    def write_evidence(self, filename: str, markdown_content: str):
        """
        Writes the markdown content to the vault.
        Strictly Write-Only. Overwrites existing files with the same name.
        """
        # Ensure filename ends with .md
        if not filename.endswith(".md"):
            filename += ".md"
            
        file_path = os.path.join(self.vault_path, "Evidence", filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        self._append_to_index(filename)
        
    def _append_to_index(self, filename: str):
        """
        Automatically updates an index.md file to link the newly generated evidence.
        """
        index_path = os.path.join(self.vault_path, "index.md")
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # If it doesn't exist, create it with a header
        if not os.path.exists(index_path):
            with open(index_path, "w", encoding="utf-8") as f:
                f.write("# Marketplace Certification Index\n\n")
                f.write("## Evidence Log\n\n")
                
        # Append link to index (Read-append only, no parsing of index)
        with open(index_path, "a", encoding="utf-8") as f:
            f.write(f"- [[Evidence/{filename}]] - Generated: {timestamp}\n")
