"""XSD Structure Validator for DTE SII"""
import os
from pathlib import Path
from typing import Dict, Any

from .xml_validator import XmlValidator

class XsdValidator:
    def __init__(self):
        try:
            import xmlschema
            self.xmlschema = xmlschema
            self.safe_mode = True
        except ImportError:
            self.xmlschema = None
            self.safe_mode = False
            
        self.xml_validator = XmlValidator()
        # Resolve schemas directory relative to this file
        self.schemas_dir = Path(__file__).parent / "schemas"

    def validate(self, xml_content: str) -> Dict[str, Any]:
        result = {
            "status": "FAIL",
            "errors": [],
            "warnings": [],
            "schema": None
        }

        if not self.safe_mode:
            result["warnings"].append("xmlschema module is not available. XSD validation not executed.")
            # We must not claim PASS for validation that never ran.
            result["status"] = "NOT_IMPLEMENTED"
            return result

        # Extract basic info first via XmlValidator to know which XSD to apply
        xml_info = self.xml_validator.validate(xml_content)
        if xml_info["status"] == "FAIL":
            result["errors"].append("Failed initial XML structure validation.")
            result["errors"].extend(xml_info["errors"])
            return result

        tipo_dte = xml_info.get("metadata", {}).get("tipo_dte")
        if not tipo_dte:
            result["errors"].append("TipoDTE not found in XML, cannot determine which XSD to apply.")
            return result

        # Basic routing of DTE types to XSD schema files based on official SII standards
        # Typically, Envios use EnvioDTE_v10.xsd, while individual documents use DTE_v10.xsd
        # For this scope, we assume DTE_v10.xsd for individual documents (33, 43, 52, 61)
        schema_filename = "DTE_v10.xsd"
        schema_path = self.schemas_dir / schema_filename

        if not schema_path.exists():
            result["status"] = "NOT_IMPLEMENTED"
            result["errors"].append(f"Official XSD missing for {schema_filename}")
            return result
            
        result["schema"] = schema_filename

        try:
            # Load schema securely: allow='local' forbids HTTP/HTTPS downloads
            schema = self.xmlschema.XMLSchema(str(schema_path), allow='local')
        except Exception as e:
            result["errors"].append(f"Error loading local XSD schema: {str(e)}")
            return result

        try:
            # Validate
            schema.validate(xml_content)
        except self.xmlschema.validators.exceptions.XMLSchemaValidationError as e:
            result["errors"].append(f"XSD Validation Error: {e.reason}")
        except Exception as e:
            result["errors"].append(f"Validation execution error: {str(e)}")

        if len(result["errors"]) == 0:
            result["status"] = "PASS"

        return result
