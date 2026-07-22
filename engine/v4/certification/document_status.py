from enum import Enum

class DocumentCertificationStatus(str, Enum):
    PASS = "PASS"
    FAILED = "FAILED"
    NOT_FOUND = "NOT_FOUND"
    NOT_REQUIRED = "NOT_REQUIRED"
    BLOCKED_BY_SOURCE_DATA = "BLOCKED_BY_SOURCE_DATA"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"

def compute_document_status(doc: dict) -> DocumentCertificationStatus:
    """
    Motor determinista para resolver el estado documental de la transaccion.
    """
    marketplace = doc.get("marketplace", "").upper()
    doc_state = doc.get("estado_xml", "MISSING")
    
    if doc_state in ("CONCILIADO", "DOCUMENTADO"):
        return DocumentCertificationStatus.PASS
    
    if doc_state == "MISSING":
        # Paris and Falabella are officially blocked by source data
        if marketplace in ("PARIS", "FALABELLA"):
            return DocumentCertificationStatus.BLOCKED_BY_SOURCE_DATA
        return DocumentCertificationStatus.NOT_FOUND
        
    return DocumentCertificationStatus.NOT_REQUIRED
