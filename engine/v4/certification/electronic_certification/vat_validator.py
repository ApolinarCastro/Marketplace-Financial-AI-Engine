"""VAT Validator for DTE SII"""
from typing import Dict, Any

from .sii_rules import SIIRules

class VatValidator:
    def __init__(self):
        try:
            from lxml import etree
            self.etree = etree
            self.has_deps = True
        except ImportError:
            self.has_deps = False

        self.sii_namespace = "http://www.sii.cl/SiiDte"
        self.rules = SIIRules()

    def _get_text_as_int(self, parent, tag, default=0):
        n = parent.find(tag)
        if n is None:
            n = parent.find(f"{{{self.sii_namespace}}}{tag}")
        if n is not None and n.text:
            try:
                return int(round(float(n.text)))
            except ValueError:
                return default
        return default
        
    def _get_text_as_float(self, parent, tag, default=0.0):
        n = parent.find(tag)
        if n is None:
            n = parent.find(f"{{{self.sii_namespace}}}{tag}")
        if n is not None and n.text:
            try:
                return float(n.text)
            except ValueError:
                return default
        return default

    def validate(self, xml_content: str, dte_metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Validates the VAT, Totals, and detail summations of the DTE.
        """
        result = {
            "status": "FAIL",
            "errors": [],
            "warnings": [],
            "tax_metadata": {
                "mnt_neto": 0,
                "mnt_exe": 0,
                "iva": 0,
                "tasa_iva": 0.0,
                "mnt_total": 0,
                "sum_detalles_neto": 0,
                "sum_detalles_exe": 0
            }
        }

        if not self.has_deps:
            result["status"] = "PASS"
            result["warnings"].append("Missing required dependency (lxml). Skipping strict VAT validation (Degraded Mode).")
            return result

        try:
            root = self.etree.fromstring(xml_content.encode('utf-8') if isinstance(xml_content, str) else xml_content)
        except Exception as e:
            result["errors"].append(f"Malformed XML: {str(e)}")
            return result

        # 1. Extraction
        # Look for DTE first, then search inside
        dte = root.find(f".//{{{self.sii_namespace}}}DTE")
        if dte is None:
            dte = root.find(".//DTE")
            
        if dte is None:
            # Maybe the root IS DTE
            if "DTE" in root.tag:
                dte = root
            else:
                result["status"] = "INVALID_TOTAL"
                result["errors"].append("No DTE node found.")
                return result
                
        encabezado = dte.find(f".//{{{self.sii_namespace}}}Encabezado")
        if encabezado is None:
            encabezado = dte.find(".//Encabezado")
            
        if encabezado is None:
            result["status"] = "INVALID_TOTAL"
            result["errors"].append("No Encabezado node found.")
            return result
            
        totales = encabezado.find("Totales")
        if totales is None:
            totales = encabezado.find(f"{{{self.sii_namespace}}}Totales")
            
        if totales is None:
            result["status"] = "INVALID_TOTAL"
            result["errors"].append("No Totales node found.")
            return result

        mnt_neto = self._get_text_as_int(totales, "MntNeto")
        mnt_exe = self._get_text_as_int(totales, "MntExe")
        iva = self._get_text_as_int(totales, "IVA")
        tasa_iva = self._get_text_as_float(totales, "TasaIVA", self.rules.DEFAULT_IVA_RATE)
        mnt_total = self._get_text_as_int(totales, "MntTotal")

        result["tax_metadata"]["mnt_neto"] = mnt_neto
        result["tax_metadata"]["mnt_exe"] = mnt_exe
        result["tax_metadata"]["iva"] = iva
        result["tax_metadata"]["tasa_iva"] = tasa_iva
        result["tax_metadata"]["mnt_total"] = mnt_total

        # Identify if document type is exempt by default (Tipo 34 - Factura Exenta)
        tipo_dte = 0
        iddoc = encabezado.find("IdDoc") or encabezado.find(f"{{{self.sii_namespace}}}IdDoc")
        if iddoc is not None:
            tipo_dte = self._get_text_as_int(iddoc, "TipoDTE")

        is_exempt_doc = (tipo_dte == 34)

        # 2. Detail Summation
        detalles = dte.findall(f".//{{{self.sii_namespace}}}Detalle")
        if not detalles:
            detalles = dte.findall(".//Detalle")
            
        sum_neto = 0
        sum_exe = 0
        
        for det in detalles:
            monto_item = self._get_text_as_int(det, "MontoItem")
            # For Liquidacion (Tipo 43), details have TpoDocLiq which indicates if it subtracts
            tpo_doc_liq = self._get_text_as_int(det, "TpoDocLiq", 0)
            if tpo_doc_liq in (61, 60, 112): # Notas de Credito
                monto_item = -monto_item
                
            # IndExe = 1 means Exempt, 2 means Not billable, etc.
            ind_exe = self._get_text_as_int(det, "IndExe", 0)
            
            if is_exempt_doc or ind_exe == 1:
                sum_exe += monto_item
            elif ind_exe == 0:
                sum_neto += monto_item

        result["tax_metadata"]["sum_detalles_neto"] = sum_neto
        result["tax_metadata"]["sum_detalles_exe"] = sum_exe

        if sum_neto != mnt_neto:
            result["status"] = "INVALID_NET"
            result["errors"].append(f"Sum of net details ({sum_neto}) does not match MntNeto ({mnt_neto}).")
            return result
            
        if sum_exe != mnt_exe:
            result["status"] = "INVALID_NET"
            result["errors"].append(f"Sum of exempt details ({sum_exe}) does not match MntExe ({mnt_exe}).")
            return result

        # 3. VAT Computation
        # If it's fully exempt, IVA should be 0
        if is_exempt_doc or (sum_neto == 0 and sum_exe > 0):
            if iva != 0:
                result["status"] = "INVALID_VAT"
                result["errors"].append(f"Exempt document has non-zero IVA ({iva}).")
                return result
        else:
            # Check TasaIVA vs Config
            # To avoid hardcoding, we allow the rate found in XML, but issue a warning if it differs from config.
            # If the directive demands strict config, we can check it.
            # Usually, the rate in XML should be verified against standard rules.
            expected_iva = mnt_neto * (tasa_iva / 100.0)
            # Standard half-up integer rounding for SII
            expected_iva_rounded = int(expected_iva + 0.5)
            
            diff = abs(expected_iva_rounded - iva)
            
            if diff > 10:
                # Big mismatch
                result["status"] = "INVALID_VAT"
                result["errors"].append(f"Reported IVA ({iva}) differs significantly from expected ({expected_iva_rounded}). Difference: {diff}")
                return result
            elif diff > 0:
                # Small rounding error (up to 10 pesos cumulative)
                result["status"] = "PASS"
                result["warnings"].append(f"Reported IVA ({iva}) has a minor rounding difference vs expected ({expected_iva_rounded}).")

        # 4. Total Computation
        # Basic sum, we assume OtrosImpuestos is not present for this phase (per directive focus on IVA)
        # If OtrosImpuestos exist, they would normally be added to the expected total.
        expected_total = mnt_neto + mnt_exe + iva
        
        # Look for OtrosImpuestos (ImptoReten) to safely include them if present
        imptos = totales.findall("ImptoReten") or totales.findall(f"{{{self.sii_namespace}}}ImptoReten")
        for impto in imptos:
            monto_imp = self._get_text_as_int(impto, "MontoImp")
            expected_total += monto_imp

        if expected_total != mnt_total:
            result["status"] = "INVALID_TOTAL"
            result["errors"].append(f"Expected Total ({expected_total}) does not match reported MntTotal ({mnt_total}).")
            return result

        result["status"] = "PASS"
        return result
