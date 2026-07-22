import json
import pandas as pd
from pathlib import Path

with open("recovered_data.json", "r") as f:
    recovered = json.load(f)

# Format to markdown
md_content = ["# PARIS V2 SOURCE RECOVERY\n"]
md_content.append("## Resumen de Recuperación")
md_content.append(f"- **Transacciones Totales Faltantes:** 721")
md_content.append(f"- **Transacciones Recuperadas (Monto Bruto y Neto encontrados):** {len(recovered)}")
md_content.append(f"- **Transacciones con Pérdida Documental:** {721 - len(recovered)}\n")

md_content.append("## Detalle de Transacciones Perdidas (Sin Respaldo en XLSX)")
missing_8_ids = ['15725904', '15721281', '15720946', '15719094', '15719093', '15717010', '15715419', '15715418']
md_content.append("Los siguientes IDs no se encuentran en ningún archivo fuente y se documenta su pérdida:")
for mid in missing_8_ids:
    md_content.append(f"- ID: {mid}")

md_content.append("\n## Detalle de Recuperación (Muestra de 10 transacciones)")
md_content.append("Se extrajeron `MONTO` y `MONTO_A_PAGAR` directamente desde la fuente para 713 filas.\n")
md_content.append("| ID Transacción | Monto Bruto (MONTO) | Monto a Pagar (NETO) | Comisión Calculada |")
md_content.append("|----------------|---------------------|----------------------|--------------------|")
count = 0
for tid, data in recovered.items():
    gross = data['monto_bruto']
    net = data['monto_a_pagar']
    comision = gross - net
    md_content.append(f"| {tid} | {gross} | {net} | {comision} |")
    count += 1
    if count >= 10:
        break

with open("C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/2c921f1a-4258-4b8e-be46-1ad937059ee6/PARIS_V2_SOURCE_RECOVERY.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_content))
    
print("SOURCE_RECOVERY generated.")
