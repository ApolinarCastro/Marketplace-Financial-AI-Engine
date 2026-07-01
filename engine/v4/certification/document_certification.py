from engine.v4.database import DatabaseV4
import pandas as pd

class DocumentCertificationEngine:
    """
    Independent tax document certification layer.
    Implements P20A_001_DTE_CERTIFICATION_ENGINE.
    Single Financial Truth remains in the ledger; this layer purely matches totals 
    and validates legal coverage without altering the ledger.
    """
    def __init__(self, db: DatabaseV4 = None):
        self.db = db or DatabaseV4.get()
        
    def get_all_certifications(self) -> dict:
        mps = ["ml", "paris", "falabella", "ripley"]
        res = {"_meta": {"engine": "DocumentCertificationEngine v1"}}
        for mp in mps:
            if mp == "ripley":
                res[mp.upper()] = self._certify_ripley()
            elif mp == "paris":
                res[mp.upper()] = self._certify_paris()
            elif mp == "falabella":
                res[mp.upper()] = self._certify_falabella_transaction_chain()
            else:
                res[mp.upper()] = self._certify_direct(mp)
        return res

    def _certify_paris(self) -> dict:
        # Strategy: DOCUMENT_CHAIN
        # Uses document_match_v1 which hosts the mapped chain:
        # nro_solicitud_factura -> TpoDocRef=801 -> FolioRef -> Folio Tipo 33 -> numero_factura -> Liquidacion Tipo 43
        sql_ledger = """
            SELECT 
                COALESCE(SUM(ABS(l.monto)), 0) as total_monto,
                COALESCE(SUM(CASE 
                    WHEN l.folio_xml IS NOT NULL AND l.folio_xml != 'None' AND l.folio_xml != '' THEN ABS(l.monto) 
                    WHEN d.match_status = 'MATCHED' THEN ABS(l.monto) 
                    ELSE 0 
                END), 0) as monto_cert
            FROM marketplace_ledger_v1 l
            LEFT JOIN (
                SELECT DISTINCT ledger_id, match_status
                FROM document_match_v1
                WHERE LOWER(marketplace) = 'paris'
                  AND match_status = 'MATCHED'
            ) d ON l.id_transaccion = d.ledger_id
            WHERE LOWER(l.marketplace) = 'paris'
              AND l.financial_group IN ('costos_comerciales', 'costos_operacionales', 'ajustes')
        """
        df = self.db.query(sql_ledger)
        monto_elegible = float(df.iloc[0]["total_monto"]) if not df.empty else 0.0
        monto_cert = float(df.iloc[0]["monto_cert"]) if not df.empty else 0.0
        monto_sin = max(0, monto_elegible - monto_cert)
        
        cov = (monto_cert / monto_elegible * 100) if monto_elegible > 0 else 100.0
        if monto_elegible == 0 and monto_cert == 0:
            cov = 0.0
        
        return {
            "marketplace": "PARIS",
            "cobertura": round(cov, 1),
            "monto_elegible": monto_elegible,
            "monto_certificado": monto_cert,
            "monto_sin_respaldo": monto_sin,
            "estado_legal": "DOCUMENT_CHAIN_CERTIFIED",
            "nivel_evidencia": "DOCUMENT_CHAIN"
        }

    def _certify_falabella_transaction_chain(self) -> dict:
        import pandas as pd
        import glob
        
        # 1. Load mappings from Excel
        files = glob.glob('01_Raw/Falabella/Órdenes y Transacciones/*.xlsx')
        all_mappings = []
        for f in files:
            df_excel = pd.read_excel(f, skiprows=5)
            col_id_art = None
            col_orden = None
            for c in df_excel.columns:
                if 'Id Art' in c: col_id_art = c
                if 'N' in c and 'orden' in c and 'fecha' not in c.lower(): col_orden = c
            if col_id_art and col_orden:
                subset = df_excel[[col_id_art, col_orden]].dropna()
                subset.columns = ['id_transaccion', 'id_orden']
                subset['id_transaccion'] = subset['id_transaccion'].astype(str).str.replace('.0', '', regex=False)
                subset['id_orden'] = subset['id_orden'].astype(str).str.replace('.0', '', regex=False)
                all_mappings.append(subset)
                
        matched_orders_sql = "('__dummy__')"
        if all_mappings:
            df_mappings = pd.concat(all_mappings).drop_duplicates()
            # Get links
            df_links = self.db.query("SELECT id_transaccion FROM dte_link_v1 WHERE marketplace = 'FALABELLA'")
            if not df_links.empty:
                df_links['id_transaccion_str'] = df_links['id_transaccion'].astype(str).str.replace('.0', '', regex=False)
                merged = df_links.merge(df_mappings, left_on='id_transaccion_str', right_on='id_transaccion', how='inner')
                matched_orders = merged['id_orden'].dropna().unique().tolist()
                if matched_orders:
                    matched_orders_sql = "('" + "','".join(matched_orders) + "')"

        sql_ledger = f"""
            SELECT 
                COALESCE(SUM(ABS(monto)), 0) as total_monto,
                COALESCE(SUM(CASE 
                    WHEN folio_xml IS NOT NULL AND folio_xml != 'None' AND folio_xml != '' THEN ABS(monto) 
                    WHEN CAST(id_orden AS VARCHAR) IN {matched_orders_sql} THEN ABS(monto)
                    ELSE 0 
                END), 0) as monto_cert
            FROM marketplace_ledger_v1
            WHERE LOWER(marketplace) = 'falabella'
              AND financial_group IN ('costos_comerciales', 'costos_operacionales', 'ajustes')
        """
        df = self.db.query(sql_ledger)
        monto_elegible = float(df.iloc[0]["total_monto"]) if not df.empty else 0.0
        monto_cert = float(df.iloc[0]["monto_cert"]) if not df.empty else 0.0
        monto_sin = max(0, monto_elegible - monto_cert)
        
        cov = (monto_cert / monto_elegible * 100) if monto_elegible > 0 else 100.0
        if monto_elegible == 0 and monto_cert == 0:
            cov = 0.0
        
        return {
            "marketplace": "FALABELLA",
            "cobertura": round(cov, 1),
            "monto_elegible": monto_elegible,
            "monto_certificado": monto_cert,
            "monto_sin_respaldo": monto_sin,
            "estado_legal": "TRANSACTION_CHAIN_CERTIFIED",
            "nivel_evidencia": "TRANSACTION_CHAIN"
        }

    def _certify_direct(self, mp: str) -> dict:
        # Strategy: DIRECT_LINK (1:1)
        sql_ledger = """
            SELECT 
                COALESCE(SUM(ABS(monto)), 0) as total_monto,
                COALESCE(SUM(CASE WHEN folio_xml IS NOT NULL AND folio_xml != 'None' AND folio_xml != '' THEN ABS(monto) ELSE 0 END), 0) as monto_cert
            FROM marketplace_ledger_v1
            WHERE LOWER(marketplace) = ?
              AND financial_group IN ('costos_comerciales', 'costos_operacionales', 'ajustes')
        """
        df = self.db.query(sql_ledger, [mp])
        monto_elegible = float(df.iloc[0]["total_monto"]) if not df.empty else 0.0
        monto_cert = float(df.iloc[0]["monto_cert"]) if not df.empty else 0.0
        monto_sin = monto_elegible - monto_cert
        
        cov = (monto_cert / monto_elegible * 100) if monto_elegible > 0 else 100.0
        if monto_elegible == 0 and monto_cert == 0:
            cov = 0.0
        
        return {
            "marketplace": mp.upper(),
            "cobertura": round(cov, 1),
            "monto_elegible": monto_elegible,
            "monto_certificado": monto_cert,
            "monto_sin_respaldo": monto_sin,
            "estado_legal": "LEGAL_DOCUMENT",
            "nivel_evidencia": "DIRECT_LINK"
        }

    def _certify_ripley(self) -> dict:
        return self._certify_ripley_settlement_chain_v2()

    def _certify_ripley_settlement_chain_v2(self) -> dict:
        import pandas as pd
        import glob
        
        # 1. Map SELLER -> CICLOS to get fully certified orders
        files_seller = glob.glob('01_Raw/Ripley/SELLER/*.xlsx')
        all_seller = []
        for f in files_seller:
            df = pd.read_excel(f)
            col_fac = [c for c in df.columns if 'documento liquid' in c.lower()][0]
            all_seller.append(df[[col_fac]].dropna())
            
        seller_refs = set()
        if all_seller:
            df_seller = pd.concat(all_seller)
            df_seller.columns = ['settlement_ref']
            df_seller['settlement_ref'] = df_seller['settlement_ref'].astype(str).str.replace('.0', '', regex=False)
            seller_refs = set(df_seller['settlement_ref'].unique())

        files_ciclos = glob.glob('01_Raw/Ripley/Ciclos/*.csv')
        all_ciclos = []
        for f in files_ciclos:
            df = pd.read_csv(f, delimiter=';')
            col_fac = [c for c in df.columns if 'factura' in c.lower()][0]
            col_ord = [c for c in df.columns if 'order number' in c.lower() or 'orden' in c.lower()][0]
            all_ciclos.append(df[[col_fac, col_ord]].dropna())
            
        matched_orders_sql = "('__dummy__')"
        if all_ciclos:
            df_ciclos = pd.concat(all_ciclos)
            df_ciclos.columns = ['settlement_ref', 'order_id']
            df_ciclos['settlement_ref'] = df_ciclos['settlement_ref'].astype(str).str.replace('.0', '', regex=False)
            df_ciclos['order_id'] = df_ciclos['order_id'].astype(str)
            
            # Intersection: CICLOS orders that have a settlement_ref existing in SELLER
            matched = df_ciclos[df_ciclos['settlement_ref'].isin(seller_refs)]
            matched_orders = matched['order_id'].unique().tolist()
            if matched_orders:
                matched_orders_sql = "('" + "','".join(matched_orders) + "')"

        # 2. Get ledger totals by group for Ripley
        sql_ledger = f"""
            SELECT 
                COALESCE(SUM(ABS(monto)), 0) as total_monto,
                COALESCE(SUM(CASE 
                    WHEN CAST(id_orden AS VARCHAR) IN {matched_orders_sql} THEN ABS(monto)
                    ELSE 0 
                END), 0) as monto_cert
            FROM marketplace_ledger_v1
            WHERE LOWER(marketplace) = 'ripley'
              AND financial_group IN ('costos_comerciales', 'costos_operacionales', 'ajustes')
        """
        df = self.db.query(sql_ledger)
        monto_elegible = float(df.iloc[0]["total_monto"]) if not df.empty else 0.0
        monto_cert = float(df.iloc[0]["monto_cert"]) if not df.empty else 0.0
        
        monto_sin = max(0, monto_elegible - monto_cert)
        cov = (monto_cert / monto_elegible * 100) if monto_elegible > 0 else 100.0
        if monto_elegible == 0 and monto_cert == 0:
            cov = 0.0

        return {
            "marketplace": "RIPLEY",
            "cobertura": round(cov, 1),
            "monto_elegible": monto_elegible,
            "monto_certificado": monto_cert,
            "monto_sin_respaldo": monto_sin,
            "estado_legal": "SETTLEMENT_CERTIFIED",
            "nivel_evidencia": "SETTLEMENT_CHAIN_V2"
        }
