"""IngestionOrchestrator — coordinates the full ingestion pipeline.

Stages: DETECT → VALIDATE → CLASSIFY → PERSIST → CERTIFY → KNOWLEDGE

Each stage implements StageHandler protocol (async handle()).
Failure in any stage stops the pipeline (fail-fast).
"""
from __future__ import annotations
import logging
logger = logging.getLogger(__name__)
from pathlib import Path
from typing import Any, Protocol

from engine.v4.database import DatabaseV4
from engine.v4.ingestion import IngestionRegistry, IngestionRecord
from engine.v4.ingestion.handlers.file_detector import FileDetector
from engine.v4.ingestion.handlers.integrity_validator import IntegrityValidator
from engine.v4.ingestion.handlers.marketplace_classifier import MarketplaceClassifier
from engine.v4.ingestion.handlers.persistence_engine import PersistenceEngine
from engine.v4.ingestion.handlers.certification_trigger import CertificationTrigger
from engine.v4.ingestion.handlers.knowledge_trigger import KnowledgeTrigger
from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
from engine.v4.knowledge.pattern_registry import PatternRegistry


class StageHandler(Protocol):
    async def handle(self, context: dict[str, Any]) -> dict[str, Any]:
        ...


class IngestionOrchestrator:
    def __init__(
        self,
        db: DatabaseV4 | None = None,
        registry: IngestionRegistry | None = None,
        detector: FileDetector | None = None,
        validator: IntegrityValidator | None = None,
        classifier: MarketplaceClassifier | None = None,
        persistence: PersistenceEngine | None = None,
        certification: CertificationTrigger | None = None,
        knowledge: KnowledgeTrigger | None = None,
        obsidian_path: str | None = None,
        post_persist_stages: bool = True,
    ):
        self.db = db or DatabaseV4.get(read_only=False)
        self.registry = registry or IngestionRegistry(db=self.db)
        self.detector = detector or FileDetector()
        self.validator = validator or IntegrityValidator(db=self.db)
        self.classifier = classifier or MarketplaceClassifier()
        self.persistence = persistence or PersistenceEngine(db=self.db)
        self.certification = certification or CertificationTrigger(db=self.db)
        self.obsidian_path = obsidian_path
        if knowledge is not None:
            self.knowledge = knowledge
        else:
            _ki = KnowledgeIndexer()
            _pr = PatternRegistry()
            self.knowledge = KnowledgeTrigger(
                db=self.db,
                knowledge_indexer=_ki,
                pattern_registry=_pr,
                obsidian_path=obsidian_path,
            )

        self._stages = [
            ("DETECT", self._stage_detect),
            ("VALIDATE", self._stage_validate),
            ("CLASSIFY", self._stage_classify),
            ("PERSIST", self._stage_persist),
        ]
        if post_persist_stages:
            self._stages.extend([
                ("CERTIFY", self._stage_certify),
                ("KNOWLEDGE", self._stage_knowledge),
            ])

    async def run(
        self,
        file_path: str | Path,
        original_filename: str | None = None,
        user: str = "system",
    ) -> IngestionRecord:
        path = Path(file_path) if isinstance(file_path, str) else file_path
        fname = original_filename or path.name

        record = self.registry.create_record(fname, str(path), user=user)
        duplicate = self.registry.get_completed_by_sha256(record.sha256, record.execution_id)
        if duplicate is not None:
            self.registry.update_classification(
                record,
                marketplace=duplicate.marketplace or "UNKNOWN",
                document_type=duplicate.document_type or "unknown",
                period=duplicate.period or "",
                loader=duplicate.loader_executed or "",
                pipeline=duplicate.pipeline_version or duplicate.pipeline or "",
            )
            self.registry.set_record_counts(
                record,
                read=duplicate.records_read,
                new=0,
                existing=duplicate.records_new + duplicate.records_existing,
            )
            self.registry.finalize(record, status="SKIPPED_DUPLICATE")
            return record
        context: dict[str, Any] = {
            "file_path": str(path.resolve()),
            "original_filename": fname,
            "record": record,
        }

        for stage_name, stage_fn in self._stages:
            if record.status == "FAILED":
                self.registry.add_warning(record, f"Pipeline stopped at stage {stage_name} (previous failure)")
                break
            try:
                stage_result = await stage_fn(context)
                context[stage_name] = stage_result
                if stage_result.get("status") == "FAILED":
                    self.registry.add_error(record, f"{stage_name}: {stage_result.get('error', 'Unknown error')}")
                    break
                for warning in stage_result.get("warnings", []):
                    self.registry.add_warning(record, warning)
            except Exception as e:
                logger.error(f"Exception in stage {stage_name} for file {record.file_name} (exec: {record.execution_id})", exc_info=True)
                self.registry.add_error(record, f"{stage_name} exception: {e}")
                break

        certification_triggered = False
        certification_result = None
        knowledge_updated = False

        cert_stage = context.get("CERTIFY", {})
        cert_inner = cert_stage.get("cert_result", {})
        if cert_stage.get("status") != "FAILED" and cert_inner.get("overall_status"):
            certification_triggered = True
            certification_result = cert_inner.get("overall_status")

        kn_stage = context.get("KNOWLEDGE", {})
        kn_inner = kn_stage.get("knowledge_result", {})
        if kn_stage.get("status") != "FAILED" and kn_inner.get("overall_status") == "PASS":
            knowledge_updated = True

        final_status = "FAILED" if record.status == "FAILED" else "COMPLETED"
        self.registry.finalize(
            record,
            status=final_status,
            certification_triggered=certification_triggered,
            certification_result=certification_result,
            knowledge_updated=knowledge_updated,
        )

        record.details["stages_completed"] = [s[0] for s in self._stages[:self._last_completed_stage(context)]]
        return record

    async def _stage_detect(self, context: dict[str, Any]) -> dict[str, Any]:
        detection = self.detector.detect(context["file_path"], context["original_filename"])
        record: IngestionRecord = context["record"]
        record.details["detection"] = detection
        return {"status": "PASS", "detection": detection}

    async def _stage_validate(self, context: dict[str, Any]) -> dict[str, Any]:
        detection = context.get("DETECT", {}).get("detection", {})
        issues = self.validator.validate(
            context["file_path"],
            detection.get("sha256", ""),
            detection.get("extension", ""),
        )
        if issues:
            return {"status": "FAILED", "error": f"Validation failed: {issues[0]['detail']}", "issues": issues}
        return {"status": "PASS", "issues": []}

    async def _stage_classify(self, context: dict[str, Any]) -> dict[str, Any]:
        classification = self.classifier.classify(context["file_path"], context["original_filename"])
        record: IngestionRecord = context["record"]
        self.registry.update_classification(
            record,
            marketplace=classification.get("marketplace") or "UNKNOWN",
            document_type=classification.get("document_type") or "unknown",
            period=classification.get("period") or "",
            loader=classification.get("loader") or "",
            pipeline=classification.get("pipeline") or "",
        )
        record.details["classification"] = classification
        return {"status": "PASS", "classification": classification}

    async def _stage_persist(self, context: dict[str, Any]) -> dict[str, Any]:
        classification = context.get("CLASSIFY", {}).get("classification", {})
        detection = context.get("DETECT", {}).get("detection", {})
        marketplace = classification.get("marketplace", "UNKNOWN")
        sha256 = detection.get("sha256", "")
        record: IngestionRecord = context["record"]
        result = self.persistence.persist(
            context["file_path"], marketplace, sha256,
            execution_id=record.execution_id,
            document_type=classification.get("document_type"),
            period=classification.get("period"),
        )
        self.registry.update_records(
            record,
            inserted=result.get("records_inserted", 0),
            rejected=len(result.get("errors", [])),
        )
        self.registry.set_record_counts(
            record,
            read=result.get("records_read", result.get("records_inserted", 0)),
            new=result.get("records_inserted", 0),
            existing=result.get("records_existing", 0),
        )
        if result.get("errors"):
            return {"status": "FAILED", "error": "; ".join(result["errors"]), "persist_result": result}
        if result.get("records_inserted", 0) == 0:
            return {"status": "FAILED", "error": "NO_DATA: 0 records inserted", "persist_result": result}
        return {"status": "PASS", "persist_result": result}

    async def _stage_certify(self, context: dict[str, Any]) -> dict[str, Any]:
        classification = context.get("CLASSIFY", {}).get("classification", {})
        marketplace = classification.get("marketplace", "UNKNOWN")
        period = classification.get("period")
        result = self.certification.trigger(marketplace, period)
        return {"status": "PASS", "cert_result": result}

    async def _stage_knowledge(self, context: dict[str, Any]) -> dict[str, Any]:
        classification = context.get("CLASSIFY", {}).get("classification", {})
        marketplace = classification.get("marketplace", "UNKNOWN")
        period = classification.get("period")
        result = self.knowledge.trigger(marketplace, period)
        return {"status": "PASS", "knowledge_result": result}

    def _last_completed_stage(self, context: dict[str, Any]) -> int:
        for i, (name, _) in enumerate(self._stages):
            if context.get(name, {}).get("status") not in ("PASS",):
                return i
        return len(self._stages)
