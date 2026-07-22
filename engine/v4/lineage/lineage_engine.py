"""
lineage_engine.py — Full data lineage for any transaction, order, or document.

Answers: Where does this figure come from? What file originated it?
What transformation / taxonomy rule / reconciliation certified it?
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from engine.v4.database import DatabaseV4


@dataclass
class LineageStep:
    step: str
    source: str
    detail: str
    monto: float
    fecha: str
    rule: str
    evidence_sql: str


@dataclass
class LineageRecord:
    id_transaccion: str
    marketplace: str
    detalle: str
    monto: float
    fecha: str
    archivo_origen: str
    financial_group: str
    clasificacion_operativa: str
    folio_xml: str | None
    include_in_operational_pnl: bool
    steps: list[LineageStep] = field(default_factory=list)


class LineageEngine:
    """Trace any transaction/order/document through the full pipeline."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()

    def trace_transaction(self, id_transaccion: str) -> LineageRecord | None:
        """Trace a single transaction by its id."""
        sql = """
            SELECT l.marketplace, l.id_transaccion, l.detalle, l.monto, l.fecha,
                   l.archivo_origen, l.financial_group, l.clasificacion_operativa,
                   l.folio_xml, COALESCE(l.include_in_operational_pnl, 1) as pnl_flag
            FROM marketplace_ledger_v1 l
            WHERE l.id_transaccion = ?
        """
        df = self.db.query(sql, [id_transaccion])
        if df.empty:
            return None

        row = df.iloc[0]
        record = LineageRecord(
            id_transaccion=str(row["id_transaccion"]),
            marketplace=str(row["marketplace"]),
            detalle=str(row["detalle"]),
            monto=float(row["monto"]),
            fecha=str(row["fecha"]),
            archivo_origen=str(row["archivo_origen"]),
            financial_group=str(row["financial_group"] or "sin_clasificar"),
            clasificacion_operativa=str(row["clasificacion_operativa"] or ""),
            folio_xml=str(row["folio_xml"]) if row["folio_xml"] else None,
            include_in_operational_pnl=bool(row["pnl_flag"]),
        )

        # Step 1: Raw source
        record.steps.append(LineageStep(
            step="RAW_SOURCE", source=record.archivo_origen,
            detail=f"Original file: {record.archivo_origen}",
            monto=record.monto, fecha=record.fecha,
            rule="file_ingestion", evidence_sql=sql,
        ))

        # Step 2: Classification
        record.steps.append(LineageStep(
            step="CLASSIFICATION", source=f"taxonomy/{record.financial_group}",
            detail=f"Classified as '{record.financial_group}' / '{record.clasificacion_operativa}'",
            monto=record.monto, fecha=record.fecha,
            rule=f"financial_group={record.financial_group}",
            evidence_sql=f"SELECT financial_group, clasificacion_operativa FROM marketplace_ledger_v1 WHERE id_transaccion='{record.id_transaccion}'",
        ))

        return record

    def trace_order(self, id_orden: str) -> list[LineageRecord]:
        """Trace all transactions belonging to an order."""
        sql = """
            SELECT DISTINCT l.id_transaccion
            FROM marketplace_ledger_v1 l
            WHERE l.id_orden = ?
        """
        df = self.db.query(sql, [id_orden])
        records = []
        for _, row in df.iterrows():
            rec = self.trace_transaction(str(row["id_transaccion"]))
            if rec:
                records.append(rec)
        return records

    def trace_document(self, folio_xml: str) -> list[LineageRecord]:
        """Trace all transactions linked to an XML document (DTE folio)."""
        sql = """
            SELECT l.id_transaccion
            FROM marketplace_ledger_v1 l
            WHERE l.folio_xml = ?
        """
        df = self.db.query(sql, [folio_xml])
        records = []
        for _, row in df.iterrows():
            rec = self.trace_transaction(str(row["id_transaccion"]))
            if rec:
                records.append(rec)
        return records

    def _trace_reconciliation(self, marketplace: str, periodo: str) -> LineageStep | None:
        """Check if this marketplace/period was reconciled."""
        from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine
        try:
            recon = ReconciliationEngine(self.db)
            result = recon.validate_marketplace_consistency(marketplace, periodo)
            return LineageStep(
                step="RECONCILIATION",
                source=f"ReconciliationEngine.{marketplace}.{periodo}",
                detail=f"Delta: ${result.delta:,.2f}, Status: {result.certification_status}",
                monto=result.delta, fecha=periodo,
                rule=f"certification_status={result.certification_status}",
                evidence_sql=f"ReconciliationEngine.validate_marketplace_consistency('{marketplace}', '{periodo}')",
            )
        except Exception:
            return None
