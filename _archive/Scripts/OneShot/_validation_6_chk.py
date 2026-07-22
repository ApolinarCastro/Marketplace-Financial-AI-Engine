import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET

xml_dir = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\RIPLEY\Documentos Recepcionados")
xml_files = list(xml_dir.glob("*.xml"))[:10]
for f in xml_files:
    root = ET.parse(f).getroot()
    def get_text(node, tag):
        for elem in node.iter():
            if tag in elem.tag:
                return elem.text
        return None
    print(get_text(root, 'Folio'))
