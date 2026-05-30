import duckdb
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

class DuckDBManager:
    def __init__(self, db_path: str = "database/reconciliation.db"):
        self.db_path = db_path
        self.conn = None
        self._ensure_database_dir()
    
    def _ensure_database_dir(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self):
        self.conn = duckdb.connect(self.db_path)
        # Make DuckDB a little stricter/predictable.
        try:
            self.conn.execute("SET timezone='UTC'")
        except Exception:
            pass
        return self.conn
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def execute(self, query: str, params=None):
        if not self.conn:
            self.connect()
        if params:
            return self.conn.execute(query, params)
        return self.conn.execute(query)
    
    def execute_many(self, query: str, params_list: list):
        if not self.conn:
            self.connect()
        self.conn.executemany(query, params_list)
    
    def df_query(self, query: str, params=None):
        if not self.conn:
            self.connect()
        if params:
            return self.conn.execute(query, params).df()
        return self.conn.execute(query).df()
    
    def create_tables(self):
        if not self.conn:
            self.connect()
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS stg_file_registry (
                file_path TEXT,
                file_name TEXT,
                marketplace TEXT,
                period TEXT,
                file_hash TEXT,
                load_timestamp TIMESTAMP,
                status TEXT DEFAULT 'PENDING'
            )
        """)

        # Registry constraints/indexes (DuckDB doesn't enforce PK like OLTP DBs).
        try:
            self.conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_registry_hash ON stg_file_registry(file_hash)")
        except Exception:
            pass
        try:
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_registry_market_period ON stg_file_registry(marketplace, period)")
        except Exception:
            pass
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS fact_ledger_movimientos (
                marketplace TEXT,
                event_date DATE,
                event_type_std TEXT,
                amount_signed DOUBLE,
                currency TEXT,
                order_id_mp TEXT,
                shipment_id_mp TEXT,
                payment_id_mp TEXT,
                document_id_mp TEXT,
                detail_id_mp TEXT,
                sku TEXT,
                item_id_mp TEXT,
                report_type TEXT,
                source_file TEXT,
                load_timestamp TIMESTAMP,
                hash TEXT
            )
        """)

        try:
            self.conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_ledger_hash ON fact_ledger_movimientos(hash)")
        except Exception:
            pass
        
        # cur_sap_ov: base columns + dynamic raw columns added on import.
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cur_sap_ov (
                event_date DATE,
                order_id TEXT,
                amount_signed DOUBLE,
                currency TEXT,
                source_file TEXT,
                load_timestamp TIMESTAMP,
                file_hash TEXT
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS fact_conc_sap_vs_marketplace (
                sap_order_id TEXT,
                mp_order_id TEXT,
                sap_amount DOUBLE,
                mp_amount DOUBLE,
                difference DOUBLE,
                status TEXT
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS fact_conc_caja_total (
                marketplace TEXT,
                event_date DATE,
                event_type TEXT,
                amount_signed DOUBLE,
                currency TEXT,
                order_id_mp TEXT,
                balance_cumulative DOUBLE,
                status TEXT
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS fact_excepciones (
                marketplace TEXT,
                event_date DATE,
                amount DOUBLE,
                order_id TEXT,
                cause_std TEXT,
                severity TEXT DEFAULT 'ERROR',
                hash TEXT,
                load_timestamp TIMESTAMP
            )
        """)
        
        # Stored as parquet in 06_IA_Propuestas/ per spec; keep DB table optional.
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS dim_conceptos_no_clasificados (
                concept_raw TEXT,
                source_file TEXT,
                detected_at TIMESTAMP
            )
        """)
        
        self._create_indexes()
    
    def _create_indexes(self):
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_ledger_order_id ON fact_ledger_movimientos(order_id_mp)",
            "CREATE INDEX IF NOT EXISTS idx_ledger_payment_id ON fact_ledger_movimientos(payment_id_mp)",
            "CREATE INDEX IF NOT EXISTS idx_ledger_document_id ON fact_ledger_movimientos(document_id_mp)",
            "CREATE INDEX IF NOT EXISTS idx_ledger_marketplace ON fact_ledger_movimientos(marketplace)",
            "CREATE INDEX IF NOT EXISTS idx_ledger_date ON fact_ledger_movimientos(event_date)",
            "CREATE INDEX IF NOT EXISTS idx_sap_order ON cur_sap_ov(order_id)",
            "CREATE INDEX IF NOT EXISTS idx_excepciones_order ON fact_excepciones(order_id)"
        ]
        
        for idx_sql in indexes:
            try:
                self.conn.execute(idx_sql)
            except Exception:
                pass
    
    def table_exists(self, table_name: str) -> bool:
        result = self.conn.execute(f"""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = '{table_name}'
        """).fetchone()
        return result[0] > 0
    
    def get_table_count(self, table_name: str) -> int:
        result = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        return result[0] if result else 0
    
    def truncate_table(self, table_name: str):
        self.conn.execute(f"DELETE FROM {table_name}")

    def _table_columns(self, table_name: str) -> list[str]:
        try:
            info = self.conn.execute(f"PRAGMA table_info('{table_name}')").fetchall()
            return [row[1] for row in info]
        except Exception:
            try:
                info = self.conn.execute(f"DESCRIBE {table_name}").fetchall()
                return [row[0] for row in info]
            except Exception:
                return []

    def insert_from_dataframe(self, df: pd.DataFrame, table_name: str, mode: str = "append", pk_cols: list = None):
        """
        Inserta un DataFrame en DuckDB con soporte para De-duplicación.
        pk_cols: Columnas que definen la unicidad para evitar duplicados si mode='upsert' (simulado).
        """
        if df is None or len(df) == 0:
            return
        if not self.conn:
            self.connect()

        if mode == "replace":
            self.truncate_table(table_name)

        table_cols = self._table_columns(table_name)
        df2 = df.copy()

        # Asegurar columnas en la tabla
        for c in df2.columns:
            if c not in table_cols:
                try:
                    # Intentar inferir tipo básico
                    dtype = "DOUBLE" if df2[c].dtype in ['float64', 'int64'] else "TEXT"
                    self.conn.execute(f'ALTER TABLE {table_name} ADD COLUMN "{c}" {dtype}')
                    table_cols.append(c)
                except Exception:
                    pass

        # Alinear DataFrame con las columnas de la tabla (columnas faltantes como NULL)
        for c in table_cols:
            if c not in df2.columns:
                df2[c] = None
        df2 = df2[table_cols]

        # Registrar temporalmente para inserción SQL
        self.conn.register("_tmp_df", df2)
        cols_sql = ",".join([f'"{c}"' for c in table_cols])
        
        if pk_cols:
            # Lógica de "Upsert": eliminamos los que ya existen por PK antes de insertar
            pk_condition = " AND ".join([f'{table_name}."{c}" = _tmp_df."{c}"' for c in pk_cols])
            self.conn.execute(f"""
                DELETE FROM {table_name} 
                WHERE EXISTS (SELECT 1 FROM _tmp_df WHERE {pk_condition})
            """)
        
        self.conn.execute(f"INSERT INTO {table_name} ({cols_sql}) SELECT {cols_sql} FROM _tmp_df")
        self.conn.unregister("_tmp_df")

    def get_reconciliation_results(self):
        """
        Ejecuta el cruce masivo SAP vs LEDGER directamente en SQL.
        Mucho más rápido que hacerlo en Pandas para miles de registros.
        """
        return self.df_query("""
            WITH sap_totals AS (
                SELECT order_id, SUM(amount_signed) as sap_val, ANY_VALUE(source_file) as sap_source
                FROM cur_sap_ov 
                GROUP BY 1
            ),
            mp_totals AS (
                SELECT order_id_mp, marketplace, SUM(amount_signed) as mp_val, COUNT(*) as events
                FROM fact_ledger_movimientos
                GROUP BY 1, 2
            )
            SELECT 
                s.order_id as 'Orden de Venta',
                m.marketplace as 'Marketplace',
                s.sap_val as 'Valor Sap',
                COALESCE(m.mp_val, 0) as 'Monto_Neto',
                (s.sap_val - COALESCE(m.mp_val, 0)) as 'Diferencia',
                CASE 
                    WHEN m.order_id_mp IS NULL THEN 'No Conciliado'
                    WHEN ABS(s.sap_val - m.mp_val) < 10 THEN 'Conciliado'
                    ELSE 'Discrepancia'
                END as 'Estado_Antigravity'
            FROM sap_totals s
            LEFT JOIN mp_totals m ON s.order_id = m.order_id_mp
        """)


_db_instance = None

def get_db() -> DuckDBManager:
    global _db_instance
    if _db_instance is None:
        _db_instance = DuckDBManager()
        _db_instance.connect()
        _db_instance.create_tables()
    return _db_instance

def close_db():
    global _db_instance
    if _db_instance:
        _db_instance.close()
        _db_instance = None
