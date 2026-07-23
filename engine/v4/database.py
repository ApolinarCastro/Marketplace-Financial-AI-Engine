"""
Meli Financial Auditor v3.5
Database Manager — Unified Schema
"""
import duckdb
from pathlib import Path
import logging
import threading
import signal

logger = logging.getLogger("meli.db")
ROOT = Path("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine")
DB_PATH = ROOT / "data" / "db" / "meli_financial_v4.db"

class DatabaseV4:
    _instance = None
    _shutdown_registered = False

    def __init__(self, db_path=DB_PATH, read_only=True):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path), read_only=read_only)
        self._closed = False
        import tempfile
        tmp_dir = tempfile.gettempdir().replace("\\", "/")
        self.conn.execute(f"SET temp_directory='{tmp_dir}';")
        self.lock = threading.Lock()
        if not read_only:
            self._create_schema()

    def close(self):
        if self._closed:
            return
        self._closed = True
        try:
            self.conn.close()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.warning(f"Error closing database connection: {e}")

    @classmethod
    def get(cls, read_only=True):
        if cls._instance is not None:
            # Detect zombie singleton: connection was closed but _instance still alive
            if getattr(cls._instance, '_closed', False):
                cls.reset()
            # If we need write access but current connection is read-only, recreate
            elif not read_only and getattr(cls._instance, 'is_read_only', True):
                cls.reset()
        if cls._instance is None:
            cls._instance = cls(read_only=read_only)
            cls._instance.is_read_only = read_only
            cls._register_shutdown_hook()
        return cls._instance

    @classmethod
    def _register_shutdown_hook(cls):
        if cls._shutdown_registered:
            return
        cls._shutdown_registered = True
        import atexit
        atexit.register(cls.reset)

    @classmethod
    def reset(cls):
        if cls._instance:
            cls._instance.close()
            cls._instance = None

    def execute(self, sql, params=None):
        with self.lock:
            return self.conn.execute(sql, params)

    def query(self, sql, params=None):
        with self.lock:
            return self.conn.execute(sql, params).df()

    def insert_df(self, df, table, dedup_cols=None):
        if df.empty: return 0
        with self.lock:
            temp_name = f"stg_temp_{id(df)}"
            self.conn.register(temp_name, df)
            cols = ", ".join(df.columns)
            if dedup_cols:
                where_clause = " AND ".join([f"COALESCE(t.{c}, '') = COALESCE(s.{c}, '')" for c in dedup_cols])
                sql = f"INSERT INTO {table} ({cols}) SELECT {cols} FROM {temp_name} s WHERE NOT EXISTS (SELECT 1 FROM {table} t WHERE {where_clause})"
                self.conn.execute(sql)
            else:
                self.conn.execute(f"INSERT INTO {table} ({cols}) SELECT {cols} FROM {temp_name}")
            self.conn.unregister(temp_name)
            return len(df)

    def _create_schema(self):
        # Hot-migration: ensure include_in_operational_pnl is added if db exists on disk
        # This MUST run before views are created, because views reference this column!
        try:
            self.conn.execute("ALTER TABLE marketplace_ledger_clasificado_v1 ADD COLUMN include_in_operational_pnl BOOLEAN")
        except Exception:
            pass
        try:
            self.conn.execute("ALTER TABLE marketplace_ledger_clasificado_v1 ADD COLUMN financial_group TEXT")
        except Exception:
            pass
        try:
            self.conn.execute("ALTER TABLE marketplace_ledger_clasificado_v1 ADD COLUMN financial_subgroup TEXT")
        except Exception:
            pass

        # Hot-migration: ensure ledger support columns exist in marketplace_ledger_v1
        for col, col_type in [("clasificacion_operativa", "TEXT"), ("include_in_operational_pnl", "BOOLEAN"), ("financial_group", "TEXT")]:
            try:
                self.conn.execute(f"ALTER TABLE marketplace_ledger_v1 ADD COLUMN {col} {col_type}")
            except Exception:
                pass
        try:
            self.conn.execute("ALTER TABLE marketplace_ledger_v1 ADD COLUMN execution_id TEXT")
        except Exception:
            pass

        # Hot-migration: add extra DTE columns if they don't exist
        for col in ["tipo_dte", "rut_receptor", "marketplace"]:
            try:
                self.conn.execute(f"ALTER TABLE dte_truth_v1 ADD COLUMN {col} TEXT")
            except Exception:
                pass

        ddl = [
            # ── V4 Core Tables (React Dashboard needs these) ──
            "CREATE TABLE IF NOT EXISTS ventas_marketplace (order_id TEXT, sku TEXT, quantity INTEGER, unit_price DOUBLE, gross_amount DOUBLE, sale_date DATE, marketplace TEXT, source_file TEXT, load_ts TIMESTAMP DEFAULT current_timestamp)",
            "CREATE TABLE IF NOT EXISTS transaction_ledger (operation_id TEXT, order_id TEXT, event_type TEXT, description TEXT, amount DOUBLE, event_date DATE, marketplace TEXT, source_file TEXT, folio TEXT, load_ts TIMESTAMP DEFAULT current_timestamp)",
            "CREATE TABLE IF NOT EXISTS order_reconciliation (order_id TEXT, internal_amount DOUBLE, marketplace_amount DOUBLE, difference DOUBLE, reconciliation_status TEXT, match_key TEXT, marketplace TEXT, reconciliation_date TIMESTAMP DEFAULT current_timestamp)",
            "CREATE TABLE IF NOT EXISTS exceptions (order_id TEXT, marketplace TEXT, exception_type TEXT, severity TEXT, description TEXT, detected_at TIMESTAMP DEFAULT current_timestamp)",
            "CREATE TABLE IF NOT EXISTS financial_reconciliation (order_id TEXT, gross_sales DOUBLE, fees DOUBLE, shipping_cost DOUBLE, refunds DOUBLE, net_expected DOUBLE, released_amount DOUBLE, difference DOUBLE, financial_status TEXT, marketplace TEXT)",
            "CREATE TABLE IF NOT EXISTS liberaciones (order_id TEXT, release_date DATE, released_amount DOUBLE, marketplace TEXT)",
            "CREATE TABLE IF NOT EXISTS retiros (withdrawal_id TEXT, withdrawal_date DATE, withdrawal_amount DOUBLE, bank_account TEXT, marketplace TEXT)",
            "CREATE TABLE IF NOT EXISTS bank_statement (transaction_date DATE, amount DOUBLE, description TEXT, reference TEXT)",
            
            # ── Marketplace Financial Auditor v3.5 Layers ──
            
            # Layer 1: Source (marketplace_ledger_v1)
            "CREATE TABLE IF NOT EXISTS marketplace_ledger_v1 (marketplace TEXT, id_transaccion TEXT, id_orden TEXT, fecha DATE, detalle TEXT, monto DOUBLE, tipo_movimiento TEXT, archivo_origen TEXT, folio_xml TEXT, estado_xml TEXT, clasificacion_operativa TEXT, include_in_operational_pnl BOOLEAN, financial_group TEXT, load_ts TIMESTAMP DEFAULT current_timestamp)",
            
            # Layer 2: Classification (marketplace_ledger_clasificado_v1)
            "CREATE TABLE IF NOT EXISTS marketplace_ledger_clasificado_v1 (marketplace TEXT, id_transaccion TEXT, id_orden TEXT, detalle TEXT, tipo_movimiento TEXT, monto DOUBLE, fecha DATE, clasificacion_operativa TEXT, confianza_clasificacion DOUBLE, origen_clasificacion TEXT, include_in_operational_pnl BOOLEAN, financial_group TEXT, financial_subgroup TEXT)",
            
            # Layer 4: Financial Closing (marketplace_cierre_financiero_v1)
            "CREATE TABLE IF NOT EXISTS marketplace_cierre_financiero_v1 (marketplace TEXT, periodo_inicio DATE, periodo_fin DATE, total_ingresos DOUBLE, total_costos_operacionales DOUBLE, total_costos_comerciales DOUBLE, total_ajustes DOUBLE, resultado_neto DOUBLE, created_at TIMESTAMP DEFAULT current_timestamp)",
            
            # Layer 5: Audit (marketplace_auditoria_v1)
            "CREATE TABLE IF NOT EXISTS marketplace_auditoria_v1 (marketplace TEXT, check_name TEXT, condition_detected TEXT, action_taken TEXT, order_id TEXT, detected_at TIMESTAMP DEFAULT current_timestamp)",
            
            # Layer 6: Correction (marketplace_correcciones_v1)
            "CREATE TABLE IF NOT EXISTS marketplace_correcciones_v1 (marketplace TEXT, id_transaccion TEXT, detalle_original TEXT, detalle_corregido TEXT, motivo TEXT, usuario TEXT, fecha TIMESTAMP DEFAULT current_timestamp)",
            
            # Layer 7: Legal Truth (DTE Index)
            "CREATE TABLE IF NOT EXISTS dte_truth_v1 (folio TEXT PRIMARY KEY, monto_neto DOUBLE, monto_iva DOUBLE, monto_total DOUBLE, fecha_emision DATE, emisor_rut TEXT, emisor_nombre TEXT, tipo_dte TEXT, rut_receptor TEXT, marketplace TEXT, load_ts TIMESTAMP DEFAULT current_timestamp)",
 
            # ── Legacy/Support Tables ──
            "CREATE TABLE IF NOT EXISTS cargos_no_clasificados (original_term TEXT, marketplace TEXT, frequency INTEGER, suggested_type TEXT, detected_at TIMESTAMP DEFAULT current_timestamp)",
            "CREATE TABLE IF NOT EXISTS inconsistencias_financieras (order_id TEXT, marketplace TEXT, amount_expected DOUBLE, amount_actual DOUBLE, delta DOUBLE, severity TEXT, detected_at TIMESTAMP DEFAULT current_timestamp)",
            "CREATE TABLE IF NOT EXISTS pipeline_log (event TEXT, status TEXT, details TEXT, timestamp TIMESTAMP DEFAULT current_timestamp)",
            "CREATE TABLE IF NOT EXISTS TABLA_MAPEO (marketplace TEXT, original_term TEXT, normalized_term TEXT, cost_type TEXT, cost_subtype TEXT, confidence DOUBLE)",
            "CREATE TABLE IF NOT EXISTS ai_suggestions_log (id_transaccion TEXT, categoria_original TEXT, categoria_sugerida TEXT, confidence DOUBLE, suggested_at TIMESTAMP DEFAULT current_timestamp, status TEXT DEFAULT 'PENDIENTE')",
            
            # Files Registry
            "CREATE TABLE IF NOT EXISTS file_registry (file_hash TEXT PRIMARY KEY, file_name TEXT, source TEXT, rows_processed INTEGER, processed_at TIMESTAMP DEFAULT current_timestamp)",
 
            # Views for Dashboard
            """
            CREATE OR REPLACE VIEW vw_dashboard_kpis AS 
            SELECT 
                COALESCE(SUM(internal_amount), 0) as total_sales_internal,
                (SELECT COALESCE(SUM(gross_amount), 0) FROM ventas_marketplace) as total_sales_marketplace,
                COUNT(order_id) as total_orders,
                SUM(CASE WHEN reconciliation_status = 'CONCILIADO' THEN 1 ELSE 0 END) as orders_reconciled,
                SUM(CASE WHEN reconciliation_status = 'DISCREPANCIA' THEN 1 ELSE 0 END) as orders_with_difference,
                SUM(CASE WHEN reconciliation_status = 'NO_CONCILIADO' THEN 1 ELSE 0 END) as orders_without_match
            FROM order_reconciliation;
            """,
            "CREATE OR REPLACE VIEW vw_ml_misclassifications AS SELECT * FROM marketplace_auditoria_v1 WHERE marketplace='ML' AND check_name='MISCLASSIFIED';",
            "CREATE OR REPLACE VIEW financial_operational_view_v1 AS SELECT * FROM marketplace_ledger_clasificado_v1 WHERE include_in_operational_pnl = TRUE;",
            "CREATE OR REPLACE VIEW risk_postsale_view_v1 AS SELECT * FROM marketplace_ledger_clasificado_v1 WHERE include_in_operational_pnl = FALSE;"
        ]
        for sql in ddl:
            self.conn.execute(sql)

        for col, col_type in [
            ("file_path", "TEXT"),
            ("content_sha256", "TEXT"),
            ("hash_algorithm", "TEXT"),
            ("file_size_bytes", "BIGINT"),
            ("marketplace", "TEXT"),
            ("document_type", "TEXT"),
            ("period", "TEXT"),
            ("registered_at", "TIMESTAMP"),
        ]:
            try:
                self.conn.execute(f"ALTER TABLE file_registry ADD COLUMN {col} {col_type}")
            except Exception:
                pass
            
    def file_registered(self, fhash: str) -> bool:
        res = self.query("SELECT 1 FROM file_registry WHERE file_hash = ?", [fhash])
        return not res.empty

    def register_file(
        self, fpath: str | Path, fname: str, source: str, fhash: str, rows: int,
        document_type: str | None = None, period: str | None = None,
    ):
        self.execute(
            "INSERT OR REPLACE INTO file_registry "
            "(file_hash, file_name, source, rows_processed, file_path, content_sha256, "
            "hash_algorithm, file_size_bytes, marketplace, document_type, period, registered_at) "
            "VALUES (?, ?, ?, ?, ?, ?, 'SHA-256', ?, ?, ?, ?, CURRENT_TIMESTAMP)",
            [fhash, fname, source, rows, str(Path(fpath).resolve()), fhash,
             Path(fpath).stat().st_size, source, document_type, period]
        )

    def truncate(self, table: str):
        self.execute(f"TRUNCATE TABLE {table}")

    def count(self, table: str) -> int:
        return int(self.query(f"SELECT COUNT(*) AS n FROM {table}")["n"].iloc[0])
