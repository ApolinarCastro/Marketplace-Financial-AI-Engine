"""
test_taxonomy_equivalence.py — FASE GREEN: parallel classification comparison.

Verifies that YAML-based classification produces EXACTLY the same results
as the legacy Python-based classification for all 4 marketplaces.
100% equivalence required. Delta = 0.
"""
import pytest
import pandas as pd
from taxonomy import taxonomy_loader as tl
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import (
    RAW_TO_CLASSIFICATION_MAP,
    FINANCIAL_STRUCTURE,
    CLASIFICACION_TO_FINANCIAL_GROUP,
    NORMALIZED_CLASSIFICATION_MAP,
    normalize_detail as legacy_normalize,
)


# ── Structural tests (FASE RED) ──

class TestTaxonomyStructure:
    """Verify YAML files == Python structures with 100% equivalence."""

    def test_group_count_matches(self):
        rules = tl.load_rules()
        assert set(rules.keys()) == set(FINANCIAL_STRUCTURE.keys())

    def test_concept_list_matches(self):
        rules = tl.load_rules()
        for group, concepts in FINANCIAL_STRUCTURE.items():
            yaml_concepts = set(rules[group]["concepts"])
            py_concepts = set(concepts)
            assert yaml_concepts == py_concepts, (
                f"Group '{group}' mismatch. "
                f"Missing in YAML: {py_concepts - yaml_concepts}. "
                f"Extra in YAML: {yaml_concepts - py_concepts}"
            )

    def test_mapping_count_matches(self):
        mappings = tl.load_mappings()
        assert len(mappings) == len(RAW_TO_CLASSIFICATION_MAP)

    def test_normalized_map_matches(self):
        rules = tl.load_rules()
        mappings = tl.load_mappings()
        yaml_norm = tl.build_normalized_mappings(mappings)
        assert len(yaml_norm) == len(NORMALIZED_CLASSIFICATION_MAP)
        for norm_key, expected_concept in NORMALIZED_CLASSIFICATION_MAP.items():
            assert yaml_norm.get(norm_key) == expected_concept, f"Norm key mismatch: {norm_key}"

    def test_concept_to_group_matches(self):
        rules = tl.load_rules()
        concept_map = tl.build_concept_to_group_map(rules)
        for concept, expected_group in CLASIFICACION_TO_FINANCIAL_GROUP.items():
            assert concept_map.get(concept) == expected_group, f"Group mismatch: {concept}"

    def test_validate_taxonomy_consistent(self):
        rules = tl.load_rules()
        mappings = tl.load_mappings()
        v = tl.validate_taxonomy(rules, mappings)
        # Dynamic concepts are expected, not a failure
        dynamic_issues = [i for i in v.get("issues", []) if "dynamic" in i]
        other_issues = [i for i in v.get("issues", []) if "dynamic" not in i]
        assert len(other_issues) == 0, f"Unexpected validation issues: {other_issues}"


# ── Runtime equivalence tests (FASE GREEN) ──

@pytest.fixture(scope="module")
def db():
    return DatabaseV4.get()


@pytest.fixture(scope="module")
def all_ledger_rows(db):
    """Load all ledger rows once for classification comparison."""
    return db.query("SELECT marketplace, id_transaccion, id_orden, detalle, tipo_movimiento, monto, fecha FROM marketplace_ledger_v1")


class TestTaxonomyRuntimeEquivalence:
    """Run both classification methods and verify 100% identical results."""

    def _legacy_classify(self, source: pd.DataFrame) -> pd.DataFrame:
        """Replicate the legacy run_classification logic for comparison."""
        details = source['detalle'].astype(str).str.strip()
        blank_mask = details.isna() | details.str.lower().isin(['', '0', '0.0', 'nan', 'none', 'null'])
        details[blank_mask] = "Ajuste Poscobro"
        norm_details = details.apply(legacy_normalize)
        clean_names = norm_details.map(NORMALIZED_CLASSIFICATION_MAP)
        clasif = clean_names.copy()
        conf = pd.Series(1.0, index=source.index)
        origen = pd.Series("atomic_match", index=source.index)
        unmatched_mask = clean_names.isna()

        # Payout rule
        payout_mask = unmatched_mask & (
            details.str.lower().str.contains('pre_payout_|post_payout_|withdraw|retiro de dinero|reserve_for_dispute', na=False)
        )
        clasif[payout_mask] = "Retiro de dinero"
        conf[payout_mask] = 1.0
        origen[payout_mask] = "payout_rule"
        unmatched_mask = unmatched_mask & ~payout_mask

        fechas = source['fecha'].astype(str).str[:10]
        ids = source['id_transaccion'].astype(str)
        historic_mask = unmatched_mask & (
            ((fechas != 'nan') & (fechas != 'NaT') & (fechas != 'None') & (fechas <= '2025-12-31')) |
            (ids.str.contains('2023') | ids.str.contains('2024') | ids.str.contains('2025'))
        )
        clasif[historic_mask] = "Ajuste histórico (pre-2026)"
        conf[historic_mask] = 1.0
        origen[historic_mask] = "auto_history"
        unmasked = unmatched_mask & ~historic_mask
        clasif[unmasked] = "NO_CLASIFICADO"
        conf[unmasked] = 0.0
        origen[unmasked] = "unrecognized"

        # include_in_operational_pnl
        op_flag = pd.Series(True, index=source.index)
        ml_mask = source['marketplace'] == 'ML'
        ml_exclusions = {
            "reserve_for_dispute", "Mediación", "bpp_refunded", "bpp_covered",
            "partially_bpp_refunded", "ppv_covered_melienvio", "ppv_valid",
            "reconciled", "AJUSTE POSCOBRO", "cashback", "cashback_cancel",
            "Reserva para devolución en envío BBP", "Retenciones & Provisiones",
            "Ajuste por Compra Protegida (BPP)", "Ajuste por Disputa no Respondida",
        }
        is_excluded = (
            clasif.isin(ml_exclusions) |
            details.isin(ml_exclusions) |
            details.str.lower().str.contains('reserve_for_dispute|withdraw|retiro de dinero|mediacion|mediacin|mediación', na=False)
        )
        op_flag[ml_mask] = ~is_excluded[ml_mask]
        general_exclusions = {"A pagar", "Pago", "Liberación de dinero", "Retiro de dinero",
                              "Transferencia", "Retenciones & Provisiones",
                              "Amount transferred to tienda", "transfer_amount"}
        op_flag[clasif.isin(general_exclusions) | details.isin(general_exclusions)] = False

        # Financial group
        financial_group_col = clasif.map(CLASIFICACION_TO_FINANCIAL_GROUP)

        return pd.DataFrame({
            'clasificacion_operativa': clasif,
            'confianza_clasificacion': conf,
            'origen_clasificacion': origen,
            'include_in_operational_pnl': op_flag,
            'financial_group': financial_group_col,
        })

    def _yaml_classify(self, source: pd.DataFrame) -> pd.DataFrame:
        """Classify using YAML taxonomy (same logic, YAML data)."""
        rules = tl.load_rules()
        mappings = tl.load_mappings()
        concept_to_group = tl.build_concept_to_group_map(rules)
        norm_map = tl.build_normalized_mappings(mappings)

        details = source['detalle'].astype(str).str.strip()
        blank_mask = details.isna() | details.str.lower().isin(['', '0', '0.0', 'nan', 'none', 'null'])
        details[blank_mask] = "Ajuste Poscobro"
        norm_details = details.apply(tl.normalize_detail)
        clean_names = norm_details.map(norm_map)
        clasif = clean_names.copy()
        conf = pd.Series(1.0, index=source.index)
        origen = pd.Series("atomic_match", index=source.index)
        unmatched_mask = clean_names.isna()

        payout_mask = unmatched_mask & (
            details.str.lower().str.contains('pre_payout_|post_payout_|withdraw|retiro de dinero|reserve_for_dispute', na=False)
        )
        clasif[payout_mask] = "Retiro de dinero"
        conf[payout_mask] = 1.0
        origen[payout_mask] = "payout_rule"
        unmatched_mask = unmatched_mask & ~payout_mask

        fechas = source['fecha'].astype(str).str[:10]
        ids = source['id_transaccion'].astype(str)
        historic_mask = unmatched_mask & (
            ((fechas != 'nan') & (fechas != 'NaT') & (fechas != 'None') & (fechas <= '2025-12-31')) |
            (ids.str.contains('2023') | ids.str.contains('2024') | ids.str.contains('2025'))
        )
        clasif[historic_mask] = "Ajuste histórico (pre-2026)"
        conf[historic_mask] = 1.0
        origen[historic_mask] = "auto_history"
        unmasked = unmatched_mask & ~historic_mask
        clasif[unmasked] = "NO_CLASIFICADO"
        conf[unmasked] = 0.0
        origen[unmasked] = "unrecognized"

        op_flag = pd.Series(True, index=source.index)
        ml_mask = source['marketplace'] == 'ML'
        ml_exclusions = {
            "reserve_for_dispute", "Mediación", "bpp_refunded", "bpp_covered",
            "partially_bpp_refunded", "ppv_covered_melienvio", "ppv_valid",
            "reconciled", "AJUSTE POSCOBRO", "cashback", "cashback_cancel",
            "Reserva para devolución en envío BBP", "Retenciones & Provisiones",
            "Ajuste por Compra Protegida (BPP)", "Ajuste por Disputa no Respondida",
        }
        is_excluded = (
            clasif.isin(ml_exclusions) |
            details.isin(ml_exclusions) |
            details.str.lower().str.contains('reserve_for_dispute|withdraw|retiro de dinero|mediacion|mediacin|mediación', na=False)
        )
        op_flag[ml_mask] = ~is_excluded[ml_mask]
        general_exclusions = {"A pagar", "Pago", "Liberación de dinero", "Retiro de dinero",
                              "Transferencia", "Retenciones & Provisiones",
                              "Amount transferred to tienda", "transfer_amount"}
        op_flag[clasif.isin(general_exclusions) | details.isin(general_exclusions)] = False

        financial_group_col = clasif.map(concept_to_group)

        return pd.DataFrame({
            'clasificacion_operativa': clasif,
            'confianza_clasificacion': conf,
            'origen_clasificacion': origen,
            'include_in_operational_pnl': op_flag,
            'financial_group': financial_group_col,
        })

    @pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
    def test_classification_identical(self, all_ledger_rows, mp):
        """Verify legacy and YAML classification produce identical results per marketplace."""
        mp_rows = all_ledger_rows[all_ledger_rows['marketplace'] == mp].copy()
        if mp_rows.empty:
            pytest.skip(f"No data for {mp}")

        legacy = self._legacy_classify(mp_rows)
        yaml = self._yaml_classify(mp_rows)

        assert len(legacy) == len(yaml), f"Row count mismatch for {mp}"

        # Compare each field
        for field in ['clasificacion_operativa', 'confianza_clasificacion',
                       'origen_clasificacion', 'include_in_operational_pnl',
                       'financial_group']:
            legacy_vals = legacy[field].fillna("__NONE__")
            yaml_vals = yaml[field].fillna("__NONE__")
            mismatches = (legacy_vals != yaml_vals)
            n_mismatch = mismatches.sum()
            assert n_mismatch == 0, (
                f"{mp}: {n_mismatch} mismatches in '{field}'. "
                f"Examples: {mp_rows[mismatches][['detalle', 'id_transaccion']].head(3).to_dict('records')}"
            )

    @pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
    def test_financial_group_monetary_equivalence(self, all_ledger_rows, mp):
        """Verify SUM(monto) per financial_group is identical between legacy and YAML."""
        mp_rows = all_ledger_rows[all_ledger_rows['marketplace'] == mp].copy()
        if mp_rows.empty:
            pytest.skip(f"No data for {mp}")

        legacy = self._legacy_classify(mp_rows)
        yaml = self._yaml_classify(mp_rows)

        legacy['monto'] = mp_rows['monto'].values
        yaml['monto'] = mp_rows['monto'].values

        leg_agg = legacy.groupby('financial_group')['monto'].sum()
        yam_agg = yaml.groupby('financial_group')['monto'].sum()

        all_groups = set(list(leg_agg.index) + list(yam_agg.index))
        for g in all_groups:
            lv = leg_agg.get(g, 0)
            yv = yam_agg.get(g, 0)
            assert abs(lv - yv) < 0.01, (
                f"{mp} financial_group '{g}': legacy={lv:.2f} vs yaml={yv:.2f}, delta={lv-yv:.2f}"
            )

    @pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
    def test_operational_pnl_equivalence(self, all_ledger_rows, mp):
        """Verify SUM(monto) for operational_pnl is identical."""
        mp_rows = all_ledger_rows[all_ledger_rows['marketplace'] == mp].copy()
        if mp_rows.empty:
            pytest.skip(f"No data for {mp}")

        legacy = self._legacy_classify(mp_rows)
        yaml = self._yaml_classify(mp_rows)

        legacy['monto'] = mp_rows['monto'].values
        yaml['monto'] = mp_rows['monto'].values

        leg_op = legacy[legacy['include_in_operational_pnl'] == True]['monto'].sum()
        yam_op = yaml[yaml['include_in_operational_pnl'] == True]['monto'].sum()
        assert abs(leg_op - yam_op) < 0.01, (
            f"{mp} operational PnL: legacy={leg_op:.2f} vs yaml={yam_op:.2f}, delta={leg_op-yam_op:.2f}"
        )
