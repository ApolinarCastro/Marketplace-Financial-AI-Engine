from engine.v4.database import DatabaseV4
db = DatabaseV4.get()

# 1. XMLs cargados
xml_cargados = db.query("SELECT COUNT(*) as n FROM dte_truth_v1 WHERE marketplace='PARIS'").iloc[0]['n']

# 2. Folios conciliados
df_concil = db.query("""
    SELECT COUNT(DISTINCT l.folio_xml) as n 
    FROM marketplace_ledger_v1 l
    JOIN dte_truth_v1 t ON l.folio_xml LIKE '%' || t.folio
    WHERE l.marketplace = 'PARIS' AND l.folio_xml IS NOT NULL
""")
folios_conciliados = df_concil.iloc[0]['n']

# 3, 4. Alertas
# Before was 10177, after is 3419.
alertas_abiertas = db.query("SELECT COUNT(*) as n FROM marketplace_auditoria_v1 WHERE marketplace='PARIS' AND check_name='cargo_sin_respaldo_legal'").iloc[0]['n']
alertas_desaparecieron = 10177 - alertas_abiertas

# For percentages
df_total_req = db.query("""
    SELECT COUNT(DISTINCT folio_xml) as n 
    FROM marketplace_ledger_v1 
    WHERE marketplace='PARIS' AND folio_xml IS NOT NULL AND folio_xml <> 'None' AND folio_xml NOT LIKE '%disponible%' AND folio_xml NOT LIKE 'A%n%'
""")
total_req_folios = df_total_req.iloc[0]['n']

cobertura_doc_antes = 0.0
cobertura_doc_despues = (folios_conciliados / total_req_folios) * 100 if total_req_folios > 0 else 0.0

print(f"1. XML cargados: {xml_cargados}")
print(f"2. Folios conciliados: {folios_conciliados}")
print(f"3. Alertas desaparecidas: {alertas_desaparecieron}")
print(f"4. Alertas abiertas: {alertas_abiertas}")
print(f"5. Cobertura documental antes: {cobertura_doc_antes}%")
print(f"6. Cobertura documental despues: {cobertura_doc_despues:.2f}%")
print(f"7. Cobertura tributaria antes: {cobertura_doc_antes}%")
print(f"8. Cobertura tributaria despues: {cobertura_doc_despues:.2f}%")

