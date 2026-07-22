# Secuencia de Integración (Diagrama Lógico)

1. **UI (Browser)** -> Envía archivo XML vía POST a `/api/v4/electronic_certification/validate`.
2. **FastAPI (api.py)** -> Recibe el archivo y lo pasa a `ElectronicCertificationEngine`.
3. **ElectronicCertificationEngine** -> Parsea el XML, extrae Folio, RUT, Montos, IVA.
4. **ElectronicCertificationEngine** -> Llama a `ECC` (Engine of Cryptographic Certification) para validar la firma XMLDSig y el CAF.
5. **ElectronicCertificationEngine** -> Devuelve el dictamen (Valido/Invalido) a FastAPI.
6. **FastAPI (api.py)** -> Invoca `EvidenceEngine` para generar un hash criptográfico de la transacción validada.
7. **FastAPI (api.py)** -> Devuelve JSON a la UI.
8. **UI (Browser)** -> Pinta los checks verdes en el Pipeline de Validación.
9. **UI (Browser)** -> (Opcional) Usuario hace clic en "Abrir en Obsidian" -> Invoca `/api/v4/obsidian/export`.
10. **ObsidianAdapter** -> Escribe el Markdown en el Vault local.
