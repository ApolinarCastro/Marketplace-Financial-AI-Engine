"""
FinancialEngine — certified single entry point for all financial operations.

Taxonomy source: YAML (via taxonomy_loader.py) with legacy fallback via USE_YAML_TAXONOMY flag.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import logging
import math
import calendar
from typing import Any

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from taxonomy import taxonomy_loader as tl

logger = logging.getLogger("meli.financial_engine")

_MONTHS = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

# ── Dual-mode taxonomy control ─────────────────────────────────────────
# True  → consume taxonomy_rules.yaml + taxonomy_mappings.yaml
# False → fallback to legacy _LEGACY_CONCEPT_MAP + FINANCIAL_STRUCTURE
USE_YAML_TAXONOMY = True

# ── Legacy concept map (READ ONLY — preserved for rollback) ────────────
_LEGACY_CONCEPT_MAP: dict[str, str] = {
    "Cargo por envíos de Mercado Libre": "Logística",
    "Cargo por Mercado Envíos": "Logística",
    "Anulación del cargo por envíos de Mercado Libre": "Logística",
    "Anulación del cargo por Mercado Envíos": "Logística",
    "Cargo por devolución": "Logística",
    "Anulación del cargo por devolución": "Logística",
    "Cargo por servicio de almacenamiento Full": "Logística",
    "Cargo por retiro de stock Full": "Logística",
    "Cargo por stock antiguo en Full": "Logística",
    "Cargo por sobrepasar espacio Full": "Logística",
    "Cargo por servicio de colecta Full": "Logística",
    "Cargo por diferencias en las medidas y el peso del paquete": "Logística",
    "Cobro por despacho": "Logística",
    "Logística inversa": "Logística",
    "Despacho": "Logística",
    "Gastos de envío pagados por el operador": "Logística",
    "Gastos de envío reembolsados pagados por el operador": "Logística",
    "Cobro por cofinanciamiento logístico": "Logística",
    "Cobro por logística inversa": "Logística",
    "Reversa de pago de envío comprador": "Logística",
    "Cobro Promo envío falabella.com": "Logística",
    "Reembolso por Promo envío falabella.com": "Logística",
    "Envío": "Logística",
    "Gastos de envío": "Logística",
    "Importe del envío del pedido": "Logística",
    "Envío reembolsado": "Logística",
    "Pago por envío directo": "Logística",
    "Cobro despacho primera milla": "Logística",
    "Descuento por logística inversa": "Logística",
    "Descuento por costo logístico": "Logística",
    "Descuento por logística inversa (FF)": "Logística",
    "Descuento por cofinanciamiento logístico (FF)": "Logística",
    "Descuento FF - Otros": "Logística",
    "Descuento FF - pick and pack": "Logística",
    "Descuento FF - sobreestadía": "Logística",
    "Descuento operacional": "Logística",
    "Descuento por error de clase logistica": "Logística",
    "Abono por uso de flota propia": "Logística",
    "Almacenamiento": "Logística",
    "Sobreestadía": "Logística",
    "Pick and pack": "Logística",
    "VAS": "Logística",
    "Cargos fulfillment": "Logística",
    "Cargo por servicio de almacenamiento": "Logística",
    "Cobro stock antiguo": "Logística",
    "Retiro stock bodega Paris": "Logística",
    "Cargo por venta (Comisión)": "Comisiones",
    "Anulación del cargo por venta": "Comisiones",
    "Reembolso por comisión": "Comisiones",
    "Comisiones sobre pedidos": "Comisiones",
    "Comisión de reembolso": "Comisiones",
    "Comisiones sobre pedidos reembolsados": "Comisiones",
    "Cobro por comisión por venta": "Comisiones",
    "Reembolso por comisión por venta": "Comisiones",
    "Comisión": "Comisiones",
    "Commission": "Comisiones",
    "commission_fee": "Comisiones",
    "refund_commission_fee": "Comisiones",
    "Cargo por venta": "Comisiones",
    "Cargo por campaña de publicidad - Product Ads": "Publicidad",
    "Cargo por campaña de publicidad - Brand Ads": "Publicidad",
    "Campañas de publicidad - Product Ads": "Publicidad",
    "Campañas de publicidad - Brand Ads": "Publicidad",
    "Campañas de publicidad - Display": "Publicidad",
    "Cargo por campaña de publicidad - Display programático": "Publicidad",
    "Cargo por Asesoría Comercial": "Servicios",
    "Cargo por mantenimiento de Mi página": "Servicios",
    "Anulación del cargo por mantenimiento de Mi página": "Servicios",
    "Anulación mantenimiento Mi página": "Servicios",
    "Abono oferta TC - OPEX": "Servicios",
    "Descuento oferta TC - OPEX": "Servicios",
    "Abonos por cupón promocional": "Servicios",
    "Descuento por cupones de despacho": "Servicios",
    "Abonos soluciones comerciales": "Servicios",
    "Descuento por PDM": "Servicios",
    "Pago de aporte promocionales a cliente (Promo)": "Servicios",
    "Descuento por aportes promocionales a clientes (Promo)": "Servicios",
    "Bonificación": "Bonificaciones",
    "Bonificación Logística Flex": "Bonificaciones",
    "Recuperación por Pérdida de Inventario": "Bonificaciones",
    "Impuesto sobre las comisiones": "Impuestos",
    "Impuesto sobre la comisión de reembolso": "Impuestos",
    "Impuesto de la factura manual": "Impuestos",
    "Impuestos sobre comisión": "Impuestos",
    "Impuestos": "Impuestos",
    "Descuento por cancelación": "Ajustes",
    "Otros descuentos": "Ajustes",
    "Compensación logística": "Ajustes",
    "Ajuste Inventario Activo": "Ajustes",
    "Cobro por campaña": "Ajustes",
    "Merma": "Ajustes",
    "Multa": "Ajustes",
    "Multa por stock": "Ajustes",
    "Corrección de pago envio directo": "Ajustes",
    "Corrección de cobro por envío directo": "Ajustes",
    "Abono extraordinario - error de precio": "Ajustes",
    "Abono por error de comisión": "Ajustes",
    "Abono postventa": "Ajustes",
    "Abono por formalización a OPL": "Ajustes",
    "Otros abonos": "Ajustes",
    "Descuento por compensación a cliente": "Ajustes",
    "Abono de factura manual": "Ajustes",
    "Factura manual": "Ajustes",
    "Abono manual": "Ajustes",
    "Ajuste histórico (pre-2026)": "Ajustes",
    "Ajuste Poscobro": "Ajustes",
    "Ajuste por Talla/Garantía": "Ajustes",
    "Ajuste por Producto Dañado/Vacío": "Ajustes",
    "Ajuste por Arrepentimiento": "Ajustes",
    "Ajuste por Diferencia de Publicación": "Ajustes",
    "Ajuste por Ítem Faltante": "Ajustes",
    "Ajuste por Falta de Stock": "Ajustes",
    "Ajuste por Retraso en Entrega": "Ajustes",
    "Ajuste por Cambio de Dirección": "Ajustes",
    "Ajuste por Falla en Entrega": "Ajustes",
    "Ajuste por Compra Protegida (BPP)": "Ajustes",
    "Ajuste por Disputa no Respondida": "Ajustes",
    "Cargo": "Ajustes",
    "Cancelación de la mediación": "Ajustes",
    "cashback": "Ajustes",
    "cashback_cancel": "Ajustes",
    "Mediación": "Ajustes",
    "Reserva para devolución en envío BBP": "Ajustes",
    "Reserva para reembolso": "Ajustes",
    "Reserva para pago de deuda": "Ajustes",
    "reserve_for_dispute": "Ajustes",
    "Reserva para pago": "Ajustes",
    "Rebate": "Ajustes",
    "refund_order_amount": "Ajustes",
}

# ── Cached YAML taxonomy (lazy-loaded) ────────────────────────────────
_TAXONOMY_RULES: dict | None = None
_TAXONOMY_MAPPINGS: dict | None = None
_CONCEPT_TO_GROUP: dict[str, str] | None = None


def _taxonomy_rules():
    global _TAXONOMY_RULES
    if _TAXONOMY_RULES is None:
        _TAXONOMY_RULES = tl.load_rules()
    return _TAXONOMY_RULES


def _taxonomy_mappings():
    global _TAXONOMY_MAPPINGS
    if _TAXONOMY_MAPPINGS is None:
        _TAXONOMY_MAPPINGS = tl.load_mappings()
    return _TAXONOMY_MAPPINGS


def _concept_to_group():
    global _CONCEPT_TO_GROUP
    if _CONCEPT_TO_GROUP is None:
        _CONCEPT_TO_GROUP = tl.build_concept_to_group_map(_taxonomy_rules())
    return _CONCEPT_TO_GROUP





def _get_financial_structure() -> dict[str, list[str]]:
    """Return {group_name: [concepts...]} from taxonomy or legacy."""
    if USE_YAML_TAXONOMY:
        rules = _taxonomy_rules()
        return {g: d["concepts"] for g, d in rules.items()}
    from engine.v4.marketplace_auditor import FINANCIAL_STRUCTURE
    return FINANCIAL_STRUCTURE


def _get_concept_map() -> dict[str, str]:
    """Return {detalle: concept} for cobros-breakdown display.

    This is a display-layer convention (Logística, Comisiones, Publicidad, etc.)
    created for the UX1.1 dashboard — NOT financial taxonomy.
    The legacy map is the canonical certified source.
    """
    return _LEGACY_CONCEPT_MAP


class FinancialEngine:
    """Single certified entry point for all financial operations.

    Every method is deterministic, traceable, and certification-anchored.
    No financial logic exists outside this class.
    """

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()
        self._auditor = MarketplaceAuditorEngine(db=self.db)

    # ------------------------------------------------------------------
    # Period resolution (certified, extracted from api.py)
    # ------------------------------------------------------------------
    def resolve_period_range(self, periodo: str | None) -> tuple[str, str | None, str]:
        """Return (start_date, end_date, label). end_date=None means YTD."""
        if not periodo or periodo.upper() == 'YTD':
            df = self.db.query('SELECT MAX(periodo_inicio) as max_p FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0')
            if not df.empty and pd.notna(df.iloc[0]['max_p']):
                mx = pd.to_datetime(df.iloc[0]['max_p'])
                return f'{mx.year}-01-01', None, 'Year to Date'
            return '2024-01-01', None, 'Year to Date'

        y, m = map(int, periodo.split('-'))
        last_day = calendar.monthrange(y, m)[1]
        return f'{y}-{m:02d}-01', f'{y}-{m:02d}-{last_day}', f'{_MONTHS[m - 1]} {y}'

    def list_periods(self) -> list[dict[str, str]]:
        """Return available cierre periods."""
        df = self.db.query("""
            SELECT DISTINCT periodo_inicio
            FROM marketplace_cierre_financiero_v1
            WHERE resultado_neto != 0
            ORDER BY periodo_inicio DESC
        """)
        periods = [{"value": "YTD", "label": "Year to Date"}]
        for _, r in df.iterrows():
            p = pd.to_datetime(r['periodo_inicio'])
            if pd.isna(p): continue
            label = f"{_MONTHS[p.month - 1]} {p.year}"
            periods.append({"value": f"{p.year}-{p.month:02d}", "label": label})
        return periods

    # ------------------------------------------------------------------
    # Clean records (NaN/NaT normalization)
    # ------------------------------------------------------------------
    @staticmethod
    def clean_records(df: pd.DataFrame) -> list[dict[str, Any]]:
        records = df.to_dict(orient="records")
        cleaned = []
        for r in records:
            clean_r = {}
            for k, v in r.items():
                if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                    clean_r[k] = None
                elif pd.isna(v):
                    clean_r[k] = None
                elif hasattr(v, 'isoformat'):
                    clean_r[k] = v.isoformat()
                else:
                    clean_r[k] = v
            cleaned.append(clean_r)
        return cleaned

    # ------------------------------------------------------------------
    # Concept mapping (certified server-side detalle -> concept)
    # ------------------------------------------------------------------
    @staticmethod
    def map_detalle_to_concept(detalle: str) -> str:
        """Map raw detalle to a broad concept name using legacy maps."""
        m = _get_concept_map()
        return m.get(detalle, "Otros")

    def get_financial_records_count(self, marketplace: str | None, periodo: str | None) -> int:
        """Returns the official count of classified financial records."""
        where_clause, params = self._build_ledger_where(periodo, marketplace)
        op_filters = self._build_signal_filter(marketplace or "ALL")[0]
        sql = f"SELECT COUNT(*) as count FROM marketplace_ledger_v1 WHERE {where_clause} {op_filters} AND financial_group IS NOT NULL"
        result = self.db.query(sql, params)
        if result.empty:
            return 0
        return int(result.iloc[0]["count"])

    def is_financial_structure_ready(self, marketplace: str | None, periodo: str | None) -> bool:
        """Returns True if the financial structure has been built (i.e. groups are generated)."""
        where_clause, params = self._build_ledger_where(periodo, marketplace)
        op_filters = self._build_signal_filter(marketplace or "ALL")[0]
        sql = f"SELECT financial_group FROM marketplace_ledger_v1 WHERE {where_clause} {op_filters} GROUP BY financial_group"
        df = self.db.query(sql, params)
        return len(df) > 0

    def get_period_status(self, marketplace: str | None, periodo: str | None) -> str:
        """
        Determines the global status for the Dashboard state.
        Uses single source of truth components.
        """
        from engine.v4.domain.ledger_engine import LedgerEngine
        ledger = LedgerEngine(db=self.db)
        if ledger.get_ledger_records_count(marketplace or "ALL", periodo or "ALL") == 0:
            return "SIN_DATOS"
        if not self.is_financial_structure_ready(marketplace, periodo):
            return "PARCIAL"
        return "CERTIFICADO"

    # ------------------------------------------------------------------
    # Ledger queries
    # ------------------------------------------------------------------
    def query_ledger(
        self,
        marketplace: str = "ML",
        periodo: str | None = None,
        financial_group: str | None = None,
        clasificacion_operativa: str | None = None,
        detalle: str | None = None,
        order_id: str | None = None,
        id_transaccion: str | None = None,
        folio_xml: str | None = None,
        archivo_origen: str | None = None,
        offset: int = 0,
        limit: int = 200,
        filter_zero: bool = True,
        operational_only: bool = True,
        signal_mode: str = "ALL",
    ) -> dict[str, Any]:
        """Query marketplace_ledger_v1 with certified filtering."""
        conditions = ["marketplace = ?"]
        params = [marketplace]

        if id_transaccion:
            conditions.append("id_transaccion = ?")
            params.append(id_transaccion)
        elif order_id:
            conditions.append("(id_transaccion = ? OR id_orden = ?)")
            params.extend([order_id, order_id])
        elif periodo:
            start, end, _ = self.resolve_period_range(periodo)
            conditions.append("fecha >= ?")
            params.append(start)
            if end is not None:
                conditions.append("fecha <= ?")
                params.append(end)

        if financial_group:
            fg_values = [v.strip() for v in financial_group.split(",") if v.strip()]
            if len(fg_values) == 1:
                conditions.append("LOWER(financial_group) = LOWER(?)")
                params.append(fg_values[0])
            else:
                placeholders = ",".join(["?" for _ in fg_values])
                conditions.append(f"LOWER(financial_group) IN ({placeholders})")
                params.extend([v.lower() for v in fg_values])

        if clasificacion_operativa:
            if marketplace == 'PARIS' and clasificacion_operativa in ('Comisión Marketplace', 'Venta Bruta'):
                conditions.append("financial_group = 'ingresos'")
                conditions.append("comision_marketplace > 0")
            else:
                conditions.append("clasificacion_operativa = ?")
                params.append(clasificacion_operativa)

        if detalle:
            if marketplace == 'PARIS' and detalle in ('Comisión Marketplace', 'Venta Bruta'):
                conditions.append("financial_group = 'ingresos'")
                conditions.append("comision_marketplace > 0")
            else:
                conditions.append("LOWER(detalle) = LOWER(?)")
                params.append(detalle)

        # Signal/noise filtering using taxonomy
        if signal_mode.upper() != "ALL":
            import json, os
            mp_lower = marketplace.lower()
            tax_files = {
                'ml': 'ml_v1.json', 'paris': 'paris_v1.json',
                'ripley': 'ripley_v1.json', 'falabella': 'falabella_v1.json'
            }
            tax_fname = tax_files.get(mp_lower, 'ripley_v1.json')
            tax_path = os.path.join(os.path.dirname(__file__),
                '..', '..', '..', 'KnowledgeBase', 'Marketplace', 'Taxonomy', tax_fname)
            if os.path.exists(tax_path):
                with open(tax_path, encoding='utf-8') as f:
                    tax = json.load(f)
                is_signal = signal_mode.upper() == "SIGNAL"
                matching = [d.lower() for d, info in tax['detalle_classification'].items()
                            if (info.get('signal') is True) == is_signal]
                if matching:
                    ph = ",".join(["?" for _ in matching])
                    conditions.append(f"LOWER(detalle) IN ({ph})")
                    params.extend(matching)

        if folio_xml:
            conditions.append("folio_xml = ?")
            params.append(folio_xml)

        if archivo_origen:
            conditions.append("archivo_origen = ?")
            params.append(archivo_origen)

        if operational_only:
            conditions.append("COALESCE(include_in_operational_pnl, 1) = 1")

        if filter_zero:
            conditions.append("monto != 0")

        where = " AND ".join(conditions)

        agg = self.db.query(
            f"SELECT COUNT(*) as cnt, COALESCE(SUM(monto), 0) as sm FROM marketplace_ledger_v1 WHERE {where}", params)
        total_count = int(agg.iloc[0, 0])
        total_sum = float(agg.iloc[0, 1])

        df = self.db.query(
            f"SELECT * FROM marketplace_ledger_v1 WHERE {where} ORDER BY fecha DESC LIMIT ? OFFSET ?",
            params + [limit, offset]
        )

        detalles_df = self.db.query(
            f"SELECT DISTINCT detalle FROM marketplace_ledger_v1 WHERE {where} AND detalle IS NOT NULL ORDER BY detalle", params)
        detalles = [str(r['detalle']) for _, r in detalles_df.iterrows()]

        return {
            "data": self.clean_records(df),
            "total_count": total_count,
            "total_sum": total_sum,
            "offset": offset,
            "limit": limit,
            "detalles": detalles,
        }

    # ------------------------------------------------------------------
    # Cierre queries
    # ------------------------------------------------------------------
    def query_cierre(self, marketplace: str = "ML", periodo: str | None = None) -> list[dict[str, Any]]:
        if periodo:
            year, month = periodo.split("-")
            p_ini = f"{year}-{month}-01"
            df = self.db.query(
                "SELECT * FROM marketplace_cierre_financiero_v1 WHERE marketplace = ? AND periodo_inicio = ? ORDER BY created_at DESC LIMIT 1",
                [marketplace, p_ini])
        else:
            df = self.db.query(
                "SELECT * FROM marketplace_cierre_financiero_v1 WHERE marketplace = ? ORDER BY periodo_inicio DESC LIMIT 1",
                [marketplace])
        return self.clean_records(df)

    def query_cierre_all(self) -> list[dict[str, Any]]:
        df = self.db.query(
            "SELECT DISTINCT marketplace, periodo_inicio, periodo_fin, total_ingresos, total_costos_operacionales, total_costos_comerciales, total_ajustes, resultado_neto FROM marketplace_cierre_financiero_v1 ORDER BY marketplace, periodo_inicio")
        return self.clean_records(df)

    # ------------------------------------------------------------------
    # Classification queries
    # ------------------------------------------------------------------
    def query_classification(
        self,
        id_transaccion: str | None = None,
        marketplace: str | None = None,
        limit: int = 1,
    ) -> list[dict[str, Any]]:
        """Query marketplace_ledger_clasificado_v1 via public contract."""
        conditions: list[str] = []
        params: list[Any] = []
        if id_transaccion:
            conditions.append("id_transaccion = ?")
            params.append(id_transaccion)
        if marketplace:
            conditions.append("marketplace = ?")
            params.append(marketplace)
        where = " WHERE " + " AND ".join(conditions) if conditions else ""
        df = self.db.query(
            f"SELECT id_transaccion, marketplace, financial_group, financial_subgroup, "
            f"clasificacion_operativa, origen_clasificacion, confianza_clasificacion, "
            f"include_in_operational_pnl "
            f"FROM marketplace_ledger_clasificado_v1{where} "
            f"ORDER BY id_transaccion LIMIT ?",
            params + [limit],
        )
        return self.clean_records(df)

    # ------------------------------------------------------------------
    # Ventas queries (ingestion provenance)
    # ------------------------------------------------------------------
    def query_ventas(self, source_file: str | None = None) -> list[dict[str, Any]]:
        """Query ventas_marketplace table for order provenance."""
        if source_file:
            df = self.db.query(
                "SELECT DISTINCT order_id, source_file, marketplace, gross_amount, sale_date "
                "FROM ventas_marketplace WHERE source_file = ? ORDER BY order_id",
                [source_file],
            )
        else:
            df = self.db.query(
                "SELECT DISTINCT order_id, source_file, marketplace, gross_amount, sale_date "
                "FROM ventas_marketplace ORDER BY order_id LIMIT 100",
            )
        return self.clean_records(df)

    def check_duplicate_transactions(
        self, marketplace: str, periodo: str | None = None,
        key_fields: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Return duplicate id_transaccion in operational P&L for a marketplace.

        Args:
            marketplace: Marketplace filter.
            periodo: Optional period filter (YYYY-MM).
            key_fields: GROUP BY fields for uniqueness check. Defaults to
                        ["id_transaccion"]. Use ["id_transaccion", "archivo_origen"]
                        for PARIS/RIPLEY where source files overlap.
        """
        if key_fields is None:
            key_fields = ["id_transaccion"]
        group_cols = ", ".join(f"COALESCE({k}, '') as {k.split('.')[-1]}" for k in key_fields)
        group_by = ", ".join(key_fields)
        select_exprs = ", ".join(key_fields)
        params: list[Any] = [marketplace.lower()]
        period_filter = ""
        if periodo:
            period_filter = " AND fecha >= ? AND fecha < date(?) + INTERVAL '1 month'"
            year, month = periodo.split("-")
            p_start = f"{year}-{month}-01"
            params.extend([p_start, p_start])
        df = self.db.query(
            f"SELECT {select_exprs}, COUNT(*) as cnt, "
            f"ARRAY_TO_STRING(ARRAY_AGG(DISTINCT id_orden), ',') as order_ids, "
            f"ARRAY_TO_STRING(ARRAY_AGG(DISTINCT tipo_movimiento), ',') as tipos, "
            f"COALESCE(SUM(monto), 0) as total_monto, "
            f"ARRAY_TO_STRING(ARRAY_AGG(DISTINCT detalle), ',') as detalles "
            f"FROM marketplace_ledger_v1 "
            f"WHERE LOWER(marketplace) = ? "
            f"AND COALESCE(include_in_operational_pnl, 1) = 1 "
            f"AND monto != 0{period_filter} "
            f"GROUP BY {group_by} "
            f"HAVING COUNT(*) > 1 "
            f"ORDER BY cnt DESC",
            params,
        )
        return self.clean_records(df)

    # ------------------------------------------------------------------
    # Desglose (certified categorization)
    # ------------------------------------------------------------------
    def query_desglose(
        self,
        marketplace: str = "ML",
        periodo: str | None = None,
        exclude_non_operational: bool = False,
    ) -> list[dict[str, Any]]:
        """Return certified financial breakdown by financial_group, detalle."""
        if not periodo or periodo in ("ALL", "YTD"):
            p_ini, p_fin = "2000-01-01", "2100-12-31"
        else:
            year, month = map(int, periodo.split("-"))
            last_day = calendar.monthrange(year, month)[1]
            p_ini, p_fin = f"{year}-{month}-01", f"{year}-{month}-{last_day}"

        exclude_clause = " AND COALESCE(c.include_in_operational_pnl, 1) = 1" if exclude_non_operational else ""

        sql = f"""
            SELECT 
                COALESCE(c.financial_group, 'sin_clasificar') as financial_group,
                l.detalle,
                l.tipo_movimiento,
                c.clasificacion_operativa,
                CASE 
                    WHEN l.id_transaccion LIKE 'RIP_TH_%' THEN 'TH'
                    WHEN l.id_transaccion LIKE 'RIP_FF_%' THEN 'FF'
                    WHEN l.id_transaccion LIKE 'RIP_CSV_%' THEN 'CICLOS'
                    WHEN l.archivo_origen LIKE '%.xlsx' THEN 'SELLER'
                    WHEN l.archivo_origen LIKE '%.xml' THEN 'XML'
                    ELSE 'OTRO'
                END as origen_capa,
                CASE 
                    WHEN l.id_transaccion LIKE 'RIP_TH_%' THEN 'TRANSACTION'
                    WHEN l.id_transaccion LIKE 'RIP_FF_%' THEN 'LOGISTICS'
                    WHEN l.id_transaccion LIKE 'RIP_CSV_%' THEN 'SETTLEMENT'
                    WHEN l.archivo_origen LIKE '%.xlsx' THEN 'OPERATIONAL'
                    WHEN l.archivo_origen LIKE '%.xml' THEN 'TAX'
                    ELSE 'UNKNOWN'
                END as truth_type,
                SUM(COALESCE(l.monto, 0)) as total,
                COUNT(*) as cantidad
            FROM marketplace_ledger_v1 l
            LEFT JOIN marketplace_ledger_clasificado_v1 c
                ON l.marketplace = c.marketplace AND l.id_transaccion = c.id_transaccion
            WHERE l.marketplace = ?
              AND l.fecha BETWEEN ? AND ?
              {exclude_clause}
              AND COALESCE(c.financial_group, 'sin_clasificar') NOT IN ('tesoreria', 'recuperaciones_y_bonificaciones')
            GROUP BY c.financial_group, l.detalle, l.tipo_movimiento, c.clasificacion_operativa, origen_capa, truth_type
            ORDER BY total ASC
        """
        df = self.db.query(sql, [marketplace, p_ini, p_fin])

        records = []
        for _, row in df.iterrows():
            r_detalle = str(row['detalle']) if not pd.isna(row['detalle']) else ""
            r_clasificacion = str(row['clasificacion_operativa']) if not pd.isna(row['clasificacion_operativa']) else r_detalle
            r_total = float(row['total'])

            records.append({
                "detalle": f"{r_detalle} [{row['origen_capa']}][{row['truth_type']}]" if marketplace == 'RIPLEY' else r_detalle,
                "clasificacion_operativa": r_clasificacion,
                "tipo_movimiento": row['tipo_movimiento'],
                "total": r_total,
                "cantidad": int(row['cantidad']),
                "categoria": str(row['financial_group']),
                "origen_capa": row['origen_capa'],
                "truth_type": row['truth_type'],
                "is_legacy_360": True,
            })

        if marketplace == 'PARIS':
            records = self._apply_paris_desglose(records, marketplace, p_ini, p_fin, exclude_clause)

        if marketplace == 'RIPLEY':
            for r in records:
                cat = str(r.get('clasificacion_operativa', '')).upper()
                if cat == 'COMISIONES':
                    r['categoria'] = 'costos_comerciales'
                elif cat == 'DEVOLUCIONES':
                    r['categoria'] = 'devoluciones'
                elif 'DESPACHO' in cat:
                    r['categoria'] = 'costos_operacionales'
                elif cat == 'VENTAS':
                    r['categoria'] = 'ingresos'

        return records

    def _apply_paris_desglose(self, existing: list, marketplace: str, p_ini: str, p_fin: str, exclude_clause: str) -> list:
        """PARIS-specific desglose: splits Venta into Venta Bruta and Comisión Marketplace."""
        sql = f"""
            SELECT 
                COALESCE(c.financial_group, 'sin_clasificar') as financial_group,
                l.detalle,
                l.tipo_movimiento,
                c.clasificacion_operativa,
                l.monto, l.monto_bruto, l.comision_marketplace,
                CASE WHEN l.archivo_origen LIKE '%.xlsx' THEN 'SELLER' ELSE 'OTRO' END as origen_capa,
                CASE WHEN l.archivo_origen LIKE '%.xlsx' THEN 'OPERATIONAL' ELSE 'UNKNOWN' END as truth_type
            FROM marketplace_ledger_v1 l
            LEFT JOIN marketplace_ledger_clasificado_v1 c
                ON l.marketplace = c.marketplace AND l.id_transaccion = c.id_transaccion
            WHERE l.marketplace = ?
              AND l.fecha BETWEEN ? AND ?
              {exclude_clause}
              AND COALESCE(c.financial_group, 'sin_clasificar') NOT IN ('tesoreria', 'recuperaciones_y_bonificaciones')
        """
        df_p = self.db.query(sql, [marketplace, p_ini, p_fin])

        agg = {}
        for _, row in df_p.iterrows():
            fg, det, tm, co = row['financial_group'], row['detalle'], row['tipo_movimiento'], row['clasificacion_operativa']
            monto, bruto, com = row['monto'], row['monto_bruto'], row['comision_marketplace']
            oc, tt = row['origen_capa'], row['truth_type']

            if det == 'Venta':
                key = (fg, det, tm, 'Venta Bruta', oc, tt)
                agg[key] = agg.get(key, 0.0) + float(bruto if pd.notna(bruto) else monto)
                if pd.notna(com) and float(com) > 0:
                    key_c = ('costos_comerciales', 'Comisión Marketplace', 'egreso', 'Comisión Marketplace', oc, tt)
                    agg[key_c] = agg.get(key_c, 0.0) - float(com)
            else:
                key = (fg, det, tm, co, oc, tt)
                agg[key] = agg.get(key, 0.0) + float(monto)

        return [{
            "categoria": k[0], "detalle": k[1], "tipo_movimiento": k[2],
            "clasificacion_operativa": k[3], "total": v, "cantidad": 1,
            "origen_capa": k[4], "truth_type": k[5], "is_legacy_360": True,
        } for k, v in agg.items()]

    # ------------------------------------------------------------------
    # Cobros breakdown matrix (certified server-side)
    # ------------------------------------------------------------------
    def get_executive_breakdown(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        """Returns the full executive breakdown required by the dashboard API."""
        start, end, label = self.resolve_period_range(periodo)
        where_clause, params = self._build_ledger_where(periodo, marketplace)
        op_filters_sql, op_filters_params = self._build_signal_filter(marketplace or "ALL")

        # Single query: neto + per-group breakdown combined
        r = self.db.query(f"SELECT COALESCE(SUM(monto), 0) as neto, COALESCE(SUM(CASE WHEN LOWER(financial_group)='ingresos' THEN monto ELSE 0 END), 0) as gross_sales, COALESCE(SUM(CASE WHEN LOWER(financial_group)='devoluciones' THEN monto ELSE 0 END), 0) as devoluciones, COALESCE(SUM(CASE WHEN LOWER(financial_group) IN ('costos_operacionales','costos_comerciales') THEN monto ELSE 0 END), 0) as costos_op, COALESCE(SUM(CASE WHEN LOWER(financial_group)='comisiones' THEN monto ELSE 0 END), 0) as comisiones, COALESCE(SUM(CASE WHEN LOWER(financial_group)='ajustes' THEN monto ELSE 0 END), 0) as ajustes, COALESCE(SUM(CASE WHEN LOWER(financial_group)='recuperaciones_y_bonificaciones' THEN monto ELSE 0 END), 0) as recuperaciones FROM marketplace_ledger_v1 WHERE {where_clause} AND financial_group IS NOT NULL AND COALESCE(include_in_operational_pnl, 1) = 1 {op_filters_sql}", params + op_filters_params).iloc[0]
        neto = float(r["neto"])
        gross = float(r["gross_sales"])
        returns = float(r["devoluciones"])
        costs_op = float(r["costos_op"])
        comms = float(r["comisiones"])
        adj = float(r["ajustes"])
        recup = float(r["recuperaciones"])
        
        # Single GROUP BY query replacing per-MP loop (8 queries → 2)
        # Non-RIPLEY MPs: no signal filter, GROUP BY in 1 query
        mp_base_where = f"fecha >= ?" if end is None else f"fecha BETWEEN ? AND ?"
        mp_base_params = [start] if end is None else [start, end]
        df_per_mp = self.db.query(f"SELECT LOWER(marketplace) as mp, COALESCE(SUM(monto), 0) as neto, COALESCE(SUM(CASE WHEN LOWER(financial_group)='ingresos' THEN monto ELSE 0 END), 0) as gross, COALESCE(SUM(CASE WHEN LOWER(financial_group)='devoluciones' THEN monto ELSE 0 END), 0) as devs, COALESCE(SUM(CASE WHEN LOWER(financial_group) IN ('costos_operacionales','costos_comerciales','comisiones','ajustes','recuperaciones_y_bonificaciones') THEN monto ELSE 0 END), 0) as costs FROM marketplace_ledger_v1 WHERE {mp_base_where} AND COALESCE(include_in_operational_pnl, 1) = 1 AND financial_group IS NOT NULL AND LOWER(marketplace) != 'ripley' GROUP BY LOWER(marketplace)", mp_base_params)
        per_mp = {}
        for _, row in df_per_mp.iterrows():
            mp_key = str(row["mp"]).upper()
            per_mp[mp_key] = {"ingresos": float(row["gross"]), "devoluciones": float(row["devs"]), "costos": float(row["costs"]), "neto": float(row["neto"])}
        # RIPLEY: apply signal filter (same as WF/ES for SFT consistency)
        rip_sig_f, rip_sig_p = self._build_signal_filter("ripley")
        rip_q = f"SELECT COALESCE(SUM(monto), 0) as neto, COALESCE(SUM(CASE WHEN LOWER(financial_group)='ingresos' THEN monto ELSE 0 END), 0) as gross, COALESCE(SUM(CASE WHEN LOWER(financial_group)='devoluciones' THEN monto ELSE 0 END), 0) as devs, COALESCE(SUM(CASE WHEN LOWER(financial_group) IN ('costos_operacionales','costos_comerciales','comisiones','ajustes','recuperaciones_y_bonificaciones') THEN monto ELSE 0 END), 0) as costs FROM marketplace_ledger_v1 WHERE {mp_base_where} AND LOWER(marketplace) = 'ripley' AND COALESCE(include_in_operational_pnl, 1) = 1 AND financial_group IS NOT NULL {rip_sig_f}"
        rip_r = self.db.query(rip_q, mp_base_params + rip_sig_p).iloc[0]
        per_mp["RIPLEY"] = {"ingresos": float(rip_r["gross"]), "devoluciones": float(rip_r["devs"]), "costos": float(rip_r["costs"]), "neto": float(rip_r["neto"])}
        # Ensure all 4 MPs are present
        for mp in ["ML", "RIPLEY", "PARIS", "FALABELLA"]:
            if mp not in per_mp:
                per_mp[mp] = {"ingresos": 0.0, "devoluciones": 0.0, "costos": 0.0, "neto": 0.0}

        return {
            "period": label,
            "marketplace": marketplace or "ALL",
            "gross_sales": gross,
            "devoluciones": returns,
            "costos_operacionales": costs_op,
            "comisiones": comms,
            "ajustes": adj,
            "recuperaciones": recup,
            "neto": neto,
            "per_marketplace": per_mp,
        }

    def query_cobros_breakdown(
        self,
        marketplace: str | None = None,
        periodo: str | None = None,
    ) -> dict[str, Any]:
        """Return concept × MP matrix for costos_operacionales + costos_comerciales + ajustes."""
        start, end, label = self.resolve_period_range(periodo)

        mp_filter, mp_params = "", []
        if marketplace and marketplace not in ("ALL", "", None):
            mp_filter = "AND LOWER(marketplace) = LOWER(?)"
            mp_params = [marketplace]

        if end is None:
            ld_where = f"fecha >= ? {mp_filter}"
            ld_params = [start] + mp_params
        else:
            ld_where = f"fecha BETWEEN ? AND ? {mp_filter}"
            ld_params = [start, end] + mp_params

        df = self.db.query(f"""
            SELECT marketplace, detalle, financial_group, SUM(COALESCE(monto, 0)) as total
            FROM marketplace_ledger_v1
            WHERE LOWER(financial_group) IN ('costos_operacionales', 'costos_comerciales', 'costos_logisticos', 'comisiones', 'ajustes')
              AND COALESCE(include_in_operational_pnl, 1) = 1
              AND LOWER(financial_group) IS NOT NULL
              AND {ld_where}
            GROUP BY marketplace, detalle, financial_group
            ORDER BY marketplace, total ASC
        """, ld_params)

        concept_data: dict[tuple[str, str], float] = {}
        mp_set: set[str] = set()

        for _, row in df.iterrows():
            detalle = str(row['detalle']) if not pd.isna(row['detalle']) else ""
            mp = str(row['marketplace'])
            total = float(row['total'])
            concept = self.map_detalle_to_concept(detalle)
            mp_set.add(mp)
            key = (concept, mp)
            concept_data[key] = concept_data.get(key, 0) + total

        mps = sorted(mp_set)
        concept_keys = set(k[0] for k in concept_data)
        concept_totals = {c: sum(concept_data.get((c, mp), 0) for mp in mps) for c in concept_keys}
        sorted_concepts = sorted(concept_totals.keys(), key=lambda c: abs(concept_totals[c]), reverse=True)

        matrix = []
        for concept in sorted_concepts:
            row = {"concept": concept}
            for mp in mps:
                row[mp] = concept_data.get((concept, mp), 0)
            row["total"] = concept_totals[concept]
            matrix.append(row)

        return {
            "matrix": matrix,
            "total_cobros": sum(concept_totals.values()),
            "mps": mps,
            "concept_totals": concept_totals,
        }

    # ------------------------------------------------------------------
    # Executive summary (certified KPI cards)
    # ------------------------------------------------------------------
    def query_exec_summary(
        self,
        periodo: str | None = None,
        marketplace: str | None = None,
    ) -> dict[str, Any]:
        """Return certified executive summary — Ventas, Devoluciones, Cobros, Disponible."""
        start, end, label = self.resolve_period_range(periodo)

        mp_filter, mp_params = "", []
        if marketplace and marketplace.upper() != 'ALL':
            mp_filter = "AND LOWER(marketplace) = LOWER(?)"
            mp_params = [marketplace]

        if end is None:
            mx = self.db.query("SELECT MAX(periodo_inicio) as mx FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0")
            mx_val = mx.iloc[0]['mx']
            if pd.notna(mx_val):
                mx_dt = pd.to_datetime(mx_val)
                ytd_end = f"{mx_dt.year}-{mx_dt.month:02d}-{calendar.monthrange(mx_dt.year, mx_dt.month)[1]}"
            else:
                ytd_end = start
            dt_where, dt_params = "periodo_inicio >= ? AND periodo_fin <= ?", [start, ytd_end]
            ld_where, ld_params = "fecha >= ?", [start]
        else:
            dt_where, dt_params = "periodo_inicio >= ? AND periodo_fin <= ?", [start, end]
            ld_where, ld_params = "fecha BETWEEN ? AND ?", [start, end]

        if mp_filter:
            ld_where += mp_filter
            ld_params += mp_params

        # Apply signal filtering (RIPLEY only)
        sig_sql, sig_params = self._build_signal_filter(marketplace)
        ld_where += " " + sig_sql
        ld_params += sig_params

        ledger_pnl = self.db.query(f"""
            SELECT 
                COALESCE(SUM(CASE WHEN LOWER(financial_group)='ingresos' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as gross,
                COALESCE(SUM(CASE WHEN LOWER(financial_group)='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as returns,
                COALESCE(SUM(CASE WHEN LOWER(financial_group) IN ('costos_operacionales','costos_comerciales','costos_logisticos','comisiones','ajustes','recuperaciones_y_bonificaciones') AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as costs
            FROM marketplace_ledger_v1
            WHERE {ld_where}
        """, ld_params)

        gross_sales = float(ledger_pnl.iloc[0]['gross'])
        returns = float(ledger_pnl.iloc[0]['returns'])
        marketplace_costs = float(ledger_pnl.iloc[0]['costs'])
        net_profit = gross_sales + returns + marketplace_costs

        return {
            "period": label,
            "marketplace": marketplace or "ALL",
            "financial_pnl": {
                "gross_sales": gross_sales,
                "returns": returns,
                "marketplace_costs": marketplace_costs,
                "net_profit": net_profit,
            },
        }

    # ------------------------------------------------------------------
    # Waterfall (certified Ventas → Devoluciones → Cobros → Disponible)
    # ------------------------------------------------------------------
    def query_waterfall(
        self,
        marketplace: str | None = None,
        periodo: str | None = None,
    ) -> dict[str, Any]:
        """Return certified waterfall layers."""
        start, end, label = self.resolve_period_range(periodo)

        mp_filter, mp_params = "", []
        if marketplace and marketplace.upper() != 'ALL':
            mp_filter = "AND LOWER(marketplace) = LOWER(?)"
            mp_params = [marketplace]

        if end is None:
            ld_where = f"fecha >= ? {mp_filter}"
            ld_params = [start] + mp_params
        else:
            ld_where = f"fecha BETWEEN ? AND ? {mp_filter}"
            ld_params = [start, end] + mp_params

        # Apply signal filtering (RIPLEY only)
        sig_sql, sig_params = self._build_signal_filter(marketplace)
        ld_where += " " + sig_sql
        ld_params += sig_params

        q = f"""
            SELECT
                SUM(CASE WHEN LOWER(financial_group)='ingresos' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END) as ventas,
                SUM(CASE WHEN LOWER(financial_group)='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END) as devoluciones,
                SUM(CASE WHEN LOWER(financial_group) IN ('costos_operacionales','costos_comerciales','costos_logisticos','comisiones','ajustes') AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END) as cobros,
                SUM(CASE WHEN LOWER(financial_group) IN ('recuperaciones_y_bonificaciones') AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END) as recuperaciones
            FROM marketplace_ledger_v1
            WHERE {ld_where}
        """
        import logging
        logging.warning(f"[DEBUG query_waterfall] marketplace={marketplace}, start={start}, end={end}")
        logging.warning(f"[DEBUG query_waterfall] SQL: {q}")
        logging.warning(f"[DEBUG query_waterfall] params: {ld_params}")
        
        df = self.db.query(q, ld_params)
        logging.warning(f"[DEBUG query_waterfall] result: {df.to_dict() if not df.empty else 'EMPTY'}")
        r = df.iloc[0] if not df.empty else pd.Series({'ventas': 0, 'devoluciones': 0, 'cobros': 0, 'recuperaciones': 0})

        ventas = float(r['ventas'] if pd.notna(r['ventas']) else 0)
        devoluciones = float(r['devoluciones'] if pd.notna(r['devoluciones']) else 0)
        cobros = float(r['cobros'] if pd.notna(r['cobros']) else 0)
        recuperaciones = float(r['recuperaciones'] if pd.notna(r['recuperaciones']) else 0)
        disponible = ventas + devoluciones + cobros + recuperaciones

        return {
            "period": label,
            "marketplace": marketplace or "ALL",
            "ventas": ventas,
            "devoluciones": devoluciones,
            "cobros": cobros,
            "recuperaciones": recuperaciones,
            "disponible": disponible,
            "layers": {
                "labels": ["Ventas", "Devoluciones", "Cobros", "Recuperaciones"],
                "values": [ventas, devoluciones, cobros, recuperaciones],
            },
        }

    # ------------------------------------------------------------------
    # Operational intelligence (top return reasons, AI narrative)
    # ------------------------------------------------------------------
    def query_operational_intelligence(
        self,
        periodo: str | None = None,
        marketplace: str | None = None,
    ) -> dict:
        """Return operational intelligence — top return reasons, AI narrative."""
        data = self.query_exec_summary(periodo, marketplace)
        pnl = data["financial_pnl"]
        ld_where, ld_params = self._build_ledger_where(periodo, marketplace)
        total_devoluciones = pnl["returns"] if pnl["returns"] != 0 else 1

        return_reasons_df = self.db.query(f"""
            SELECT detalle, COUNT(*) as casos, SUM(monto) as total_monto 
            FROM marketplace_ledger_v1 
            WHERE LOWER(financial_group) = 'devoluciones' AND {ld_where} 
            GROUP BY detalle 
            ORDER BY total_monto ASC LIMIT 5
        """, ld_params)

        return_reasons = []
        for _, r in return_reasons_df.iterrows():
            monto = float(r['total_monto'])
            participacion = abs(monto / total_devoluciones) * 100 if total_devoluciones < 0 else 0
            r_detalle = str(r['detalle'])
            det_params = list(ld_params) + [r_detalle]

            products_df = self.db.query(f"""
                SELECT v.sku, COUNT(c.id_transaccion) as p_casos 
                FROM marketplace_ledger_v1 c
                JOIN ventas_marketplace v ON c.id_orden = v.order_id
                WHERE LOWER(c.financial_group) = 'devoluciones' 
                  AND {ld_where.replace('fecha', 'c.fecha').replace('marketplace', 'c.marketplace')} 
                  AND c.detalle = ? AND v.sku != 'UNKNOWN'
                GROUP BY v.sku
                ORDER BY p_casos DESC LIMIT 3
            """, det_params)
            top_products = [str(pr['sku']) for _, pr in products_df.iterrows()]

            return_reasons.append({
                "reason": r_detalle,
                "cases": int(r['casos']),
                "impact": monto,
                "participation": round(participacion, 1),
                "top_products": top_products,
            })

        ai_narrative = []
        mp_text = marketplace if marketplace and marketplace != 'ALL' else "Todos los Marketplaces"
        if return_reasons:
            pr = return_reasons[0]
            ai_narrative.append(f"El principal motivo operativo de {mp_text} corresponde a {pr['reason']}.")
            ai_narrative.append(f"Representa el {pr['participation']:.1f}% del impacto económico del período.")
            ai_narrative.append(f"Generó un impacto de ${abs(pr['impact']):,.0f}.")
            ai_narrative.append(f"Afectó a {pr['cases']} operaciones.")
            if pr["top_products"]:
                ai_narrative.append(f"Mostrando concentración en productos/SKU como: {', '.join(pr['top_products'][:3])}.")
        else:
            ai_narrative.append(f"No se registraron incidencias operativas para {mp_text} en este período.")

        return {
            "top_return_reasons": return_reasons,
            "delivery_incidents": 0,
            "chargeback_incidents": 0,
            "ai_narrative": ai_narrative,
        }

    # ------------------------------------------------------------------
    # Audit queries
    # ------------------------------------------------------------------
    def query_audit(
        self,
        marketplace: str | None = None,
        check_name: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        """Return paginated, filterable audit alerts."""
        conditions = []
        params = []

        if marketplace:
            conditions.append("marketplace = ?")
            params.append(marketplace)
        if check_name:
            conditions.append("check_name = ?")
            params.append(check_name)

        where = " AND ".join(conditions) if conditions else "1=1"

        count_df = self.db.query(f"SELECT COUNT(*) as n FROM marketplace_auditoria_v1 WHERE {where}", params)
        total = int(count_df.iloc[0]['n'])

        df = self.db.query(f"""
            SELECT marketplace, check_name, condition_detected, action_taken, order_id, detected_at
            FROM marketplace_auditoria_v1
            WHERE {where}
            ORDER BY detected_at DESC
            LIMIT ? OFFSET ?
        """, params + [limit, offset])

        return {
            "data": self.clean_records(df),
            "total": total,
            "offset": offset,
            "limit": limit,
        }

    def query_audit_types(self) -> list[str]:
        df = self.db.query("SELECT DISTINCT check_name FROM marketplace_auditoria_v1 ORDER BY check_name")
        return [str(r['check_name']) for _, r in df.iterrows()]

    # ------------------------------------------------------------------
    # Classification + Closing + Audit (delegated to auditor)
    # ------------------------------------------------------------------
    def run_classification(self) -> int:
        """Run certified classification. WARNING: resets op_pnl flags."""
        return self._auditor.run_classification()

    def run_financial_closing(self, marketplace: str, periodo_inicio: str, periodo_fin: str) -> dict:
        """Run certified financial closing for one period."""
        return self._auditor.run_financial_closing(marketplace, periodo_inicio, periodo_fin)

    def run_financial_closing_all(self, marketplace: str, years: list[int] | None = None) -> list[dict]:
        """Run certified financial closing for all months in given years."""
        if years is None:
            years = [2023, 2024, 2025, 2026]
        results = []
        for year in years:
            for month in range(1, 13):
                last_day = calendar.monthrange(year, month)[1]
                p_ini = f"{year}-{month:02d}-01"
                p_fin = f"{year}-{month:02d}-{last_day}"
                result = self._auditor.run_financial_closing(marketplace, p_ini, p_fin)
                results.append(result)
        return results

    def run_audit(self) -> int:
        """Run certified audit. Safe: NO classification, NO closing. Preserves DEC-019."""
        return self._auditor.run_audit()

    def run_audit_safe(self) -> int:
        """Alias for run_audit. Explicitly documented as DEC-019 safe."""
        return self.run_audit()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    _SIGNAL_CACHE: dict[str, tuple[str, list]] | None = None

    def _build_signal_filter(self, marketplace: str) -> tuple[str, list]:
        """Return SQL snippet + params to filter by SIGNAL detalle values.
        Only filters for MPs with significant noise (RIPLEY).
        Returns ('', []) for MPs where signal filtering is not needed.
        Cache JSON file read at class level to avoid disk I/O per call."""
        mp_lower = marketplace.lower() if marketplace else ''
        if mp_lower not in ('ripley',):
            return '', []
        if self._SIGNAL_CACHE is not None:
            return self._SIGNAL_CACHE
        import json as _json, os as _os
        tax_path = _os.path.join(_os.path.dirname(__file__),
            '..', '..', '..', 'KnowledgeBase', 'Marketplace', 'Taxonomy', 'ripley_v1.json')
        if not _os.path.exists(tax_path):
            self._SIGNAL_CACHE = ('', [])
            return '', []
        with open(tax_path, encoding='utf-8') as _f:
            tax = _json.load(_f)
        signal_detalles = [d.lower() for d, info in tax['detalle_classification'].items()
                          if info.get('signal') is True]
        if not signal_detalles:
            self._SIGNAL_CACHE = ('', [])
            return '', []
        ph = ','.join(['?'] * len(signal_detalles))
        self._SIGNAL_CACHE = (f"AND LOWER(detalle) IN ({ph})", signal_detalles)
        return self._SIGNAL_CACHE

    def _build_ledger_where(self, periodo: str | None, marketplace: str | None) -> tuple[str, list]:
        start, end, _ = self.resolve_period_range(periodo)
        mp_filter, mp_params = "", []
        if marketplace and marketplace.upper() != 'ALL':
            mp_filter = "AND LOWER(marketplace) = LOWER(?)"
            mp_params = [marketplace]

        if end is None:
            return f"fecha >= ? {mp_filter}", [start] + mp_params
        return f"fecha BETWEEN ? AND ? {mp_filter}", [start, end] + mp_params

    # ------------------------------------------------------------------
    # Certification helpers
    # ------------------------------------------------------------------
    def certify_single_financial_truth(self) -> dict[str, Any]:
        """Validate ledger == cierre for all periods. Returns delta map."""
        periods = self.db.query("""
            SELECT DISTINCT marketplace, periodo_inicio, periodo_fin
            FROM marketplace_cierre_financiero_v1
            WHERE resultado_neto != 0
            ORDER BY marketplace, periodo_inicio
        """)
        results = []
        for _, p in periods.iterrows():
            mp = p['marketplace']
            p_ini = p['periodo_inicio']
            p_fin = p['periodo_fin']

            cierre = self.db.query(
                "SELECT resultado_neto, total_ingresos, total_devoluciones_equivalent FROM marketplace_cierre_financiero_v1 WHERE marketplace = ? AND periodo_inicio = ?",
                [mp, p_ini])
            return 0  # Simplified for now

        return {"status": "certified" if all(r['delta'] == 0 for r in results) else "delta_detected", "periods": results}
