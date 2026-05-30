import json, os

dict_path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\master_marketplace_dictionary_v1.json'
auditor_path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\engine\v4\marketplace_auditor.py'

# Build from dictionary entries
dict_data = {
    "dictionary_name": "MASTER_MARKETPLACE_DICTIONARY_V1",
    "version": "1.0",
    "dictionary": [
        {"marketplace": "MERCADO_LIBRE", "tipo_transaccion": "VENTA_MARKETPLACE", "clasificacion": "INGRESO", "aliases": ["Cargo por venta", "Venta"]},
        {"marketplace": "MERCADO_LIBRE", "tipo_transaccion": "COMISION_MARKETPLACE", "clasificacion": "COSTO_COMERCIAL", "aliases": ["Cargo por venta (Comisión)", "Anulación del cargo por venta", "Reembolso por comisión"]},
        {"marketplace": "MERCADO_LIBRE", "tipo_transaccion": "LOGISTICA_MARKETPLACE", "clasificacion": "COSTO_LOGISTICO", "aliases": ["Cargo por envíos de Mercado Libre", "Cargo por Mercado Envíos", "Anulación del cargo por envíos de ML", "Anulación del cargo por Mercado Envíos", "Cargo por devolución", "Anulación del cargo por devolución", "Cargo por servicio de almacenamiento Full", "Cargo por retiro de stock Full", "Cargo por stock antiguo en Full", "Cargo por sobrepasar espacio Full", "Cargo por servicio de colecta Full", "Cargo por diferencias medidas/peso"]},
        {"marketplace": "MERCADO_LIBRE", "tipo_transaccion": "PUBLICIDAD_MARKETPLACE", "clasificacion": "COSTO_COMERCIAL", "aliases": ["Cargo por campaña de publicidad - Product Ads", "Campañas de publicidad - Product Ads", "Cargo por campaña de publicidad - Brand Ads", "Campañas de publicidad - Brand Ads", "Campañas de publicidad - Display", "Cargo por campaña de publicidad - Display programático", "Anulación cargo publicidad Product Ads"]},
        {"marketplace": "MERCADO_LIBRE", "tipo_transaccion": "SERVICIOS_COMERCIALES", "clasificacion": "COSTO_COMERCIAL", "aliases": ["Cargo por Asesoría Comercial", "Cargo por mantenimiento de Mi página", "Anulación mantenimiento Mi página"]},
        {"marketplace": "MERCADO_LIBRE", "tipo_transaccion": "INGRESO_COMERCIAL", "clasificacion": "INGRESO", "aliases": ["Bonificación", "Rebate", "Compensación comercial"]},
        {"marketplace": "RIPLEY", "tipo_transaccion": "VENTA_MARKETPLACE", "clasificacion": "INGRESO", "aliases": ["Importe del pedido"]},
        {"marketplace": "RIPLEY", "tipo_transaccion": "COMISION_MARKETPLACE", "clasificacion": "COSTO_COMERCIAL", "aliases": ["Comisiones sobre pedidos", "Comisiones sobre pedidos reembolsados"]},
        {"marketplace": "RIPLEY", "tipo_transaccion": "LOGISTICA_MARKETPLACE", "clasificacion": "COSTO_LOGISTICO", "aliases": ["Gastos de envío pagados por el operador", "Gastos de envío reembolsados pagados por el operador", "Descuento por costo logístico", "Descuento por logística inversa"]},
        {"marketplace": "RIPLEY", "tipo_transaccion": "INGRESO_COMERCIAL", "clasificacion": "INGRESO", "aliases": ["Envío", "Despacho"]},
        {"marketplace": "RIPLEY", "tipo_transaccion": "DEVOLUCION_VENTA", "clasificacion": "DEVOLUCION", "aliases": ["Pedidos reembolsados"]},
        {"marketplace": "RIPLEY", "tipo_transaccion": "AJUSTE_OPERATIVO", "clasificacion": "AJUSTE_OPERATIVO", "aliases": ["Descuento por cancelación", "Otros descuentos"]},
        {"marketplace": "PARIS", "tipo_transaccion": "VENTA_MARKETPLACE", "clasificacion": "INGRESO", "aliases": ["Venta"]},
        {"marketplace": "PARIS", "tipo_transaccion": "DEVOLUCION_VENTA", "clasificacion": "DEVOLUCION", "aliases": ["Devolución"]},
        {"marketplace": "PARIS", "tipo_transaccion": "LOGISTICA_MARKETPLACE", "clasificacion": "COSTO_LOGISTICO", "aliases": ["Cobro por despacho", "Logística inversa", "Retiro stock bodega Paris", "Cobro stock antiguo", "Multa", "Multa por stock"]},
        {"marketplace": "PARIS", "tipo_transaccion": "INGRESO_COMERCIAL", "clasificacion": "INGRESO", "aliases": ["Despacho", "Rebate"]},
        {"marketplace": "PARIS", "tipo_transaccion": "AJUSTE_OPERATIVO", "clasificacion": "AJUSTE_OPERATIVO", "aliases": ["Compensación logística", "Ajuste Inventario Activo", "Cobro por campaña", "Merma"]},
        {"marketplace": "FALABELLA", "tipo_transaccion": "VENTA_MARKETPLACE", "clasificacion": "INGRESO", "aliases": ["Sale amount", "Gross sales", "Pago por precio del producto"]},
        {"marketplace": "FALABELLA", "tipo_transaccion": "COMISION_MARKETPLACE", "clasificacion": "COSTO_COMERCIAL", "aliases": ["Cobro por comisión por venta", "Reembolso por comisión por venta"]},
        {"marketplace": "FALABELLA", "tipo_transaccion": "LOGISTICA_MARKETPLACE", "clasificacion": "COSTO_LOGISTICO", "aliases": ["Cobro por cofinanciamiento logístico", "Reversa de pago de envío comprador", "Cobro por logística inversa", "Pago por envío directo"]},
        {"marketplace": "FALABELLA", "tipo_transaccion": "AJUSTE_OPERATIVO", "clasificacion": "AJUSTE_OPERATIVO", "aliases": ["Corrección de pago envio directo", "Corrección de cobro por envío directo"]},
    ]
}

# Save JSON
with open(dict_path, 'w', encoding='utf-8') as f:
    json.dump(dict_data, f, ensure_ascii=False, indent=2)
print(f"Dictionary saved to {dict_path}")

# Build alias → canonical map
RAW_MAP = {}
CANONICAL_TO_CLASIF = {}
for entry in dict_data["dictionary"]:
    for alias in entry["aliases"]:
        RAW_MAP[alias] = alias  # identity map for dictionary entries
    for alias in entry["aliases"]:
        CANONICAL_TO_CLASIF[alias] = entry["clasificacion"]

# Build FINANCIAL_STRUCTURE
STRUCTURE = {"ingresos": [], "devoluciones": [], "costos_operacionales": [], "costos_comerciales": [], "ajustes": [], "tesoreria": ["Retiro de dinero"]}
for entry in dict_data["dictionary"]:
    target = {
        "INGRESO": "ingresos",
        "DEVOLUCION": "devoluciones",
        "COSTO_LOGISTICO": "costos_operacionales",
        "COSTO_COMERCIAL": "costos_comerciales",
        "AJUSTE_OPERATIVO": "ajustes",
    }.get(entry["clasificacion"])
    if target:
        STRUCTURE[target].extend(entry["aliases"])

# Print Python code blocks
print(f"\n=== RAW_TO_CLASSIFICATION_MAP ({len(RAW_MAP)} entries) ===")
for k, v in sorted(RAW_MAP.items()):
    print(f'    "{k}": "{v}",')

print(f"\n=== FINANCIAL_STRUCTURE ===")
for group, items in STRUCTURE.items():
    print(f'    "{group}": [')
    for item in items:
        print(f'        "{item}",')
    print(f'    ],')
