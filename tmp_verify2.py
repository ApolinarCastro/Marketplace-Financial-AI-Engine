import sys, warnings; sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine'); warnings.filterwarnings('ignore')
import duckdb
con = duckdb.connect(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\meli_financial_v4.db', read_only=True)

print('=== ML: Paired mechanism totals in ledger_clasificado ===')
r = con.execute("""
    SELECT clasificacion_operativa, COUNT(*) as n, ROUND(SUM(monto),0) as total
    FROM marketplace_ledger_clasificado_v1
    WHERE marketplace='ML' AND clasificacion_operativa IN ('Ajuste por Compra Protegida (BPP)','Ajuste Poscobro Conciliado','Ajuste Poscobro General')
    GROUP BY clasificacion_operativa ORDER BY total DESC
""").fetchdf()
print(r.to_string(index=False))

print('\n=== ML: Neto comparison ===')
r2 = con.execute("""
    SELECT 
      ROUND(SUM(CASE WHEN clasificacion_operativa IN ('Ajuste por Compra Protegida (BPP)','Ajuste Poscobro Conciliado','Ajuste Poscobro General') THEN monto ELSE 0 END),0) as paired_total,
      ROUND(SUM(monto),0) as ledger_total,
      ROUND(SUM(CASE WHEN clasificacion_operativa NOT IN ('Ajuste por Compra Protegida (BPP)','Ajuste Poscobro Conciliado','Ajuste Poscobro General') THEN monto ELSE 0 END),0) as neto_sin_paired
    FROM marketplace_ledger_clasificado_v1 WHERE marketplace='ML'
""").fetchdf().iloc[0]
print(f'Paired mechanisms total:  ${float(r2["paired_total"]):>12,.0f}')
print(f'Ledger TOTAL:             ${float(r2["ledger_total"]):>12,.0f}')
print(f'Neto SIN paired:          ${float(r2["neto_sin_paired"]):>12,.0f}')

r3 = con.execute("SELECT ROUND(SUM(resultado_neto),0) as neto FROM marketplace_cierre_financiero_v1 WHERE marketplace='ML'").fetchdf().iloc[0]
print(f'Cierre Neto (post-fix):   ${float(r3["neto"]):>12,.0f}')
delta = float(r2["neto_sin_paired"]) - float(r3["neto"])
print(f'Delta ledger vs cierre:   ${delta:>12,.0f}')

# Per-period comparison
print('\n=== Per-period: Clasificado vs Cierre ===')
rows = con.execute("""
    SELECT c.periodo_inicio, c.resultado_neto as cierre_neto,
           ROUND(SUM(CASE WHEN l.clasificacion_operativa NOT IN ('Ajuste por Compra Protegida (BPP)','Ajuste Poscobro Conciliado','Ajuste Poscobro General') THEN l.monto ELSE 0 END),0) as clasif_neto
    FROM marketplace_cierre_financiero_v1 c
    LEFT JOIN marketplace_ledger_clasificado_v1 l ON l.marketplace=c.marketplace 
        AND CAST(l.fecha AS DATE) >= CAST(c.periodo_inicio AS DATE)
        AND CAST(l.fecha AS DATE) <= CAST(c.periodo_fin AS DATE)
        AND l.marketplace='ML'
    WHERE c.marketplace='ML'
    GROUP BY c.periodo_inicio, c.resultado_neto
    ORDER BY c.periodo_inicio
""").fetchdf()
print(rows.to_string(index=False))

print('\n=== dte_truth_v1 check ===')
try:
    r4 = con.execute("SELECT COUNT(*) as n FROM dte_truth_v1").fetchdf().iloc[0]
    print(f'dte_truth_v1 has {int(r4["n"])} rows')
except Exception as e:
    print(f'dte_truth_v1 error: {e}')

print('\n=== auditoria_v1 breakdown ===')
r5 = con.execute("SELECT marketplace, check_name, COUNT(*) as n FROM marketplace_auditoria_v1 GROUP BY marketplace, check_name ORDER BY marketplace, n DESC").fetchdf()
print(r5.to_string(index=False))

con.close()
