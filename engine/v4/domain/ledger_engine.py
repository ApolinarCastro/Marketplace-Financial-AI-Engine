import pandas as pd
from typing import Optional
from engine.v4.database import DatabaseV4
from engine.v4.period_utils import _resolve_period_range
from engine.v4.domain.financial_engine import FinancialEngine

class LedgerEngine:
    """
    Motor oficial responsable de las interacciones con el Ledger crudo (marketplace_ledger_v1).
    Proporciona información certificada sobre los registros cargados, para evitar
    reconstrucción de consultas SQL en el ensamblador (api.py).
    """

    def __init__(self, db: Optional[DatabaseV4] = None):
        self.db = db or DatabaseV4.get()
        self._financial_engine = FinancialEngine(db=self.db)

    def get_ledger_records_count(self, marketplace: str, periodo: str) -> int:
        """
        Retorna la cantidad oficial de registros crudos en el ledger para el período y marketplace dados.
        Reutiliza los filtros oficiales del FinancialEngine para asegurar paridad.
        """
        where_clause, params = self._financial_engine._build_ledger_where(periodo, marketplace)
        
        sql = f"SELECT COUNT(*) as count FROM marketplace_ledger_v1 WHERE {where_clause}"
        result = self.db.query(sql, params)
        if result.empty:
            return 0
        return int(result.iloc[0]["count"])
