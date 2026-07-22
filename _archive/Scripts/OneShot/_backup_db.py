
import shutil
src = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\meli_financial_v4.db'
dst = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\backups\meli_financial_v4_CERTIFIED_BASELINE_V1_20260624_150042.db'
shutil.copy2(src, dst)
print("copied", os.path.getsize(dst))
