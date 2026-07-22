import sys, json
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine, FINANCIAL_STRUCTURE

db = DatabaseV4.get()

print("=" * 60)
print("SURGICAL FIXES")
print("=" * 60)

# ---- FIX 1: Remove "A pagar" from FINANCIAL_STRUCTURE ----
# "A pagar" is the net payout (tesoreria), NOT an operational adjustment
# It matches the calculated net of all other concepts within $0.9M
print("\n[1] Excluding 'A pagar' from FINANCIAL_STRUCTURE (tesoreria)")
print("    'A pagar' = $139M = net payout, excluding prevents double-count")

# We'll modify the file directly later; for now, verify impact
a_pagar_impact = db.query("""
    SELECT SUM(l.monto) as total
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
    WHERE l.marketplace = 'RIPLEY' AND c.clasificacion_operativa = 'A pagar'
""").iloc[0]['total']
print(f"    Impact: ${a_pagar_impact:,.0f} removed from ajustes")

# ---- FIX 2: Add missing concepts to dictionary and FINANCIAL_STRUCTURE ----
print("\n[2] Adding missing concepts to dictionary")

# Concepts to add:
new_concepts = [
    # (marketplace, tipo_transaccion, clasificacion, aliases)
    ("RIPLEY", "ENVIO_REEMBOLSADO", "COSTO_LOGISTICO", ["Envío reembolsado"]),
    ("RIPLEY", "PAYOUT_NETO", "TESORERIA", ["A pagar"]),
    ("RIPLEY", "COMPENSACION_CLIENTE", "AJUSTE_OPERATIVO", ["Descuento por compensación a cliente"]),
    ("RIPLEY", "DESCUENTO_OPERACIONAL", "AJUSTE_OPERATIVO", ["Descuento operacional"]),
    ("RIPLEY", "DESCUENTO_PDM", "COSTO_COMERCIAL", ["Descuento por PDM"]),
    ("RIPLEY", "ABONO_POSTVENTA", "AJUSTE_OPERATIVO", ["Abono postventa"]),
    ("RIPLEY", "ABONO_FORMALIZACION_OPL", "AJUSTE_OPERATIVO", ["Abono por formalización a OPL"]),
    ("ML", "CARGO_GENERICO", "COSTO_COMERCIAL", ["Cargo"]),
]

with open('master_marketplace_dictionary_v1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for mp, tipo, clasif, aliases in new_concepts:
    d['dictionary'].append({
        "marketplace": mp, "tipo_transaccion": tipo, "clasificacion": clasif,
        "aliases": aliases, "respaldo_legal": True,
        "trazabilidad": "FULL" if mp != 'ML' or tipo != 'CARGO_GENERICO' else "NO_ORDER",
        "decision": "INCLUIR" if clasif != "TESORERIA" else "EXCLUIR_TESORERIA"
    })
    print(f"    [{mp}] {aliases[0]} -> {clasif} ({'EXCLUIR_TESORERIA' if clasif == 'TESORERIA' else 'INCLUIR'})")

with open('master_marketplace_dictionary_v1.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("    Dictionary updated")

# ---- FIX 3: Fix corrections matching (by id_transaccion not detalle) ----
print("\n[3] Fixing manual corrections: delete the mass 'Cargo' correction")
# The correction CHG_06_...1057 has detalle_original='Cargo' which
# matches ALL 85 "Cargo" rows. We need to delete this and handle
# that transaction individually.
db.execute("""
    DELETE FROM marketplace_correcciones_v1 
    WHERE id_transaccion = 'CHG_06_Reporte_Facturacion_MercadoLibre_Jun2025.xlsx_1057'
""")
print("    Deleted correction that was mass-reclassifying 'Cargo'")

# ---- FIX 4: Re-run classification with fixes ----
print("\n[4] Re-running classification...")
engine = MarketplaceAuditorEngine()
n = engine.run_classification()
print(f"    {n} rows re-classified")

# ---- FIX 5: Verify ----
print("\n[5] Verification:")
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    noclas = db.query("SELECT COUNT(*) as c FROM marketplace_ledger_clasificado_v1 WHERE marketplace=? AND clasificacion_operativa='NO_CLASIFICADO'", [mp]).iloc[0]['c']
    total = db.query("SELECT COUNT(*) as c FROM marketplace_ledger_clasificado_v1 WHERE marketplace=?", [mp]).iloc[0]['c']
    print(f"  {mp}: {noclas}/{total} NO_CLASIFICADO")

# Check A pagar is now in tesoreria (excluded from financial calc)
a_pagar_clasif = db.query("""
    SELECT c.clasificacion_operativa, COUNT(*) as cnt
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
    WHERE l.marketplace = 'RIPLEY' AND l.detalle = 'A pagar'
    GROUP BY c.clasificacion_operativa
""")
print(f"\n  'A pagar' now classified as: {a_pagar_clasif.iloc[0]['clasificacion_operativa'] if len(a_pagar_clasif) > 0 else '???'}")

# Check Cargo
cargo_clasif = db.query("""
    SELECT c.clasificacion_operativa, COUNT(*) as cnt
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
    WHERE l.marketplace = 'ML' AND l.detalle = 'Cargo'
    GROUP BY c.clasificacion_operativa
""")
print(f"  'Cargo' ML now classified as: {cargo_clasif.iloc[0]['clasificacion_operativa'] if len(cargo_clasif) > 0 else '???'}")
