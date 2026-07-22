import uuid

class RipleyETL:
    def __init__(self):
        self.memory_ledger = []
        
    def _create_base_record(self, settlement_data, dte_data, group, amount, status):
        # Fallbacks for missing data
        settle = settlement_data or {}
        dte = dte_data or {}
        
        return {
            "id_orden": settle.get("id_orden_compra"),
            "fecha": settle.get("fecha_liquidado"),
            "monto": amount,
            "financial_group": group,
            "folio_xml": dte.get("folio_dte"),
            "id_transaccion": str(uuid.uuid4()) if amount is not None else None,
            "status": status,
            "marketplace": "RIPLEY"
        }
        
    def transform_comision(self, settlement_data, dte_data):
        if not settlement_data:
            return self._create_base_record(None, dte_data, "costos_comerciales", None, "MISSING_SETTLEMENT")
        if not dte_data:
            return self._create_base_record(settlement_data, None, "costos_comerciales", None, "BLOCKED_BY_SOURCE_DATA")
            
        settle_amt = settlement_data.get("monto_comision_settle", 0)
        dte_amt = dte_data.get("monto_comision", 0)
        
        if settle_amt != dte_amt:
            return self._create_base_record(settlement_data, dte_data, "costos_comerciales", None, "DIFFERENCE_REJECTED")
            
        return self._create_base_record(settlement_data, dte_data, "costos_comerciales", -dte_amt, "VALIDATED")

    def transform_opex(self, settlement_data, dte_data):
        if not settlement_data:
            return self._create_base_record(None, dte_data, "costos_operacionales", None, "MISSING_SETTLEMENT")
        if not dte_data:
            return self._create_base_record(settlement_data, None, "costos_operacionales", None, "BLOCKED_BY_SOURCE_DATA")
            
        settle_amt = settlement_data.get("monto_opex_settle", 0)
        dte_amt = dte_data.get("costo_operacional", 0)
        
        if settle_amt != dte_amt:
            return self._create_base_record(settlement_data, dte_data, "costos_operacionales", None, "DIFFERENCE_REJECTED")
            
        return self._create_base_record(settlement_data, dte_data, "costos_operacionales", -dte_amt, "VALIDATED")

    def transform_otros_cobros(self, settlement_data, dte_data):
        if not settlement_data:
            return self._create_base_record(None, dte_data, "otros_costos", None, "MISSING_SETTLEMENT")
        if not dte_data:
            return self._create_base_record(settlement_data, None, "otros_costos", None, "BLOCKED_BY_SOURCE_DATA")
            
        settle_amt = settlement_data.get("monto_otros_settle", 0)
        dte_amt = dte_data.get("otros_cobros", 0)
        
        if settle_amt != dte_amt:
            return self._create_base_record(settlement_data, dte_data, "otros_costos", None, "DIFFERENCE_REJECTED")
            
        return self._create_base_record(settlement_data, dte_data, "otros_costos", -dte_amt, "VALIDATED")

    def transform_promotional_recovery(self, dte_data):
        if not dte_data:
            return self._create_base_record(None, None, "promociones_y_reembolsos", None, "BLOCKED_BY_SOURCE_DATA")
        amt = dte_data.get("monto_recuperacion", 0)
        return self._create_base_record(None, dte_data, "promociones_y_reembolsos", amt, "VALIDATED")

    def transform_credit_note_compensation(self, dte_data):
        if not dte_data:
            return self._create_base_record(None, None, "costos_comerciales", None, "BLOCKED_BY_SOURCE_DATA")
        amt = dte_data.get("monto_reverso_comision", 0)
        return self._create_base_record(None, dte_data, "costos_comerciales", amt, "VALIDATED")

    def run_pipeline_in_memory(self, input_records):
        self.memory_ledger = []
        settlements = {r["id_orden_compra"]: r for r in input_records if r.get("type") == "SETTLE"}
        dtes = {r["id_orden_compra"]: r for r in input_records if r.get("type") == "DTE" and r.get("id_orden_compra")}
        
        validations_passed = True
        
        for order_id, settle in settlements.items():
            dte = dtes.get(order_id)
            
            # Venta (Settlement Only)
            venta_rec = self._create_base_record(settle, None, "ventas", settle.get("monto_venta"), "VALIDATED")
            self.memory_ledger.append(venta_rec)
            
            # Comision
            if "monto_comision_settle" in settle:
                com_rec = self.transform_comision(settle, dte)
                self.memory_ledger.append(com_rec)
                if com_rec["status"] != "VALIDATED": validations_passed = False
                
            # OPEX
            if "monto_opex_settle" in settle:
                opex_rec = self.transform_opex(settle, dte)
                self.memory_ledger.append(opex_rec)
                if opex_rec["status"] != "VALIDATED": validations_passed = False
                
        return {
            "validations_passed": validations_passed,
            "promoted_records": [r for r in self.memory_ledger if r["status"] == "VALIDATED"]
        }
