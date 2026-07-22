"""Handlers for the ingestion pipeline stages.

Each handler implements StageHandler protocol used by IngestionOrchestrator.
Zero financial logic. Zero direct SQL.
"""
from engine.v4.ingestion.handlers.file_detector import FileDetector
from engine.v4.ingestion.handlers.integrity_validator import IntegrityValidator
from engine.v4.ingestion.handlers.marketplace_classifier import MarketplaceClassifier
from engine.v4.ingestion.handlers.persistence_engine import PersistenceEngine
from engine.v4.ingestion.handlers.certification_trigger import CertificationTrigger
from engine.v4.ingestion.handlers.knowledge_trigger import KnowledgeTrigger

__all__ = [
    "FileDetector", "IntegrityValidator", "MarketplaceClassifier",
    "PersistenceEngine", "CertificationTrigger", "KnowledgeTrigger",
]
