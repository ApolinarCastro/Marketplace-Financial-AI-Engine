"""XML Structure Validator for DTE SII"""
import re
from typing import Dict, Any

class XmlValidator:
    def __init__(self):
        try:
            import defusedxml.ElementTree as ET
            self.ET = ET
            self.safe_mode = True
        except ImportError:
            import xml.etree.ElementTree as ET
            self.ET = ET
            self.safe_mode = False

        self.sii_namespace = "http://www.sii.cl/SiiDte"
        self.ns = {'sii': self.sii_namespace}

    def validate(self, xml_content: str) -> Dict[str, Any]:
        result = {
            "status": "FAIL",
            "errors": [],
            "warnings": [],
            "metadata": {
                "tipo_dte": None,
                "folio": None,
                "emisor": None,
                "receptor": None,
                "fch_emis": None
            }
        }

        if not self.safe_mode:
            result["warnings"].append("defusedxml module is not available. Using standard xml.etree.ElementTree (Degraded Mode).")

        try:
            # Parse the XML
            root = self.ET.fromstring(xml_content)
        except Exception as e:
            result["errors"].append(f"Malformed XML: {str(e)}")
            return result

        # Find the DTE node. It might be wrapped in EnvioDTE -> SetDTE, and it might have different namespaces.
        # ElementTree supports searching without strict namespace using .//*[local-name()='DTE'] in XPath, but ET standard find doesn't.
        # We will iterate to find the first node that ends with 'DTE' and has 'version'.
        def find_dte_node(element):
            tag_local = element.tag.split('}')[-1]
            if tag_local == 'DTE':
                return element
            for child in element:
                res = find_dte_node(child)
                if res is not None:
                    return res
            return None

        dte_node = find_dte_node(root)
        if dte_node is None:
            result["errors"].append("Could not find any DTE node in the XML.")
            return result
            
        # Version validation
        version = dte_node.attrib.get('version')
        if not version:
            result["errors"].append("Missing 'version' attribute on DTE node.")

        # For a robust structure check, we search with or without namespace dynamically based on the dte_node.
        ns_prefix = "{" + dte_node.tag.split('}')[0].strip('{') + "}" if '}' in dte_node.tag else ""
        
        # In SII schema, the child of <DTE> can be <Documento>, <Liquidacion>, <Factura>, etc.
        # But it always contains an <Encabezado> child.
        # We search for Encabezado recursively inside DTE.
        def find_tag(element, tag_name):
            if element.tag.split('}')[-1] == tag_name:
                return element
            for child in element:
                res = find_tag(child, tag_name)
                if res is not None:
                    return res
            return None

        encabezado = find_tag(dte_node, "Encabezado")
        if encabezado is None:
            result["errors"].append("Missing mandatory node: 'Encabezado'.")
            return result

        # The ID prefix dynamic discovery
        ns_prefix = "{" + encabezado.tag.split('}')[0].strip('{') + "}" if '}' in encabezado.tag else ""

        # Metadata extraction
        id_doc = encabezado.find(f"{ns_prefix}IdDoc")
        if id_doc is not None:
            tipo_dte = id_doc.find(f"{ns_prefix}TipoDTE")
            if tipo_dte is not None and tipo_dte.text:
                result["metadata"]["tipo_dte"] = tipo_dte.text.strip()
            
            folio = id_doc.find(f"{ns_prefix}Folio")
            if folio is not None and folio.text:
                result["metadata"]["folio"] = folio.text.strip()

            fch_emis = id_doc.find(f"{ns_prefix}FchEmis")
            if fch_emis is not None and fch_emis.text:
                result["metadata"]["fch_emis"] = fch_emis.text.strip()

        emisor = encabezado.find(f"{ns_prefix}Emisor")
        if emisor is not None:
            rut_emisor = emisor.find(f"{ns_prefix}RUTEmisor")
            if rut_emisor is not None and rut_emisor.text:
                result["metadata"]["emisor"] = rut_emisor.text.strip()

        receptor = encabezado.find(f"{ns_prefix}Receptor")
        if receptor is not None:
            rut_recep = receptor.find(f"{ns_prefix}RUTRecep")
            if rut_recep is not None and rut_recep.text:
                result["metadata"]["receptor"] = rut_recep.text.strip()

        if len(result["errors"]) == 0:
            result["status"] = "PASS"

        return result
