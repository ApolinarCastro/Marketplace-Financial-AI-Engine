import pandas as pd

import logging
from engine.v4.database import DatabaseV4
from engine.v4.logging_config import log_event

logger = logging.getLogger("meli.auditor")

RAW_TO_CLASSIFICATION_MAP = {
    # Mercado Libre (Facturación limpia y Poscobro)
    "Cargo por venta (Venta)": "Cargo por venta (Venta)",
    "Cargo por venta (Comisión)": "Cargo por venta (Comisión)",
    "Devolución de venta": "Devolución de venta",
    "Cargo por Mercado Envíos": "Cargo por Mercado Envíos",
    "Cargo por envíos de Mercado Libre": "Cargo por envíos de Mercado Libre",
    "Cargo por servicio de almacenamiento Full": "Cargo por servicio de almacenamiento Full",
    "Cargo por retiro de stock Full": "Cargo por retiro de stock Full",
    "Cargo por stock antiguo en Full": "Cargo por stock antiguo en Full",
    "Cargo por sobrepasar espacio Full": "Cargo por sobrepasar espacio Full",
    "Cargo por devolución": "Cargo por devolución",
    "Cargo por diferencias en las medidas y el peso del paquete": "Cargo por diferencias en las medidas y el peso del paquete",
    "Cargo por campaña de publicidad - Product Ads": "Cargo por campaña de publicidad - Product Ads",
    "Cargo por campaña de publicidad - Brand Ads": "Cargo por campaña de publicidad - Brand Ads",
    "Campañas de publicidad - Display": "Campañas de publicidad - Display",
    "Cargo por Asesoría Comercial": "Cargo por Asesoría Comercial",
    "Cargo por mantenimiento de Mi página": "Cargo por mantenimiento de Mi página",
    "Bonificación": "Bonificación",
    "Anulación del cargo por venta": "Anulación del cargo por venta",
    "Anulación del cargo por Mercado Envíos": "Anulación del cargo por Mercado Envíos",
    "Anulación del cargo por envíos de Mercado Libre": "Anulación del cargo por envíos de Mercado Libre",
    "Anulación del cargo por devolución": "Anulación del cargo por devolución",
    "Envío": "Envío",
    "Envio": "Envío",
    "Devolución de dinero\nEnvío": "Devolución de dinero\nEnvío",
    "Abono manual": "Abono manual",
    "Importe del pedido": "Importe del pedido",
    "Pago": "Pago",
    "Ajuste histórico (pre-2026)": "Ajuste histórico (pre-2026)",
    "Ajuste Poscobro": "Cargo por devolución",

    # Mercado Libre — Conceptos crudos del ledger real (Adopción Diccionario Maestro)
    "fee_for_divergence_in_package_dimensions": "Cargo por diferencias en las medidas y el peso del paquete",
    "fee_for_divergence_in_package_dimensions_cancel": "Cancelación del cargo por diferencias en las medidas y el peso del paquete",

    # Mercado Libre — Nuevos conceptos Master Spec
    "Cargo": "Abono manual",

    # Mercado Libre — Variantes con errores de codificación
    "Devolucin de dinero\nEnvo": "Devolución de dinero\nEnvío",
    "Devolucin de dinero\nEnvio": "Devolución de dinero\nEnvío",

    # Mercado Libre — Nuevas reservas e identificadores masivos

    # Mercado Libre (Poscobro Técnico Inglés) -> Mapeo a Clasificación Limpia
    "smaller_than_expected_fashion": "Ajuste por Talla/Garantía",
    "bigger_than_expected_fashion": "Ajuste por Talla/Garantía",
    "size_not_useful_repentant": "Ajuste por Talla/Garantía",
    "not_match_size_guide_fashion": "Ajuste por Talla/Garantía",
    "broken_item_fashion": "Ajuste por Producto Dañado/Vacío",
    "empty_box": "Ajuste por Producto Dañado/Vacío",
    "damaged_package_empty_box": "Ajuste por Producto Dañado/Vacío",
    "repentant_buyer": "Ajuste por Arrepentimiento",
    "undelivered_repentant_buyer": "Ajuste por Arrepentimiento",
    "dont_want_it_another_cause_fashion": "Ajuste por Arrepentimiento",
    "buy_out_of_ml": "Ajuste por Arrepentimiento",
    "different_than_published": "Ajuste por Diferencia de Publicación",
    "different_color_or_size_fashion": "Ajuste por Diferencia de Publicación",
    "different_item_other": "Ajuste por Diferencia de Publicación",
    "missing_item": "Ajuste por Ítem Faltante",
    "out_of_stock": "Ajuste por Falta de Stock",
    "delivery_date_was_not_met": "Ajuste por Retraso en Entrega",
    "estimated_delivery_out_of_time": "Ajuste por Retraso en Entrega",
    "change_receiver_address": "Ajuste por Cambio de Dirección",
    "undelivered_other": "Ajuste por Falla en Entrega",
    "delivered_but_not_receive_package": "Ajuste por Falla en Entrega",
    "reconciled": "Recuperación por Pérdida de Inventario",
    "bpp_refunded": "Ajuste por Compra Protegida (BPP)",
    "respondent_unanswered": "Ajuste por Disputa no Respondida",
    "nan": "Bonificación Logística Flex",
    "bpp_covered": "Ajuste por Compra Protegida (BPP)",
    "partially_bpp_refunded": "Ajuste por Compra Protegida (BPP)",
    "compensated": "Cargo por devolución",
    "by_admin": "Bonificación Logística Flex",

    # Mercado Libre — Mediaciones y Cashback
    "Cancelación de la mediación": "Cancelación de la mediación",
    "Cancelacion de la mediacion": "Cancelación de la mediación",
    "Cancelacin de la mediacin": "Cancelación de la mediación",
    "cashback": "cashback",
    "cashback_cancel": "cashback_cancel",

    # Mercado Libre — Orphan codes que caían en fallback "histórico"
    "bought_by_mistake": "Ajuste por Arrepentimiento",
    "CREDIT_NOT_PROCESSED": "Bonificación Logística Flex",
    "damaged_package_broken_item_fashion": "Ajuste por Producto Dañado/Vacío",
    "different_color_or_size": "Ajuste por Diferencia de Publicación",
    "different_color_or_size_fashion_change": "Ajuste por Diferencia de Publicación",
    "different_item_other_change": "Ajuste por Diferencia de Publicación",
    "INVALID_AUTHORIZATION": "Bonificación Logística Flex",
    "item_not_useful_fashion_different": "Ajuste por Arrepentimiento",
    "item_not_useful_fashion_different_change": "Ajuste por Arrepentimiento",
    "missing_accessories": "Ajuste por Ítem Faltante",
    "missing_invoice": "Cargo por devolución",
    "not_expected_quality_different": "Ajuste por Diferencia de Publicación",
    "not_reconciled": "Bonificación Logística Flex",
    "ppv_covered_melienvio": "Ajuste por Compra Protegida (BPP)",
    "ppv_valid": "Ajuste por Compra Protegida (BPP)",
    "refund_account_money": "Bonificación Logística Flex",
    "refunded": "Bonificación Logística Flex",
    "unauthorized_purchase": "Ajuste por Disputa no Respondida",

    # RIPLEY
    "Gastos de envío pagados por el operador": "Gastos de envío pagados por el operador",
    "Gastos de envio pagados por el operador": "Gastos de envío pagados por el operador",
    "Gastos de envo pagados por el operador": "Gastos de envío pagados por el operador",
    "Gastos de envÃ­o pagados por el operador": "Gastos de envío pagados por el operador",
    "Comisiones sobre pedidos": "Comisiones sobre pedidos",
    "Pedidos reembolsados": "Pedidos reembolsados",
    "Comisiones": "Comisiones sobre pedidos",
    "A pagar": "A pagar",
    "Comisiones sobre pedidos reembolsados": "Comisiones sobre pedidos reembolsados",
    "Envío reembolsado": "Envío reembolsado",
    "Envio reembolsado": "Envío reembolsado",
    "Envo reembolsado": "Envío reembolsado",
    "EnvÃ­o reembolsado": "Envío reembolsado",
    "Gastos de envío reembolsados pagados por el operador": "Gastos de envío reembolsados pagados por el operador",
    "Gastos de envio reembolsados pagados por el operador": "Gastos de envío reembolsados pagados por el operador",
    "Gastos de envo reembolsados pagados por el operador": "Gastos de envío reembolsados pagados por el operador",
    "Gastos de envÃ­o reembolsados pagados por el operador": "Gastos de envío reembolsados pagados por el operador",
    "Abono oferta TC - OPEX": "Abono oferta TC - OPEX",
    "Descuento por cancelacion": "Descuento por cancelación",
    "Descuento por cancelacin": "Descuento por cancelación",
    "Descuento por cancelaciÃ³n": "Descuento por cancelación",
    "Otros abonos": "Otros abonos",
    "Otros descuentos": "Otros descuentos",
    "Abono postventa": "Abono postventa",
    "Importe del envío del pedido": "Importe del envío del pedido",
    "Gastos de envío": "Gastos de envío",
    "Importe de reembolso": "Importe de reembolso",
    "Importe del pedido reembolsado": "Importe del pedido reembolsado",
    "Importe del envío del pedido reembolsado": "Importe del envío del pedido reembolsado",
    "Comisión de reembolso": "Comisión de reembolso",
    "Impuesto sobre las comisiones": "Impuesto sobre las comisiones",
    "Impuesto sobre la comisión de reembolso": "Impuesto sobre la comisión de reembolso",
    "Impuesto de la factura manual": "Impuesto de la factura manual",
    "Factura manual": "Factura manual",
    "Recargo por precio mínimo": "Recargo por precio mínimo",

    # Ripley — Nuevos Conceptos Master Spec
    
    # Ripley — Additional operational/commercial fee mappings
    "Subtotal": "Subtotal",
    "Precio total": "Precio total",
    "order_amount": "order_amount",
    "Commission": "Commission",
    "commission_fee": "commission_fee",
    "refund_commission_fee": "refund_commission_fee",
    "Impuestos sobre comisión": "Impuestos sobre comisión",
    "Impuestos": "Impuestos",
    "Amount transferred to tienda": "Amount transferred to tienda",
    "transfer_amount": "transfer_amount",
    "refund_order_amount": "refund_order_amount",
    "Descuento por logística inversa (FF)": "Descuento por logística inversa (FF)",
    "Descuento por cofinanciamiento logístico (FF)": "Descuento por cofinanciamiento logístico (FF)",
    "Comisión": "Comisión",
    "Comision": "Comisión",
    "Comisin": "Comisión",
    "Abono por formalización a OPL": "Abono por formalización a OPL",
    "Abonos por cupón promocional": "Abonos por cupón promocional",
    "Cobro despacho primera milla": "Cobro despacho primera milla",
    "Descuento FF - Otros": "Descuento FF - Otros",
    "Descuento FF - pick and pack": "Descuento FF - pick and pack",
    "Descuento FF - sobreestadía": "Descuento FF - sobreestadía",
    "Descuento oferta TC - OPEX": "Descuento oferta TC - OPEX",
    "Descuento operacional": "Descuento operacional",
    "Descuento por PDM": "Descuento por PDM",
    "Descuento por cancelación": "Descuento por cancelación",
    "Descuento por compensación a cliente": "Descuento por compensación a cliente",
    "Descuento por costo logístico": "Descuento por costo logístico",
    "Descuento por cupones de despacho": "Descuento por cupones de despacho",
    "Descuento por error de clase logistica": "Descuento por error de clase logistica",
    "Abono por uso de flota propia": "Abono por uso de flota propia",
    "Abono por error de comisión": "Abono por error de comisión",
    "Abonos soluciones comerciales": "Abonos soluciones comerciales",
    "Abono extraordinario - error de precio": "Abono extraordinario - error de precio",

    # PARIS
    "Cobro por despacho": "Cobro por despacho",
    "Venta": "Venta",
    "Cargo por venta (Comisión)": "Cargo por venta (Comisión)",
    "Cargo por venta (Comision)": "Cargo por venta (Comisión)",
    "Devolución": "Devolución",
    "Devolucion": "Devolución",
    "Devolucin": "Devolución",
    "DevoluciÃ³n": "Devolución",
    "Devolucin": "Devolución",
    "Devolucin": "Devolución",
    "Despacho": "Despacho",
    "Logística inversa": "Logística inversa",
    "Logistica inversa": "Logística inversa",
    "Logstica inversa": "Logística inversa",
    "LogÃ­stica inversa": "Logística inversa",
    "Compensación logística": "Compensación logística",
    "Compensacion logistica": "Compensación logística",
    "Compensacin logstica": "Compensación logística",
    "CompensaciÃ³n logÃ­stica": "Compensación logística",
    "Compensacin logstica": "Compensación logística",
    "Compensacin logstica": "Compensación logística",
    # París — Nuevos Conceptos Master Spec
    "Cobro por campaña": "Cobro por campaña",
    "Cobro por campaa": "Cobro por campaña",
    "Cobro por campaa": "Cobro por campaña",
    "Rebate": "Rebate",
    "Cobro stock antiguo": "Cobro stock antiguo",
    "Ajuste Inventario Activo": "Ajuste Inventario Activo",
    "Retiro stock bodega Paris": "Retiro stock bodega Paris",
    "Merma": "Merma",
    "Multa": "Multa",
    "Multa por stock": "Multa por stock",

    # FALABELLA
    "Cobro por cofinanciamiento logístico": "Cobro por cofinanciamiento logístico",
    "Cobro por comisión por venta": "Cobro por comisión por venta",
    "Cobro por comisin por cancelacin": "Cobro por comisión por venta",
    "Cobro por comisión por cancelación": "Cobro por comisión por venta",
    "Cobro por comisin por cancelacin": "Cobro por comisión por venta",
    "Reversa de pago de envío comprador": "Reversa de pago de envío comprador",
    "Cobro Promo envío falabella.com": "Cobro Promo envío falabella.com",
    "Reembolso por Promo envío falabella.com": "Reembolso por Promo envío falabella.com",
    "Reembolso por comisión por venta": "Reembolso por comisión por venta",
    "Reembolso por comision por venta": "Reembolso por comisión por venta",
    "Reembolso por comisin por venta": "Reembolso por comisión por venta",
    "Reembolso por comisiÃ³n por venta": "Reembolso por comisión por venta",
    "Cobro por logística inversa": "Cobro por logística inversa",
    "Cobro por logistica inversa": "Cobro por logística inversa",
    "Cobro por logstica inversa": "Cobro por logística inversa",
    "Cobro por logÃ­stica inversa": "Cobro por logística inversa",
    # Falabella — Nuevos Conceptos Master Spec
    "Pago por precio del producto": "Pago por precio del producto",
    "Descuento por devolución de producto": "Descuento por devolución de producto",
    "Pago de envío comprador": "Pago de envío comprador",
    "Corrección de cobro por envío directo": "Corrección de cobro por envío directo",

    # SHOPIFY / MERCADO PAGO (Nuevos Conceptos Master Spec)
    # MASTER_MARKETPLACE_DICTIONARY_V1 — New canonical aliases
    "Campañas de publicidad - Product Ads": "Campañas de publicidad - Product Ads",
    "Campañas de publicidad - Brand Ads": "Campañas de publicidad - Brand Ads",
    "Cargo por campaña de publicidad - Display programático": "Cargo por campaña de publicidad - Display programático",
    "Descuento por logística inversa": "Descuento por logística inversa",
    "Pago por envío directo": "Pago por envío directo",
    "Corrección de pago envio directo": "Corrección de pago envio directo",
    "Corrección de cobro por envío directo": "Corrección de cobro por envío directo",

    # Mercado Libre — Mapeos Canónicos y Reservas
    "Pago": "Pago",
    "Mediación": "Mediación",
    "Mediacin": "Mediación",
    "Mediacion": "Mediación",
    "Reserva para pago de deuda": "Reserva para pago de deuda",
    "Reserva para devolución en envío BBP": "Reserva para devolución en envío BBP",
    "Reserva para devolucin en envo BBP": "Reserva para devolución en envío BBP",
    "Reserva para devolucion en envio BBP": "Reserva para devolución en envío BBP",
    "Devolución de dinero": "Devolución de dinero",
    "Devolucion de dinero": "Devolución de dinero",
    "Devolucin de dinero": "Devolución de dinero",
    "Reserva para pago": "Reserva para pago",
    "Reserva para reembolso": "Reserva para reembolso",

    # Falabella — Aportes Promocionales
    "Pago de aporte promocionales a cliente (Promo)": "Pago de aporte promocionales a cliente (Promo)",
    "Descuento por aportes promocionales a clientes (Promo)": "Descuento por aportes promocionales a clientes (Promo)",

    # YAML taxonomy additions (2026-07): sync with taxonomy_mappings.yaml
    "Pago normal": "Pago normal",
    "Publicidad": "Cargo por campaña de publicidad - Product Ads",
}

# ---------------------------------------------------------------------------
# FINANCIAL_STRUCTURE — Clasificación Contable según MASTER_DICTIONARY_V1
# ---------------------------------------------------------------------------
FINANCIAL_STRUCTURE = {
    "ingresos": [
        "Cargo por venta", "Cargo por venta (Venta)", "Venta", "Bonificación", "Rebate",
        "Compensación comercial", "Importe del pedido", "Importe del envío del pedido",
        "Despacho", "Sale amount", "Gross sales",
        "Pago por precio del producto",
        "Subtotal", "Precio total", "order_amount", "Pago normal"
    ],
    "devoluciones": [
        "Pedidos reembolsados", "Devolución", "Devolución de venta", "Devolución de dinero",
        "Descuento por devolución de producto",
        "Cancelación del cargo por diferencias en las medidas y el peso del paquete",
        "Importe del pedido reembolsado", "Importe del envío del pedido reembolsado",
        "Importe de reembolso",
        "refund_order_amount", "Devoluciones", "Abonos", "Reversos",
        # Poscobro reason_details removed from financial structure per PHASE_16F_STABILIZATION.
        # They are operational traceability only — see return_reason_traceability domain.
    ],
    "costos_operacionales": [
        "Cargo por envíos de Mercado Libre", "Cargo por Mercado Envíos",
        "Anulación del cargo por envíos de ML", "Anulación del cargo por Mercado Envíos",
        "Anulación del cargo por envíos de Mercado Libre",
        "Cargo por devolución", "Anulación del cargo por devolución",
        "Cargo por servicio de almacenamiento Full", "Cargo por retiro de stock Full",
        "Cargo por stock antiguo en Full", "Cargo por sobrepasar espacio Full",
        "Cargo por servicio de colecta Full", "Cargo por diferencias medidas/peso",
        "Cargo por diferencias en las medidas y el peso del paquete",
        "Gastos de envío pagados por el operador",
        "Gastos de envío reembolsados pagados por el operador",
        "Descuento por costo logístico", "Descuento por logística inversa",
        "Descuento por logistica inversa",
        "Cobro por despacho", "Logística inversa", "Retiro stock bodega Paris",
        "Cobro stock antiguo",
        "Cobro por cofinanciamiento logístico", "Reversa de pago de envío comprador",
        "Cobro por logística inversa", "Pago por envío directo",
        "Cobro despacho primera milla",
        "Descuento FF - Otros", "Descuento FF - pick and pack", "Descuento FF - sobreestadía",
        "Descuento operacional", "Descuento por error de clase logistica",
        "Abono por uso de flota propia",
        "Envío reembolsado",
        "Reembolso por Promo envío falabella.com", "Cobro Promo envío falabella.com",
        "Pago de envío comprador",
        "Envío", "Gastos de envío",
        "Descuento por logística inversa (FF)", "Descuento por cofinanciamiento logístico (FF)",
        "almacenamiento", "sobreestadía", "pick and pack", "VAS", "cargos fulfillment",
    ],
    "costos_comerciales": [
        "Cargo por venta (Comisión)", "Anulación del cargo por venta",
        "Reembolso por comisión",
        "Cargo por campaña de publicidad - Product Ads",
        "Campañas de publicidad - Product Ads",
        "Cargo por campaña de publicidad - Brand Ads",
        "Campañas de publicidad - Brand Ads", "Campañas de publicidad - Display",
        "Cargo por campaña de publicidad - Display programático",
        "Anulación cargo publicidad Product Ads",
        "Cargo por Asesoría Comercial", "Cargo por mantenimiento de Mi página",
        "Anulación del cargo por mantenimiento de Mi página",
        "Anulación mantenimiento Mi página",
        "Comisiones sobre pedidos",
        "Comisión de reembolso", "Impuesto sobre las comisiones", "Impuesto sobre la comisión de reembolso",
        "Impuesto de la factura manual", "Recargo por precio mínimo",
        "Comisiones sobre pedidos reembolsados",
        "Cobro por comisión por venta", "Reembolso por comisión por venta",
        "Abono oferta TC - OPEX", "Descuento oferta TC - OPEX",
        "Abonos por cupón promocional", "Descuento por cupones de despacho",
        "Abonos soluciones comerciales", "Descuento por PDM",
        "Pago de aporte promocionales a cliente (Promo)", "Descuento por aportes promocionales a clientes (Promo)",
        "Comisión", "Comisiones", "Cobro por comisión por cancelación", "Commission", "commission_fee", "refund_commission_fee"
    ],
    "recuperaciones_y_bonificaciones": [
        "Recuperación por Pérdida de Inventario",
        "Bonificación Logística Flex",
    ],

    "ajustes": [
        "Descuento por cancelación", "Otros descuentos",
        "Compensación logística", "Ajuste Inventario Activo",
        "Cobro por campaña", "Merma",
        "Multa", "Multa por stock",
        "Corrección de pago envio directo", "Corrección de cobro por envío directo",
        "Abono extraordinario - error de precio", "Abono por error de comisión",
        "Abono postventa", "Abono por formalización a OPL",
        "Otros abonos", "Descuento por compensación a cliente",
        # Legacy concepts (non-dictionary but still in ledger)
        "Mediación", "Reserva para devolución en envío BBP", "Reserva para reembolso",
        "Reserva para pago de deuda", "reserve_for_dispute", "Reserva para pago",
        "Abono de factura manual",
        "Factura manual",
        "Abono manual", "Ajuste histórico (pre-2026)",
        "Cargo",
        "Cancelación de la mediación", "cashback", "cashback_cancel",
        "Pago",
    ],
    "tesoreria": [
        "Retiro de dinero",
        "A pagar",
        "Amount transferred to tienda",
        "transfer_amount"
    ],
    "impuestos": [
        "Impuestos sobre comisión",
        "Impuestos"
    ]
}

def _fix_mojibake(text):
    """Fix double-encoded UTF-8 mojibake (exact replica of taxonomy_loader._fix_mojibake)."""
    try:
        return text.encode('latin-1').decode('utf-8')
    except Exception:
        return text


def normalize_detail(text):
    if not isinstance(text, str): return ""
    import unicodedata
    import re
    t = _fix_mojibake(text.strip()).lower()
    # Normalize unicode to NFD and strip Mn category (accents)
    t = ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')
    # Replace any weird characters/symbols (like replacement character) or multiple spaces
    t = re.sub(r'[^a-z0-9\s_]', '', t)
    # Simplify spaces
    t = re.sub(r'\s+', ' ', t).strip()
    return t

NORMALIZED_CLASSIFICATION_MAP = {
    normalize_detail(k): v for k, v in RAW_TO_CLASSIFICATION_MAP.items() if k
}

# Reverse map: clasificacion_operativa → financial_group
CLASIFICACION_TO_FINANCIAL_GROUP = {}
for group_name, labels in FINANCIAL_STRUCTURE.items():
    for label in labels:
        CLASIFICACION_TO_FINANCIAL_GROUP[label] = group_name

class MarketplaceAuditorEngine:
    def __init__(self, db=None):
        self.db = db if db is not None else DatabaseV4.get()

    def run_classification_for_transaction(self, transaction_id):
        self.db.execute("DELETE FROM marketplace_ledger_clasificado_v1 WHERE id_transaccion = ?", [transaction_id])
        source = self.db.query("SELECT marketplace, id_transaccion, id_orden, detalle, tipo_movimiento, monto, fecha FROM marketplace_ledger_v1 WHERE id_transaccion = ?", [transaction_id])
        if source.empty: return 0
        return self._classify_dataframe(source)

    def run_classification(self, marketplace=None):
        if marketplace:
            logger.info(f"Iniciando clasificación v4.0 para marketplace={marketplace}")
            self.db.execute("DELETE FROM marketplace_ledger_clasificado_v1 WHERE marketplace = ?", [marketplace])
            source = self.db.query("SELECT marketplace, id_transaccion, id_orden, detalle, tipo_movimiento, monto, fecha FROM marketplace_ledger_v1 WHERE marketplace = ?", [marketplace])
        else:
            logger.info("Iniciando clasificación v4.0 (Full Reset Vectorizado)")
            self.db.execute("DELETE FROM marketplace_ledger_clasificado_v1")
            source = self.db.query("SELECT marketplace, id_transaccion, id_orden, detalle, tipo_movimiento, monto, fecha FROM marketplace_ledger_v1")
        
        if source.empty: return 0
        return self._classify_dataframe(source)

    def _classify_dataframe(self, source):

        # Vectorized classification for high performance

        details = source['detalle'].astype(str).str.strip()
        
        # Handle blank/null/0/nan raw details
        blank_mask = details.isna() | details.str.lower().isin(['', '0', '0.0', 'nan', 'none', 'null'])
        details[blank_mask] = "Ajuste Poscobro"

        # Apply normalization and map
        norm_details = details.apply(normalize_detail)
        clean_names = norm_details.map(NORMALIZED_CLASSIFICATION_MAP)
        
        clasif = clean_names.copy()
        conf = pd.Series(1.0, index=source.index)
        origen = pd.Series("atomic_match", index=source.index)
        
        # Identify missing matches
        unmatched_mask = clean_names.isna()
        
        # 1. REGLA DINÁMICA DE TESORERÍA (Payouts y Retiros de Mercado Pago)
        payout_mask = unmatched_mask & (
            details.str.lower().str.contains('pre_payout_', na=False) |
            details.str.lower().str.contains('post_payout_', na=False) |
            details.str.lower().str.contains('withdraw', na=False) |
            details.str.lower().str.contains('retiro de dinero', na=False) |
            details.str.lower().str.contains('reserve_for_dispute', na=False)
        )
        clasif[payout_mask] = "Retiro de dinero"
        conf[payout_mask] = 1.0
        origen[payout_mask] = "payout_rule"
        
        # Update unmatched mask to exclude payouts
        unmatched_mask = unmatched_mask & ~payout_mask
        
        # Apply date and history rules for unmatched rows
        fechas = source['fecha'].astype(str).str[:10]
        ids = source['id_transaccion'].astype(str)
        
        # Historic pre-2026 rule
        historic_mask = unmatched_mask & (
            ((fechas != 'nan') & (fechas != 'NaT') & (fechas != 'None') & (fechas <= '2025-12-31')) |
            (ids.str.contains('2023') | ids.str.contains('2024') | ids.str.contains('2025'))
        )
        
        clasif[historic_mask] = "Ajuste histórico (pre-2026)"
        conf[historic_mask] = 1.0
        origen[historic_mask] = "auto_history"
        
        # Unrecognized rows mask
        unrecognized_mask = unmatched_mask & ~historic_mask
        clasif[unrecognized_mask] = "NO_CLASIFICADO"
        conf[unrecognized_mask] = 0.0
        origen[unrecognized_mask] = "unrecognized"
        
        # Determine include_in_operational_pnl (default is True)
        op_flag = pd.Series(True, index=source.index)
        
        # Isolated Mercado Libre Exclusion Patch: all rows operational except specific exclusions
        ml_mask = source['marketplace'] == 'ML'
        
        # MODERNIZED 2026-06-06: Excluir solo MECHANISMS (paired events con zero net cash).
        # ROOT_EVENT/REAL_CASH son OPERACIONALES (True): repentant_buyer, broken_item_fashion,
        #   bigger_than_expected_fashion, smaller_than_expected_fashion, etc.
        # Ver: governance/INCLUDE_IN_OPERATIONAL_PNL_FINAL_DECISION.md
        # Ver: governance/INCLUDE_IN_OPERATIONAL_PNL_TRUTH_REPORT.md
        ml_mandatory_exclusions = {
            "reserve_for_dispute",
            "Mediación",
            "bpp_refunded",
            "bpp_covered",
            "partially_bpp_refunded",
            "ppv_covered_melienvio",
            "ppv_valid",
            "reconciled",
            "AJUSTE POSCOBRO",
            "cashback",
            "cashback_cancel",
            "Reserva para devolución en envío BBP",
            "Retenciones & Provisiones",
            # ALL poscobro reason_details EXCLUDED from operational P&L per PHASE_16F_STABILIZATION.
            # These are operational traceability only, not financial concepts.
            # Both MECHANISMS (paired, zero net cash) and ROOT_EVENT (prior certified as same-event):
            "Ajuste por Compra Protegida (BPP)",
            "Ajuste por Disputa no Respondida",
            "Ajuste por Arrepentimiento",
            "Ajuste por Talla/Garantía", 
            "Ajuste por Producto Dañado/Vacío",
            "Ajuste por Diferencia de Publicación",
            "Ajuste por Ítem Faltante",
            "Ajuste por Retraso en Entrega",
            "Ajuste por Cambio de Dirección",
            "Ajuste por Falla en Entrega",
            "Ajuste por Falta de Stock",
        }

        is_excluded = (
            clasif.isin(ml_mandatory_exclusions) | 
            details.isin(ml_mandatory_exclusions) |
            details.str.lower().str.contains('reserve_for_dispute|withdraw|retiro de dinero|mediacion|mediacin|mediación', na=False)
        )
        
        op_flag[ml_mask] = ~is_excluded[ml_mask]

        # General treasury/payable exclusion across all marketplaces
        general_exclusions = {"A pagar", "Pago", "Liberación de dinero", "Retiro de dinero", "Transferencia", "Retenciones & Provisiones", "Amount transferred to tienda", "transfer_amount"}
        op_flag[clasif.isin(general_exclusions) | details.isin(general_exclusions)] = False

        # Ripley duplicate-order validation gate (ADJ_03):
        # order_id present simultaneously in Importe del pedido + Precio total + Subtotal
        # must produce exactly one SIGNAL contributor.
        ripley_mask = source['marketplace'] == 'RIPLEY'
        is_importe = source['detalle'] == 'Importe del pedido'
        is_precio = source['detalle'] == 'Precio total'
        is_subtotal = source['detalle'] == 'Subtotal'
        
        overlapping_orders = set()
        if ripley_mask.any():
            orders_with_importe = set(source[ripley_mask & is_importe]['id_orden'].dropna())
            orders_with_precio = set(source[ripley_mask & is_precio]['id_orden'].dropna())
            orders_with_subtotal = set(source[ripley_mask & is_subtotal]['id_orden'].dropna())
            overlapping_orders = orders_with_importe.intersection(orders_with_precio).intersection(orders_with_subtotal)
            
        # Exclude cycles and TH rows from operational P&L (ADJ_01)
        ripley_exclude_mask = ripley_mask & (
            source['id_transaccion'].astype(str).str.startswith('RIP_CSV_') | 
            source['id_transaccion'].astype(str).str.startswith('RIP_TH_')
        )
        op_flag[ripley_exclude_mask] = False
        
        # Exclude duplicates from operational P&L if all three details are present (ADJ_03)
        if overlapping_orders:
            exclude_duplicates_mask = ripley_mask & source['id_orden'].isin(overlapping_orders) & (is_precio | is_subtotal)
            op_flag[exclude_duplicates_mask] = False

        # Map clasificacion to financial group directly
        financial_group_col = clasif.map(CLASIFICACION_TO_FINANCIAL_GROUP)

        results = pd.DataFrame({
            'clasificacion_operativa': clasif,
            'confianza_clasificacion': conf,
            'origen_clasificacion': origen,
            'include_in_operational_pnl': op_flag,
            'financial_group': financial_group_col
        })

        out = pd.concat([source[['marketplace', 'id_transaccion', 'id_orden', 'detalle', 'tipo_movimiento', 'monto', 'fecha']], results], axis=1)
        n = self.db.insert_df(out, "marketplace_ledger_clasificado_v1")
        
        # Aplicar correcciones manuales guardadas para que persistan
        try:
            self.db.execute("SELECT 1 FROM marketplace_correcciones_v1 LIMIT 1")
            self.db.execute("""
                UPDATE marketplace_ledger_clasificado_v1
                SET clasificacion_operativa = mc.detalle_corregido,
                    origen_clasificacion = 'manual_correction',
                    confianza_clasificacion = 1.0
                FROM marketplace_correcciones_v1 mc
                WHERE marketplace_ledger_clasificado_v1.id_transaccion = mc.id_transaccion
            """)
        except Exception:
            pass # Tabla aún no creada

        # Propagar clasificacion_operativa y financial_group a marketplace_ledger_v1
        try:
            case_clauses = " ".join(
                f"WHEN '{co.replace(chr(39), chr(39)+chr(39))}' THEN '{fg}'"
                for co, fg in CLASIFICACION_TO_FINANCIAL_GROUP.items()
                if co
            )
            import tempfile
            tmp_dir = tempfile.gettempdir().replace("\\", "/")
            self.db.execute(f"SET temp_directory='{tmp_dir}';")
            # Match on (id_transaccion, detalle) because id_transaccion is not unique per row
            sql = f"""
                UPDATE marketplace_ledger_v1
                SET clasificacion_operativa = sub.clasificacion_operativa,
                    include_in_operational_pnl = sub.include_in_operational_pnl,
                    financial_group = CASE sub.clasificacion_operativa
                        {case_clauses}
                        ELSE NULL
                    END
                FROM marketplace_ledger_clasificado_v1 sub
                WHERE marketplace_ledger_v1.id_transaccion = sub.id_transaccion
                  AND marketplace_ledger_v1.detalle = sub.detalle
            """
            self.db.execute(sql)
            logger.info("Propagated classification to marketplace_ledger_v1")
        except Exception as e:
            logger.warning(f"SQL propagation failed: {e}")
            # Fallback: propagation via Python (only if SQL fails)
            try:
                logger.info("Fallback: propagating via Python loop...")
                rows = self.db.query("""
                    SELECT id_transaccion, detalle, clasificacion_operativa, include_in_operational_pnl
                    FROM marketplace_ledger_clasificado_v1
                """)
                for _, r in rows.iterrows():
                    fg = CLASIFICACION_TO_FINANCIAL_GROUP.get(r['clasificacion_operativa'])
                    self.db.execute(
                        "UPDATE marketplace_ledger_v1 SET clasificacion_operativa=?, include_in_operational_pnl=?, financial_group=? WHERE id_transaccion=? AND detalle=?",
                        [r['clasificacion_operativa'], bool(r['include_in_operational_pnl']), fg, r['id_transaccion'], r['detalle']]
                    )
                logger.info(f"Fallback propagation complete: {len(rows)} rows")
            except Exception as e2:
                logger.warning(f"Fallback propagation also failed: {e2}")

        log_event(logger, "classification_completed", table="marketplace_ledger_clasificado_v1", count=n)
        try:
            self.db.execute("INSERT INTO pipeline_log (event, status, details) VALUES ('classification', 'COMPLETED', ?)", [f"Clasificadas {n} filas en marketplace_ledger_clasificado_v1"])
        except Exception:
            pass  # pipeline_log table may not exist
        return n

    def run_financial_closing(self, marketplace, periodo_inicio, periodo_fin):
        self.db.execute("DELETE FROM marketplace_cierre_financiero_v1 WHERE marketplace = ? AND CAST(periodo_inicio AS DATE) = CAST(? AS DATE) AND CAST(periodo_fin AS DATE) = CAST(? AS DATE)", [marketplace, periodo_inicio, periodo_fin])
        
        def fmt(items): return "'" + "','".join(items) + "'"
        
        sql = f"""
            SELECT 
                SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ingresos"])}) THEN monto ELSE 0 END) as total_ingresos,
                SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["devoluciones"])}) THEN monto ELSE 0 END) as total_devoluciones,
                SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_operacionales"])}) THEN monto ELSE 0 END) as total_costos_op,
                SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_comerciales"])}) THEN monto ELSE 0 END) as total_costos_com,
                SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ajustes"])}) OR clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["recuperaciones_y_bonificaciones"])}) OR clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["impuestos"])}) THEN monto ELSE 0 END) as total_ajustes
            FROM marketplace_ledger_clasificado_v1
            WHERE marketplace = ? AND fecha BETWEEN ? AND ?
              AND include_in_operational_pnl = TRUE
        """
        
        stats = self.db.query(sql, [marketplace, periodo_inicio, periodo_fin]).iloc[0]
        
        def _safe(v):
            """Guard against NaN/None from empty SUM(): NaN or 0 == NaN in Python!"""
            import math
            try:
                f = float(v)
                return 0.0 if (math.isnan(f) or math.isinf(f)) else f
            except (TypeError, ValueError):
                return 0.0

        ing = _safe(stats['total_ingresos'])
        dev = _safe(stats['total_devoluciones'])
        cop = _safe(stats['total_costos_op'])
        ccm = _safe(stats['total_costos_com'])
        aju = _safe(stats['total_ajustes'])
        neto = ing + dev + cop + ccm + aju

        # total_ajustes en la tabla almacena devoluciones+ajustes para compatibilidad
        self.db.execute("""
            INSERT INTO marketplace_cierre_financiero_v1 
            (marketplace, periodo_inicio, periodo_fin, total_ingresos, total_costos_operacionales, 
             total_costos_comerciales, total_ajustes, resultado_neto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [marketplace, periodo_inicio, periodo_fin, ing, cop, ccm, dev + aju, neto])
        
        logger.info(f"CIERRE {periodo_inicio}: Ing={ing:,.0f} Dev={dev:,.0f} CostOp={cop:,.0f} CostCom={ccm:,.0f} Aju={aju:,.0f} NETO={neto:,.0f}")
        try:
            self.db.execute("INSERT INTO pipeline_log (event, status, details) VALUES ('closing', 'COMPLETED', ?)",
                            [f"{marketplace} {periodo_inicio} a {periodo_fin}: Neto=${neto:,.0f}"])
        except Exception:
            pass
        return {"neto": neto, "ingresos": ing, "devoluciones": dev, "costos_op": cop, "costos_com": ccm, "ajustes": aju}

    def run_audit(self):
        self.db.execute("DELETE FROM marketplace_auditoria_v1")
        
        # 1. No Clasificados
        self.db.execute("""
            INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken, order_id)
            SELECT marketplace, 'movimientos_no_clasificados', 'Detalle "' || detalle || '" desconocido', 'Radar Alert', id_transaccion
            FROM marketplace_ledger_clasificado_v1 WHERE clasificacion_operativa = 'NO_CLASIFICADO'
        """)
        
        # 2. Validación OTROS <= 5% (Monto Absoluto)
        total_monto = self.db.query("SELECT COALESCE(SUM(ABS(monto)), 0) as total FROM marketplace_ledger_v1").iloc[0]['total']
        if total_monto > 0:
            unclassified_monto = self.db.query("""
                SELECT COALESCE(SUM(ABS(monto)), 0) as total 
                FROM marketplace_ledger_clasificado_v1
                WHERE clasificacion_operativa = 'NO_CLASIFICADO'
            """).iloc[0]['total']
            
            porcentaje = (unclassified_monto / total_monto) * 100
            if porcentaje > 5.0:
                self.db.execute(f"""
                    INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken, order_id)
                    VALUES ('ML', 'limite_otros_excedido', 'Movimientos NO_CLASIFICADO representan el {porcentaje:.2f}% del total absoluto ({unclassified_monto:,.2f}/{total_monto:,.2f})', 'Reclasificación Requerida', 'GLOBAL_AUDIT')
                """)
        
        # 3. Integración de Auditoría de clasificación ML (MISCLASSIFIED)
        try:
            from engine.v4.marketplace_auditor_ml import audit_ml_misclassifications
            # Ponemos a salvo la instancia de la DB para que no de error
            audit_ml_misclassifications()
        except Exception as e:
            logger.error(f"Error running audit_ml_misclassifications: {e}")
        
        # 4. ML-specific audit checks (ML has 0 rows in legacy auditor due to false negative bugs)
        self._audit_ml_dte_coverage()
        self._audit_ml_adjustment_ratio()
        self._audit_ml_period_gap()
        
        # 5. Certificación Legal (Crucial) — FIXED: exact match instead of LIKE suffix to prevent
        # false negatives for ML's structured folio_xml format (033-XXXXXXX)
        try:
            self.db.execute("SELECT 1 FROM document_match_v1 LIMIT 1")
            has_document_match = True
        except Exception:
            has_document_match = False
        
        norm = "regexp_replace(regexp_replace(l.folio_xml, '\\.0$', ''), '^[0-9]+-0*', '')"
        l_sub = "(SELECT DISTINCT folio_xml, id_orden, marketplace FROM marketplace_ledger_v1 WHERE COALESCE(include_in_operational_pnl, 1) = 1 AND folio_xml IS NOT NULL AND folio_xml <> 'None' AND folio_xml NOT LIKE '%disponible%' AND folio_xml NOT LIKE 'A%n%')"
        # RIPLEY excluded from cargo_sin_respaldo_legal per PHASE_16F_STABILIZATION:
        # P16F-04 confirmed 12,822/12,822 are false positives — XLSX order refs vs SII DTE folios
        # are structurally different numbering systems. Settlement Bridge pending.
        ripley_exclude = "AND LOWER(l.marketplace) <> 'ripley'"
        if has_document_match:
            self.db.execute(f"""
                INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken, order_id)
                SELECT
                    l.marketplace,
                    'cargo_sin_respaldo_legal',
                    'Folio ' || l.folio_xml || ' no existe en DTE Truth ni en Conciliación',
                    'Certificación Fallida',
                    l.id_orden
                FROM {l_sub} l
                LEFT JOIN dte_truth_v1 t ON {norm} = t.folio
                LEFT JOIN document_match_v1 m ON l.id_orden = m.order_id
                WHERE t.folio IS NULL
                  AND m.match_id IS NULL
                  AND (
                    l.id_orden NOT LIKE '%2023%'
                    AND l.id_orden NOT LIKE '%2024%'
                    AND l.id_orden NOT LIKE '%2025%'
                  )
                  {ripley_exclude}
            """)
        else:
            self.db.execute(f"""
                INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken, order_id)
                SELECT
                    l.marketplace,
                    'cargo_sin_respaldo_legal',
                    'Folio ' || l.folio_xml || ' no existe en DTE Truth',
                    'Certificación Fallida',
                    l.id_orden
                FROM {l_sub} l
                LEFT JOIN dte_truth_v1 t ON {norm} = t.folio
                WHERE t.folio IS NULL
                  AND (
                    l.id_orden NOT LIKE '%2023%'
                    AND l.id_orden NOT LIKE '%2024%'
                    AND l.id_orden NOT LIKE '%2025%'
                  )
                  {ripley_exclude}
            """)

        # Ripley-specific audit: document the structural folio limitation
        self._audit_ripley_folio_coverage()

        n = self.db.count("marketplace_auditoria_v1")
        logger.info(f"Auditoría completada: {n} hallazgos en marketplace_auditoria_v1")
        try:
            self.db.execute("INSERT INTO pipeline_log (event, status, details) VALUES ('audit', 'COMPLETED', ?)", [f"Auditoría completada: {n} hallazgos en marketplace_auditoria_v1"])
        except Exception:
            pass
        return n

    def _audit_ripley_folio_coverage(self):
        """Document Ripley folio situation: XLSX refs vs SII DTE folios are structurally incompatible.
        Inserts a single informational entry per audit run, not per-row false positives."""
        try:
            ripley_folio_count = self.db.query("""
                SELECT COUNT(*) as cnt,
                       COUNT(DISTINCT folio_xml) as distinct_folios,
                       SUM(CASE WHEN folio_xml IS NOT NULL AND folio_xml <> 'None' THEN 1 ELSE 0 END) as with_folio
                FROM marketplace_ledger_v1
                WHERE LOWER(marketplace) = 'ripley'
                  AND COALESCE(include_in_operational_pnl, 1) = 1
            """).iloc[0]
            total = int(ripley_folio_count['cnt'])
            distinct = int(ripley_folio_count['distinct_folios'])
            with_folio = int(ripley_folio_count['with_folio'])
            pct = round(with_folio / total * 100, 1) if total > 0 else 0
            self.db.execute("""
                INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken, order_id)
                VALUES ('RIPLEY', 'folio_estructural_sin_respaldo_sii',
                        'Ripley folios son referencias XLSX (' || ? || ' distinct, ' || ? || '% cobertura). '
                        'No son folios SII DTE. Requiere Settlement Bridge para certificación legal.',
                        'Certificación Legal PENDIENTE — Settlement Bridge requerido',
                        'GLOBAL_AUDIT')
            """, [distinct, pct])
            logger.info(f"Ripley folio coverage: {with_folio}/{total} ({pct}%), {distinct} distinct. Structural limitation documented.")
        except Exception as e:
            logger.error(f"Ripley folio coverage check failed: {e}")

    def _audit_ml_dte_coverage(self):
        """Check ML DTE coverage: folio_xml vs total rows."""
        try:
            res = self.db.query("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN folio_xml IS NOT NULL THEN 1 ELSE 0 END) as with_xml
                FROM marketplace_ledger_v1
                WHERE LOWER(marketplace) = 'ml'
            """).iloc[0]
            total = int(res['total'])
            with_xml = int(res['with_xml'])
            cov = (with_xml / total * 100) if total > 0 else 0
            if cov < 50.0:
                self.db.execute("""
                    INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken, order_id)
                    VALUES ('ML', 'dte_coverage_baja', 'Cobertura DTE ML solo ' || ? || '% (' || ? || '/' || ? || ')', 'Monitoreo Requerido', 'GLOBAL_AUDIT')
                """, [round(cov, 1), with_xml, total])
                logger.info(f"Audit ML: DTE Coverage={cov:.1f}% ({with_xml}/{total}) — BAJA")
            else:
                logger.info(f"Audit ML: DTE Coverage={cov:.1f}% ({with_xml}/{total}) — OK")
        except Exception as e:
            logger.error(f"ML DTE coverage check failed: {e}")

    def _audit_ml_adjustment_ratio(self):
        """Check ML adjustment ratio: ajustes+riesgos+recuperaciones vs ingresos."""
        try:
            res = self.db.query("""
                SELECT
                    COALESCE(SUM(CASE WHEN LOWER(financial_group) = 'ingresos' THEN ABS(monto) ELSE 0 END), 0) as gross,
                    COALESCE(SUM(CASE WHEN LOWER(financial_group) IN ('ajustes', 'recuperaciones_y_bonificaciones') THEN ABS(monto) ELSE 0 END), 0) as adjustments
                FROM marketplace_ledger_v1
                WHERE LOWER(marketplace) = 'ml'
                  AND COALESCE(include_in_operational_pnl, 1) = 1
            """).iloc[0]
            gross = float(res['gross'])
            adj = float(res['adjustments'])
            ratio = (adj / gross * 100) if gross > 0 else 0
            logger.info(f"Audit ML: Adjustment Ratio={ratio:.1f}% (${adj:,.0f} adj on ${gross:,.0f} gross)")
            if ratio > 70.0:
                self.db.execute("""
                    INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken, order_id)
                    VALUES ('ML', 'ajuste_ratio_elevada', 'Ajustes representan ' || ? || '% del ingreso bruto', 'Monitoreo Requerido', 'GLOBAL_AUDIT')
                """, [round(ratio, 1)])
        except Exception as e:
            logger.error(f"ML adjustment ratio check failed: {e}")

    def _audit_ml_period_gap(self):
        """Check ML data freshness — latest period with revenue."""
        try:
            res = self.db.query("""
                SELECT MAX(fecha) as ultima_fecha,
                       COUNT(*) as total_rows
                FROM marketplace_ledger_v1
                WHERE LOWER(marketplace) = 'ml'
                  AND LOWER(financial_group) = 'ingresos'
                  AND monto > 0
            """).iloc[0]
            last_date = str(res['ultima_fecha'])[:10] if res['ultima_fecha'] else 'N/A'
            total = int(res['total_rows'])
            from datetime import datetime, timedelta
            today = datetime.now().strftime('%Y-%m-%d')
            if last_date != 'N/A':
                last_dt = datetime.strptime(last_date[:10], '%Y-%m-%d')
                days_gap = (datetime.now() - last_dt).days
                logger.info(f"Audit ML: Last revenue date={last_date}, gap={days_gap}d, rows={total}")
                if days_gap > 60:
                    self.db.execute("""
                        INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken, order_id)
                        VALUES ('ML', 'periodo_desactualizado', 'Último ingreso ML: ' || ? || ' (hace ' || ? || ' días)', 'Carga de Datos Requerida', 'GLOBAL_AUDIT')
                    """, [last_date, days_gap])
            else:
                logger.warning("Audit ML: No revenue data found")
        except Exception as e:
            logger.error(f"ML period gap check failed: {e}")

    def add_correction(self, id_transaccion, detalle_original, detalle_corregido, motivo, usuario="system"):
        self.db.execute("""
            INSERT INTO marketplace_correcciones_v1 (id_transaccion, detalle_original, detalle_corregido, motivo, usuario)
            VALUES (?, ?, ?, ?, ?)
        """, [id_transaccion, detalle_original, detalle_corregido, motivo, usuario])
        
        self.db.execute("""
            UPDATE marketplace_ledger_clasificado_v1
            SET clasificacion_operativa = ?, origen_clasificacion = 'manual_correction', confianza_clasificacion = 1.0
            WHERE id_transaccion = ?
        """, [detalle_corregido, id_transaccion])
        log_event(logger, "manual_correction", id=id_transaccion, new_detail=detalle_corregido)
