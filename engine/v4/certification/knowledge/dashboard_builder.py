import os
import shutil

class DashboardBuilder:
    def __init__(self, vault_path: str, templates_dir: str = None):
        self.vault_path = vault_path
        if not templates_dir:
            self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        else:
            self.templates_dir = templates_dir
            
    def deploy_dashboards(self):
        """
        Write-Only. Copies predefined Dataview Markdown dashboards from 
        the templates directory into the Obsidian Vault.
        """
        dashboards_vault_dir = os.path.join(self.vault_path, "Dashboards")
        os.makedirs(dashboards_vault_dir, exist_ok=True)
        
        dashboards = [
            "executive_dashboard.md",
            "documentary_dashboard.md",
            "risk_dashboard.md",
            "marketplace_dashboard.md"
        ]
        
        for dashboard in dashboards:
            src_path = os.path.join(self.templates_dir, dashboard)
            dest_path = os.path.join(dashboards_vault_dir, dashboard)
            
            # If the template exists, copy it to the Vault
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
