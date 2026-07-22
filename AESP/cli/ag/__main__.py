import argparse
import sys
from .commands import doctor, registry, skill, capability, workflow, knowledge, project, audit, validate, install, upgrade, run

def main():
    parser = argparse.ArgumentParser(description="Antigravity Enterprise Skills Platform (AESP) CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ag doctor
    parser_doctor = subparsers.add_parser("doctor", help="Check AESP system health and statuses")
    parser_doctor.add_argument("--project", action="store_true", help="Check project specific status")

    # ag registry
    parser_registry = subparsers.add_parser("registry", help="Manage registries")

    # ag run
    parser_run = subparsers.add_parser("run", help="Execute a project workflow")
    parser_run.add_argument("project", help="Project name")
    parser_run.add_argument("workflow", help="Workflow name")

    # other commands
        # ag workflow
    parser_workflow = subparsers.add_parser("workflow", help="Manage workflows")
    parser_workflow.add_argument("action", nargs="?", help="Action to perform (e.g. audit)")

    for cmd in ["skill", "capability", "knowledge", "project", "audit", "validate", "install", "upgrade"]:
        subparsers.add_parser(cmd, help=f"{cmd.capitalize()} management")

    args = parser.parse_args()

    if args.command == "doctor":
        doctor.run(args)
    elif args.command == "registry":
        registry.run(args)
    elif args.command == "run":
        run.execute_run(args)
    elif args.command == "workflow":
        workflow.run(args)
    elif args.command:
        print(f"Command '{args.command}' is acknowledged but functionality is pending.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
