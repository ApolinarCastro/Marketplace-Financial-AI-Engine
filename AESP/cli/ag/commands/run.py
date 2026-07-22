import os
import sys
# Add workspace root to sys.path to allow importing AESP
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

try:
    from AESP.runtime.engine import ProjectRuntime, WorkflowEngine
except ImportError as e:
    print(f"Error loading AESP runtime: {e}")
    sys.exit(1)

def execute_run(args):
    # Locate project.yaml in the current working directory
    cwd = os.getcwd()
    pr = ProjectRuntime(cwd)
    try:
        config = pr.load()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
        
    if config['project']['name'] != args.project:
        print(f"Warning: Project name mismatch. Expected {args.project}, found {config['project']['name']}")
        
    we = WorkflowEngine()
    we.execute(args.project, args.workflow)
