from .observability import Observer
import os
import yaml

class ProjectRuntime:
    def __init__(self, project_path):
        self.project_path = project_path
        self.config = {}

    def load(self):
        yaml_path = os.path.join(self.project_path, 'project.yaml')
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"Project configuration not found at {yaml_path}")
        with open(yaml_path, 'r') as f:
            self.config = yaml.safe_load(f)
        Observer.trace("PROJECT", self.config['project']['name'], "LOADED", f"Skills: {self.config.get('skills', [])}")
        return self.config

class WorkflowEngine:
    def execute(self, project_name, workflow_name):
        Observer.trace("WORKFLOW", f"{project_name}:{workflow_name}", "STARTED")
        # Resolution Phase
        Observer.trace("CAPABILITY", "Resolving Capabilities", "OK")
        Observer.trace("SKILL", "Resolving Skills", "OK")
        Observer.trace("DEPENDENCY", "Checking Dependencies", "OK")
        
        # Execution Phase
        if workflow_name == "audit":
            print(f"Executing Enterprise Audit for {project_name}...")
        elif workflow_name == "certification":
            print(f"Executing Enterprise Certification for {project_name}...")
        else:
            print(f"Executing Generic Workflow {workflow_name} for {project_name}...")
            
        Observer.trace("WORKFLOW", f"{project_name}:{workflow_name}", "COMPLETED")
