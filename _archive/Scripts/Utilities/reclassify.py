from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
import calendar
engine = MarketplaceAuditorEngine()
engine.run_classification()
for year in [2025, 2026]:
    for month in range(1, 13):
        last_day = calendar.monthrange(year, month)[1]
        p_ini = f"{year}-{month:02d}-01"
        p_fin = f"{year}-{month:02d}-{last_day}"
        engine.run_financial_closing("RIPLEY", p_ini, p_fin)
