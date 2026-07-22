import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

xml_dir = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\RIPLEY\Documentos Recepcionados")
xml_files = list(xml_dir.glob("*.xml"))

print("--- 1. ESTADÍSTICAS XML ---")
print(f"Archivos XML detectados: {len(xml_files)}")

data = []
validos = 0
rechazados = 0
motivos = {}

for f in xml_files:
    try:
        tree = ET.parse(f)
        root = tree.getroot()
        
        def get_text(node, tag):
            for elem in node.iter():
                if tag in elem.tag:
                    return elem.text
            return None

        # Extract Folio
        folio = get_text(root, 'Folio')
        tpo_dte = get_text(root, 'TipoDTE')
        fch_emis = get_text(root, 'FchEmis')
        rut_emisor = get_text(root, 'RUTEmisor') or get_text(root, 'RutEmisor')
        rut_receptor = get_text(root, 'RUTRecep') or get_text(root, 'RutReceptor')
        rzn_soc = get_text(root, 'RznSoc')
        mnt_neto = get_text(root, 'MntNeto')
        iva = get_text(root, 'IVA')
        mnt_total = get_text(root, 'MntTotal')
        
        if not folio:
            rechazados += 1
            motivos['Falta Folio'] = motivos.get('Falta Folio', 0) + 1
            continue
            
        data.append({
            'Folio': str(folio).strip(),
            'TpoDTE': str(tpo_dte).strip() if tpo_dte else '',
            'FchEmis': fch_emis,
            'RutEmisor': rut_emisor,
            'RutReceptor': rut_receptor,
            'RznSoc': rzn_soc,
            'MntNeto': float(mnt_neto) if mnt_neto else 0.0,
            'IVA': float(iva) if iva else 0.0,
            'MntTotal': float(mnt_total) if mnt_total else 0.0
        })
        validos += 1
    except Exception as e:
        rechazados += 1
        err = str(e)[:50]
        motivos[err] = motivos.get(err, 0) + 1

print(f"XML válidos procesados: {validos}")
print(f"XML rechazados: {rechazados}")
if rechazados > 0:
    print("Motivos de rechazo:", motivos)

df_xml = pd.DataFrame(data)

if len(df_xml) > 0:
    print(f"Folios únicos detectados: {df_xml['Folio'].nunique()}")
    print("Emisores detectados:")
    print(df_xml.groupby(['RutEmisor', 'RznSoc']).size().reset_index(name='count').to_string(index=False))
    print("\nTotales tributarios acumulados en XML:")
    print(f"Total Neto: ${df_xml['MntNeto'].sum():,.0f}")
    print(f"Total IVA:  ${df_xml['IVA'].sum():,.0f}")
    print(f"Total Fact: ${df_xml['MntTotal'].sum():,.0f}")

print("\n--- 2. MATCHING TRIBUTARIO (Ciclos vs XML) ---")

q_ciclos = """
SELECT 
    folio_xml,
    COUNT(DISTINCT id_orden) as ordenes,
    SUM(CASE WHEN detalle='Comisión' THEN monto ELSE 0 END) as comision,
    SUM(CASE WHEN detalle='Impuestos' THEN monto ELSE 0 END) as iva
FROM marketplace_ledger_v1
WHERE marketplace='RIPLEY' AND folio_xml IS NOT NULL AND folio_xml != ''
GROUP BY folio_xml
"""
df_ciclos = db.query(q_ciclos)

if df_ciclos.empty or len(df_xml) == 0:
    print("No hay datos en Ciclos para matching.")
else:
    # Ensure types match
    df_ciclos['folio_xml'] = df_ciclos['folio_xml'].astype(str).str.split('.').str[0].str.strip()
    df_xml['Folio'] = df_xml['Folio'].astype(str).str.strip()

    # Convert positive in ciclos because commission is usually negative in ledger
    df_ciclos['comision_abs'] = df_ciclos['comision'].abs()
    df_ciclos['iva_abs'] = df_ciclos['iva'].abs()
    df_ciclos['total_facturado_ciclos'] = df_ciclos['comision_abs'] + df_ciclos['iva_abs']

    match_df = pd.merge(df_ciclos, df_xml, left_on='folio_xml', right_on='Folio', how='outer', indicator=True)

    exact_match = match_df[match_df['_merge'] == 'both'].copy()
    ciclos_only = match_df[match_df['_merge'] == 'left_only'].copy()
    xml_only = match_df[match_df['_merge'] == 'right_only'].copy()

    print(f"Match exacto (folio): {len(exact_match)}")
    print(f"Sin match en XML (solo en Ciclos): {len(ciclos_only)}")
    print(f"Sin match en Ciclos (solo en XML): {len(xml_only)}")
    
    total_folios_in_ciclos = len(df_ciclos)
    if total_folios_in_ciclos > 0:
        print(f"% conciliación (folios Ciclos que tienen XML): {(len(exact_match)/total_folios_in_ciclos)*100:.2f}%")

    print("\n--- 3. VALIDACIÓN TRIBUTARIA (Diferencias en Montos) ---")
    if len(exact_match) > 0:
        exact_match['diff_comision_neto'] = exact_match['MntNeto'] - exact_match['comision_abs']
        exact_match['diff_iva'] = exact_match['IVA'] - exact_match['iva_abs']
        exact_match['diff_total'] = exact_match['MntTotal'] - exact_match['total_facturado_ciclos']

        # Summarize
        print("Totales en Ciclos (sobre folios matched):")
        print(f"  Neto (Comisión):  ${exact_match['comision_abs'].sum():,.0f}")
        print(f"  IVA:              ${exact_match['iva_abs'].sum():,.0f}")
        print(f"  Total:            ${exact_match['total_facturado_ciclos'].sum():,.0f}")

        print("\nTotales en XML DTE (sobre folios matched):")
        print(f"  MntNeto:          ${exact_match['MntNeto'].sum():,.0f}")
        print(f"  IVA:              ${exact_match['IVA'].sum():,.0f}")
        print(f"  MntTotal:         ${exact_match['MntTotal'].sum():,.0f}")

        diff_neto = exact_match['diff_comision_neto'].sum()
        diff_iva = exact_match['diff_iva'].sum()
        diff_tot = exact_match['diff_total'].sum()

        print("\nDiferencias Absolutas (XML - Ciclos):")
        print(f"  Neto:  ${diff_neto:,.0f} ({(diff_neto/exact_match['MntNeto'].sum())*100 if exact_match['MntNeto'].sum() else 0:.4f}%)")
        print(f"  IVA:   ${diff_iva:,.0f} ({(diff_iva/exact_match['IVA'].sum())*100 if exact_match['IVA'].sum() else 0:.4f}%)")
        print(f"  Total: ${diff_tot:,.0f} ({(diff_tot/exact_match['MntTotal'].sum())*100 if exact_match['MntTotal'].sum() else 0:.4f}%)")
        
        print("\nEjemplo de diferencias a nivel folio (primeros 5 con diferencia > $10):")
        with_diff = exact_match[exact_match['diff_total'].abs() > 10].head(5)
        if len(with_diff) > 0:
            print(with_diff[['folio_xml', 'comision_abs', 'MntNeto', 'iva_abs', 'IVA', 'total_facturado_ciclos', 'MntTotal', 'diff_total']].to_string())
        else:
            print("No hay diferencias significativas mayores a $10 a nivel folio.")
    else:
        print("No hay match para comparar montos.")

    print("\n--- 4. RIESGOS ---")
    duplicate_folios = df_xml[df_xml.duplicated(['Folio'], keep=False)]
    if len(duplicate_folios) > 0:
        print(f"Folios duplicados en XML: {duplicate_folios['Folio'].nunique()}")
    else:
        print("Folios duplicados en XML: 0")
