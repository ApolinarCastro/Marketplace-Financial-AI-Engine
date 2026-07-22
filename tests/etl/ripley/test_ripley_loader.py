import pytest
from engine.v4.etl.ripley_loader import RipleyETL

class TestRipleyETL:
    def setup_method(self):
        self.etl = RipleyETL()
    
    def test_comisiones(self):
        settlement_data = {"id_orden_compra": "ORD123", "fecha_liquidado": "2026-06-01", "monto_venta": 1000, "monto_comision_settle": 100}
        dte_data = {"monto_comision": 100, "folio_dte": 999}
        result = self.etl.transform_comision(settlement_data, dte_data)
        assert result["monto"] == -100
        assert result["financial_group"] == "costos_comerciales"
        assert result["status"] == "VALIDATED"
        
    def test_opex(self):
        settlement_data = {"id_orden_compra": "ORD123", "fecha_liquidado": "2026-06-01", "monto_opex_settle": 50}
        dte_data = {"costo_operacional": 50, "folio_dte": 999}
        result = self.etl.transform_opex(settlement_data, dte_data)
        assert result["monto"] == -50
        assert result["financial_group"] == "costos_operacionales"
        assert result["status"] == "VALIDATED"
        
    def test_otros_cobros(self):
        settlement_data = {"id_orden_compra": "ORD123", "monto_otros_settle": 20}
        dte_data = {"otros_cobros": 20, "folio_dte": 999}
        result = self.etl.transform_otros_cobros(settlement_data, dte_data)
        assert result["monto"] == -20
        assert result["financial_group"] == "otros_costos"
        
    def test_promotional_recovery(self):
        dte_data = {"tipo_dte": 33, "monto_recuperacion": 300, "folio_dte": 888}
        result = self.etl.transform_promotional_recovery(dte_data)
        assert result["monto"] == 300
        assert result["financial_group"] == "promociones_y_reembolsos"
        assert result["status"] == "VALIDATED"
        
    def test_credit_note_compensation(self):
        dte_data = {"tipo_dte": 61, "monto_reverso_comision": 50, "folio_dte": 777}
        result = self.etl.transform_credit_note_compensation(dte_data)
        assert result["monto"] == 50
        assert result["financial_group"] == "costos_comerciales"
        assert result["status"] == "VALIDATED"
        
    def test_ausencia_facturacion(self):
        settlement_data = {"id_orden_compra": "ORD123", "monto_comision_settle": 100}
        result = self.etl.transform_comision(settlement_data, None)
        assert result["status"] == "BLOCKED_BY_SOURCE_DATA"
        
    def test_ausencia_settlement(self):
        dte_data = {"monto_comision": 100, "folio_dte": 999}
        result = self.etl.transform_comision(None, dte_data)
        assert result["status"] == "MISSING_SETTLEMENT"
        
    def test_diferencias(self):
        settlement_data = {"id_orden_compra": "ORD123", "monto_comision_settle": 100}
        dte_data = {"monto_comision": 101, "folio_dte": 999}
        result = self.etl.transform_comision(settlement_data, dte_data)
        assert result["status"] == "DIFFERENCE_REJECTED"
        
    def test_end_to_end_ripley_pipeline(self):
        pipeline_result = self.etl.run_pipeline_in_memory([
            {"type": "SETTLE", "id_orden_compra": "ORD1", "monto_venta": 1000, "monto_comision_settle": 100},
            {"type": "DTE", "folio_dte": 999, "id_orden_compra": "ORD1", "monto_comision": 100}
        ])
        assert pipeline_result["validations_passed"] == True
        assert len(pipeline_result["promoted_records"]) == 2
