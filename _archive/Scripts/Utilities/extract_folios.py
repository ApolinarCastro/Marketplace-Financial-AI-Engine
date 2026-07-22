import glob
import xml.etree.ElementTree as ET

namespaces = {'ns0': 'http://www.sii.cl/SiiDte'}

xml_files = glob.glob('01_Raw/ML/Documentos Recepcionados/*.xml')
folios = []
for f in xml_files[:20]:
    try:
        tree = ET.parse(f)
        root = tree.getroot()
        
        # the path to folio might depend on DTE vs Liquidacion
        # just find all Folio tags
        for folio_node in root.findall('.//ns0:Folio', namespaces):
            folios.append((f, folio_node.text))
    except Exception as e:
        pass

print("Sample XML folios found:")
for f, folio in folios:
    print(f"{f} -> Folio: {folio}")
