import argparse
import json

from engine.v4.pipeline import AntigravityEngineV4


def main() -> None:
    parser = argparse.ArgumentParser(description="Marketplace Conciliacion V4 CLI")
    parser.add_argument(
        "--mode",
        choices=["full", "ingest", "reconcile", "report"],
        default="full",
        help="Modo de ejecucion del pipeline V4",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Omite la generacion de reportes al correr el pipeline completo",
    )
    args = parser.parse_args()

    engine = AntigravityEngineV4()

    if args.mode == "full":
        result = engine.run(skip_reporting=args.no_report)
    elif args.mode == "ingest":
        result = engine.run_ingestion_only()
    elif args.mode == "reconcile":
        result = engine.run_reconciliation_only()
    else:
        from engine.v4.reporting import generate_all_reports

        result = {"reports": generate_all_reports(engine.db)}

    print(json.dumps(result, indent=2, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
