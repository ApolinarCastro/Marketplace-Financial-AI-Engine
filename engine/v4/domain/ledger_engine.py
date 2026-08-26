"""
Meli Financial AI Engine v4.0
Phase 5 Step 1 — Unified Transaction Ledger Engine
Canonical domain component responsible for unified transaction ledger operations, schema enforcement, traceability, and evidence linkage across all certified marketplaces.
"""
import math
import pandas as pd
from typing import Optional, Dict, Any, List
from engine.v4.database import DatabaseV4
from engine.v4.domain.financial_engine import FinancialEngine

def _clean_val(val: Any) -> Any:
    if val is None or pd.isna(val):
        return None
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return None
    return val

class LedgerEngine:
    """
    Motor oficial responsable de las interacciones con el Ledger Unificado (v_ledger_certified).
    Proporciona información certificada, filtrado, trazabilidad por orden/transacción
    y estructuración de evidencias sobre los 598,112 registros.
    """

    def __init__(self, db: Optional[DatabaseV4] = None):
        self.db = db or DatabaseV4.get()
        self._financial_engine = FinancialEngine(db=self.db)

    def get_ledger_records_count(self, marketplace: Optional[str] = None, periodo: Optional[str] = None) -> int:
        """
        Retorna la cantidad oficial de registros crudos en el ledger para el período y marketplace dados.
        Reutiliza los filtros oficiales del FinancialEngine para asegurar paridad.
        """
        where_clause, params = self._financial_engine._build_ledger_where(periodo, marketplace)
        sql = f"SELECT COUNT(*) as count FROM v_ledger_certified WHERE {where_clause}"
        result = self.db.query(sql, params)
        if result.empty:
            return 0
        return int(result.iloc[0]["count"])

    def get_total_records_count(self, marketplace: Optional[str] = None) -> int:
        """Alias para obtener la cantidad total de registros según marketplace (o global si es None)."""
        return self.get_ledger_records_count(marketplace=marketplace)

    def query_unified_ledger(
        self,
        marketplace: Optional[str] = None,
        period: Optional[str] = None,
        page: int = 1,
        limit: int = 50,
        financial_group: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Consulta paginada del Ledger Unificado retornando una estructura estandarizada con todos
        los atributos requeridos por la arquitectura Evidence-First.
        """
        where_conditions = []
        params = []

        if marketplace and marketplace.upper() != "ALL":
            where_conditions.append("UPPER(marketplace) = ?")
            params.append(marketplace.upper())

        if period and period.upper() != "ALL":
            where_clause_p, params_p = self._financial_engine._build_ledger_where(period, None)
            where_conditions.append(where_clause_p)
            params.extend(params_p)

        if financial_group:
            where_conditions.append("LOWER(financial_group) = ?")
            params.append(financial_group.lower())

        if search_term:
            where_conditions.append("(id_transaccion LIKE ? OR id_orden LIKE ? OR detalle LIKE ? OR folio_xml LIKE ?)")
            term = f"%{search_term}%"
            params.extend([term, term, term, term])

        where_sql = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""

        count_sql = f"SELECT COUNT(*) as count FROM v_ledger_certified {where_sql}"
        count_df = self.db.query(count_sql, params)
        total_records = int(count_df.iloc[0]["count"]) if not count_df.empty else 0

        offset = (page - 1) * limit
        query_sql = f"""
            SELECT 
                marketplace,
                id_transaccion,
                id_orden,
                fecha,
                detalle,
                monto,
                tipo_movimiento,
                archivo_origen,
                folio_xml,
                estado_xml,
                financial_group,
                clasificacion_operativa,
                has_dte_link,
                dte_folio,
                dte_tipo,
                dte_source,
                dte_cert_type,
                document_status,
                in_operational_pnl
            FROM v_ledger_certified
            {where_sql}
            ORDER BY fecha DESC, id_transaccion ASC
            LIMIT ? OFFSET ?
        """
        query_params = params + [limit, offset]
        df = self.db.query(query_sql, query_params)

        records = []
        if not df.empty:
            for _, row in df.iterrows():
                rec = self._format_ledger_record(row)
                records.append(rec)

        return {
            "total_records": total_records,
            "page": page,
            "limit": limit,
            "records": records
        }

    def get_transaction_by_id(self, id_transaccion: str) -> Optional[Dict[str, Any]]:
        """Obtiene el detalle completo y cadena de evidencia de una transacción específica por su ID."""
        sql = "SELECT * FROM v_ledger_certified WHERE id_transaccion = ?"
        df = self.db.query(sql, [id_transaccion])
        if df.empty:
            return None
        return self._format_ledger_record(df.iloc[0])

    def get_order_ledger_trace(self, id_orden: str) -> List[Dict[str, Any]]:
        """Obtiene la traza completa de todos los movimientos asociados a un ID de orden en el Ledger."""
        sql = "SELECT * FROM v_ledger_certified WHERE id_orden = ? ORDER BY fecha ASC"
        df = self.db.query(sql, [id_orden])
        records = []
        if not df.empty:
            for _, row in df.iterrows():
                records.append(self._format_ledger_record(row))
        return records

    def get_ledger_summary(self, marketplace: Optional[str] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """Calcula el resumen financiero agregado del ledger por grupos financieros con cero delta."""
        where_clause, params = self._financial_engine._build_ledger_where(period, marketplace)
        sql = f"""
            SELECT 
                financial_group,
                COUNT(*) as count,
                SUM(monto) as total_monto
            FROM v_ledger_certified
            WHERE {where_clause}
            GROUP BY financial_group
        """
        df = self.db.query(sql, params)
        groups = {}
        total_monto = 0.0
        total_records = 0

        if not df.empty:
            for _, row in df.iterrows():
                fg = str(row["financial_group"] or "sin_clasificar")
                cnt = int(row["count"])
                mnt = float(row["total_monto"] or 0.0)
                groups[fg] = {"count": cnt, "total_monto": round(mnt, 4)}
                total_monto += mnt
                total_records += cnt

        return {
            "marketplace": marketplace or "ALL",
            "period": period or "ALL",
            "total_records": total_records,
            "total_monto": round(total_monto, 4),
            "financial_groups": groups
        }

    def _format_ledger_record(self, row: pd.Series) -> Dict[str, Any]:
        """Formatea la fila del dataframe al esquema estándar de movimiento financiero con cadena de evidencia limpia."""
        row_dict = row.to_dict()
        
        doc_folio = _clean_val(row_dict.get("dte_folio")) or _clean_val(row_dict.get("folio_xml")) or "SIN_DOCUMENTO"
        doc_status = _clean_val(row_dict.get("document_status")) or _clean_val(row_dict.get("estado_xml")) or "PENDIENTE"
        
        fecha_str = str(row_dict.get("fecha"))[:10] if _clean_val(row_dict.get("fecha")) is not None else None

        evidencia = {
            "archivo_origen": _clean_val(row_dict.get("archivo_origen")),
            "folio_xml": _clean_val(row_dict.get("folio_xml")),
            "has_dte_link": bool(row_dict.get("has_dte_link", False)),
            "dte_folio": _clean_val(row_dict.get("dte_folio")),
            "dte_tipo": _clean_val(row_dict.get("dte_tipo")),
            "dte_source": _clean_val(row_dict.get("dte_source")),
            "dte_cert_type": _clean_val(row_dict.get("dte_cert_type")),
            "certified": bool(row_dict.get("has_dte_link", False))
        }

        monto_val = _clean_val(row_dict.get("monto"))
        monto_float = float(monto_val) if monto_val is not None else 0.0

        return {
            "marketplace": _clean_val(row_dict.get("marketplace")),
            "id_transaccion": _clean_val(row_dict.get("id_transaccion")),
            "id_orden": _clean_val(row_dict.get("id_orden")),
            "fecha": fecha_str,
            "detalle": _clean_val(row_dict.get("detalle")),
            "monto": monto_float,
            "tipo_movimiento": _clean_val(row_dict.get("tipo_movimiento")),
            "archivo_origen": _clean_val(row_dict.get("archivo_origen")),
            "financial_group": _clean_val(row_dict.get("financial_group")),
            "clasificacion_operativa": _clean_val(row_dict.get("clasificacion_operativa")),
            "documento": str(doc_folio) if doc_folio is not None else "SIN_DOCUMENTO",
            "estado_documento": str(doc_status) if doc_status is not None else "PENDIENTE",
            "in_operational_pnl": bool(row_dict.get("in_operational_pnl", True)),
            "evidencia": evidencia
        }
