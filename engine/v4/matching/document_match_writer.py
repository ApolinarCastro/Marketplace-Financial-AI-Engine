"""DocumentMatchWriter — deterministic persistence for validated document matches.

Stores an already-decided match record into `document_match_v1`.
This module NEVER decides whether two documents match: the caller provides
a validated match (match_status already determined by a matcher, auditor,
or certified test fixture).

Single responsibility: validated match record -> document_match_v1.

Idempotency: the natural key (marketplace, ledger_id) identifies one match
per ledger transaction. Writing an identical match twice returns
SKIPPED_EXISTING with ROW_COUNT unchanged (never a silent duplicate).
Writing a conflicting match for the same key raises DocumentMatchConflictError.
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Any

from engine.v4.database import DatabaseV4

logger = logging.getLogger("meli.document_match_writer")

# Exact spellings consumed by ReconciliationEngine Level 4
# (reconciliation_engine.py: match_status = 'CONCILIATED' filter).
VALID_MATCH_STATUSES = (
    "CONCILIATED",
    "MATCHED",
    "MATCHED_CERTIFIED",
    "MATCHED_WITH_TOLERANCE",
    "AMOUNT_MISMATCH",
    "PENDING",
    "REJECTED",
)

# Fields the reconciliation contract requires to be non-null.
REQUIRED_FIELDS = ("marketplace", "ledger_id", "match_status", "document_date")


class DocumentMatchError(ValueError):
    """Raised when a match record fails validation."""


class DocumentMatchConflictError(DocumentMatchError):
    """Raised when a different match already exists for (marketplace, ledger_id)."""


def _norm_compare(value: Any) -> str:
    """Normalize a value for idempotency comparison.

    Dates/Timestamps compare by calendar date (engine stores DATE;
    drivers may return datetime/Timestamp objects).
    """
    if value is None:
        return ""
    if hasattr(value, "strftime"):
        try:
            return str(value.strftime("%Y-%m-%d"))
        except Exception:
            pass
    return str(value)


def deterministic_match_id(marketplace: str, ledger_id: str) -> str:
    """Stable identifier for one ledger transaction match.

    SHA-256 over the natural key, truncated for readability.
    Identical inputs always produce the identical id (reproducible).
    """
    digest = hashlib.sha256(f"{marketplace}|{ledger_id}".encode("utf-8")).hexdigest()
    return f"dm-{digest[:16]}"


class DocumentMatchWriter:
    """Persists validated document matches into document_match_v1."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()

    def validate(self, record: dict[str, Any]) -> dict[str, Any]:
        """Validate a match record. Returns normalized copy. Raises on invalid."""
        if not isinstance(record, dict):
            raise DocumentMatchError("match record must be a dict")

        missing = [f for f in REQUIRED_FIELDS if not record.get(f)]
        if missing:
            raise DocumentMatchError(
                f"missing required fields: {', '.join(missing)}"
            )

        status = str(record.get("match_status"))
        if status not in VALID_MATCH_STATUSES:
            raise DocumentMatchError(
                f"invalid match_status {status!r}; "
                f"must be one of {', '.join(VALID_MATCH_STATUSES)}"
            )

        normalized = dict(record)
        normalized["marketplace"] = str(record["marketplace"]).strip().upper()
        normalized["ledger_id"] = str(record["ledger_id"]).strip()
        normalized["match_status"] = status
        if not normalized["marketplace"]:
            raise DocumentMatchError("marketplace must be non-empty")
        if not normalized["ledger_id"]:
            raise DocumentMatchError("ledger_id must be non-empty")
        normalized.setdefault("match_id", deterministic_match_id(
            normalized["marketplace"], normalized["ledger_id"]))
        return normalized

    def find_existing(
        self, marketplace: str, ledger_id: str
    ) -> dict[str, Any] | None:
        """Return the existing match for (marketplace, ledger_id), if any."""
        df = self.db.query(
            "SELECT * FROM document_match_v1 WHERE marketplace = ? AND ledger_id = ?",
            [marketplace, ledger_id],
        )
        if df.empty:
            return None
        return df.iloc[0].to_dict()

    def write(self, record: dict[str, Any]) -> dict[str, Any]:
        """Persist a validated match. Idempotent on identical re-write.

        Returns {"outcome": "INSERTED"|"SKIPPED_EXISTING", "match_id": ...}.
        Raises DocumentMatchConflictError on conflicting re-write,
        DocumentMatchError on invalid record.
        """
        rec = self.validate(record)
        existing = self.find_existing(rec["marketplace"], rec["ledger_id"])
        if existing is not None:
            comparable = ("match_status", "folio_xml", "order_id",
                          "document_date", "document_amount")
            same = all(
                _norm_compare(existing.get(k)) == _norm_compare(rec.get(k))
                for k in comparable
            )
            if same:
                logger.info(
                    "document match already exists (idempotent): %s/%s",
                    rec["marketplace"], rec["ledger_id"],
                )
                return {"outcome": "SKIPPED_EXISTING",
                        "match_id": str(existing.get("match_id"))}
            raise DocumentMatchConflictError(
                f"conflicting match exists for "
                f"{rec['marketplace']}/{rec['ledger_id']}: "
                f"existing status={existing.get('match_status')!r} "
                f"vs new status={rec['match_status']!r}"
            )

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        self.db.execute(
            "INSERT INTO document_match_v1 (match_id, marketplace, ledger_id, "
            "order_id, folio_xml, tipo_dte, match_rule, match_source, "
            "match_timestamp, match_status, document_date, document_amount, "
            "reference_document, created_by, execution_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                rec.get("match_id"),
                rec.get("marketplace"),
                rec.get("ledger_id"),
                rec.get("order_id"),
                rec.get("folio_xml"),
                rec.get("tipo_dte"),
                rec.get("match_rule"),
                rec.get("match_source"),
                rec.get("match_timestamp") or now,
                rec.get("match_status"),
                rec.get("document_date"),
                rec.get("document_amount"),
                rec.get("reference_document"),
                rec.get("created_by"),
                rec.get("execution_id"),
            ],
        )
        logger.info(
            "document match persisted: %s/%s status=%s",
            rec["marketplace"], rec["ledger_id"], rec["match_status"],
        )
        return {"outcome": "INSERTED", "match_id": str(rec.get("match_id"))}

    def count(self) -> int:
        """Total rows in document_match_v1."""
        return int(self.db.query("SELECT COUNT(*) AS n FROM document_match_v1")["n"].iloc[0])
