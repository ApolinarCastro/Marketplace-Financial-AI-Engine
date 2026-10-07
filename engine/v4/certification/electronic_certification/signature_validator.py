"""XMLDSig Cryptographic Validator for DTE SII"""
from typing import Dict, Any
import datetime
import base64

class SignatureValidator:
    def __init__(self):
        try:
            from lxml import etree
            from signxml import XMLVerifier
            from cryptography import x509
            from cryptography.hazmat.backends import default_backend
            self.etree = etree
            self.XMLVerifier = XMLVerifier
            self.x509 = x509
            self.default_backend = default_backend
            self.has_deps = True
        except ImportError:
            self.has_deps = False

        self.xmldsig_namespace = "http://www.w3.org/2000/09/xmldsig#"

    def validate(self, xml_content: str) -> Dict[str, Any]:
        result = {
            "status": "FAIL",
            "errors": [],
            "warnings": [],
            "certificate": {
                "subject": None,
                "issuer": None,
                "serial": None,
                "valid_from": None,
                "valid_to": None
            }
        }

        if not self.has_deps:
            # Missing lxml/signxml/cryptography: cryptographic verification
            # cannot execute. NEVER report PASS for unexecuted validation.
            result["status"] = "NOT_IMPLEMENTED"
            result["warnings"].append("Missing required dependencies (lxml, signxml, cryptography). Signature validation not executed.")
            return result

        try:
            # Parse XML with lxml
            root = self.etree.fromstring(xml_content.encode('utf-8') if isinstance(xml_content, str) else xml_content)
        except Exception as e:
            result["errors"].append(f"Malformed XML: {str(e)}")
            return result

        # Structural validation using XPath
        signatures = root.xpath('//ds:Signature', namespaces={'ds': self.xmldsig_namespace})
        if not signatures:
            result["errors"].append("FAIL: XML sin firma. No Signature node found.")
            return result
            
        signature_node = signatures[0]

        # Ensure structural elements exist
        signed_info = signature_node.find(f"{{{self.xmldsig_namespace}}}SignedInfo")
        if signed_info is None:
            result["errors"].append("Missing SignedInfo node.")
            return result

        # Check X509 Certificate
        x509_cert_node = signature_node.find(f".//{{{self.xmldsig_namespace}}}X509Certificate")
        if x509_cert_node is None or not x509_cert_node.text:
            result["status"] = "INVALID_CERTIFICATE"
            result["errors"].append("Missing or empty X509Certificate node.")
            return result

        try:
            cert_bytes = base64.b64decode(x509_cert_node.text.strip())
            cert = self.x509.load_der_x509_certificate(cert_bytes, self.default_backend())
            
            result["certificate"]["subject"] = cert.subject.rfc4514_string()
            result["certificate"]["issuer"] = cert.issuer.rfc4514_string()
            result["certificate"]["serial"] = str(cert.serial_number)
            
            # cryptography x509 returns naive datetimes representing UTC
            result["certificate"]["valid_from"] = cert.not_valid_before.isoformat()
            result["certificate"]["valid_to"] = cert.not_valid_after.isoformat()
            
            # Check expiration
            now = datetime.datetime.utcnow()
            if now < cert.not_valid_before or now > cert.not_valid_after:
                result["status"] = "EXPIRED_CERTIFICATE"
                result["errors"].append("Certificate is expired or not yet valid.")
                return result
                
        except Exception as e:
            result["status"] = "INVALID_CERTIFICATE"
            result["errors"].append(f"Failed to parse X509Certificate: {str(e)}")
            return result

        # Cryptographic Signature Verification
        try:
            # signxml will mathematically verify DigestValue and SignatureValue.
            verifier = self.XMLVerifier()
            # Use resolve_uri=False for offline, safe validation
            verifier.verify(root, x509_cert=cert_bytes, expect_references=True)
        except Exception as e:
            result["status"] = "INVALID_SIGNATURE"
            result["errors"].append(f"Cryptographic signature verification failed: {str(e)}")
            return result

        result["status"] = "PASS"
        return result
