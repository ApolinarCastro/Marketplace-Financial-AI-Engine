import sys, warnings; sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine'); warnings.filterwarnings('ignore')
import duckdb, json

con = duckdb.connect(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\meli_financial_v4.db', read_only=True)

def q(sql):
    try: return con.execute(sql).fetchdf()
    except Exception as e: return f"ERROR: {e}"

def s(sql):
    try:
        r = con.execute(sql).fetchdf().iloc[0]
        return dict(r)
    except Exception as e: return f"ERROR: {e}"

results = {}

# ===== FASE 1: SINGLE FINANCIAL TRUTH =====
results['fase1'] = {}

# 1. Row counts
for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    l = s(f"SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace='{mp}'")
    cl = s(f"SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 WHERE marketplace='{mp}'")
    cf = s(f"SELECT COUNT(*) as n FROM marketplace_cierre_financiero_v1 WHERE marketplace='{mp}'")
    delta_rows = int(l['n']) - int(cl['n'])
    results['fase1'][mp] = {
        'ledger_rows': int(l['n']),
        'clasificado_rows': int(cl['n']),
        'cierre_rows': int(cf['n']),
        'delta_ledger_vs_clasificado_rows': delta_rows
    }

# 2. Monetary deltas
results['fase1']['monetary'] = {}
total_ledger = s("SELECT COALESCE(ROUND(SUM(monto),0),0) as t FROM marketplace_ledger_v1")
total_clasif = s("SELECT COALESCE(ROUND(SUM(monto),0),0) as t FROM marketplace_ledger_clasificado_v1")
results['fase1']['monetary']['ledger_total'] = float(total_ledger['t'])
results['fase1']['monetary']['clasificado_total'] = float(total_clasif['t'])
results['fase1']['monetary']['delta_ledger_vs_clasificado'] = float(total_ledger['t']) - float(total_clasif['t'])

# 3. Per MP monetary check ledger vs clasificado
results['fase1']['monetary_per_mp'] = {}
for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    l = s(f"SELECT COALESCE(ROUND(SUM(monto),0),0) as t FROM marketplace_ledger_v1 WHERE marketplace='{mp}'")
    c = s(f"SELECT COALESCE(ROUND(SUM(monto),0),0) as t FROM marketplace_ledger_clasificado_v1 WHERE marketplace='{mp}'")
    neto = s(f"SELECT COALESCE(ROUND(SUM(resultado_neto),0),0) as t FROM marketplace_cierre_financiero_v1 WHERE marketplace='{mp}'")
    results['fase1']['monetary_per_mp'][mp] = {
        'ledger': float(l['t']),
        'clasificado': float(c['t']),
        'cierre_neto': float(neto['t']),
        'delta_ledger_clasif': float(l['t']) - float(c['t']),
        'delta_clasif_cierre': float(c['t']) - float(neto['t'])
    }

# 4. Check for UNCLASSIFIED rows
results['fase1']['unclassified'] = {}
for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    r = s(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(monto),0),0) as t FROM marketplace_ledger_clasificado_v1 WHERE marketplace='{mp}' AND clasificacion_operativa='NO_CLASIFICADO'")
    results['fase1']['unclassified'][mp] = {'rows': int(r['n']), 'amount': float(r['t'])}

# ===== FASE 2: DATA FRESHNESS =====
results['fase2'] = {}
for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    raw = s(f"SELECT MIN(fecha) as min_f, MAX(fecha) as max_f, COUNT(*) as n, COALESCE(ROUND(SUM(monto),0),0) as t FROM marketplace_ledger_v1 WHERE marketplace='{mp}'")
    clasif = s(f"SELECT MIN(fecha) as min_f, MAX(fecha) as max_f FROM marketplace_ledger_clasificado_v1 WHERE marketplace='{mp}'")
    cierre = s(f"SELECT MIN(periodo_inicio) as min_f, MAX(periodo_fin) as max_f FROM marketplace_cierre_financiero_v1 WHERE marketplace='{mp}'")
    jun = s(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(monto),0),0) as t FROM marketplace_ledger_v1 WHERE marketplace='{mp}' AND fecha >= '2026-06-01' AND fecha <= '2026-06-30'")
    results['fase2'][mp] = {
        'ledger_min': str(raw['min_f']),
        'ledger_max': str(raw['max_f']),
        'ledger_rows': int(raw['n']),
        'ledger_total': float(raw['t']),
        'clasif_min': str(clasif['min_f']),
        'clasif_max': str(clasif['max_f']),
        'cierre_min': str(cierre['min_f']),
        'cierre_max': str(cierre['max_f']),
        'junio_rows': int(jun['n']),
        'junio_amount': float(jun['t'])
    }

# ===== FASE 4: AUDIT =====
results['fase4'] = {}
total_audit = s("SELECT COUNT(*) as n FROM marketplace_auditoria_v1")
results['fase4']['total_rows'] = int(total_audit['n'])
results['fase4']['per_mp'] = {}
for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    r = s(f"SELECT COUNT(*) as n FROM marketplace_auditoria_v1 WHERE marketplace='{mp}'")
    results['fase4']['per_mp'][mp] = int(r['n'])

results['fase4']['breakdown'] = q("SELECT marketplace, check_name, COUNT(*) as n FROM marketplace_auditoria_v1 GROUP BY marketplace, check_name ORDER BY marketplace, n DESC")

# ML specifically - check dte_truth and audit_ml
results['fase4']['ml_details'] = {}
try:
    dte = s("SELECT COUNT(*) as n FROM dte_truth_v1")
    results['fase4']['ml_details']['dte_truth_rows'] = int(dte['n'])
except: results['fase4']['ml_details']['dte_truth_rows'] = 0

# Check if audit_ml_misclassifications produces rows
try:
    ml_audit_check = s("SELECT COUNT(*) as n FROM marketplace_auditoria_v1 WHERE marketplace='ML' AND check_name='ml_misclassification'")
    results['fase4']['ml_details']['ml_misclassification_rows'] = int(ml_audit_check['n'])
except: results['fase4']['ml_details']['ml_misclassification_rows'] = 0

# Check cargo_sin_respaldo_legal for ML
try:
    legal_check = q("""
        SELECT l.folio_xml, l.id_orden FROM marketplace_ledger_v1 l
        LEFT JOIN dte_truth_v1 t ON l.folio_xml LIKE '%' || t.folio
        WHERE l.marketplace='ML' AND l.folio_xml IS NOT NULL AND l.folio_xml NOT LIKE 'None'
        AND l.folio_xml NOT LIKE '%disponible%' AND l.folio_xml NOT LIKE 'A%n%'
        AND t.folio IS NULL
        AND l.fecha > '2025-12-31'
        LIMIT 5
    """)
    results['fase4']['ml_details']['legal_check_sample'] = len(legal_check)
except Exception as e:
    results['fase4']['ml_details']['legal_check_sample'] = f"ERROR: {e}"

# Check what ML audit rows exist
results['fase4']['ml_existing_rows'] = q("SELECT * FROM marketplace_auditoria_v1 WHERE marketplace='ML' LIMIT 5")

# ===== SUMMARY FOR FASE 1 =====
# LEDGER = CLASIFICACION check
all_match = True
for mp, data in results['fase1']['monetary_per_mp'].items():
    if data['delta_ledger_clasif'] != 0 or data['delta_clasif_cierre'] != 0:
        all_match = False

results['fase1']['all_match'] = all_match

print(json.dumps(results, indent=2, default=str))
con.close()
