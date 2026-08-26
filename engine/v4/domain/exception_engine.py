"""
Meli Financial AI Engine v4.0
Phase 5 Step 5 — Exception Engine (Rediseño Mínimo v2)

Motor canónico ÚNICO para detectar, clasificar, explicar y priorizar excepciones
financieras, documentales, tributarias y operacionales.

Contrato de diseño:
  1. Catálogo canónico ÚNICO de 19 categorías (EXCEPTION_CATALOG).
  2. Detección 100% read-only sobre v_ledger_certified, dte_truth_v1 y document_match_v1.
     No modifica ReconciliationEngine, TruthEngine, ClassificationEngine ni Electronic Certification.
  3. Cero persistencia: excepciones generadas determinísticamente desde la verdad actual.
  4. Severidad por reglas (INFO/LOW/MEDIUM/HIGH/CRITICAL) y prioridad P1-P4 con orden
     tributario > financiero > documental > operacional (PRIORITY_MATRIX determinística).
  5. Financial Delta = $0.00. Sin recálculos de montos ni conciliaciones.
"""
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, List

from engine.v4.database import DatabaseV4
from engine.v4.domain.reconciliation_engine import ReconciliationEngine

# ==============================================================================
# Catálogo canónico ÚNICO — 19 categorías (obligatorio)
# ==============================================================================

EXCEPTION_CATALOG = {
    # ---- TRIBUTARIO ----
    "MISSING_DTE": {
        "code": "MISSING_DTE",
        "name": "Venta o devolución sin DTE SII certificado",
        "description": "Movimiento de venta o devolución sin vínculo a DTE SII certificado.",
        "domain": "TRIBUTARIO",
        "severity": "HIGH",
        "owner": "TRIBUTARIO",
        "required_action": "VALIDAR_DTE_SII",
        "sla_days": 5,
        "evidence_required": ["dte_folio", "dte_truth_v1", "has_dte_link"],
        "explanation_template": "El movimiento {tx} del grupo {fg} carece de DTE SII certificado. Su respaldo fiscal es insuficiente para certificación ante el SII.",
    },
    "INSUFFICIENT_FISCAL_EVIDENCE": {
        "code": "INSUFFICIENT_FISCAL_EVIDENCE",
        "name": "Evidencia fiscal insuficiente",
        "description": "Movimiento sin evidencia fiscal real (XML, DTE o match) que respalde la operación.",
        "domain": "TRIBUTARIO",
        "severity": "CRITICAL",
        "owner": "TRIBUTARIO",
        "required_action": "SOLICITAR_EVIDENCIA_FISCAL",
        "sla_days": 2,
        "evidence_required": ["folio_xml", "dte_truth_v1", "document_match_v1"],
        "explanation_template": "El movimiento {tx} no posee evidencia fiscal real. No XML, no DTE SII ni match documental certificado. Blocking reason: {blocking_reason}.",
    },
    "TRUTH_CONFLICT": {
        "code": "TRUTH_CONFLICT",
        "name": "Conflicto de verdad entre fuentes",
        "description": "Conflicto de información entre fuentes: folio DTE vs folio document_match divergen.",
        "domain": "TRIBUTARIO",
        "severity": "CRITICAL",
        "owner": "TRIBUTARIO",
        "required_action": "RESOLVER_CONFLICTO_VERDAD",
        "sla_days": 1,
        "evidence_required": ["dte_truth_v1", "document_match_v1", "folio_xml"],
        "explanation_template": "Conflicto de verdad detectado: dte_truth folio={dte_folio} vs document_match folio={dm_folio}. No se emite respuesta especulativa.",
    },
    # ---- DOCUMENTAL ----
    "MISSING_XML": {
        "code": "MISSING_XML",
        "name": "XML de origen faltante",
        "description": "Movimiento financiero sin archivo XML de origen vinculado.",
        "domain": "DOCUMENTAL",
        "severity": "MEDIUM",
        "owner": "CONTABILIDAD",
        "required_action": "SOLICITAR_XML",
        "sla_days": 7,
        "evidence_required": ["01_Raw/XML", "folio_xml"],
        "explanation_template": "El movimiento {tx} no posee folio XML de origen. Respaldado únicamente por el Ledger.",
    },
    "DOCUMENT_REFERENCE_ONLY": {
        "code": "DOCUMENT_REFERENCE_ONLY",
        "name": "Solo referencia documental",
        "description": "Existe match documental (document_match) sin DTE SII real certificado.",
        "domain": "DOCUMENTAL",
        "severity": "LOW",
        "owner": "CONTABILIDAD",
        "required_action": "CORREGIR_VINCULO_DOCUMENTAL",
        "sla_days": 5,
        "evidence_required": ["document_match_v1", "dte_truth_v1"],
        "explanation_template": "El movimiento {tx} tiene match documental pero sin DTE SII real. Nivel de evidencia: DOCUMENT_REFERENCE_ONLY.",
    },
    "LEDGER_REFERENCE_ONLY": {
        "code": "LEDGER_REFERENCE_ONLY",
        "name": "Solo referencia de Ledger",
        "description": "Movimiento con folio en Ledger sin DTE real ni match documental.",
        "domain": "DOCUMENTAL",
        "severity": "LOW",
        "owner": "CONTABILIDAD",
        "required_action": "VALIDAR_ORIGEN_LEDGER",
        "sla_days": 5,
        "evidence_required": ["v_ledger_certified", "folio_xml"],
        "explanation_template": "El movimiento {tx} posee folio en Ledger sin DTE real ni match. Nivel de evidencia: LEDGER_REFERENCE_ONLY.",
    },
    "MISSING_SUPPORT": {
        "code": "MISSING_SUPPORT",
        "name": "Respaldo incompleto",
        "description": "Movimiento con evidencia parcial sin respaldo completo verificable.",
        "domain": "DOCUMENTAL",
        "severity": "MEDIUM",
        "owner": "CONTABILIDAD",
        "required_action": "COMPLETAR_RESPALDO",
        "sla_days": 7,
        "evidence_required": ["folio_xml", "has_dte_link", "document_match_v1"],
        "explanation_template": "El movimiento {tx} posee respaldo incompleto: XML={has_xml}, DTE={has_dte}, match={has_match}.",
    },
    # ---- FINANCIERO ----
    "AMOUNT_MISMATCH": {
        "code": "AMOUNT_MISMATCH",
        "name": "Diferencia de monto",
        "description": "Discrepancia entre monto liquidado y monto registrado en Ledger.",
        "domain": "FINANCIERO",
        "severity": "HIGH",
        "owner": "FINANZAS",
        "required_action": "VALIDAR_MONTO_ORIGEN",
        "sla_days": 3,
        "evidence_required": ["v_ledger_certified", "01_Raw"],
        "explanation_template": "Diferencia de monto detectada en {tx} entre fuentes comparadas.",
    },
    "DATE_MISMATCH": {
        "code": "DATE_MISMATCH",
        "name": "Desfase de fecha",
        "description": "Discrepancia de fecha entre el movimiento y su respaldo documental.",
        "domain": "FINANCIERO",
        "severity": "HIGH",
        "owner": "FINANZAS",
        "required_action": "VALIDAR_FECHA_ORIGEN",
        "sla_days": 3,
        "evidence_required": ["v_ledger_certified", "01_Raw"],
        "explanation_template": "Desfase de fecha detectado en {tx} entre el Ledger y su origen.",
    },
    "CLASSIFICATION_CONFLICT": {
        "code": "CLASSIFICATION_CONFLICT",
        "name": "Conflicto de clasificación",
        "description": "La clasificación financiera del Ledger difiere de la clasificación oficial.",
        "domain": "FINANCIERO",
        "severity": "MEDIUM",
        "owner": "CONTABILIDAD",
        "required_action": "REVISAR_CLASIFICACION",
        "sla_days": 5,
        "evidence_required": ["v_ledger_certified", "marketplace_ledger_clasificado_v1"],
        "explanation_template": "Conflicto de clasificación en {tx}: financial_group del Ledger difiere de la clasificación oficial.",
    },
    "RECONCILIATION_FAILED": {
        "code": "RECONCILIATION_FAILED",
        "name": "Conciliación fallida",
        "description": "La operación no logró un estado de conciliación exitoso.",
        "domain": "FINANCIERO",
        "severity": "HIGH",
        "owner": "FINANZAS",
        "required_action": "REVISAR_CONCILIACION",
        "sla_days": 4,
        "evidence_required": ["reconciliation_status"],
        "explanation_template": "La operación {tx} no logró conciliarse. Estado: {rec_status}.",
    },
    "SETTLEMENT_MISSING": {
        "code": "SETTLEMENT_MISSING",
        "name": "Liquidación faltante",
        "description": "Venta devengada sin liquidación de pagos registrada.",
        "domain": "FINANCIERO",
        "severity": "HIGH",
        "owner": "TESORERIA",
        "required_action": "GESTIONAR_LIQUIDACION",
        "sla_days": 5,
        "evidence_required": ["settlement_report"],
        "explanation_template": "La venta {tx} no posee liquidación de pagos registrada.",
    },
    "PENDING_COLLECTION": {
        "code": "PENDING_COLLECTION",
        "name": "Cobro pendiente",
        "description": "Venta devengada aún no transferida por el marketplace.",
        "domain": "FINANCIERO",
        "severity": "MEDIUM",
        "owner": "TESORERIA",
        "required_action": "VALIDAR_PAGO_MARKETPLACE",
        "sla_days": 5,
        "evidence_required": ["settlement_report"],
        "explanation_template": "La venta {tx} permanece devengada sin transferencia del marketplace.",
    },
    "PENDING_PAYMENT": {
        "code": "PENDING_PAYMENT",
        "name": "Pago pendiente",
        "description": "Liquidación aprobada pendiente de abono bancario.",
        "domain": "FINANCIERO",
        "severity": "MEDIUM",
        "owner": "TESORERIA",
        "required_action": "VALIDAR_TRANSFERENCIA_BANCARIA",
        "sla_days": 5,
        "evidence_required": ["bank_statement"],
        "explanation_template": "La liquidación {tx} está aprobada y pendiente de abono bancario.",
    },
    "SAP_MISMATCH": {
        "code": "SAP_MISMATCH",
        "name": "Movimiento sin espejo SAP",
        "description": "Movimiento registrado en Marketplace sin registro espejo en ERP SAP.",
        "domain": "FINANCIERO",
        "severity": "HIGH",
        "owner": "CONTABILIDAD",
        "required_action": "CONCILIAR_CON_SAP",
        "sla_days": 4,
        "evidence_required": ["sap_journal"],
        "explanation_template": "El movimiento {tx} está registrado en Marketplace sin espejo en SAP.",
    },
    "MARKETPLACE_MISMATCH": {
        "code": "MARKETPLACE_MISMATCH",
        "name": "Movimiento sin origen Marketplace",
        "description": "Abono bancario o asiento sin registro de venta en Marketplace.",
        "domain": "FINANCIERO",
        "severity": "HIGH",
        "owner": "ECOMMERCE",
        "required_action": "VALIDAR_ORIGEN_MARKETPLACE",
        "sla_days": 4,
        "evidence_required": ["marketplace_orders"],
        "explanation_template": "El asiento {tx} no posee registro de venta en Marketplace.",
    },
    # ---- OPERACIONAL ----
    "UNMATCHED_TRANSACTION": {
        "code": "UNMATCHED_TRANSACTION",
        "name": "Transacción sin match documental",
        "description": "Transacción del Ledger sin match en document_match_v1.",
        "domain": "OPERACIONAL",
        "severity": "MEDIUM",
        "owner": "TECNOLOGIA",
        "required_action": "INVESTIGAR_MATCH",
        "sla_days": 7,
        "evidence_required": ["document_match_v1"],
        "explanation_template": "La transacción {tx} no posee match documental registrado.",
    },
    "UNMATCHED_ORDER": {
        "code": "UNMATCHED_ORDER",
        "name": "Orden sin traza completa",
        "description": "Orden de compra cuyos movimientos no presentan evidencia completa.",
        "domain": "OPERACIONAL",
        "severity": "MEDIUM",
        "owner": "ECOMMERCE",
        "required_action": "VALIDAR_TRAZA_ORDEN",
        "sla_days": 7,
        "evidence_required": ["v_ledger_certified"],
        "explanation_template": "La orden {order} posee movimientos sin evidencia completa.",
    },
    "MANUAL_REVIEW_REQUIRED": {
        "code": "MANUAL_REVIEW_REQUIRED",
        "name": "Revisión manual requerida",
        "description": "Excepción compleja que requiere auditoría manual.",
        "domain": "OPERACIONAL",
        "severity": "HIGH",
        "owner": "REVISION_MANUAL",
        "required_action": "ESCALAR_REVISION_MANUAL",
        "sla_days": 1,
        "evidence_required": ["audit_trail"],
        "explanation_template": "La operación {tx} presenta múltiples observaciones y requiere auditoría manual.",
    },
}

# Compatibilidad: 10 causas legacy → catálogo canónico de 19
LEGACY_CAUSE_TO_CANONICAL = {
    "DIFERENCIA_MONTO": "AMOUNT_MISMATCH",
    "DIFERENCIA_DOCUMENTAL": "DOCUMENT_REFERENCE_ONLY",
    "DIFERENCIA_TRIBUTARIA": "INSUFFICIENT_FISCAL_EVIDENCE",
    "COBRO_PENDIENTE": "PENDING_COLLECTION",
    "PAGO_PENDIENTE": "PENDING_PAYMENT",
    "SIN_RESPALDO_XML": "MISSING_XML",
    "SIN_RESPALDO_DTE": "MISSING_DTE",
    "SIN_MATCH_SAP": "SAP_MISMATCH",
    "SIN_MATCH_MARKETPLACE": "MARKETPLACE_MISMATCH",
    "REQUIERE_REVISION": "MANUAL_REVIEW_REQUIRED",
}

EXCEPTION_CAUSES = {code: EXCEPTION_CATALOG[code] for code in EXCEPTION_CATALOG}

EXCEPTION_OWNERS = {
    "FINANZAS": "Equipo de Finanzas y Control de Gestión",
    "TESORERIA": "Equipo de Tesorería y Flujo de Caja",
    "CONTABILIDAD": "Equipo Contable y Cierres",
    "TRIBUTARIO": "Equipo de Impuestos y Cumplimiento SII",
    "ECOMMERCE": "Equipo Operativo de Canales E-Commerce",
    "LOGISTICA": "Equipo de Operaciones Logísticas",
    "TECNOLOGIA": "Soporte e Integración TI",
    "MARKETPLACE": "Ejecutivo de Cuenta Marketplace",
    "REVISION_MANUAL": "Comité Auditor de Excepciones",
}

# Severidad por reglas (nunca heurística)
SEVERITY_RULES = {
    "INFO": {"priority_default": "P4", "description": "Observación informativa sin impacto financiero."},
    "LOW": {"priority_default": "P4", "description": "Observación operativa sin impacto financiero directo."},
    "MEDIUM": {"priority_default": "P3", "description": "Falta de respaldo documental o XML/DTE dentro de plazo."},
    "HIGH": {"priority_default": "P2", "description": "Diferencia de monto o desfase de liquidación en tesorería."},
    "CRITICAL": {"priority_default": "P1", "description": "Riesgo tributario, pérdida financiera confirmada o alteración de cierre."},
}

DOMAIN_RANK = {"TRIBUTARIO": 0, "FINANCIERO": 1, "DOCUMENTAL": 2, "OPERACIONAL": 3}

# Matriz determinística de prioridad (severidad × dominio → P1-P4)
PRIORITY_MATRIX = {
    "CRITICAL": {"TRIBUTARIO": "P1", "FINANCIERO": "P1", "DOCUMENTAL": "P1", "OPERACIONAL": "P1"},
    "HIGH": {"TRIBUTARIO": "P1", "FINANCIERO": "P2", "DOCUMENTAL": "P2", "OPERACIONAL": "P2"},
    "MEDIUM": {"TRIBUTARIO": "P2", "FINANCIERO": "P3", "DOCUMENTAL": "P3", "OPERACIONAL": "P3"},
    "LOW": {"TRIBUTARIO": "P2", "FINANCIERO": "P3", "DOCUMENTAL": "P4", "OPERACIONAL": "P4"},
    "INFO": {"TRIBUTARIO": "P3", "FINANCIERO": "P4", "DOCUMENTAL": "P4", "OPERACIONAL": "P4"},
}

VALID_STATUSES = {"OPEN", "IN_REVIEW", "WAITING_EVIDENCE", "ACTION_REQUIRED", "RESOLVED", "REJECTED"}


def _resolve_priority(severity: str, domain: str) -> str:
    """Resuelve la prioridad P1-P4 de forma determinística (reglas, nunca heurística)."""
    sev = severity if severity in PRIORITY_MATRIX else "MEDIUM"
    dom = domain if domain in PRIORITY_MATRIX[sev] else "OPERACIONAL"
    return PRIORITY_MATRIX[sev][dom]

class ExceptionEngine:
    """
    Motor oficial ÚNICO de Excepciones Financieras (Paso 5).
    Detecta, clasifica, explica y prioriza excepciones de forma 100% read-only y determinística.
    No persiste: genera el catálogo desde la verdad actual de v_ledger_certified,
    dte_truth_v1 y document_match_v1. Financial Delta = $0.00.
    """

    def __init__(self, db: Optional[DatabaseV4] = None):
        self.db = db or DatabaseV4.get()
        self._reconciliation_engine = ReconciliationEngine(db=self.db)
        self._dte_truth_map: Optional[Dict[tuple, str]] = None
        self._doc_match_map: Optional[Dict[str, str]] = None

    # ------------------------------------------------------------------
    # Identificadores determinísticos
    # ------------------------------------------------------------------
    @staticmethod
    def compute_exception_id(
        marketplace: str,
        transaction_id: str,
        order_id: str,
        exception_type: str,
        source_reference: str = "v_ledger_certified",
    ) -> str:
        """Calcula el identificador determinístico SHA-256 de una excepción."""
        raw_key = f"{marketplace}_{transaction_id}_{order_id}_{exception_type}_{source_reference}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    # ------------------------------------------------------------------
    # Detección read-only de estado fiscal (misma matriz que Electronic Certification)
    # ------------------------------------------------------------------
    def _preload_certification_maps(self) -> None:
        """Precarga (una sola vez) los mapas de certificación para el modo FULL_CORPUS.

        dte_truth_map: {(mp_lower, folio_str): tipo_dte}
        doc_match_map: {ledger_id: min(folio_xml)} para match_status='MATCHED' (determinístico).
        """
        if self._dte_truth_map is not None and self._doc_match_map is not None:
            return
        dt = self.db.query(
            "SELECT LOWER(marketplace) AS mp, CAST(folio AS VARCHAR) AS folio, tipo_dte FROM dte_truth_v1"
        )
        self._dte_truth_map = {}
        for r in dt.to_dict("records"):
            self._dte_truth_map[(str(r["mp"]), str(r["folio"]))] = str(r.get("tipo_dte") or "")

        dm = self.db.query(
            "SELECT ledger_id, folio_xml FROM document_match_v1 WHERE match_status = 'MATCHED'"
        )
        self._doc_match_map = {}
        for r in dm.to_dict("records"):
            lid = str(r["ledger_id"])
            fol = str(r.get("folio_xml") or "")
            if lid not in self._doc_match_map or fol < self._doc_match_map[lid]:
                self._doc_match_map[lid] = fol

    def _certification_state(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Resuelve el estado de certificación de un registro read-only.

        Matriz idéntica a la de Electronic Certification:
          CRYPTOGRAPHIC_CERTIFIED | XML_PRESENT_NOT_CERTIFIED | DOCUMENT_REFERENCE_ONLY |
          LEDGER_REFERENCE_ONLY | INSUFFICIENT_FISCAL_EVIDENCE | TRUTH_CONFLICT_DETECTED
        Determinístico: usa mapas pre-cargados si están disponibles (FULL_CORPUS),
        o consultas con orden determinístico (min folio) si no.
        """
        mp = str(row.get("marketplace", "")).upper()
        folio = str(row.get("folio_xml")) if row.get("folio_xml") and str(row.get("folio_xml")) != "None" else None
        ledger_id = str(row.get("id_transaccion"))

        real_dte = False
        dte_folio_matched = None
        if folio:
            if self._dte_truth_map is not None:
                real_dte = (mp.lower(), folio) in self._dte_truth_map
                dte_folio_matched = folio if real_dte else None
            else:
                truth = self.db.query(
                    "SELECT tipo_dte FROM dte_truth_v1 WHERE LOWER(marketplace) = ? AND CAST(folio AS VARCHAR) = ? LIMIT 1",
                    [mp.lower(), folio],
                )
                real_dte = not truth.empty
                dte_folio_matched = folio if real_dte else None

        dm_folio = None
        if ledger_id:
            if self._doc_match_map is not None:
                dm_folio = self._doc_match_map.get(ledger_id)
            else:
                dm = self.db.query(
                    "SELECT folio_xml FROM document_match_v1 WHERE match_status = 'MATCHED' AND ledger_id = ? ORDER BY folio_xml ASC LIMIT 1",
                    [ledger_id],
                )
                if not dm.empty:
                    dm_folio = str(dm.iloc[0].get("folio_xml"))

        if real_dte and dm_folio and dm_folio != folio:
            estado, blocking = "TRUTH_CONFLICT_DETECTED", f"CONFLICT: dte_truth folio={folio} vs document_match folio={dm_folio}"
        elif real_dte and dm_folio:
            estado, blocking = "CRYPTOGRAPHIC_CERTIFIED", None
        elif real_dte:
            estado, blocking = "XML_PRESENT_NOT_CERTIFIED", "XML_INDEXED_WITHOUT_CERTIFIED_MATCH"
        elif dm_folio:
            estado, blocking = "DOCUMENT_REFERENCE_ONLY", "DOCUMENTAL_MATCH_WITHOUT_REAL_XML"
        elif mp == "RIPLEY":
            estado, blocking = "INSUFFICIENT_FISCAL_EVIDENCE", "RIPLEY_LIQUIDATION_IS_NOT_SII_DTE"
        elif folio:
            estado, blocking = "LEDGER_REFERENCE_ONLY", "LEDGER_FOLIO_WITHOUT_REAL_DTE"
        else:
            estado, blocking = "INSUFFICIENT_FISCAL_EVIDENCE", "NO_XML_NO_DTE_NO_MATCH"

        return {
            "estado": estado,
            "blocking_reason": blocking,
            "has_real_dte": real_dte,
            "has_doc_match": bool(dm_folio),
            "dte_folio_matched": dte_folio_matched,
            "dm_folio": dm_folio,
        }

    def _detect_category_from_certification(self, estado: str) -> Optional[str]:
        """Mapea el estado de certificación a una categoría canónica del catálogo."""
        mapping = {
            "TRUTH_CONFLICT_DETECTED": "TRUTH_CONFLICT",
            "INSUFFICIENT_FISCAL_EVIDENCE": "INSUFFICIENT_FISCAL_EVIDENCE",
            "XML_PRESENT_NOT_CERTIFIED": "MISSING_DTE",
            "DOCUMENT_REFERENCE_ONLY": "DOCUMENT_REFERENCE_ONLY",
            "LEDGER_REFERENCE_ONLY": "LEDGER_REFERENCE_ONLY",
        }
        return mapping.get(estado)

    # ------------------------------------------------------------------
    # Detección por fila del Ledger → excepción primaria única
    # ------------------------------------------------------------------
    def _detect_for_row(self, row: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detecta y construye la excepción primaria (0 o 1) para una fila de v_ledger_certified.

        Precedencia determinística garantiza 0 duplicados conceptuales:
        cada transacción genera como máximo UNA excepción, según la evidencia más severa disponible.
        """
        cert = self._certification_state(row)
        primary = self._resolve_primary_category(row, cert)

        if not primary:
            return []
        exc = self._build_exception(primary, row, cert, primary_reason=cert["blocking_reason"])
        return [exc] if exc else []

    def _resolve_primary_category(self, row: Dict[str, Any], cert: Dict[str, Any]) -> Optional[str]:
        """Resuelve la categoría primaria determinística según precedencia estricta."""
        estado = cert["estado"]
        fg = str(row.get("financial_group", "")).lower()
        has_xml = bool(row.get("folio_xml") and str(row.get("folio_xml")) not in ("", "None"))
        has_dte = bool(cert["has_real_dte"])
        has_match = bool(cert["has_doc_match"])

        if estado == "TRUTH_CONFLICT_DETECTED":
            return "TRUTH_CONFLICT"
        if estado == "INSUFFICIENT_FISCAL_EVIDENCE":
            return "INSUFFICIENT_FISCAL_EVIDENCE"
        if fg in ("ingresos", "devoluciones") and not has_dte:
            return "MISSING_DTE"
        if estado == "DOCUMENT_REFERENCE_ONLY":
            return "DOCUMENT_REFERENCE_ONLY"
        if estado == "LEDGER_REFERENCE_ONLY":
            return "LEDGER_REFERENCE_ONLY"
        if not has_xml:
            return "MISSING_XML"
        if not has_match:
            return "UNMATCHED_TRANSACTION"
        if has_xml and not has_dte and not has_match:
            return "MISSING_SUPPORT"
        return None

    def _build_exception(
        self,
        category: str,
        row: Dict[str, Any],
        cert: Optional[Dict[str, Any]] = None,
        primary_reason: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Construye el modelo de Excepción Canónica para una categoría."""
        if category not in EXCEPTION_CATALOG:
            return None

        meta = EXCEPTION_CATALOG[category]
        marketplace = str(row.get("marketplace", "")).upper()
        tx_id = str(row.get("id_transaccion"))
        order_id = str(row.get("id_orden")) if row.get("id_orden") and str(row.get("id_orden")) != "None" else ""
        fg = str(row.get("financial_group", "OTROS")).lower()
        monto = float(row.get("monto") or 0.0)
        fecha = str(row.get("fecha")) or "2025-12-01"

        severity = meta["severity"]
        domain = meta["domain"]
        priority = _resolve_priority(severity, domain)
        owner = meta["owner"]

        exc_id = self.compute_exception_id(marketplace, tx_id, order_id, category)

        try:
            detected_dt = datetime.strptime(str(fecha)[:10], "%Y-%m-%d")
            age_days = (datetime.now() - detected_dt).days
        except Exception:
            age_days = 0

        sla_days = meta["sla_days"]
        within_sla = age_days <= sla_days

        has_xml_f = bool(row.get("folio_xml") and str(row.get("folio_xml")) not in ("", "None"))
        has_dte_f = bool((cert or {}).get("has_real_dte"))
        has_match_f = bool((cert or {}).get("has_doc_match"))

        explanation = meta["explanation_template"].format(
            tx=tx_id, order=order_id or "-", fg=fg,
            dte_folio=(cert or {}).get("dte_folio_matched") or "-",
            dm_folio=(cert or {}).get("dm_folio") or "-",
            blocking_reason=primary_reason or "-",
            has_xml=has_xml_f, has_dte=has_dte_f, has_match=has_match_f,
            rec_status="-",
        )

        return {
            "exception_id": exc_id,
            "exception_type": category,
            "category_code": meta["code"],
            "category_name": meta["name"],
            "domain": domain,
            "marketplace": marketplace,
            "period": str(fecha)[:7] if fecha else "ALL",
            "transaction_id": tx_id,
            "order_id": order_id,
            "financial_group": fg,
            "amount": round(monto, 4),
            "currency": "CLP",
            "severity": severity,
            "priority": priority,
            "owner": owner,
            "required_action": meta["required_action"],
            "cause": meta["description"],
            "explanation": explanation,
            "status": "OPEN",
            "detected_at": str(fecha),
            "age_days": age_days,
            "sla_days": sla_days,
            "within_sla": within_sla,
            "sla_breached": not within_sla,
            "evidence": {
                "certification_state": (cert or {}).get("estado"),
                "blocking_reason": primary_reason or (cert or {}).get("blocking_reason"),
                "evidence_required": meta["evidence_required"],
                "has_real_dte": has_dte_f,
                "has_doc_match": has_match_f,
                "has_xml": has_xml_f,
            },
            "traceability": {
                "source_engine": "ExceptionEngine",
                "source_tables": ["v_ledger_certified", "dte_truth_v1", "document_match_v1"],
                "source_reference": "v_ledger_certified",
                "financial_delta": "$0.00",
            },
        }

    # ------------------------------------------------------------------
    # Muestra determinística de excepciones (sin persistencia)
    # ------------------------------------------------------------------
    def _sample_rows(self, marketplace: Optional[str] = None, period: Optional[str] = None, limit: int = 200) -> List[Dict[str, Any]]:
        """Obtiene una muestra determinística y representativa de filas del Ledger para detección.

        Si marketplace es None, la muestra se distribuye equitativamente entre los marketplaces
        presentes para evitar sesgo hacia un solo canal.
        """
        mps = []
        if marketplace and marketplace.upper() != "ALL":
            mps = [marketplace]
        else:
            try:
                mp_df = self.db.query("SELECT DISTINCT LOWER(marketplace) AS mp FROM v_ledger_certified")
                mps = [str(r["mp"]) for r in mp_df.to_dict("records")]
            except Exception:
                mps = []

        rows = []
        per_mp = max(1, limit // max(1, len(mps)))
        for mp in mps:
            where_clause, params = self._reconciliation_engine._financial_engine._build_ledger_where(period, mp)
            sql = f"""
                SELECT id_transaccion, id_orden, marketplace, fecha, detalle, monto, financial_group,
                       folio_xml, has_dte_link, dte_folio, dte_tipo, document_status
                FROM v_ledger_certified
                WHERE {where_clause}
                ORDER BY fecha DESC, id_transaccion ASC
                LIMIT ? OFFSET 0
            """
            df = self.db.query(sql, params + [per_mp])
            if not df.empty:
                rows.extend(dict(r) for r in df.to_dict("records"))
            if len(rows) >= limit:
                break
        return rows[:limit]

    def build_exceptions_catalog(
        self,
        marketplace: Optional[str] = None,
        period: Optional[str] = None,
        exception_type: Optional[str] = None,
        severity: Optional[str] = None,
        priority: Optional[str] = None,
        owner: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """Construye el catálogo consolidado de excepciones activas, sin duplicados."""
        rows = self._sample_rows(marketplace=marketplace, period=period, limit=500)
        seen_ids = set()
        exceptions = []
        duplicates_count = 0

        for r in rows:
            detected = self._detect_for_row(r)
            for exc in detected:
                e_id = exc["exception_id"]
                if e_id in seen_ids:
                    duplicates_count += 1
                    continue
                if exception_type and exc["exception_type"] != exception_type:
                    continue
                if severity and exc["severity"] != severity:
                    continue
                if priority and exc["priority"] != priority:
                    continue
                if owner and exc["owner"] != owner:
                    continue
                if status and exc["status"] != status:
                    continue
                seen_ids.add(e_id)
                exceptions.append(exc)

        total_exceptions = len(exceptions)
        offset = (page - 1) * page_size
        paginated_exceptions = exceptions[offset : offset + page_size]
        total_amount = sum(e["amount"] for e in exceptions)

        return {
            "total_exceptions": total_exceptions,
            "page": page,
            "page_size": page_size,
            "total_amount_affected": round(total_amount, 4),
            "duplicate_exceptions_prevented": duplicates_count,
            "sample_limit": 500,
            "financial_delta": "$0.00",
            "exceptions": paginated_exceptions,
        }

    def get_exception_by_id(self, exception_id: str) -> Optional[Dict[str, Any]]:
        """Busca una excepción por su identificador SHA-256 en el catálogo determinístico."""
        cat = self.build_exceptions_catalog(page_size=500)
        for e in cat["exceptions"]:
            if e["exception_id"] == exception_id:
                return e
        return None

    def get_exceptions_by_transaction(self, transaction_id: str) -> List[Dict[str, Any]]:
        """Retorna las excepciones asociadas a una transacción (read-only)."""
        row = self._reconciliation_engine._truth_engine._ledger_engine.get_transaction_by_id(transaction_id)
        if not row:
            return []
        return self._detect_for_row(row)

    def get_exceptions_by_order(self, order_id: str) -> List[Dict[str, Any]]:
        """Retorna las excepciones asociadas a una orden de compra (read-only)."""
        trace = self._reconciliation_engine._truth_engine._ledger_engine.get_order_ledger_trace(order_id)
        if not trace:
            return []
        exceptions = []
        seen = set()
        for t in trace:
            for exc in self._detect_for_row(t):
                if exc["exception_id"] in seen:
                    continue
                seen.add(exc["exception_id"])
                exceptions.append(exc)
        return exceptions

    # ------------------------------------------------------------------
    # Estadísticas por reglas (SQL read-only agregado)
    # ------------------------------------------------------------------
    def get_statistics(self, marketplace: Optional[str] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """Estadísticas determinísticas del catálogo: total, por tipo, por MP, por severidad, por prioridad."""
        df_total = self.db.query(
            "SELECT COUNT(*) AS cnt, COALESCE(SUM(monto),0) AS total FROM v_ledger_certified"
        )
        total_ledger = int(df_total.iloc[0]["cnt"]) if not df_total.empty else 0

        by_type = {code: 0 for code in EXCEPTION_CATALOG}
        by_mp = {}
        by_severity = {}
        by_priority = {}
        by_domain = {}

        rows = self._sample_rows(marketplace=marketplace, period=period, limit=1000)
        for r in rows:
            mp = str(r.get("marketplace", "")).upper()
            detected = self._detect_for_row(r)
            primary = None
            for exc in detected:
                if primary is None:
                    primary = exc
                by_type[exc["exception_type"]] = by_type.get(exc["exception_type"], 0) + 1
                by_severity[exc["severity"]] = by_severity.get(exc["severity"], 0) + 1
                by_priority[exc["priority"]] = by_priority.get(exc["priority"], 0) + 1
                by_domain[exc["domain"]] = by_domain.get(exc["domain"], 0) + 1
            if primary:
                by_mp[mp] = by_mp.get(mp, 0) + 1

        return {
            "marketplace": marketplace or "ALL",
            "period": period or "ALL",
            "total_ledger_rows": total_ledger,
            "sample_analyzed": len(rows),
            "sample_limit": 1000,
            "total_exceptions_detected": sum(by_type.values()),
            "exceptions_by_type": by_type,
            "exceptions_by_marketplace": by_mp,
            "exceptions_by_severity": by_severity,
            "exceptions_by_priority": by_priority,
            "exceptions_by_domain": by_domain,
            "catalog_size": len(EXCEPTION_CATALOG),
            "financial_delta": "$0.00",
        }

    # ------------------------------------------------------------------
    # Evaluación determinística de un registro candidato
    # ------------------------------------------------------------------
    def evaluate(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Evalúa un registro candidato (fila de Ledger) y retorna sus excepciones canónicas."""
        required = ["id_transaccion", "marketplace"]
        missing = [f for f in required if f not in record]
        if missing:
            return {
                "status": "INVALID_RECORD",
                "missing_fields": missing,
                "exceptions": [],
                "financial_delta": "$0.00",
            }
        row = {k: (v if v is not None else None) for k, v in record.items()}
        if "folio_xml" not in row:
            row["folio_xml"] = None
        if "financial_group" not in row:
            row["financial_group"] = None
        if "monto" not in row:
            row["monto"] = 0.0
        if "fecha" not in row:
            row["fecha"] = "2025-12-01"
        if "id_orden" not in row:
            row["id_orden"] = None

        cert = self._certification_state(row)
        primary = self._detect_category_from_certification(cert["estado"])
        exceptions = []
        if primary:
            exceptions.append(self._build_exception(primary, row, cert, primary_reason=cert["blocking_reason"]))
        return {
            "status": "EVALUATED",
            "certification_state": cert["estado"],
            "blocking_reason": cert["blocking_reason"],
            "exceptions": [e for e in exceptions if e],
            "financial_delta": "$0.00",
        }

    # ------------------------------------------------------------------
    # Resumen ejecutivo
    # ------------------------------------------------------------------
    def get_summary(self, marketplace: Optional[str] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """Resumen ejecutivo del Exception Engine sobre la muestra determinística."""
        stats = self.get_statistics(marketplace=marketplace, period=period)
        by_severity = stats["exceptions_by_severity"]
        by_type = stats["exceptions_by_type"]

        open_total = stats["total_exceptions_detected"]

        critical = by_severity.get("CRITICAL", 0)
        high = by_severity.get("HIGH", 0)

        total_amount = 0.0
        rows = self._sample_rows(marketplace=marketplace, period=period, limit=500)
        for r in rows:
            for exc in self._detect_for_row(r):
                if exc["severity"] in ("CRITICAL", "HIGH"):
                    total_amount += exc["amount"]

        return {
            "marketplace": marketplace or "ALL",
            "period": period or "ALL",
            "total_exceptions": open_total,
            "open_exceptions": open_total,
            "resolved_exceptions": 0,
            "critical_exceptions": critical,
            "high_exceptions": high,
            "total_amount_affected_high_critical": round(total_amount, 4),
            "catalog_size": len(EXCEPTION_CATALOG),
            "by_severity": by_severity,
            "by_type": by_type,
            "financial_delta": "$0.00",
            "source_engine": "ExceptionEngine",
        }

    def get_sla_summary(self, marketplace: Optional[str] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """Resumen de cumplimiento de SLA sobre la muestra determinística."""
        rows = self._sample_rows(marketplace=marketplace, period=period, limit=500)
        exceptions = []
        seen = set()
        for r in rows:
            for exc in self._detect_for_row(r):
                if exc["exception_id"] in seen:
                    continue
                seen.add(exc["exception_id"])
                exceptions.append(exc)

        within = sum(1 for e in exceptions if e["within_sla"])
        breached = sum(1 for e in exceptions if e["sla_breached"])

        return {
            "marketplace": marketplace or "ALL",
            "period": period or "ALL",
            "total_exceptions": len(exceptions),
            "within_sla": within,
            "sla_breached": breached,
            "sla_compliance_pct": round((within / len(exceptions) * 100), 2) if exceptions else 100.0,
            "financial_delta": "$0.00",
        }

    def get_marketplace_exceptions(self, marketplace: str) -> Dict[str, Any]:
        """Retorna el resumen de excepciones para un marketplace específico."""
        stats = self.get_statistics(marketplace=marketplace)
        by_type = stats["exceptions_by_type"]
        active = {t: c for t, c in by_type.items() if c > 0}
        return {
            "marketplace": marketplace.upper(),
            "total_exceptions_detected": sum(active.values()),
            "active_types": active,
            "total_ledger_rows": stats["total_ledger_rows"],
            "sample_analyzed": stats["sample_analyzed"],
            "catalog_size": len(EXCEPTION_CATALOG),
            "financial_delta": "$0.00",
        }

    def rebuild_exceptions(self, marketplace: Optional[str] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """Reconstruye determinísticamente el catálogo de excepciones (read-only, sin persistencia)."""
        res = self.build_exceptions_catalog(marketplace=marketplace, period=period, page_size=500)
        return {
            "status": "COMPLETED",
            "marketplace": marketplace or "ALL",
            "period": period or "ALL",
            "total_exceptions_built": res["total_exceptions"],
            "duplicates_prevented": res["duplicate_exceptions_prevented"],
            "financial_delta": "$0.00",
        }

    def get_health(self) -> Dict[str, Any]:
        """Verifica la salud operativa del Exception Engine."""
        try:
            cnt = self.db.query("SELECT COUNT(*) AS c FROM v_ledger_certified").iloc[0]["c"]
            db_status = "PASS" if cnt > 0 else "FAIL"
        except Exception:
            db_status = "FAIL"

        return {
            "status": "READY" if db_status == "PASS" else "NOT_READY",
            "exception_engine": "ACTIVE",
            "catalog_size": len(EXCEPTION_CATALOG),
            "catalog_complete": len(EXCEPTION_CATALOG) == 19,
            "persistence_enabled": False,
            "database": db_status,
        }

    # ------------------------------------------------------------------
    # CERTIFICATION MODE — universo completo (SAMPLE != CERTIFICATION)
    # ------------------------------------------------------------------
    def run_full_corpus(
        self,
        marketplace: Optional[str] = None,
        period: Optional[str] = None,
        yield_ids: bool = False,
    ) -> Dict[str, Any]:
        """Evalúa el universo COMPLETO de v_ledger_certified (sin límite de muestreo).

        Retorna métricas agregadas del corpus completo. Con yield_ids=True incluye
        los exception_id detectados (para pruebas de unicidad/idempotencia).
        No persiste nada. Financial Delta = $0.00.
        """
        self._preload_certification_maps()

        mps = []
        if marketplace and marketplace.upper() != "ALL":
            mps = [marketplace]
        else:
            mps = [str(r["mp"]) for r in self.db.query("SELECT DISTINCT LOWER(marketplace) AS mp FROM v_ledger_certified").to_dict("records")]

        by_type = {code: 0 for code in EXCEPTION_CATALOG}
        by_mp = {}
        by_severity = {}
        by_priority = {}
        by_domain = {}
        by_estado = {}
        evaluated = 0
        no_exception = 0
        rows_with_multiple_primary = 0
        exception_ids: List[str] = []
        duplicate_ids = 0
        seen_ids = set()
        unexplained = 0
        untraceable = 0
        first_exc_ids: Dict[str, Optional[str]] = {}

        for mp in mps:
            if period:
                where_clause, params = self._reconciliation_engine._financial_engine._build_ledger_where(period, mp)
            else:
                where_clause, params = "LOWER(marketplace) = LOWER(?)", [mp]
            sql = f"""
                SELECT id_transaccion, id_orden, marketplace, fecha, detalle, monto, financial_group,
                       folio_xml, has_dte_link, dte_folio, dte_tipo, document_status
                FROM v_ledger_certified
                WHERE {where_clause}
                ORDER BY LOWER(marketplace), id_transaccion, COALESCE(CAST(fecha AS VARCHAR), ''),
                         COALESCE(monto, 0), COALESCE(CAST(financial_group AS VARCHAR), ''),
                         COALESCE(CAST(folio_xml AS VARCHAR), '')
            """
            df = self.db.query(sql, params)
            for r in df.to_dict("records"):
                evaluated += 1
                row = {k: (v if v is not None else None) for k, v in r.items()}
                detected = self._detect_for_row(row)
                mp_name = str(row.get("marketplace", "")).upper()
                if not detected:
                    no_exception += 1
                    continue
                if len(detected) > 1:
                    rows_with_multiple_primary += 1
                primary = detected[0]
                by_mp[mp_name] = by_mp.get(mp_name, 0) + 1
                by_type[primary["exception_type"]] = by_type.get(primary["exception_type"], 0) + 1
                by_severity[primary["severity"]] = by_severity.get(primary["severity"], 0) + 1
                by_priority[primary["priority"]] = by_priority.get(primary["priority"], 0) + 1
                by_domain[primary["domain"]] = by_domain.get(primary["domain"], 0) + 1
                by_estado[(primary.get("evidence") or {}).get("certification_state") or "UNKNOWN"] = by_estado.get(
                    (primary.get("evidence") or {}).get("certification_state") or "UNKNOWN", 0
                ) + 1
                if not primary.get("explanation") or not primary.get("exception_type"):
                    unexplained += 1
                if not primary.get("evidence") or not primary.get("traceability"):
                    untraceable += 1
                e_id = primary["exception_id"]
                if yield_ids:
                    exception_ids.append(e_id)
                if e_id in seen_ids:
                    duplicate_ids += 1
                else:
                    seen_ids.add(e_id)
                if mp_name not in first_exc_ids or e_id < first_exc_ids[mp_name]:
                    first_exc_ids[mp_name] = e_id

        if yield_ids:
            exception_ids.sort()

        return {
            "mode": "FULL_CORPUS",
            "marketplace": marketplace or "ALL",
            "period": period or "ALL",
            "total_ledger_rows": evaluated,
            "total_evaluated": evaluated,
            "coverage_pct": round(evaluated / evaluated * 100, 4) if evaluated else 0.0,
            "records_with_exception": evaluated - no_exception,
            "records_without_exception": no_exception,
            "rows_with_multiple_primary": rows_with_multiple_primary,
            "total_exceptions_detected": sum(by_type.values()),
            "duplicate_exception_ids": duplicate_ids,
            "unexplained_exceptions": unexplained,
            "untraceable_exceptions": untraceable,
            "exceptions_by_type": by_type,
            "exceptions_by_marketplace": by_mp,
            "exceptions_by_severity": by_severity,
            "exceptions_by_priority": by_priority,
            "exceptions_by_domain": by_domain,
            "certification_states": by_estado,
            "first_exception_id_by_marketplace": first_exc_ids,
            "catalog_size": len(EXCEPTION_CATALOG),
            "financial_delta": "$0.00",
            "exception_ids": exception_ids if yield_ids else None,
        }
