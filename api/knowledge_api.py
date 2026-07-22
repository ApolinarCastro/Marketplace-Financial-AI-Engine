"""Knowledge API ? standalone FastAPI app and reusable router.

Run independently:  uvicorn api.knowledge_api:knowledge_app --port 3002
Reuse in api.py:    app.include_router(knowledge_router)
"""
from __future__ import annotations
from pathlib import Path
from typing import Any
from fastapi import APIRouter, Body, FastAPI, Query
from fastapi.responses import JSONResponse

from engine.v4.certification.knowledge.obsidian_adapter import ObsidianAdapter
from engine.v4.database import DatabaseV4
from engine.v4.knowledge.kce import KnowledgeConsolidationEngine, KCEConfig

knowledge_app = FastAPI(title="Knowledge API", version="1.0", description="Knowledge Consolidation Engine API")
knowledge_router = APIRouter(prefix="/api/v4/knowledge", tags=["knowledge"])

ROOT = Path(__file__).resolve().parent.parent


def _get_kce() -> KnowledgeConsolidationEngine:
    db = DatabaseV4.get()
    cfg = KCEConfig(
        governance_dir=str(ROOT / "governance"),
        knowledge_index_path=str(ROOT / "knowledge_index.yaml"),
        taxonomy_dir=str(ROOT / "KnowledgeBase" / "Marketplace" / "Taxonomy"),
    )
    return KnowledgeConsolidationEngine(db=db, config=cfg)


@knowledge_router.post("/consolidate")
def run_consolidation(dry_run: bool = Query(True)):
    kce = _get_kce()
    kce.cfg.dry_run = dry_run
    result = kce.consolidate()
    return {
        "status": "dry_run" if dry_run else "consolidated",
        "audit_entries": len(result.audit_entries),
        "decision_entries": len(result.decision_entries),
        "taxonomy_entries": len(result.taxonomy_entries),
        "index_added": result.index_added,
        "index_updated": result.index_updated,
        "files_scanned": result.files_scanned,
        "coverage_gaps": len(result.coverage_gaps),
    }


@knowledge_router.get("/status")
def knowledge_status():
    kce = _get_kce()
    return kce.status_report()


@knowledge_router.get("/coverage-gaps")
def coverage_gaps():
    kce = _get_kce()
    result = kce.consolidate()
    return {"total_gaps": len(result.coverage_gaps), "gaps": result.coverage_gaps[:50]}


@knowledge_router.get("/audit-coverage")
def audit_coverage():
    db = DatabaseV4.get()
    scanner = __import__("engine.v4.knowledge.audit_scanner", fromlist=["AuditScanner"]).AuditScanner(db)
    return scanner.coverage_summary()


@knowledge_router.get("/retention-recs")
def retention_recommendations():
    kce = _get_kce()
    kce.cfg.auto_archive = True
    result = kce.consolidate()
    return {"recommendations": result.retention_recommendations}


@knowledge_router.get("")
def list_knowledge(
    type: str | None = Query(None, alias="type"),
    status: str | None = Query(None),
    search: str | None = Query(None),
):
    kce = _get_kce()
    if search or type or status:
        results = kce.indexer.search(keyword=search or "", type_filter=type, status_filter=status)
        return {"total": len(results), "knowledge": results}
    entries = kce.indexer.read()
    return {"total": len(entries), "knowledge": entries}


@knowledge_router.post("/export")
def export_knowledge(
    payload: dict[str, Any] = Body(...),
    vault_path: str | None = Query(None, description="Optional target vault path"),
):
    adapter = ObsidianAdapter(vault_path=vault_path or str(ROOT / "vault"))
    adapter.export_evidence(payload)
    return {
        "status": "success",
        "message": "Evidence exported to Obsidian",
        "evidence_hash": payload.get("evidence_object", {}).get("evidence_hash"),
    }


@knowledge_router.get("/{knowledge_id}")
def get_knowledge(knowledge_id: str):
    kce = _get_kce()
    entry = kce.indexer.get(knowledge_id)
    if not entry:
        return JSONResponse({"error": f"Knowledge entry '{knowledge_id}' not found"}, status_code=404)
    return entry


knowledge_app.include_router(knowledge_router)
