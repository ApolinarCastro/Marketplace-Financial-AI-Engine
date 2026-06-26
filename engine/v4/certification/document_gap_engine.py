from engine.v4.database import DatabaseV4
import pandas as pd

class DocumentGapEngine:
    def __init__(self):
        self.db = DatabaseV4.get()
        self.eligible_groups = ['costos_comerciales', 'costos_operacionales', 'ajustes']
        self.gap_taxonomy = {
            'CERTIFIED': {'severity': 'NONE', 'description': 'Movimiento completamente certificado.'},
            'XML_MISSING': {'severity': 'HIGH', 'description': 'No existe XML asociado.'},
            'BROKEN_REFERENCE': {'severity': 'HIGH', 'description': 'Existe XML pero no puede enlazarse.'},
            'SETTLEMENT_PENDING': {'severity': 'MEDIUM', 'description': 'Settlement aun no consolidado.'},
            'INVALID_DTE': {'severity': 'HIGH', 'description': 'Documento tributario invalido.'},
            'DUPLICATED_DOCUMENT': {'severity': 'MEDIUM', 'description': 'Documento duplicado.'},
            'OUTSIDE_ELIGIBLE_UNIVERSE': {'severity': 'INFO', 'description': 'Movimiento fuera del universo certificable.'}
        }
        
    def get_document_gaps(self, marketplace=None, limit=500):
        # Placeholder implementation querying the ledger
        where_clause = f"WHERE marketplace='{marketplace}'" if marketplace and marketplace != 'ALL' else "WHERE 1=1"
        query = f"""
            SELECT 
                l.marketplace,
                l.fecha as periodo,
                l.financial_group,
                l.id_transaccion as transaction_id,
                l.id_orden as order_id,
                l.folio_xml,
                l.monto,
                d.match_status,
                d.match_rule
            FROM marketplace_ledger_v1 l
            LEFT JOIN (
                SELECT DISTINCT ledger_id, match_status, match_rule 
                FROM document_match_v1
            ) d ON l.id_transaccion = d.ledger_id
            {where_clause}
            LIMIT {limit}
        """
        df = self.db.query(query)
        if df.empty:
            return []
            
        # Dynamically map Falabella transaction chain
        import glob
        db = DatabaseV4.get()

        # Load dynamic mapping for Falabella
        files = glob.glob('01_Raw/Falabella/Órdenes y Transacciones/*.xlsx')
        falabella_matched_orders = set()
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
                
        if all_mappings:
            df_mappings = pd.concat(all_mappings).drop_duplicates()
            df_links = db.query("SELECT id_transaccion FROM dte_link_v1 WHERE marketplace = 'FALABELLA'")
            if not df_links.empty:
                df_links['id_transaccion_str'] = df_links['id_transaccion'].astype(str).str.replace('.0', '', regex=False)
                merged = df_links.merge(df_mappings, left_on='id_transaccion_str', right_on='id_transaccion', how='inner')
                falabella_matched_orders = set(merged['id_orden'].dropna().unique().tolist())

        # Load dynamic mapping for Ripley (SETTLEMENT_CHAIN_V2)
        ripley_matched_orders = set()
        files_seller = glob.glob('01_Raw/Ripley/SELLER/*.xlsx')
        all_seller = []
        for f in files_seller:
            df_s = pd.read_excel(f)
            col_fac = [c for c in df_s.columns if 'documento liquid' in c.lower()][0]
            all_seller.append(df_s[[col_fac]].dropna())
            
        seller_refs = set()
        if all_seller:
            df_seller = pd.concat(all_seller)
            df_seller.columns = ['settlement_ref']
            df_seller['settlement_ref'] = df_seller['settlement_ref'].astype(str).str.replace('.0', '', regex=False)
            seller_refs = set(df_seller['settlement_ref'].unique())

        files_ciclos = glob.glob('01_Raw/Ripley/Ciclos/*.csv')
        all_ciclos = []
        for f in files_ciclos:
            df_c = pd.read_csv(f, delimiter=';')
            col_fac = [c for c in df_c.columns if 'factura' in c.lower()][0]
            col_ord = [c for c in df_c.columns if 'order number' in c.lower() or 'orden' in c.lower()][0]
            all_ciclos.append(df_c[[col_fac, col_ord]].dropna())
            
        if all_ciclos:
            df_ciclos = pd.concat(all_ciclos)
            df_ciclos.columns = ['settlement_ref', 'order_id']
            df_ciclos['settlement_ref'] = df_ciclos['settlement_ref'].astype(str).str.replace('.0', '', regex=False)
            df_ciclos['order_id'] = df_ciclos['order_id'].astype(str)
            
            matched_rip = df_ciclos[df_ciclos['settlement_ref'].isin(seller_refs)]
            ripley_matched_orders = set(matched_rip['order_id'].unique().tolist())
            
        results = []
        for _, row in df.iterrows():
            fg = row.get('financial_group', '')
            folio = row.get('folio_xml')
            
            estado = 'CERTIFIED'
            causa = 'N/A'
            accion = 'Ninguna'
            
            if fg not in self.eligible_groups:
                estado = 'OUTSIDE_ELIGIBLE_UNIVERSE'
                causa = 'Grupo no requiere DTE'
            elif row.get('match_status') == 'MATCHED' or \
                 (str(row['marketplace']).upper() == 'FALABELLA' and str(row['order_id']) in falabella_matched_orders) or \
                 (str(row['marketplace']).upper() == 'RIPLEY' and str(row['order_id']) in ripley_matched_orders):
                estado = 'CERTIFIED'
                if str(row['marketplace']).upper() == 'FALABELLA':
                    causa = 'TRANSACTION_CHAIN'
                elif str(row['marketplace']).upper() == 'RIPLEY':
                    causa = 'SETTLEMENT_CHAIN_V2'
                else:
                    causa = 'DOCUMENT_CHAIN'
                accion = 'Ninguna'
            elif pd.isna(folio) or not str(folio).strip() or str(folio) == 'nan' or str(folio) == 'None':
                estado = 'XML_MISSING'
                causa = 'Falta folio XML'
                accion = 'Subir o conciliar XML'
            
            results.append({
                'marketplace': row['marketplace'],
                'periodo': row['periodo'],
                'financial_group': fg,
                'transaction_id': row['transaction_id'],
                'order_id': row['order_id'],
                'document_type': 'Desconocido',
                'expected_dte': 'N/A',
                'actual_dte': 'N/A',
                'folio': str(folio) if pd.notna(folio) else '',
                'monto': float(row['monto']) if pd.notna(row['monto']) else 0.0,
                'estado_documental': estado,
                'causa': causa,
                'accion_recomendada': accion,
                'evidence_level': 5 if row['marketplace'] in ['ML', 'FALABELLA'] else (4 if row['marketplace'] == 'PARIS' else 3)
            })
            
        return results

    def get_risk_summary(self):
        from engine.v4.certification.document_certification import DocumentCertificationEngine
        cert_engine = DocumentCertificationEngine()
        res = cert_engine.get_all_certifications()
        
        summary = {
            'widgets': {},
            'marketplaces': res,
            'top_risks': [
                {'riesgo': 'Falta XML Costos Comerciales ML', 'impacto': 'Alto'},
                {'riesgo': 'Settlement pendiente Ripley', 'impacto': 'Medio'}
            ]
        }
        return summary
