# Flujos de Usuario (User Flows)

## Flujo 1: Auditoría de un GAP y Certificación Manual
1. Usuario entra a **Documentary Dashboard**.
2. Observa la tabla de GAPs y filtra por estado `XML_MISSING`.
3. Selecciona una transacción. Se abre el **Panel de Inspección**.
4. En el panel, encuentra la zona de **Carga XML**.
5. Arrastra el archivo XML proporcionado por el SII/Marketplace.
6. El Frontend llama a `/api/certification/validate_xml` (ElectronicCertificationEngine).
7. La UI muestra el pipeline de carga (Parseo -> Firma -> CAF).
8. Si es válido, se actualiza el estado a `CERTIFIED` y se genera el `Evidence Hash`.
9. El usuario hace clic en "Exportar Markdown" o "Abrir en Obsidian" para guardar la traza.
