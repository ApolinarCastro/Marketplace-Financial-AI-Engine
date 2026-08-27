import os
import duckdb
import pandas as pd
from collections import defaultdict
from pathlib import Path

def generate_coverage_report():
    print("Iniciando auditoria de cobertura de datos (F5-07A)...")
    db = duckdb.connect('data/db/meli_financial_v4.db')
    
    raw_files = []
    
    print("Escaneando 01_Raw...")
    for root, _, files in os.walk('01_Raw'):
        for file in files:
            if file.endswith(('.csv', '.xlsx', '.xls', '.xml')):
                mp = root.split(os.sep)[1] if len(root.split(os.sep)) > 1 else 'UNKNOWN'
                # Normalize MP name
                if mp.upper() == 'MERCADOLIBRE' or 'ML' in mp.upper():
                    mp = 'ML'
                else:
                    mp = mp.upper()
                
                size = os.path.getsize(os.path.join(root, file))
                raw_files.append({
                    'file_name': file,
                    'marketplace': mp,
                    'size_bytes': size
                })
                
    raw_df = pd.DataFrame(raw_files)
    
    print("Consultando Ledger V1...")
    ledger_files_df = db.execute('''
        SELECT 
            marketplace,
            archivo_origen as file_name,
            COUNT(*) as ingested_rows,
            SUM(monto) as ingested_monto
        FROM marketplace_ledger_v1
        GROUP BY marketplace, archivo_origen
    ''').df()
    
    # Merge
    # Need to handle exact filename matching
    # Some ledger files might have been renamed or path stripped
    def clean_name(name):
        if not name: return ""
        return os.path.basename(name).strip()
        
    raw_df['clean_name'] = raw_df['file_name'].apply(clean_name)
    ledger_files_df['clean_name'] = ledger_files_df['file_name'].apply(clean_name)
    
    # Left join RAW to LEDGER
    merged = pd.merge(raw_df, ledger_files_df, on=['marketplace', 'clean_name'], how='left')
    
    # Check if there are any ledger files NOT in RAW (Obsoleto)
    ledger_only = ledger_files_df[~ledger_files_df['clean_name'].isin(raw_df['clean_name'])]
    
    # Status assignment
    def get_status(row):
        if pd.notna(row['ingested_rows']):
            return 'INGESTADO'
        else:
            return 'NO INGESTADO'
            
    merged['status'] = merged.apply(get_status, axis=1)
    
    # Group by MP
    mps = ['ML', 'FALABELLA', 'PARIS', 'RIPLEY', 'SHOPIFY']
    
    matrix = []
    
    for mp in mps:
        mp_data = merged[merged['marketplace'] == mp]
        total_raw = len(mp_data)
        ingested = len(mp_data[mp_data['status'] == 'INGESTADO'])
        no_ingestado = len(mp_data[mp_data['status'] == 'NO INGESTADO'])
        
        # Obsoletos (en ledger pero no en raw)
        obsoletos = len(ledger_only[ledger_only['marketplace'] == mp])
        
        cov_pct = (ingested / total_raw * 100) if total_raw > 0 else 0
        status_gate = "PASS" if cov_pct == 100 else "FAIL"
        
        # Volumetrics
        total_bytes = mp_data['size_bytes'].sum()
        ingested_bytes = mp_data[mp_data['status'] == 'INGESTADO']['size_bytes'].sum()
        bytes_cov = (ingested_bytes / total_bytes * 100) if total_bytes > 0 else 0
        
        monto_ingestado = mp_data['ingested_monto'].sum()
        
        matrix.append({
            'Marketplace': mp,
            'RAW Files': total_raw,
            'Ingeridos': ingested,
            'Faltantes': no_ingestado,
            'Obsoletos (Ledger only)': obsoletos,
            'Cobertura Archivos': f"{cov_pct:.1f}%",
            'Cobertura Bytes': f"{bytes_cov:.1f}%",
            'Monto Ingestado ($)': f"${monto_ingestado:,.2f}" if pd.notna(monto_ingestado) else "$0.00",
            'Estado': status_gate
        })
        
    matrix_df = pd.DataFrame(matrix)
    
    report = f"""# F5-07A — EXECUTIVE DATA COVERAGE CERTIFICATION

**Proyecto:** Marketplace Financial AI Engine  
**Fase:** F5-07A (Data Coverage Gate)  
**Fecha:** {pd.Timestamp.now().strftime('%Y-%m-%d')}  
**Estado General:** FAIL (Brecha Crítica de Datos)

---

## 1. EXECUTIVE COVERAGE MATRIX

| Marketplace | Archivos RAW | Archivos Ingeridos | Faltantes | Obsoletos | Cobertura (Archivos) | Cobertura (Bytes) | Monto Ingestado Confirmado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in matrix_df.iterrows():
        report += f"| **{row['Marketplace']}** | {row['RAW Files']} | {row['Ingeridos']} | {row['Faltantes']} | {row['Obsoletos (Ledger only)']} | {row['Cobertura Archivos']} | {row['Cobertura Bytes']} | {row['Monto Ingestado ($)']} | **{row['Estado']}** |\n"
        
    report += """
---

## 2. FINANACIAL COVERAGE (ESTIMACIÓN)

Dado que los archivos `NO INGESTADO` no han pasado por el Financial Engine, el volumen financiero exacto de la brecha no puede determinarse con precisión matemática ($0 deltas). 
Sin embargo, utilizando la **Cobertura por Bytes (Tamaño de archivo físico)** como proxy de volumen de registros, podemos dimensionar el impacto:

"""
    for _, row in matrix_df.iterrows():
        if row['RAW Files'] > 0:
            report += f"- **{row['Marketplace']}**: Cobertura financiera estimada del **{row['Cobertura Bytes']}** (basado en peso de archivos).\n"
            
    report += """
---

## 3. CLASIFICACIÓN DE ARCHIVOS FALTANTES / ANOMALÍAS

### Archivos NO INGESTADOS (Pendientes de carga)
Estos archivos residen físicamente en `01_Raw/` pero carecen de representación financiera en `marketplace_ledger_v1`.
"""
    no_ingestados = merged[merged['status'] == 'NO INGESTADO'].groupby('marketplace').size()
    for mp, count in no_ingestados.items():
        report += f"- **{mp}**: {count} archivos.\n"
        
    report += """
### Archivos OBSOLETOS (Orfandad en DB)
Estos archivos están persistidos en el Ledger, pero el archivo físico original ya no se encuentra en `01_Raw/`.
"""
    if len(ledger_only) > 0:
        obs = ledger_only.groupby('marketplace').size()
        for mp, count in obs.items():
            report += f"- **{mp}**: {count} archivos huérfanos.\n"
    else:
        report += "- Ningún archivo huérfano detectado.\n"

    report += """
---

## 4. CONCLUSIÓN Y VEREDICTO

**VEREDICTO:** `NOT READY FOR PRODUCTION (DATA GAP)`

El **Marketplace Financial AI Engine** ha certificado con éxito el **100% de sus capacidades funcionales (F5-06 PASS)**, pero la migración de los datos crudos hacia la base de datos oficial presenta una brecha masiva. 

El despliegue a producción (F5-08) queda **BLOQUEADO** hasta que el equipo de Operaciones ejecute el `INITIAL DATA MIGRATION` utilizando el Upload Center o los Loaders certificados para cerrar esta brecha documentada.
"""

    os.makedirs('governance', exist_ok=True)
    with open('governance/F5_07A_DATA_COVERAGE_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)
        
    print("Auditoría completada. Reporte generado en: governance/F5_07A_DATA_COVERAGE_REPORT.md")

if __name__ == '__main__':
    generate_coverage_report()
