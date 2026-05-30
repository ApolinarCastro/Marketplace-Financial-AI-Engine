"""
ANTIGRAVITY v4.5 — Financial Closing Engine (Meli)
"""
from engine.v4.database import DatabaseV4
import pandas as pd
from datetime import timedelta
import logging

logger = logging.getLogger("antigravity.closing")

class MeliFinancialClosing:
    def __init__(self):
        self.db = DatabaseV4.get()

    def run_closing(self, periodo):
        """Orchestrates the monthly financial closing process."""
        logger.info(f"Iniciando cierre financiero para periodo: {periodo}")
        
        # 1. Payment Calendar Logic
        self._generate_payment_calendar()
        
        # 2. XML Certification Status
        self._run_xml_certification()
        
        # 3. Consolidation
        stats = self.db.query(f"""
            SELECT 
                SUM(CASE WHEN categoria_gerencial = 'INGRESO' THEN monto ELSE 0 END) as gmv,
                SUM(CASE WHEN signo = 'negativo' THEN monto ELSE 0 END) as costs,
                SUM(CASE WHEN categoria_gerencial = 'DEVOLUCION' THEN monto ELSE 0 END) as refunds,
                SUM(monto) as net_expected
            FROM meli_ledger_v1
            WHERE strftime('%Y-%m', fecha) = '{periodo}'
        """).iloc[0]

        payout = self.db.query(f"""
            SELECT SUM(monto_pagado) as paid 
            FROM meli_payouts WHERE periodo = '{periodo}'
        """).iloc[0]['paid'] or 0

        # Calculate KPIs
        ventas = stats['gmv']
        costos = abs(stats['costs'])
        neto_esperado = stats['net_expected']
        diferencia = neto_esperado - payout
        
        # Block Closing Rule
        status = "CERRADO" if abs(diferencia) <= (neto_esperado * 0.02) else "DIFERENCIA_PENDIENTE"

        # Save Closing
        self.db.execute("""
            INSERT INTO financial_closing_meli 
            (periodo, ventas_brutas, costos, devoluciones, neto_esperado, neto_pagado, diferencia, estado_cierre)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [periodo, ventas, costos, stats['refunds'], neto_esperado, payout, diferencia, status])
        
        logger.info(f"Cierre finalizado para {periodo}. Estado: {status}")
        return {"periodo": periodo, "estado": status, "diferencia": diferencia}

    def _generate_payment_calendar(self):
        """Calculates estimated payment dates using logistics rules."""
        # Logic: FLEX (2d), FULL (7d), DEFAULT (14d)
        ledger = self.db.query("""
            SELECT id_transaccion, fecha, monto, 
                   CASE WHEN id_transaccion LIKE '%FLEX%' THEN 'flex' 
                        WHEN id_transaccion LIKE '%FULL%' THEN 'full' 
                        ELSE 'default' END as logistica
            FROM meli_ledger_v1 
            WHERE categoria_gerencial = 'INGRESO'
        """)
        
        records = []
        for _, row in ledger.iterrows():
            days = 2 if row['logistica'] == 'flex' else (7 if row['logistica'] == 'full' else 14)
            payout_date = pd.to_datetime(row['fecha']) + timedelta(days=days)
            records.append((row['id_transaccion'], row['logistica'], row['fecha'], days, payout_date, row['monto']))
            
        self.db.execute("DELETE FROM meli_payment_calendar")
        self.db.conn.executemany("""
            INSERT INTO meli_payment_calendar (id_transaccion, tipo_logistica, fecha_venta, dias_pago, fecha_pago_estimada, monto_neto)
            VALUES (?, ?, ?, ?, ?, ?)
        """, records)

    def _run_xml_certification(self):
        """Matches ledger transactions with XML DTEs."""
        # Mock logic for demonstration
        self.db.execute("DELETE FROM meli_xml_certification")
        self.db.execute("""
            INSERT INTO meli_xml_certification (id_transaccion, folio_xml, monto_xml, estado_certificacion, match_confianza)
            SELECT id_transaccion, xml_folio, monto, 'CERTIFICADO', 1.0
            FROM meli_ledger_v1
            WHERE xml_folio IS NOT NULL
        """)

if __name__ == "__main__":
    closing = MeliFinancialClosing()
    closing.run_closing("2026-04")
