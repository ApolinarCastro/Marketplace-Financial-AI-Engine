"""F3-03 Main runner."""
import sys; sys.path.insert(0, ".")
import asyncio
import json
import time
import traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from f3_03_test import *

async def main():
    print("=" * 72)
    print("F3-03 - CONTROLLED INGESTION WITH FINANCIAL FIXTURE")
    print("=" * 72)
    print()

    all_passed = True
    execution_id = f"f3_03_{int(time.time())}"
    evidence = {
        "execution_id": execution_id,
        "test": "F3-03: Controlled Ingestion with Financial Fixture",
        "fixture": "5 rows ML Facturacion XLSX -> 8 ledger rows, $20800 total",
        "fixture_sha256": None,
        "baseline": str(BASELINE),
        "runs": [],
    }

    try:
        Env.setup()
        evidence["fixture_sha256"] = Env.fixture_sha256
        print(f"Fixture SHA256: {Env.fixture_sha256}")
        print(f"Temp raw dir:   {TEMP_RAW}")
        raw_files = list(TEMP_RAW.glob("*"))
        print(f"Files in temp:  {[f.name for f in raw_files]}")
        print()

        # Phase 1: 3 consecutive pipeline runs
        print("-- Phase 1: 3 Pipeline Runs (fresh DB each time) --")
        for run_num in range(1, 4):
            label = f"RUN_{run_num}"
            print(f"\n--- {label} ---")
            try:
                record = await run_pipeline()
                actual = validate_ledger()
                errors = compare(actual)

                verdict = "PASS" if not errors else "FAIL"
                if verdict == "FAIL":
                    all_passed = False

                run_ev = {
                    "run": run_num,
                    "record_status": record.status,
                    "records_inserted": record.records_inserted,
                    "ledger_rows": len(actual["ledger"]),
                    "ledger_total": actual["ledger_total"],
                    "ventas": actual["ventas"],
                    "errors": errors if errors else None,
                    "verdict": verdict,
                }
                evidence["runs"].append(run_ev)

                print(f"  Status: {record.status} | Inserted: {record.records_inserted}")
                print(f"  Ledger: {len(actual['ledger'])} rows, ${actual['ledger_total']}")
                print(f"  Ventas: {actual['ventas']}")
                if errors:
                    for e in errors:
                        print(f"  ERROR: {e}")
                print(f"  Verdict: {verdict}")
            except Exception as e:
                print(f"  EXCEPTION: {e}")
                traceback.print_exc()
                all_passed = False
                evidence["runs"].append({"run": run_num, "error": str(e), "verdict": "FAIL"})

        # Phase 2: Re-ingestion test
        print(f"\n-- Phase 2: Re-ingestion Idempotency Test --")
        try:
            # First run
            rec1 = await run_pipeline()
            act1 = validate_ledger()
            err1 = compare(act1)

            # Second run on same DB (without fresh copy)
            rec2 = await run_pipeline()
            act2 = validate_ledger()
            err2 = compare(act2)

            # Idempotency check
            re_errors = []
            if len(act1["ledger"]) != len(act2["ledger"]):
                re_errors.append(f"row count changed: {len(act1['ledger'])} -> {len(act2['ledger'])}")
            if act1["ledger_total"] != act2["ledger_total"]:
                re_errors.append(f"total changed: {act1['ledger_total']} -> {act2['ledger_total']}")

            if re_errors:
                all_passed = False

            verdict_re = "PASS" if (not err1 and not err2 and not re_errors) else "FAIL"
            if verdict_re != "PASS":
                all_passed = False

            evidence["reingestion"] = {
                "1st_status": rec1.status,
                "1st_inserted": rec1.records_inserted,
                "1st_rows": len(act1["ledger"]),
                "1st_total": act1["ledger_total"],
                "2nd_status": rec2.status,
                "2nd_inserted": rec2.records_inserted,
                "2nd_rows": len(act2["ledger"]),
                "2nd_total": act2["ledger_total"],
                "errors1": err1 if err1 else None,
                "errors2": err2 if err2 else None,
                "idempotency_errors": re_errors if re_errors else None,
                "verdict": verdict_re,
            }

            print(f"  1st: {rec1.status} | {len(act1['ledger'])} rows, ${act1['ledger_total']}")
            print(f"  2nd: {rec2.status} | {len(act2['ledger'])} rows, ${act2['ledger_total']}")
            if err1:
                for e in err1: print(f"  1st ERROR: {e}")
            if err2:
                for e in err2: print(f"  2nd ERROR: {e}")
            if re_errors:
                for e in re_errors: print(f"  IDEMPOTENCY ERROR: {e}")
            print(f"  Verdict: {verdict_re}")
        except Exception as e:
            print(f"  EXCEPTION: {e}")
            traceback.print_exc()
            all_passed = False
            evidence["reingestion"] = {"error": str(e), "verdict": "FAIL"}

    finally:
        Env.teardown()
        print(f"\n-- Cleanup: done --")

    # Final verdict
    print(f"\n{'=' * 72}")
    final_verdict = "CAP001_CERTIFIED" if all_passed else "FIXTURE_VALIDATION_FAILED"
    evidence["final_verdict"] = final_verdict
    print(f"FINAL VERDICT: {final_verdict}")

    # Save evidence
    evid_path = Path(f"evidence/fase_3/{execution_id}.json")
    evid_path.parent.mkdir(parents=True, exist_ok=True)
    evid_path.write_text(json.dumps(evidence, indent=2))
    print(f"Evidence saved: {evid_path}")

    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    asyncio.run(main())
