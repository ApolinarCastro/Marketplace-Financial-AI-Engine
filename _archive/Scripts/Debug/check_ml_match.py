import pandas as pd
import glob
import xml.etree.ElementTree as ET

f = glob.glob('01_Raw/ML/Facturacion/**/*.xlsx', recursive=True)
if f:
    df = pd.read_excel(f[0])
    df = df[df['N° de factura fiscal'].notnull()]
    if not df.empty:
        sample = df.iloc[0]
        folio = sample['N° de factura fiscal']
        print(f'Found folio: {folio} with Detalle: {sample["Detalle"]}')
        
        folio_str = str(folio).split('-')[-1]
        xml_files = glob.glob(f'01_Raw/ML/Documentos Recepcionados/*_{int(folio_str)}.xml')
        if xml_files:
            print(f'Found XML: {xml_files[0]}')
            tree = ET.parse(xml_files[0])
            root = tree.getroot()
            print(ET.tostring(root, encoding='unicode')[:500])
