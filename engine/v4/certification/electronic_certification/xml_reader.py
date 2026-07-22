import os
import re
import codecs
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("meli.xml_reader")

class XMLReader:
    """
    Componente centralizado para la lectura física de XMLs.
    Garantiza la correcta detección del encoding declarado y el manejo del BOM,
    evitando fallos UnicodeDecodeError y registrando metadatos para auditoría.
    """
    
    @staticmethod
    def read_xml(file_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Lee un archivo XML y retorna una tupla con (contenido_xml, metadatos_auditoria).
        """
        audit_metadata = {
            "file_path": file_path,
            "bom_detected": False,
            "encoding_declared": None,
            "encoding_used": None,
            "fallback_used": False
        }
        
        # 1. Leer en formato binario para detectar BOM y declaración XML
        with open(file_path, 'rb') as f:
            raw_bytes = f.read()
            
        if not raw_bytes:
            raise ValueError(f"El archivo {file_path} está vacío.")

        # 2. Detectar BOM
        encoding = None
        if raw_bytes.startswith(codecs.BOM_UTF8):
            audit_metadata["bom_detected"] = True
            encoding = 'utf-8-sig'
        elif raw_bytes.startswith(codecs.BOM_UTF16_LE):
            audit_metadata["bom_detected"] = True
            encoding = 'utf-16-le'
        elif raw_bytes.startswith(codecs.BOM_UTF16_BE):
            audit_metadata["bom_detected"] = True
            encoding = 'utf-16-be'

        # 3. Detectar declaración de encoding en el encabezado XML (si no está implícito por el BOM)
        # Buscar <?xml version="1.0" encoding="ISO-8859-1"?>
        # Tomamos los primeros 500 bytes que es donde suele estar el prologo
        header_bytes = raw_bytes[:500]
        try:
            # Usamos ascii o utf-8 (ignore) solo para parsear el header con regex
            header_str = header_bytes.decode('ascii', errors='ignore')
            match = re.search(r'<\?xml[^>]+encoding=[\'"]([^\'"]+)[\'"]', header_str, re.IGNORECASE)
            if match:
                declared_enc = match.group(1).lower()
                audit_metadata["encoding_declared"] = declared_enc
                if not encoding:  # Si el BOM no dictó el encoding, usamos el declarado
                    encoding = declared_enc
        except Exception as e:
            logger.warning(f"No se pudo parsear el encabezado de {file_path} para detectar encoding: {e}")

        # 4. Fallback si no hay BOM y no hay declaración
        if not encoding:
            encoding = 'utf-8'
            audit_metadata["fallback_used"] = True

        audit_metadata["encoding_used"] = encoding

        # 5. Intentar decodificar
        try:
            content = raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            # Si el encoding declarado o el fallback falló, intentamos recuperación de desastre
            # Solo si el fallback anterior era utf-8 (es común que no declaren y sean latin1)
            if encoding == 'utf-8' and audit_metadata["fallback_used"]:
                logger.warning(f"Fallo decodificando {file_path} con {encoding}. Intentando latin-1 como fallback secundario.")
                encoding = 'latin-1'
                audit_metadata["encoding_used"] = encoding
                content = raw_bytes.decode(encoding)
            else:
                raise

        return content, audit_metadata
