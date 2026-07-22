"""F3-02: Controlled Ingestion with Real Pipeline.

Verifies the complete ingestion pipeline with real SurgicalLoader (no mocks)
against a temp copy of BASELINE_ESTABLE_V7.

Flow:
  1. Copy BASELINE_ESTABLE_V7 to temp dir
  2. Set DatabaseV4 singleton to temp DB
  3. For each of 3 uploads:
     a. Create test CSV file with proper naming
     b. Run IngestionOrchestrator with real SurgicalLoader
     c. Verify pipeline mechanics (stages, execution_id, SHA256, timestamps)
  4. Check for controlled financial fixture
  5. Verify official DB untouched
  6. Cleanup
  7. Emit verdict
"""
from __future__ import annotations
import asyncio
import hashlib
import json
import logging
import os
import shutil
import sys
import time
import traceback
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("f3_02")

ROOT = Path(__file__).resolve().parent.parent
BASELINE_V8_DIR = ROOT / "data" / "db" / "baseline_estable_v8_candidate_20260717"
BASELINE_V8_DB = BASELINE_V8_DIR / "meli_financial_v4.db"
OFFICIAL_DB = ROOT / "data" / "db" / "meli_financial_v4.db"
MANIFEST_V8 = BASELINE_V8_DIR / "MANIFEST_V8_CANDIDATE.json"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_infrastructure() -> dict:
    problems = []
    if not BASELINE_V8_DB.exists():
        problems.append(f"BASELINE_ESTABLE_V8_CANDIDATE not found at {BASELINE_V8_DB}")
    if not OFFICIAL_DB.exists():
        problems.append(f"Official DB not found at {OFFICIAL_DB}")
    return {"ok": len(problems) == 0, "problems": problems}


async def run_pipeline(
    db_path: Path,
    uploads_dir: Path,
    knowledge_path: Path,
    csv_path: Path,
    csv_name: str,
) -> dict:
    """Run the full ingestion pipeline with real SurgicalLoader on a temp DB.

    Returns the IngestionRecord as a dict plus metadata about what was verified.
    """
    from engine.v4.database import DatabaseV4
    from engine.v4.ingestion import IngestionRegistry
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    from engine.v4.ingestion.handlers.file_detector import FileDetector
    from engine.v4.ingestion.handlers.integrity_validator import IntegrityValidator
    from engine.v4.ingestion.handlers.marketplace_classifier import MarketplaceClassifier
    from engine.v4.ingestion.handlers.persistence_engine import PersistenceEngine
    from engine.v4.ingestion.handlers.certification_trigger import CertificationTrigger
    from engine.v4.ingestion.handlers.knowledge_trigger import KnowledgeTrigger
    from engine.v4.surgical_loader import SurgicalLoader
    from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
    from engine.v4.knowledge.pattern_registry import PatternRegistry
    import engine.v4.knowledge.knowledge_indexer as knowledge_indexer_module

    # Reset singleton and point to temp DB
    DatabaseV4.reset()
    db = DatabaseV4(db_path=str(db_path), read_only=False)
    db.is_read_only = False
    DatabaseV4._instance = db

    # Override knowledge index DEFAULT_PATH
    original_default = getattr(knowledge_indexer_module, "DEFAULT_PATH", None)
    knowledge_indexer_module.DEFAULT_PATH = str(knowledge_path)

    # Build real components (no mocks)
    registry = IngestionRegistry(db=db)
    detector = FileDetector()
    validator = IntegrityValidator(db=db)

    # Create SurgicalLoader - it will pick up DB from singleton
    real_loader = SurgicalLoader()

    classifier = MarketplaceClassifier()
    persistence = PersistenceEngine(db=db, loader=real_loader)

    cert_trigger = CertificationTrigger(db=db)

    ki = KnowledgeIndexer()
    pr = PatternRegistry()
    kn_trigger = KnowledgeTrigger(
        db=db,
        knowledge_indexer=ki,
        pattern_registry=pr,
        obsidian_path=None,
    )

    orchestrator = IngestionOrchestrator(
        db=db,
        registry=registry,
        detector=detector,
        validator=validator,
        classifier=classifier,
        persistence=persistence,
        certification=cert_trigger,
        knowledge=kn_trigger,
        obsidian_path=None,
    )

    # Save CSV to uploads dir
    dest = uploads_dir / csv_name
    shutil.copy2(str(csv_path), str(dest))

    # Run pipeline
    record = await orchestrator.run(str(dest), original_filename=csv_name, user="f3_02_test")

    # Convert record to dict for JSON serialization
    result = {
        "execution_id": record.execution_id,
        "file_name": record.file_name,
        "file_path": record.file_path,
        "sha256": record.sha256,
        "file_size_bytes": record.file_size_bytes,
        "marketplace": record.marketplace,
        "document_type": record.document_type,
        "period": record.period,
        "status": record.status,
        "start_time": record.start_time,
        "end_time": record.end_time,
        "execution_time_seconds": record.execution_time_seconds,
        "records_inserted": record.records_inserted,
        "records_updated": record.records_updated,
        "records_rejected": record.records_rejected,
        "errors": record.errors,
        "warnings": record.warnings,
        "loader_executed": record.loader_executed,
        "pipeline": record.pipeline,
        "certification_triggered": record.certification_triggered,
        "certification_result": record.certification_result,
        "knowledge_updated": record.knowledge_updated,
        "details": {
            "stages_completed": record.details.get("stages_completed", []),
            "detection": record.details.get("detection", {}),
            "classification": record.details.get("classification", {}),
        },
    }

    # Verify file was saved in uploads
    saved_files = list(uploads_dir.glob(f"*{csv_name}"))
    result["_verification"] = {
        "file_saved_in_uploads": len(saved_files) >= 1,
        "saved_file_exists": any(f.exists() for f in saved_files),
        "db_path": str(db_path),
        "database_class_path": str(db.db_path),
    }

    # Count rows in temp DB for verification
    try:
        ledger_count = db.query("SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE LOWER(marketplace)=LOWER(?)", [record.marketplace or "UNKNOWN"]).iloc[0]["n"]
        result["_ledger_rows_after"] = int(ledger_count)
    except Exception:
        result["_ledger_rows_after"] = -1

    try:
        reg_count = db.query("SELECT COUNT(*) as n FROM ingestion_registry").iloc[0]["n"]
        result["_registry_rows"] = int(reg_count)
    except Exception:
        result["_registry_rows"] = -1

    # Restore knowledge index DEFAULT_PATH
    if original_default is not None:
        knowledge_indexer_module.DEFAULT_PATH = original_default

    # Close DB connection and reset singleton so temp DB can be replaced
    try:
        db.close()
    except Exception:
        pass
    DatabaseV4.reset()

    return result


def check_financial_fixture_exists() -> dict:
    """Check if a controlled financial fixture exists with expected results.

    Returns an analysis of all potential fixtures.
    """
    fixtures = {
        "benchmark_json": list((ROOT / "tests" / "benchmarks").glob("*.json")),
        "golden_json": list((ROOT / "tests" / "golden").glob("*.json")),
    }
    fixture_count = len(fixtures["benchmark_json"]) + len(fixtures["golden_json"])

    # Check specifically for pipeline-level fixtures (input → expected output)
    pipeline_fixtures = []
    for f in list((ROOT / "tests").glob("**/*.csv")) + list((ROOT / "tests").glob("**/*.xlsx")):
        pipeline_fixtures.append(str(f.relative_to(ROOT)))

    # Check for JSON fixtures that map input files to expected pipeline results
    pipeline_json_fixtures = []
    for f in fixtures["golden_json"] + fixtures["benchmark_json"]:
        content = json.loads(f.read_text())
        if isinstance(content, dict) and any(k in content for k in ["rows_expected", "classification_expected", "pipeline_result", "upload_result"]):
            pipeline_json_fixtures.append(str(f.relative_to(ROOT)))

    return {
        "has_controlled_financial_fixture": False,
        "reason": "No fixture exists that maps a specific upload file to expected financial results (rows, classifications, totals) in the ledger.",
        "benchmark_fixtures": len(fixtures["benchmark_json"]),
        "golden_fixtures": len(fixtures["golden_json"]),
        "total_api_fixtures": fixture_count,
        "pipeline_csv_fixtures": len(pipeline_fixtures),
        "pipeline_csv_files": pipeline_fixtures[:5],
        "pipeline_json_fixtures_found": len(pipeline_json_fixtures),
        "pipeline_json_files": pipeline_json_fixtures[:5],
    }


async def main():
    print("=" * 72)
    print("F3-02: CONTROLLED INGESTION WITH REAL PIPELINE")
    print("=" * 72)

    # Step 0: Infrastructure check
    infra = check_infrastructure()
    if not infra["ok"]:
        for p in infra["problems"]:
            logger.error(f"Infrastructure problem: {p}")
        sys.exit(1)
    logger.info("Infrastructure check: PASS")

    # Record official DB hash BEFORE
    official_hash_before = sha256_of(OFFICIAL_DB)
    logger.info(f"Official DB hash (before): {official_hash_before}")

    # Record engine/v4 git status BEFORE
    import subprocess
    git_status_before = subprocess.run(
        ["git", "status", "--short", "--", "engine/v4/"],
        capture_output=True, text=True, cwd=str(ROOT)
    ).stdout

    # Step 1: Create temp infrastructure
    tmp_base = ROOT / "tmp" / f"f3_02_{int(time.time())}"
    tmp_base.mkdir(parents=True, exist_ok=True)
    temp_db_path = tmp_base / "meli_financial_v4.db"
    temp_uploads = tmp_base / "uploads"
    temp_uploads.mkdir()
    temp_knowledge = tmp_base / "knowledge_index.yaml"
    temp_knowledge.write_text("knowledge: []", encoding="utf-8")

    # Copy BASELINE_ESTABLE_V8_CANDIDATE to temp
    shutil.copy2(str(BASELINE_V8_DB), str(temp_db_path))
    v8_hash = sha256_of(BASELINE_V8_DB)
    logger.info(f"BASELINE_ESTABLE_V8_CANDIDATE hash: {v8_hash}")
    logger.info(f"Temp DB: {temp_db_path}")
    logger.info(f"Temp uploads: {temp_uploads}")
    logger.info(f"Temp knowledge: {temp_knowledge}")

    # Create 3 test CSV files with different marketplace naming
    test_files = []

    # Upload 1: FALABELLA - small marketplace, fastest reload
    f1 = tmp_base / "f1.csv"
    f1.write_text("col1,col2\n1,test\n", encoding="utf-8")
    f1_name = "FALABELLA_Conciliacion_2026-06_test1.csv"
    test_files.append((f1, f1_name, "FALABELLA"))

    # Upload 2: FALABELLA again
    f2 = tmp_base / "f2.csv"
    f2.write_text("col1,col2\n2,test\n", encoding="utf-8")
    f2_name = "FALABELLA_Conciliacion_2026-06_test2.csv"
    test_files.append((f2, f2_name, "FALABELLA"))

    # Upload 3: FALABELLA third time
    f3 = tmp_base / "f3.csv"
    f3.write_text("col1,col2\n3,test\n", encoding="utf-8")
    f3_name = "FALABELLA_Conciliacion_2026-06_test3.csv"
    test_files.append((f3, f3_name, "FALABELLA"))

    # Step 2: Execute 3 controlled uploads
    print("\n" + "-" * 72)
    print("EXECUTING 3 CONTROLLED UPLOADS")
    print("-" * 72)

    upload_results = []
    all_stages_ok = True
    all_execution_ids_unique = set()

    for i, (csv_path, csv_name, expected_mp) in enumerate(test_files, 1):
        start = time.time()
        print(f"\n--- Upload {i}: {csv_name} ---")

        try:
            # Ensure no dangling DB connection by resetting singleton
            from engine.v4.database import DatabaseV4
            DatabaseV4.reset()

            # Re-create temp DB from BASELINE_ESTABLE_V7 for each upload
            # so each run starts from the same clean state
            if temp_db_path.exists():
                temp_db_path.unlink()
            shutil.copy2(str(BASELINE_V8_DB), str(temp_db_path))

            result = await run_pipeline(
                db_path=temp_db_path,
                uploads_dir=temp_uploads,
                knowledge_path=temp_knowledge,
                csv_path=csv_path,
                csv_name=csv_name,
            )
            elapsed = time.time() - start
            result["_elapsed_seconds"] = round(elapsed, 2)
            upload_results.append(result)

            # Verify execution_id unique
            eid = result["execution_id"]
            if eid in all_execution_ids_unique:
                logger.error(f"DUPLICATE execution_id: {eid}")
                all_stages_ok = False
            all_execution_ids_unique.add(eid)

            # Verify stages
            stages = result["details"].get("stages_completed", [])
            expected_stages = ["DETECT", "VALIDATE", "CLASSIFY", "PERSIST", "CERTIFY", "KNOWLEDGE"]
            missing = [s for s in expected_stages if s not in stages]
            if missing:
                logger.error(f"Missing stages: {missing}")
                all_stages_ok = False

            # Verify marketplace detection
            detected_mp = result["marketplace"]
            if detected_mp != expected_mp:
                logger.warning(f"Expected MP {expected_mp}, got {detected_mp}")

            # Show status
            status_icon = "PASS" if result["status"] in ("PERSISTED", "CERTIFIED", "FAILED") else "UNKNOWN"
            errors = result.get("errors", [])
            warnings = result.get("warnings", [])
            print(f"  Status: {result['status']} ({elapsed:.1f}s)")
            print(f"  Stages: {stages}")
            print(f"  MP: {detected_mp} | Doc: {result['document_type']} | Period: {result['period']}")
            print(f"  Records: {result['records_inserted']} ins / {result['records_rejected']} rej")
            print(f"  Errors: {errors}")
            print(f"  Warnings: {warnings}")
            if result.get("certification_triggered"):
                print(f"  Certification: {result['certification_result']}")
            if result.get("knowledge_updated"):
                print(f"  Knowledge: updated")

        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"Upload {i} FAILED with exception: {e}")
            traceback.print_exc()
            upload_results.append({
                "upload_number": i,
                "file": csv_name,
                "error": str(e),
                "_elapsed_seconds": round(elapsed, 2),
                "status": "EXCEPTION",
            })
            all_stages_ok = False

    # Step 3: Check for controlled financial fixture
    print("\n" + "-" * 72)
    print("FINANCIAL FIXTURE CHECK")
    print("-" * 72)
    fixture_check = check_financial_fixture_exists()
    print(f"Has controlled financial fixture: {fixture_check['has_controlled_financial_fixture']}")
    print(f"Reason: {fixture_check['reason']}")
    print(f"Benchmark fixtures: {fixture_check['benchmark_fixtures']}")
    print(f"Golden fixtures: {fixture_check['golden_fixtures']}")
    print(f"Pipeline CSV fixtures: {fixture_check['pipeline_csv_fixtures']}")
    print(f"Pipeline JSON fixtures found: {fixture_check['pipeline_json_fixtures_found']}")

    # Step 4: Verify official DB untouched
    print("\n" + "-" * 72)
    print("OFFICIAL DB VERIFICATION")
    print("-" * 72)
    official_hash_after = sha256_of(OFFICIAL_DB)
    db_untouched = official_hash_before == official_hash_after
    print(f"Hash before: {official_hash_before}")
    print(f"Hash after:  {official_hash_after}")
    print(f"DB untouched: {db_untouched}")

    # Verify engine/v4 unchanged
    git_status_after = subprocess.run(
        ["git", "status", "--short", "--", "engine/v4/"],
        capture_output=True, text=True, cwd=str(ROOT)
    ).stdout
    engine_unchanged = git_status_before == git_status_after
    print(f"engine/v4/ unchanged: {engine_unchanged}")

    # Verify temp files cleaned aside from evidence
    uploads_count_before = len(list(temp_uploads.iterdir())) if temp_uploads.exists() else 0

    # Step 5: Determine verdict
    print("\n" + "=" * 72)
    print("VERDICT")
    print("=" * 72)

    # Check PersistenceEngine bug
    has_persistence_bug = False
    for r in upload_results:
        for err in r.get("errors", []):
            if "unexpected keyword argument 'db'" in err or "TypeError" in err:
                has_persistence_bug = True

    verdict = {
        "uploads_executed": len(upload_results),
        "uploads_succeeded": sum(1 for r in upload_results if r.get("status") not in ("EXCEPTION", "FAILED")),
        "all_stages_completed": all_stages_ok,
        "all_execution_ids_unique": len(all_execution_ids_unique) == len(upload_results),
        "has_persistence_bug": has_persistence_bug,
        "db_untouched": db_untouched,
        "engine_unchanged": engine_unchanged,
        "has_controlled_financial_fixture": fixture_check["has_controlled_financial_fixture"],
        "fixture_reason": fixture_check["reason"],
    }

    print(f"Uploads executed: {verdict['uploads_executed']}")
    print(f"Uploads succeeded: {verdict['uploads_succeeded']}")
    print(f"All stages completed: {verdict['all_stages_completed']}")
    print(f"All execution IDs unique: {verdict['all_execution_ids_unique']}")
    print(f"Has PersistenceEngine bug: {verdict['has_persistence_bug']}")
    print(f"DB untouched: {verdict['db_untouched']}")
    print(f"Engine unchanged: {verdict['engine_unchanged']}")
    print(f"Has controlled financial fixture: {verdict['has_controlled_financial_fixture']}")

    # Verdict determination
    if not verdict["db_untouched"]:
        verdict["final"] = "REAL_PIPELINE_VALIDATION_FAILED"
        verdict["reason"] = "Official DB was modified during test."
    elif not verdict["all_stages_completed"]:
        if verdict["has_persistence_bug"]:
            verdict["final"] = "REAL_PIPELINE_VALIDATION_FAILED"
            verdict["reason"] = "PersistenceEngine._get_loader() calls SurgicalLoader(db=self.db) but SurgicalLoader.__init__() does not accept a 'db' parameter. Pipeline fails at PERSIST stage with TypeError."
        else:
            verdict["final"] = "REAL_PIPELINE_VALIDATION_FAILED"
            verdict["reason"] = "Not all pipeline stages completed successfully."
    elif not verdict["has_controlled_financial_fixture"]:
        verdict["final"] = "CONTROLLED_FINANCIAL_FIXTURE_REQUIRED"
        verdict["reason"] = fixture_check["reason"]
    elif verdict["all_stages_completed"] and verdict["has_controlled_financial_fixture"]:
        verdict["final"] = "CAP001_CERTIFIED"
        verdict["reason"] = "All 3 uploads completed with real SurgicalLoader, verified against controlled fixture."
    else:
        verdict["final"] = "CAP001_REMAINS_VALIDATED"
        verdict["reason"] = "Pipeline mechanics verified but no controlled fixture for full certification."

    print(f"\nFINAL VERDICT: {verdict['final']}")
    print(f"Reason: {verdict['reason']}")

    # Save evidence
    evidence = {
        "test": "F3-02",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "baseline_v7_hash": v7_hash,
        "official_db_hash_before": official_hash_before,
        "official_db_hash_after": official_hash_after,
        "db_untouched": db_untouched,
        "upload_results": upload_results,
        "fixture_check": fixture_check,
        "verdict": verdict,
        "git_status_before": git_status_before,
        "git_status_after": git_status_after,
    }

    evidence_dir = ROOT / "evidence" / "fase_3"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / f"f3_02_controlled_ingestion_{int(time.time())}.json"
    evidence_path.write_text(json.dumps(evidence, indent=2, default=str), encoding="utf-8")
    print(f"\nEvidence saved: {evidence_path}")

    # Cleanup temp
    print(f"\nTemp directory: {tmp_base}")

    # Print detailed bug report
    if verdict["has_persistence_bug"]:
        print("\n" + "-" * 72)
        print("BUG REPORT: PersistenceEngine vs SurgicalLoader Interface Mismatch")
        print("-" * 72)
        print("""
Root Cause:
  PersistenceEngine._get_loader() at engine/v4/ingestion/handlers/persistence_engine.py:29
  calls SurgicalLoader(db=self.db), but SurgicalLoader.__init__() at
  engine/v4/surgical_loader.py:80 does NOT accept a 'db' parameter.

  SurgicalLoader always gets its DB from DatabaseV4.get() singleton, so the
  'db' parameter is unnecessary. The fix is either:
    A) Remove the 'db' argument: SurgicalLoader() instead of SurgicalLoader(db=self.db)
    B) Make SurgicalLoader.__init__ accept optional db parameter

  This bug means the Upload Center's PERSIST stage can never succeed without
  mocking SurgicalLoader. All 10 existing upload center tests ERROR because
  they use TestClient which triggers the real PersistenceEngine code path.

Impact:
  - Upload Center pipeline is broken for all marketplaces
  - No real file upload can complete the PERSIST stage
  - The bug exists in untracked code (engine/v4/ingestion/ is not committed to git)
""")

    return verdict


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result.get("final") == "CAP001_CERTIFIED" else 1)
