from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

print("Running classification...")
engine = MarketplaceAuditorEngine()
n = engine.run_classification()
print(f"Classified {n} rows.")
