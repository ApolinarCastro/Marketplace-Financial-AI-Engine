"""
audit_contract.py — Certified Pydantic models for Audit layer.

Maps to marketplace_auditoria_v1 rows. Every alert includes evidence.
"""
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field


class AuditAlert(BaseModel):
    marketplace: str
    check_name: str
    condition_detected: str
    action_taken: str
    order_id: str | None = None
    detected_at: datetime | None = None


class AuditSummary(BaseModel):
    marketplace: str
    period_label: str
    total_alerts: int
    alerts_by_type: dict[str, int]
    alerts: list[AuditAlert] = Field(default_factory=list)


class AuditQuery(BaseModel):
    marketplace: str
    periodo: str | None = None
    check_name: str | None = None
    limit: int = 100
    offset: int = 0
