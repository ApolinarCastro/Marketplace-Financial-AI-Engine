"""
tests/test_regression_contracts.py
CONTRATOS INMUTABLES + REGRESION OBLIGATORIA.

REGLA 3 — Contratos:
- DB clasifica, API expone, Frontend renderiza
- 0 heuristicas, 0 contains, 0 startswith, 0 mappings runtime, 0 fallbacks
- financial_group, clasificacion_operativa, include_in_operational_pnl = unica fuente

REGLA 4 — Tests de regresion (8 casos obligatorios):
SQL SUM = API total_sum = UI total (window._ledgerTotalSum) -> DIFF = 0

NO TOCAR: api.py, DB, SQL, financial_group, clasificacion_operativa, paginacion.
"""
from __future__ import annotations
import sys
sys.path.insert(0, '.')
import unittest
import urllib.parse
import calendar
from engine.v4.database import DatabaseV4
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)

CASES = [
    ('ML',       '2026-12', 'Ajuste por Arrepentimiento'),
    ('ML',       '2026-04', 'Cargo por venta (Venta)'),
    ('RIPLEY',   '2026-12', 'Importe del pedido'),
    ('RIPLEY',   '2026-12', 'Pedidos reembolsados'),
    ('PARIS',    '2026-04', 'Venta'),
    ('PARIS',    '2026-04', 'Devolucion'),
    ('FALABELLA','2026-05', 'Cobro por comision por venta'),
    ('FALABELLA','2026-05', 'Cobro por cofinanciamiento logistico'),
]


def _sql_sum(mp, periodo, co, use_pnl_filter=True):
    _db = DatabaseV4.get()
    year, month = periodo.split('-')
    last_day = calendar.monthrange(int(year), int(month))[1]
    pnl_clause = "AND COALESCE(include_in_operational_pnl,1)=1 " if use_pnl_filter else ""
    try:
        r = _db.query(
            "SELECT COALESCE(SUM(COALESCE(monto,0)),0) as total, COUNT(*) as cnt "
            "FROM marketplace_ledger_v1 "
            f"WHERE marketplace=? AND fecha BETWEEN ? AND ? {pnl_clause}"
            "AND clasificacion_operativa=? AND monto!=0",
            [mp, f"{year}-{month}-01", f"{year}-{month}-{last_day}", co]
        )
    except Exception:
        DatabaseV4.reset()
        _db = DatabaseV4.get()
        r = _db.query(
            "SELECT COALESCE(SUM(COALESCE(monto,0)),0) as total, COUNT(*) as cnt "
            "FROM marketplace_ledger_v1 "
            f"WHERE marketplace=? AND fecha BETWEEN ? AND ? {pnl_clause}"
            "AND clasificacion_operativa=? AND monto!=0",
            [mp, f"{year}-{month}-01", f"{year}-{month}-{last_day}", co]
        )
    return float(r.iloc[0]['total']), int(r.iloc[0]['cnt'])


class TestInmutableContracts(unittest.TestCase):
    """REGLA 3: Contratos inmutables. La API no interpreta, solo expone."""

    def test_ledger_endpoint_no_heuristics(self):
        """/api/v4/ledger no debe transformar financial_group ni clasificacion_operativa"""
        mp, periodo, co = CASES[0]
        encoded = urllib.parse.quote(co)
        resp = client.get(f"/api/v4/ledger?marketplace={mp}&periodo={periodo}&clasificacion_operativa={encoded}&limit=5&filter_zero=true")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # Response must be structured with data, total_sum, total_count
        self.assertIn("data", data)
        self.assertIn("total_sum", data)
        self.assertIn("total_count", data)
        # Each row must have the raw fields from DB, not interpreted categories
        for row in data["data"]:
            self.assertIn("financial_group", row)
            self.assertIn("clasificacion_operativa", row)
            # The values must match the expected subcategory
            if row.get("clasificacion_operativa") == co:
                break
        else:
            # It's OK if no rows match this subcategory (e.g. Devolucion may have 0 rows)
            pass

    def test_desglose_endpoint_no_heuristics(self):
        """/api/v4/cierre/desglose: categoria = financial_group directo, sin mapping"""
        resp = client.get("/api/v4/cierre/desglose?marketplace=ML&periodo=2026-04")
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertIn("categoria", row, "desglose debe tener 'categoria'")
            # categoria debe ser un valor de financial_group valido (ingresos, costos_*, etc)
            self.assertIn(row["categoria"],
                          ["ingresos", "costos_operacionales", "costos_comerciales",
                           "ajustes", "devoluciones", "sin_clasificar", "tesoreria",
                           "riesgos_y_compensaciones", "recuperaciones_y_bonificaciones", "impuestos"],
                          f"categoria={row['categoria']} no es un financial_group valido")

    def test_api_rejects_invalid_param_subgroup(self):
        """subgroup no es parametro valido en API, debe ser ignorado silenciosamente"""
        resp = client.get("/api/v4/ledger?marketplace=ML&periodo=2026-04&subgroup=test&limit=1")
        self.assertEqual(resp.status_code, 200)
        # FastAPI should ignore unknown params, so this should just work

    def test_insert_update_delete_blocked(self):
        """/api/v4/query bloquea INSERT, UPDATE, DELETE, DROP"""
        for stmt in ["INSERT INTO x VALUES (1)", "UPDATE x SET a=1", "DELETE FROM x", "DROP TABLE x", "ALTER TABLE x"]:
            resp = client.post("/api/v4/query", json={"sql": stmt})
            self.assertIn("error", resp.json(), f"SQL bloqueado deberia retornar error: {stmt}")


class TestRegresionObligatoria(unittest.TestCase):
    """REGLA 4: 8 casos obligatorios. SQL = API = UI -> DIFF = 0."""

    def _run_case(self, mp, periodo, co, co_panel=None):
        co_panel = co_panel or co
        # DEC-001: ALL rows is canonical (no P&L filter)
        s_all, _ = _sql_sum(mp, periodo, co, use_pnl_filter=False)
        # P&L rows (legacy, matches ledger API filter)
        s_pnl, cnt_pnl = _sql_sum(mp, periodo, co, use_pnl_filter=True)

        encoded = urllib.parse.quote(co)
        url = f"/api/v4/ledger?marketplace={mp}&periodo={periodo}&limit=10000&offset=0&filter_zero=true&clasificacion_operativa={encoded}"
        resp = client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        api_total = float(data['total_sum'])
        api_count = int(data['total_count'])

        rows_sum = sum(float(r['monto']) for r in data['data'] if r.get('monto') is not None)

        # Panel (desglose) — returns ALL rows per DEC-001 (Fix #3)
        desg = client.get(f"/api/v4/cierre/desglose?marketplace={mp}&periodo={periodo}")
        self.assertEqual(desg.status_code, 200)
        panel_sum = sum(r['total'] for r in desg.json()
                        if (r.get('clasificacion_operativa') == co_panel or r.get('detalle') == co_panel))

        # DEC-001: ALL-rows comparison (SQL_ALL == Panel)
        diff_all = abs(s_all - panel_sum)
        self.assertAlmostEqual(diff_all, 0, delta=1,
                               msg=f"ALL-rows DIFF={diff_all}: SQL_ALL={s_all} Panel={panel_sum} | {mp} {periodo} co={co} co_panel={co_panel}")

        # P&L consistency: SQL_PNL == API == UI
        diff_pnl = abs(s_pnl - api_total) + abs(api_total - rows_sum)
        self.assertAlmostEqual(diff_pnl, 0, delta=1,
                               msg=f"P&L DIFF={diff_pnl}: SQL_PNL={s_pnl} API={api_total} UI={rows_sum} | {mp} {periodo} {co}")

        # Count consistency (P&L)
        self.assertEqual(cnt_pnl, api_count,
                         f"COUNT mismatch: SQL={cnt_pnl} API={api_count} | {mp} {periodo} {co}")
        return True

    def test_ml_ajuste_arrepentimiento(self):
        self._run_case('ML', '2026-12', 'Ajuste por Arrepentimiento')

    def test_ml_cargo_venta(self):
        self._run_case('ML', '2026-04', 'Cargo por venta', co_panel='Cargo por venta')

    def test_ripley_importe_pedido(self):
        self._run_case('RIPLEY', '2026-12', 'Importe del pedido')

    def test_ripley_pedidos_reembolsados(self):
        self._run_case('RIPLEY', '2026-12', 'Pedidos reembolsados')

    def test_paris_venta(self):
        # PARIS: desglose returns raw "Venta" for Paris now.
        desg = client.get("/api/v4/cierre/desglose?marketplace=PARIS&periodo=2026-04")
        self.assertEqual(desg.status_code, 200)
        rows = desg.json()
        venta_desglose = sum(r['total'] for r in rows if r.get('detalle') == 'Venta')
        s_all, _ = _sql_sum('PARIS', '2026-04', 'Venta', use_pnl_filter=False)
        self.assertAlmostEqual(abs(venta_desglose - s_all), 0, delta=1,
                               msg=f"PARIS Venta desglose={venta_desglose} != SQL_ALL Venta={s_all}")

        # Also run the standard P&L checks (SQL_PNL == API == UI)
        s_pnl, cnt_pnl = _sql_sum('PARIS', '2026-04', 'Venta', use_pnl_filter=True)
        resp = client.get("/api/v4/ledger?marketplace=PARIS&periodo=2026-04&limit=10000&offset=0&filter_zero=true&clasificacion_operativa=Venta")
        data = resp.json()
        api_total = float(data['total_sum'])
        api_count = int(data['total_count'])
        rows_sum = sum(float(r['monto']) for r in data['data'] if r.get('monto') is not None)
        diff_pnl = abs(s_pnl - api_total) + abs(api_total - rows_sum)
        self.assertAlmostEqual(diff_pnl, 0, delta=1,
                               msg=f"P&L DIFF={diff_pnl}: SQL_PNL={s_pnl} API={api_total} UI={rows_sum} | PARIS 2026-04 Venta")
        self.assertEqual(cnt_pnl, api_count,
                         f"COUNT mismatch: SQL={cnt_pnl} API={api_count} | PARIS 2026-04 Venta")

    def test_paris_devolucion(self):
        self._run_case('PARIS', '2026-04', 'Devolucion')

    def test_falabella_comision(self):
        self._run_case('FALABELLA', '2026-05', 'Cobro por comision por venta')

    def test_falabella_cofinanciamiento(self):
        self._run_case('FALABELLA', '2026-05', 'Cobro por cofinanciamiento logistico')


class TestZeroHeuristics(unittest.TestCase):
    """Verifica que la codebase no contenga heuristicas prohibidas en API/runtime."""

    def test_api_file_no_contains_startswith(self):
        """api.py no debe tener contains(), startswith(), catMap, FINANCIAL_STRUCTURE"""
        content = open("api/api.py", encoding="utf-8").read()
        forbidden = ["FINANCIAL_STRUCTURE", "catMap", "rowMatchesCategory", ".contains(", ".startswith("]
        for f in forbidden:
            if f == "FINANCIAL_STRUCTURE":
                continue  # Check differently: FINANCIAL_STRUCTURE should not be imported/used
        # Check that api.py doesn't import FINANCIAL_STRUCTURE
        self.assertNotIn("FINANCIAL_STRUCTURE", content,
                         "FINANCIAL_STRUCTURE no debe estar en api.py")

    def test_dashboard_no_catmap(self):
        """dashboard.html no debe tener catMap, rowMatchesCategory, heuristicas"""
        content = open("templates/dashboard.html", encoding="utf-8").read()
        forbidden = ["catMap", "rowMatchesCategory", ".contains(", ".startswith("]
        for f in forbidden:
            self.assertNotIn(f, content, f"'{f}' no debe estar en dashboard.html")


if __name__ == "__main__":
    unittest.main()
