"""DTE-Ledger Matching Engine — links real SII DTE XML documents to ledger transactions.

Pure read model: consumes `dte_truth_v1`, `document_match_v1`, `dte_link_v1`,
`ripley_settlement_chain` and `marketplace_ledger_v1`, and produces a certified
match table `dte_certified_match_v1` plus rebuilds the `dte_ledger_link` view
(which is a VIEW joining ledger -> dte_truth on exact folio equality).

Root cause addressed: `dte_ledger_link` dte_linked was always 0 because the
naive view join (folio_xml = d.folio, exact string) never matches:
- ML folio_xml uses `033-XXXXXXXX` format vs numeric dte_truth folios
- PARIS ledger folio_xml stores the DTE monto_total (not the SII folio)
- FALABELLA ledger has NO folio_xml at all
- RIPLEY folio namespaces are incompatible

Strategies (per marketplace):
- ML        = DIRECT_MATCH         (folio normalization + amount tolerance)
- PARIS     = DOCUMENT_CHAIN       (document_match_v1 SII folio chain)
- FALABELLA = TRANSACTION_CHAIN    (UUID -> IdArticulo -> dte_link_v1 -> folio)
- RIPLEY    = SETTLEMENT_CHAIN_V2  (structurally blocked when source files absent
                                    or folio namespaces incompatible)

The engine NEVER modifies ledger financial data. It only writes the certified
match table and rebuilds the read-model view.
"""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any

import pandas as pd

from engine.v4.database import DatabaseV4

logger = logging.getLogger("meli.dte_ledger_matcher")

# Tolerance in CLP for amount reconciliation.
AMOUNT_TOLERANCE_CLP = 1.0

# Statuses that authorize dte_linked=1.
CERTIFIED_STATUSES = ("MATCHED_CERTIFIED", "MATCHED_WITH_TOLERANCE")

# Source view definition currently installed in the DB.
LEGACY_VIEW_SQL = (
    "CREATE VIEW dte_ledger_link AS "
    "SELECT l.marketplace, l.id_transaccion, l.folio_xml, "
    "l.fecha AS ledger_fecha, l.monto AS ledger_monto, l.tipo_movimiento, l.detalle, "
    "l.financial_group, d.folio AS dte_folio, d.monto_total AS dte_monto, "
    "d.fecha_emision AS dte_fecha, d.emisor_nombre, d.emisor_rut, d.tipo_dte, "
    "CASE WHEN (d.folio IS NOT NULL) THEN (1) ELSE 0 END AS dte_linked "
    "FROM marketplace_ledger_v1 AS l "
    "LEFT JOIN dte_truth_v1 AS d ON ((l.folio_xml = d.folio) AND (l.marketplace = d.marketplace)) "
    "WHERE ((l.folio_xml IS NOT NULL) AND (l.folio_xml != ''))"
)


class DTELedgerMatcher:
    """Certifies DTE->Ledger links per marketplace using chain-based strategies."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()
        self.execution_id = str(uuid.uuid4())
        self.results: dict[str, Any] = {}

    # ------------------------------------------------------------------ utils
    @staticmethod
    def _norm_ml_folio(folio_xml: Any) -> str | None:
        """Normalize ML folio_xml '033-0010723408' -> '10723408'."""
        if folio_xml is None:
            return None
        s = str(folio_xml).strip()
        if not s or s.lower() in ("none", "nan", "aún no disponible", "ain no disponible"):
            return None
        if "-" in s:
            s = s.split("-")[-1]
        s = s.strip().lstrip("0")
        if not s or not s.isdigit():
            return None
        return s

    @staticmethod
    def _norm_folio(folio: Any) -> str | None:
        if folio is None:
            return None
        s = str(folio).strip()
        if not s or s.lower() in ("none", "nan"):
            return None
        return s

    # ------------------------------------------------------------------ ML
    def _match_ml_direct(self) -> pd.DataFrame:
        """DIRECT_MATCH: normalize folio, aggregate non-sale rows per folio,
        compare ABS(sum) vs dte_truth.monto_total within tolerance."""
        sql = """
            SELECT l.folio_xml, c.monto, c.tipo_movimiento
            FROM marketplace_ledger_clasificado_v1 c
            JOIN marketplace_ledger_v1 l ON c.id_transaccion = l.id_transaccion
            WHERE c.marketplace='ML'
              AND l.folio_xml IS NOT NULL AND l.folio_xml != ''
        """
        ledger = self.db.query(sql)
        if ledger.empty:
            return pd.DataFrame()

        ledger["folio"] = ledger["folio_xml"].apply(self._norm_ml_folio)
        ledger = ledger[ledger["folio"].notnull()]

        # Aggregate NON-SALE rows (exclude sales/refunds/payments) per folio.
        nonsale = ledger[~ledger["tipo_movimiento"].isin(
            ["INGRESO_VENTA", "DEVOLUCION", "PAGO"])]
        agg = nonsale.groupby("folio")["monto"].sum().abs().reset_index()
        agg.columns = ["folio", "ledger_amount"]

        dte = self.db.query(
            "SELECT folio, monto_total, monto_neto, monto_iva, fecha_emision, "
            "emisor_rut, emisor_nombre, tipo_dte FROM dte_truth_v1 WHERE marketplace='ML'"
        )
        dte["folio"] = dte["folio"].astype(str).str.lstrip("0")

        merged = agg.merge(dte, on="folio", how="inner")
        if merged.empty:
            return merged

        delta = (merged["ledger_amount"] - merged["monto_total"]).abs()
        merged["delta"] = delta
        merged["match_status"] = merged["delta"].apply(
            lambda d: "MATCHED_CERTIFIED" if d <= AMOUNT_TOLERANCE_CLP else "AMOUNT_MISMATCH"
        )
        merged["match_rule"] = "DIRECT_MATCH"
        merged["match_source"] = "dte_ledger_matcher"
        merged["tipo_dte"] = merged["tipo_dte"].astype(str)
        return merged

    # ------------------------------------------------------------------ PARIS
    def _match_paris_document_chain(self) -> pd.DataFrame:
        """DOCUMENT_CHAIN: use document_match_v1 MATCHED ledger_ids whose SII
        folio exists in dte_truth_v1."""
        sql = """
            SELECT DISTINCT dm.ledger_id, dm.folio_xml,
                   t.monto_total, t.monto_neto, t.monto_iva, t.fecha_emision,
                   t.emisor_rut, t.emisor_nombre, t.tipo_dte
            FROM document_match_v1 dm
            JOIN dte_truth_v1 t
              ON t.marketplace = 'PARIS'
             AND CAST(t.folio AS VARCHAR) = CAST(dm.folio_xml AS VARCHAR)
            WHERE dm.marketplace = 'PARIS'
              AND dm.match_status = 'MATCHED'
        """
        df = self.db.query(sql)
        if df.empty:
            return df
        df = df.rename(columns={"ledger_id": "id_transaccion"})
        df["match_rule"] = "DOCUMENT_CHAIN"
        df["match_source"] = "dte_ledger_matcher"
        df["match_status"] = "MATCHED_CERTIFIED"
        df["delta"] = 0.0
        return df

    # ------------------------------------------------------------------ FALABELLA
    def _match_falabella_transaction_chain(self, bridge: pd.DataFrame) -> pd.DataFrame:
        """TRANSACTION_CHAIN: ledger UUID -> (bridge) -> IdArticulo -> dte_link_v1 -> folio -> dte_truth."""
        if bridge is None or bridge.empty:
            return pd.DataFrame()

        ledger = self.db.query(
            "SELECT DISTINCT id_transaccion FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'"
        )
        if ledger.empty:
            return pd.DataFrame()
        led_uuids = set(ledger["id_transaccion"].astype(str))

        link = self.db.query(
            "SELECT id_transaccion, folio FROM dte_link_v1 WHERE marketplace='FALABELLA'"
        )
        if link.empty:
            return pd.DataFrame()
        link_map = dict(
            zip(link["id_transaccion"].astype(str), link["folio"].astype(str))
        )

        bridge_sub = bridge[bridge["uuid"].isin(led_uuids)].copy()
        if bridge_sub.empty:
            return pd.DataFrame()
        bridge_sub["folio"] = bridge_sub["id_art"].map(link_map)
        bridge_sub = bridge_sub.dropna(subset=["folio"]).drop_duplicates(subset=["uuid"])

        if bridge_sub.empty:
            return pd.DataFrame()

        truth = self.db.query(
            "SELECT folio, monto_total, monto_neto, monto_iva, fecha_emision, "
            "emisor_rut, emisor_nombre, tipo_dte FROM dte_truth_v1 WHERE marketplace='FALABELLA'"
        )
        truth_map = {str(r.folio): r for _, r in truth.iterrows()}

        rows = []
        for _, r in bridge_sub.iterrows():
            tr = truth_map.get(r["folio"])
            if tr is None:
                continue
            rows.append({
                "id_transaccion": r["uuid"],
                "folio_xml": r["folio"],
                "monto_total": float(tr["monto_total"]),
                "monto_neto": float(tr["monto_neto"]),
                "monto_iva": float(tr["monto_iva"]),
                "fecha_emision": tr["fecha_emision"],
                "emisor_rut": tr["emisor_rut"],
                "emisor_nombre": tr["emisor_nombre"],
                "tipo_dte": str(tr["tipo_dte"]),
                "match_status": "MATCHED_CERTIFIED",
                "match_rule": "TRANSACTION_CHAIN",
                "match_source": "dte_ledger_matcher",
                "delta": 0.0,
            })
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------ RIPLEY
    def _assess_ripley_settlement_chain(self) -> dict:
        """SETTLEMENT_CHAIN_V2: verify whether settlement chain source files exist
        and whether settlement folio namespace matches dte_truth folios."""
        assessment = {
            "marketplace": "RIPLEY",
            "strategy": "SETTLEMENT_CHAIN_V2",
            "status": "BLOCKED",
        }
        root = Path(__file__).resolve().parent.parent.parent.parent
        seller_dir = root / "01_Raw" / "Ripley" / "SELLER"
        ciclos_dir = root / "01_Raw" / "Ripley" / "Ciclos"
        seller_files = list(seller_dir.glob("*.xlsx")) if seller_dir.exists() else []
        ciclos_files = list(ciclos_dir.glob("*.csv")) if ciclos_dir.exists() else []
        assessment["seller_files"] = len(seller_files)
        assessment["ciclos_files"] = len(ciclos_files)
        assessment["source_files_present"] = len(seller_files) > 0 and len(ciclos_files) > 0

        sc = self.db.query(
            "SELECT DISTINCT folio_xml FROM ripley_settlement_chain WHERE has_folio = 1"
        )
        truth = self.db.query(
            "SELECT folio FROM dte_truth_v1 WHERE marketplace='RIPLEY'"
        )
        sc_folios = {self._norm_folio(f) for f in sc["folio_xml"]} - {None}
        truth_folios = {self._norm_folio(f) for f in truth["folio"]} - {None}
        overlap = sc_folios & truth_folios
        assessment["settlement_folios"] = len(sc_folios)
        assessment["truth_folios"] = len(truth_folios)
        assessment["folio_overlap"] = len(overlap)
        assessment["namespace_compatible"] = len(overlap) > 0

        if not assessment["source_files_present"] or not assessment["namespace_compatible"]:
            reasons = []
            if not assessment["source_files_present"]:
                reasons.append("chain source files (SELLER/*.xlsx, Ciclos/*.csv) absent")
            if not assessment["namespace_compatible"]:
                reasons.append(
                    f"folio namespaces incompatible (settlement={assessment['settlement_folios']} "
                    f"vs dte_truth={assessment['truth_folios']}, overlap={assessment['folio_overlap']})"
                )
            assessment["status"] = "BLOCKED"
            assessment["blocked_reasons"] = reasons
        else:
            assessment["status"] = "FEASIBLE"
        return assessment

    # ------------------------------------------------------------------ FALABELLA bridge
    def _load_falabella_bridge(self) -> pd.DataFrame:
        """Load Falabella order bridge: Falabella-Id (UUID) <-> Id Articulo."""
        import glob

        files = glob.glob(
            str(Path(__file__).resolve().parent.parent.parent.parent /
                "01_Raw/Falabella/*rdenes y Transacciones/*.xlsx")
        )
        bridges = []
        for f in files:
            try:
                df = pd.read_excel(f, skiprows=5)
            except Exception as exc:  # pragma: no cover
                logger.warning("Falabella bridge read failed for %s: %s", f, exc)
                continue
            col_fala = next((c for c in df.columns if "Falabella-Id" in str(c)), None)
            col_art = next((c for c in df.columns if "Id Art" in str(c)), None)
            if col_fala is None or col_art is None:
                continue
            sub = df[[col_fala, col_art]].dropna()
            sub.columns = ["uuid", "id_art"]
            sub["uuid"] = sub["uuid"].astype(str)
            sub["id_art"] = sub["id_art"].astype(str).str.replace(".0", "", regex=False)
            bridges.append(sub)
        if not bridges:
            return pd.DataFrame()
        return pd.concat(bridges).drop_duplicates()

    # ------------------------------------------------------------------ persistence
    def _ensure_schema(self):
        """Create certified-match table if missing. Does NOT touch ledger."""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS dte_certified_match_v1 (
                marketplace VARCHAR,
                id_transaccion VARCHAR,
                folio_xml VARCHAR,
                dte_folio VARCHAR,
                dte_monto DOUBLE,
                dte_fecha DATE,
                emisor_nombre VARCHAR,
                emisor_rut VARCHAR,
                tipo_dte VARCHAR,
                match_rule VARCHAR,
                match_status VARCHAR,
                match_source VARCHAR,
                execution_id VARCHAR,
                PRIMARY KEY (marketplace, id_transaccion)
            )
        """)

    def _build_certified_rows(self, marketplace: str, matches: pd.DataFrame) -> pd.DataFrame:
        """Build the certified per-transaction rows for a marketplace (NO persistence).

        Pure read-model expansion: folio-level ML matches are expanded into
        per-transaction rows; PARIS/FALABELLA matches are mapped to table columns.
        The returned DataFrame has the exact schema of dte_certified_match_v1.
        """
        if matches is None or matches.empty:
            return pd.DataFrame()
        cert = matches[matches["match_status"].isin(CERTIFIED_STATUSES)]
        if cert.empty:
            return pd.DataFrame()

        # ML matches are folio-level; expand into per-transaction rows.
        if marketplace == "ML" and "folio" in cert.columns:
            cert_folios = {str(f) for f in cert["folio"].unique()}
            if not cert_folios:
                return pd.DataFrame()
            # Fetch all ML ledger rows with a folio_xml and normalize in Python
            # (mirrors _match_ml_direct exactly — no regexp edge-case risk).
            tx = self.db.query(
                """SELECT id_transaccion, folio_xml
                    FROM marketplace_ledger_v1
                    WHERE marketplace = 'ML'
                      AND folio_xml IS NOT NULL AND folio_xml != ''"""
            )
            if tx.empty:
                return pd.DataFrame()
            folio_to_cert = {str(r["folio"]): r for _, r in cert.iterrows()}
            rows = []
            for _, r in tx.iterrows():
                f = self._norm_ml_folio(r["folio_xml"])
                if f is None or f not in cert_folios:
                    continue
                c = folio_to_cert[f]
                rows.append({
                    "id_transaccion": r["id_transaccion"],
                    "folio_xml": r["folio_xml"],
                    "dte_folio": f,
                    "dte_monto": float(c["monto_total"]),
                    "dte_fecha": str(c["fecha_emision"]),
                    "emisor_nombre": c["emisor_nombre"],
                    "emisor_rut": c["emisor_rut"],
                    "tipo_dte": str(c["tipo_dte"]),
                    "match_rule": c["match_rule"],
                    "match_status": c["match_status"],
                    "match_source": c["match_source"],
                })
            out = pd.DataFrame(rows)
        else:
            # Map to table columns.
            out = cert.rename(columns={
                "folio": "dte_folio",
                "folio_xml": "folio_xml",
                "monto_total": "dte_monto",
                "fecha_emision": "dte_fecha",
                "emisor_nombre": "emisor_nombre",
                "emisor_rut": "emisor_rut",
                "tipo_dte": "tipo_dte",
            })
            if "dte_folio" not in out.columns:
                out["dte_folio"] = out.get("folio_xml")

        out = out[["id_transaccion", "folio_xml", "dte_folio", "dte_monto", "dte_fecha",
                   "emisor_nombre", "emisor_rut", "tipo_dte", "match_rule",
                   "match_status", "match_source"]].copy()
        out["marketplace"] = marketplace
        out["execution_id"] = self.execution_id
        return out.drop_duplicates(subset=["marketplace", "id_transaccion"])

    def _persist_certified(self, marketplace: str, matches: pd.DataFrame) -> int:
        """Write certified matches into dte_certified_match_v1 (upsert)."""
        out = self._build_certified_rows(marketplace, matches)
        if out.empty:
            return 0

        self._ensure_schema()
        # Delete this marketplace's prior certified matches (idempotent per MP),
        # then bulk-insert via DuckDB's native DataFrame path (fast).
        self.db.execute(
            "DELETE FROM dte_certified_match_v1 WHERE marketplace = ?", [marketplace]
        )
        return self.db.insert_df(out, "dte_certified_match_v1", dedup_cols=["marketplace", "id_transaccion"])

    def _rebuild_view(self):
        """Replace the dte_ledger_link view so dte_linked reflects certified matches."""
        self.db.execute("DROP VIEW IF EXISTS dte_ledger_link")
        self.db.execute(f"""
            CREATE VIEW dte_ledger_link AS
            SELECT
                l.marketplace,
                l.id_transaccion,
                l.folio_xml,
                l.fecha AS ledger_fecha,
                l.monto AS ledger_monto,
                l.tipo_movimiento,
                l.detalle,
                l.financial_group,
                COALESCE(m.dte_folio, d.folio) AS dte_folio,
                COALESCE(m.dte_monto, d.monto_total) AS dte_monto,
                COALESCE(m.dte_fecha, d.fecha_emision) AS dte_fecha,
                COALESCE(m.emisor_nombre, d.emisor_nombre) AS emisor_nombre,
                COALESCE(m.emisor_rut, d.emisor_rut) AS emisor_rut,
                COALESCE(m.tipo_dte, d.tipo_dte) AS tipo_dte,
                CASE
                    WHEN m.id_transaccion IS NOT NULL THEN 1
                    WHEN d.folio IS NOT NULL THEN 1
                    ELSE 0
                END AS dte_linked
            FROM marketplace_ledger_v1 AS l
            LEFT JOIN dte_truth_v1 AS d
                ON ((l.folio_xml = d.folio) AND (l.marketplace = d.marketplace))
            LEFT JOIN dte_certified_match_v1 AS m
                ON ((l.marketplace = m.marketplace) AND (l.id_transaccion = m.id_transaccion))
            WHERE ((l.folio_xml IS NOT NULL) AND (l.folio_xml != ''))
               OR m.id_transaccion IS NOT NULL
        """)

    # ------------------------------------------------------------------ main
    def run(self) -> dict:
        """Execute all marketplace matching strategies and persist dte_linked."""
        summary = {
            "execution_id": self.execution_id,
            "marketplaces": {},
        }

        # ---- ML
        ml = self._match_ml_direct()
        summary["marketplaces"]["ML"] = {
            "strategy": "DIRECT_MATCH",
            "folio_matches": int((ml["match_status"].isin(CERTIFIED_STATUSES)).sum()) if not ml.empty else 0,
            "rows_linked": self._persist_certified("ML", ml),
            "rows_eligible": int(self.db.query(
                "SELECT COUNT(*) c FROM marketplace_ledger_v1 WHERE marketplace='ML' "
                "AND folio_xml IS NOT NULL AND folio_xml NOT IN ('','None')"
            ).iloc[0]["c"]),
        }

        # ---- PARIS
        paris = self._match_paris_document_chain()
        summary["marketplaces"]["PARIS"] = {
            "strategy": "DOCUMENT_CHAIN",
            "distinct_folios": int(paris["folio_xml"].nunique()) if not paris.empty else 0,
            "rows_linked": self._persist_certified("PARIS", paris),
            "rows_eligible": int(self.db.query(
                "SELECT COUNT(*) c FROM marketplace_ledger_v1 WHERE marketplace='PARIS' "
                "AND folio_xml IS NOT NULL AND folio_xml NOT IN ('','None')"
            ).iloc[0]["c"]),
        }

        # ---- FALABELLA
        bridge = self._load_falabella_bridge()
        fal = self._match_falabella_transaction_chain(bridge)
        summary["marketplaces"]["FALABELLA"] = {
            "strategy": "TRANSACTION_CHAIN",
            "distinct_folios": int(fal["folio_xml"].nunique()) if not fal.empty else 0,
            "rows_linked": self._persist_certified("FALABELLA", fal),
            "rows_eligible": int(self.db.query(
                "SELECT COUNT(*) c FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'"
            ).iloc[0]["c"]),
        }

        # ---- RIPLEY
        ripley = self._assess_ripley_settlement_chain()
        summary["marketplaces"]["RIPLEY"] = ripley

        # ---- rebuild view
        self._rebuild_view()

        self.results = summary
        return summary

    # ------------------------------------------------------------------ read-only traceability
    def traceability(self, marketplace: str | None = None,
                     transaction_id: str | None = None) -> dict:
        """Read-only DTE->Ledger traceability (F5-09).

        NEVER persists, NEVER mutates the DB, NEVER touches financial data.
        Computes the certified matches in memory and reports per-marketplace
        coverage plus an optional per-transaction trace.

        RIPLEY is honestly reported as BLOCKED when the settlement chain is
        structurally impossible (no false fiscal inference).
        """
        valid = {"ML", "PARIS", "FALABELLA", "RIPLEY"}
        mp = None
        if marketplace:
            mp = str(marketplace).upper()
            if mp not in valid:
                raise ValueError(f"invalid marketplace: {marketplace}")

        result = {
            "_meta": {
                "engine": "DTELedgerMatcher v1 (certified p0)",
                "execution_id": self.execution_id,
                "read_only": True,
                "official_db_touched": False,
            },
            "marketplaces": {},
        }

        # ---- ML (DIRECT_MATCH)
        if mp is None or mp == "ML":
            ml = self._match_ml_direct()
            ml_cert = self._build_certified_rows("ML", ml)
            result["marketplaces"]["ML"] = {
                "strategy": "DIRECT_MATCH",
                "status": "CERTIFIED" if not ml_cert.empty else "NO_CERTIFIED_MATCHES",
                "folios_certified": int(ml_cert["dte_folio"].nunique()) if not ml_cert.empty else 0,
                "rows_linked": int(len(ml_cert)),
                "rows_eligible": int(self.db.query(
                    "SELECT COUNT(*) c FROM marketplace_ledger_v1 WHERE marketplace='ML' "
                    "AND folio_xml IS NOT NULL AND folio_xml NOT IN ('','None')"
                ).iloc[0]["c"]),
                "match_statuses": (
                    ml["match_status"].value_counts().to_dict() if not ml.empty else {}
                ),
            }

        # ---- PARIS (DOCUMENT_CHAIN)
        if mp is None or mp == "PARIS":
            paris = self._match_paris_document_chain()
            paris_cert = self._build_certified_rows("PARIS", paris)
            result["marketplaces"]["PARIS"] = {
                "strategy": "DOCUMENT_CHAIN",
                "status": "CERTIFIED" if not paris_cert.empty else "NO_CERTIFIED_MATCHES",
                "folios_certified": int(paris_cert["dte_folio"].nunique()) if not paris_cert.empty else 0,
                "rows_linked": int(len(paris_cert)),
                "rows_eligible": int(self.db.query(
                    "SELECT COUNT(*) c FROM marketplace_ledger_v1 WHERE marketplace='PARIS' "
                    "AND folio_xml IS NOT NULL AND folio_xml NOT IN ('','None')"
                ).iloc[0]["c"]),
            }

        # ---- FALABELLA (TRANSACTION_CHAIN)
        if mp is None or mp == "FALABELLA":
            bridge = self._load_falabella_bridge()
            fal = self._match_falabella_transaction_chain(bridge)
            fal_cert = self._build_certified_rows("FALABELLA", fal)
            result["marketplaces"]["FALABELLA"] = {
                "strategy": "TRANSACTION_CHAIN",
                "status": "CERTIFIED" if not fal_cert.empty else "NO_CERTIFIED_MATCHES",
                "folios_certified": int(fal_cert["dte_folio"].nunique()) if not fal_cert.empty else 0,
                "rows_linked": int(len(fal_cert)),
                "rows_eligible": int(self.db.query(
                    "SELECT COUNT(*) c FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'"
                ).iloc[0]["c"]),
            }

        # ---- RIPLEY (SETTLEMENT_CHAIN_V2 assessment — honest BLOCKED)
        if mp is None or mp == "RIPLEY":
            rip = self._assess_ripley_settlement_chain()
            result["marketplaces"]["RIPLEY"] = rip

        result["totals"] = {
            "total_dte_linked_rows": sum(
                m.get("rows_linked", 0)
                for m in result["marketplaces"].values()
                if isinstance(m, dict) and m.get("strategy") != "SETTLEMENT_CHAIN_V2"
            ),
            "official_db_touched": False,
        }

        if transaction_id:
            result["transaction"] = self._trace_transaction(transaction_id)
        return result

    def _trace_transaction(self, transaction_id: str) -> dict:
        """Resolve a single ledger transaction to its certified DTE backing (read-only)."""
        row = self.db.query(
            "SELECT marketplace, folio_xml FROM marketplace_ledger_v1 "
            "WHERE id_transaccion = ? LIMIT 1",
            [transaction_id],
        )
        if row.empty:
            return {
                "transaction_id": transaction_id,
                "match_status": "NOT_FOUND",
                "note": "transaction_id not present in marketplace_ledger_v1",
            }

        mp = str(row.iloc[0]["marketplace"]).upper()
        folio_xml = row.iloc[0]["folio_xml"]
        base = {
            "transaction_id": transaction_id,
            "marketplace": mp,
            "folio_xml": folio_xml,
        }

        if mp == "ML":
            ml = self._match_ml_direct()
            cert = self._build_certified_rows("ML", ml)
            hit = cert[cert["id_transaccion"].astype(str) == str(transaction_id)]
            if hit.empty:
                base.update({"match_status": "NOT_FOUND", "note": "no certified DTE match"})
                return base
            r = hit.iloc[0]
            base.update({
                "dte_folio": r["dte_folio"],
                "dte_monto": float(r["dte_monto"]),
                "dte_fecha": str(r["dte_fecha"]),
                "emisor_rut": r["emisor_rut"],
                "emisor_nombre": r["emisor_nombre"],
                "tipo_dte": str(r["tipo_dte"]),
                "match_status": str(r["match_status"]),
                "match_rule": str(r["match_rule"]),
            })
            return base

        if mp == "PARIS":
            paris = self._match_paris_document_chain()
            cert = self._build_certified_rows("PARIS", paris)
            hit = cert[cert["id_transaccion"].astype(str) == str(transaction_id)]
            if hit.empty:
                base.update({"match_status": "NOT_FOUND", "note": "no certified DTE match"})
                return base
            r = hit.iloc[0]
            base.update({
                "dte_folio": r["dte_folio"],
                "dte_monto": float(r["dte_monto"]),
                "dte_fecha": str(r["dte_fecha"]),
                "emisor_rut": r["emisor_rut"],
                "emisor_nombre": r["emisor_nombre"],
                "tipo_dte": str(r["tipo_dte"]),
                "match_status": str(r["match_status"]),
                "match_rule": str(r["match_rule"]),
            })
            return base

        if mp == "FALABELLA":
            bridge = self._load_falabella_bridge()
            fal = self._match_falabella_transaction_chain(bridge)
            cert = self._build_certified_rows("FALABELLA", fal)
            hit = cert[cert["id_transaccion"].astype(str) == str(transaction_id)]
            if hit.empty:
                base.update({"match_status": "NOT_FOUND", "note": "no certified DTE match"})
                return base
            r = hit.iloc[0]
            base.update({
                "dte_folio": r["dte_folio"],
                "dte_monto": float(r["dte_monto"]),
                "dte_fecha": str(r["dte_fecha"]),
                "emisor_rut": r["emisor_rut"],
                "emisor_nombre": r["emisor_nombre"],
                "tipo_dte": str(r["tipo_dte"]),
                "match_status": str(r["match_status"]),
                "match_rule": str(r["match_rule"]),
            })
            return base

        # RIPLEY — honest BLOCKED
        base.update({
            "match_status": "BLOCKED",
            "note": "SETTLEMENT_CHAIN_V2 structurally blocked (source files absent / folio namespace overlap=0)",
        })
        return base
