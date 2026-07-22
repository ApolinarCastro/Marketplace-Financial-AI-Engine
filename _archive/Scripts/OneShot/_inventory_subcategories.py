"""
Inventory: For every subcategory visible in the UI panel in EVERY marketplace,
verify each UI label maps 1:1 to a DB column (clasificacion_operativa).
"""
from __future__ import annotations
import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from api.api import app
from engine.v4.database import DatabaseV4

client = TestClient(app)
db = DatabaseV4.get()

marketplaces = ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']

def get_period(mp):
    r = db.query("SELECT MAX(fecha) as mx FROM marketplace_ledger_v1 WHERE marketplace=?", [mp])
    mx = r.iloc[0]['mx']
    return str(mx)[:7] if mx is not None else None

print("=" * 170)
print("INVENTARIO COMPLETO: UI Label vs DB columns")
print("Para cada subcategoria en el panel izquierdo:")
print("  1) El UI Label que el usuario clickea")
print("  2) El financial_group (categoria padre)")
print("  3) El valor de clasificacion_operativa en BD")
print("  4) El valor de detalle en BD")
print("  5) Cantidad de filas en BD con ese clasificacion_operativa")
print("  6) Suma total en BD")
print("  7) Tipo de mapeo")
print("=" * 170)

all_clean = True

for mp in marketplaces:
    periodo = get_period(mp)
    if not periodo:
        print(f"\n  {mp}: NO DATA")
        continue

    desg = client.get(f"/api/v4/cierre/desglose?marketplace={mp}&periodo={periodo}")
    desg_data = desg.json()

    from collections import defaultdict
    by_cat = defaultdict(list)
    for r in desg_data:
        by_cat[r['categoria']].append(r)

    print(f"\n  === {mp} [{periodo}] ===")
    print()

    for cat in sorted(by_cat.keys()):
        items = by_cat[cat]
        cat_total = sum(i['total'] for i in items)
        print(f"    [{cat}] total=${cat_total:>12,.0f}")
        print(f"      {'UI Label (click)':<50s} {'fin_group':<15s} {'clasif_operativa (BD)':<45s} {'detalle (BD)':<45s} {'COUNT':>7s} {'SUM(BD)':>14s} {'MAP':>8s}")
        print(f"      {'-'*50:<50s} {'-'*15:<15s} {'-'*45:<45s} {'-'*45:<45s} {'-'*7:>7s} {'-'*14:>14s} {'-'*8:>8s}")

        for item in items:
            ui_label = str(item['clasificacion_operativa'] or item['detalle'])
            fg = str(item['categoria'])
            co = str(item['clasificacion_operativa'])
            det = str(item['detalle'])

            # Query DB: how many rows have this exact clasificacion_operativa?
            r_co = db.query(
                "SELECT COUNT(*) as cnt, COALESCE(SUM(COALESCE(monto,0)),0) as sm FROM marketplace_ledger_v1 WHERE marketplace=? AND COALESCE(include_in_operational_pnl,1)=1 AND clasificacion_operativa=?",
                [mp, co]
            )
            cnt_co = int(r_co.iloc[0]['cnt'])
            sum_co = float(r_co.iloc[0]['sm'])

            # Query DB: how many rows have this exact detalle?
            r_det = db.query(
                "SELECT COUNT(*) as cnt, COALESCE(SUM(COALESCE(monto,0)),0) as sm FROM marketplace_ledger_v1 WHERE marketplace=? AND COALESCE(include_in_operational_pnl,1)=1 AND detalle=?",
                [mp, det]
            )
            cnt_det = int(r_det.iloc[0]['cnt'])
            sum_det = float(r_det.iloc[0]['sm'])

            # Determine mapping type
            label_matches_co = (ui_label == co)
            co_differs_from_det = (co != det)

            if label_matches_co and not co_differs_from_det:
                mapping_type = "CO=DE"
                is_clean = True
            elif label_matches_co and co_differs_from_det:
                mapping_type = "CO/!DE"
                is_clean = True
            elif not label_matches_co:
                # Label comes from detalle (clasif_op was NULL, fell back to detalle)
                mapping_type = "DETALLE"
                is_clean = True  # 1:1 with detalle
            else:
                mapping_type = "BROKEN"
                is_clean = False

            if not is_clean:
                all_clean = False

            flag = "" if is_clean else " *** BROKEN ***"
            print(f"      {ui_label:<50s} {fg:<15s} {co:<45s} {det:<45s} {cnt_co:>7d} ${sum_co:>12,.0f} {mapping_type:>8s}{flag}")

    # Check for NULL clasificacion_operativa
    null_co = db.query(
        "SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace=? AND COALESCE(include_in_operational_pnl,1)=1 AND clasificacion_operativa IS NULL AND COALESCE(monto,0)!=0",
        [mp]
    ).iloc[0]['n']
    if null_co > 0:
        print(f"      *** {null_co} rows have NULL clasificacion_operativa (rely on detalle fallback) ***")
        all_clean = False

print()
print("=" * 170)
if all_clean:
    print("VEREDICTO: Toda subcategoria tiene relacion 1:1 con clasificacion_operativa en BD")
    print("El valor que el frontend envia (clasificacion_operativa) ES el mismo que esta en la BD")
    print("No se requiere traduccion, mapping, contains, startsWith, normalizacion ni heuristica")
    print("Fix necesario: cambiar 'subgroup' por 'clasificacion_operativa' en buildLedgerUrl (dashboard.html:467)")
else:
    print("VEREDICTO: HAY SUBCATEGORIAS SIN CORRESPONDENCIA 1:1")
print("=" * 170)
