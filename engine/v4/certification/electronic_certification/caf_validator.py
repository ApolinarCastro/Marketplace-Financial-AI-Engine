"""CAF Validator for DTE SII"""
from typing import Dict, Any
import datetime

from .sii_rules import SIIRules

class CafValidator:
    def __init__(self):
        try:
            from lxml import etree
            self.etree = etree
            self.has_deps = True
        except ImportError:
            self.has_deps = False

        self.sii_namespace = "http://www.sii.cl/SiiDte"
        self.rules = SIIRules()

    def validate(self, xml_content: str, dte_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the CAF embedded inside the DTE XML.
        Expects dte_metadata to contain: tipo_dte, folio, emisor, fch_emis
        """
        result = {
            "status": "FAIL",
            "errors": [],
            "warnings": [],
            "caf_metadata": {
                "re": None,
                "td": None,
                "rng_d": None,
                "rng_h": None,
                "fa": None
            }
        }

        if not self.has_deps:
            result["status"] = "NOT_IMPLEMENTED"
            result["warnings"].append("Missing required dependency (lxml). CAF validation not executed.")
            return result

        try:
            root = self.etree.fromstring(xml_content.encode('utf-8') if isinstance(xml_content, str) else xml_content)
        except Exception as e:
            result["errors"].append(f"Malformed XML: {str(e)}")
            return result

        # Extract CAF Node. It's usually inside <Documento>...<TED>...<DD>...<CAF>
        # but the CAF itself is an XML node inside the DTE
        caf_nodes = root.xpath('//sii:CAF | //CAF', namespaces={'sii': self.sii_namespace})
        
        if not caf_nodes:
            result["status"] = "INVALID_CAF"
            result["errors"].append("No CAF node found in XML.")
            return result

        caf_node = caf_nodes[0]
        
        da_node = caf_node.find("DA")
        if da_node is None:
            # Maybe namespace is present even in sub-nodes if not properly structured
            da_node = caf_node.find(f"{{{self.sii_namespace}}}DA")
            if da_node is None:
                result["status"] = "INVALID_CAF"
                result["errors"].append("CAF missing <DA> node.")
                return result

        # Extract DA Metadata
        def _get_text(parent, tag):
            n = parent.find(tag)
            if n is None:
                n = parent.find(f"{{{self.sii_namespace}}}{tag}")
            return n.text.strip() if (n is not None and n.text) else None

        re = _get_text(da_node, "RE")
        td = _get_text(da_node, "TD")
        rngf_node = da_node.find("RngF")
        if rngf_node is None:
            rngf_node = da_node.find(f"{{{self.sii_namespace}}}RngF")
        if rngf_node is None:
            rngf_node = da_node.find("RNG")
        if rngf_node is None:
            rngf_node = da_node.find(f"{{{self.sii_namespace}}}RNG")
            
        rng_d, rng_h = None, None
        if rngf_node is not None:
            rng_d = _get_text(rngf_node, "D")
            rng_h = _get_text(rngf_node, "H")

        fa = _get_text(da_node, "FA")

        result["caf_metadata"]["re"] = re
        result["caf_metadata"]["td"] = td
        result["caf_metadata"]["rng_d"] = rng_d
        result["caf_metadata"]["rng_h"] = rng_h
        result["caf_metadata"]["fa"] = fa

        # Validations against DTE metadata
        dte_emisor = dte_metadata.get("emisor")
        dte_tipo = dte_metadata.get("tipo_dte")
        dte_folio = dte_metadata.get("folio")
        dte_fch_emis = dte_metadata.get("fch_emis") # the emission date of the document

        if not re or not td or not rng_d or not rng_h or not fa:
            result["status"] = "INVALID_CAF"
            result["errors"].append("CAF <DA> node is missing mandatory elements.")
            return result

        if dte_emisor and dte_emisor != re:
            result["status"] = "INVALID_EMISOR"
            result["errors"].append(f"CAF RUT Emisor ({re}) does not match DTE Emisor ({dte_emisor}).")
            return result

        if dte_tipo and str(dte_tipo) != str(td):
            result["status"] = "INVALID_CAF"
            result["errors"].append(f"CAF TipoDTE ({td}) does not match DTE TipoDTE ({dte_tipo}).")
            return result

        try:
            folio_int = int(dte_folio) if dte_folio else 0
            d_int = int(rng_d)
            h_int = int(rng_h)
            
            if folio_int < d_int or folio_int > h_int:
                result["status"] = "FOLIO_OUT_OF_RANGE"
                result["errors"].append(f"DTE Folio {folio_int} is outside CAF bounds [{d_int}, {h_int}].")
                return result
        except ValueError:
            result["status"] = "INVALID_CAF"
            result["errors"].append("Folio or Rango properties are not valid integers.")
            return result

        # Validate FA (Fecha de Autorizacion) expiration
        # Instead of strict hardcoded 6 months, we use the config rule SIIRules.CAF_VALIDITY_DAYS
        try:
            fa_date = datetime.datetime.strptime(fa, "%Y-%m-%d").date()
            # If DTE emission date is provided, validate CAF against the emission date instead of *now*.
            # A DTE emitted back then was valid if FA was within range. 
            if dte_fch_emis:
                emis_date = datetime.datetime.strptime(dte_fch_emis, "%Y-%m-%d").date()
            else:
                emis_date = datetime.datetime.now().date()
                
            delta_days = (emis_date - fa_date).days
            
            if delta_days < 0:
                # FA is in the future
                result["status"] = "INVALID_CAF"
                result["errors"].append(f"CAF Fecha Autorizacion ({fa}) is in the future.")
                return result
                
            if delta_days > self.rules.CAF_VALIDITY_DAYS:
                result["status"] = "EXPIRED_CAF"
                result["errors"].append(f"CAF expired. Generated on {fa}, Emission on {emis_date} (>{self.rules.CAF_VALIDITY_DAYS} days).")
                return result
                
        except ValueError:
            result["status"] = "INVALID_CAF"
            result["errors"].append(f"Invalid date format in CAF FA ({fa}) or DTE FchEmis ({dte_fch_emis}).")
            return result

        result["status"] = "PASS"
        return result
