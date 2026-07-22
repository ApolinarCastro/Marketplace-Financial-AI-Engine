"""MarketplaceClassifier — Stage 2 of ingestion pipeline.

Determines which marketplace, loader, and pipeline to use for a given file.
Uses filename patterns, detected marketplace/doc-type, and file path structure.

Zero financial logic. Zero DB writes.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Any

from engine.v4.ingestion.handlers.file_detector import FileDetector


class MarketplaceClassifier:
    LOADER_MAP: dict[str, str] = {
        "ML": "SurgicalLoader",
        "PARIS": "SurgicalLoader",
        "RIPLEY": "SurgicalLoader",
        "FALABELLA": "SurgicalLoader",
        "SHOPIFY": "SurgicalLoader",
    }

    PIPELINE_MAP: dict[str, str] = {
        "ML": "ml_v4",
        "PARIS": "paris_v4",
        "RIPLEY": "ripley_v4",
        "FALABELLA": "falabella_v4",
        "SHOPIFY": "shopify_v4",
    }

    def __init__(self):
        self._detector = FileDetector()

    def classify(self, file_path: str | Path, original_filename: str | None = None) -> dict[str, Any]:
        path = Path(file_path) if isinstance(file_path, str) else file_path
        fname = original_filename or path.name
        detection = self._detector.detect(str(path), fname)
        result: dict[str, Any] = {
            "marketplace": detection["marketplace"],
            "document_type": detection["document_type"],
            "period": detection["period"],
            "loader": None,
            "pipeline": None,
            "confidence": "LOW",
        }

        if detection["marketplace"]:
            mp = detection["marketplace"]
            result["loader"] = self.LOADER_MAP.get(mp)
            result["pipeline"] = self.PIPELINE_MAP.get(mp)
            result["confidence"] = "HIGH" if mp in self.LOADER_MAP else "MEDIUM"
        else:
            path_str = str(path).lower()
            for mp_key in ["ml", "mercadolibre", "paris", "ripley", "falabella", "shopify"]:
                if mp_key in path_str:
                    mapped = mp_key.upper() if mp_key != "mercadolibre" else "ML"
                    if mapped == "ML":
                        mapped = "ML"
                    elif mp_key == "mercadolibre":
                        mapped = "ML"
                    else:
                        mapped = mp_key.upper()
                    result["marketplace"] = mapped
                    result["loader"] = self.LOADER_MAP.get(mapped)
                    result["pipeline"] = self.PIPELINE_MAP.get(mapped)
                    result["confidence"] = "MEDIUM"
                    break

        return result
