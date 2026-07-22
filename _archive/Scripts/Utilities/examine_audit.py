import json

# Read the auditor file
with open("engine/v4/marketplace_auditor.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Check if we have PosCobro concepts that should be excluded
poscobro_concepts = [
    'reserve_for_dispute',
    'Mediación',
    'bpp_refunded',
    'bpp_covered',
    'partially_bpp_refunded',
    'ppv_covered_melienvio',
    'ppv_valid',
    'reconciled',
    'AJUSTE POSCOBRO',
    'cashback',
    'cashback_cancel',
    'Reserva para devolución en envío BBP',
    'Retenciones & Provisiones',
]

print("Looking for the legal audit section...")

# Find the section
idx = content.find("Certificación Legal (Crucial)")
if idx > 0:
    print(f"Found at position {idx}")
    # Show context
    print(content[idx:idx+2000])
else:
    print("Not found")