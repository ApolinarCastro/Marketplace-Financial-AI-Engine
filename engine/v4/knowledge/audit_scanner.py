"""KCE Module 1: AuditScanner — reads marketplace_auditoria_v1 and generates knowledge entries."""
from __future__ import annotations
import pandas as pd
from dataclasses import dataclass, field


@dataclass
class AuditKnowledgeEntry:
    knowledge_id: str
    knowledge_type: str = "audit"
    title: str = ""
    summary: str = ""
    status: str = "OPEN"
    marketplace: str = ""
    check_name: str = ""
    row_count: int = 0
    sample_conditions: list[str] = field(default_factory=list)


class AuditScanner:
    def __init__(self, db):
        self.db = db

    def scan(self) -> list[AuditKnowledgeEntry]:
        entries: list[AuditKnowledgeEntry] = []
        rows = self.db.query(
            "SELECT marketplace, check_name, condition_detected, COUNT(*) as cnt "
            "FROM marketplace_auditoria_v1 "
            "GROUP BY marketplace, check_name, condition_detected "
            "ORDER BY marketplace, check_name, cnt DESC"
        )
        if rows.empty:
            return entries

        for (mp, check), grp in rows.groupby(["marketplace", "check_name"], sort=False):
            total = int(grp["cnt"].sum())
            top_conditions = grp.head(3)["condition_detected"].tolist()
            eid = f"AUDIT-{mp}-{check.upper()[:20]}"
            entries.append(AuditKnowledgeEntry(
                knowledge_id=eid,
                marketplace=mp,
                check_name=check,
                title=f"{mp}: {check} ({total} rows)",
                summary=f"{total} auditoria rows for {mp}/{check}. Top conditions: {'; '.join(top_conditions)}",
                status="OPEN" if total > 0 else "RESOLVED",
                row_count=total,
                sample_conditions=top_conditions,
            ))
        return entries

    def coverage_summary(self) -> dict:
        row = self.db.query(
            "SELECT marketplace, COUNT(*) as cnt, COUNT(DISTINCT check_name) as checks "
            "FROM marketplace_auditoria_v1 GROUP BY marketplace ORDER BY marketplace"
        )
        if row.empty:
            return {}
        return {r["marketplace"]: {"rows": int(r["cnt"]), "checks": int(r["checks"])} for _, r in row.iterrows()}
