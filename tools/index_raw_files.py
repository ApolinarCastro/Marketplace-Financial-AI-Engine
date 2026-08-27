"""CLI tool for RAW Files Indexing & Integrity Registry — CAP-TD-008.

Supports --root, --dry-run, --output flags.
Safe by default (dry-run=True, raw_mutations=0).
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from engine.v4.ingestion.raw_file_indexer import RawFileIndexer


def main():
    parser = argparse.ArgumentParser(description="RAW Files Indexer CLI")
    parser.add_argument("--root", type=str, default="01_Raw", help="Root directory to scan")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Safe simulation mode")
    parser.add_argument("--output", type=str, default="evidence/fase_1b/CAP-TD-008.json", help="Evidence output path")
    args = parser.parse_args()

    indexer = RawFileIndexer(root_dir=args.root)
    records = indexer.scan(execution_id="EXEC-CAP-TD-008-CLI", dry_run=args.dry_run)
    report = indexer.generate_report(records, execution_id="EXEC-CAP-TD-008-CLI", dry_run=args.dry_run)

    print(f"RAW Files Indexing Completed.")
    print(f"Total files scanned: {report['total_files']}")
    print(f"Valid files: {report['valid_files']}")
    print(f"Marketplaces: {json.dumps(report['marketplaces'])}")
    print(f"RAW mutations: {report['raw_mutations']}")

    out_p = Path(args.output)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_p, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    main()
