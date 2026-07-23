import pandas as pd
from pathlib import Path
import os
import shutil

def main():
    root = Path('.').resolve()
    base_out = root / "data" / "db" / "f5_03_uploads" / "01_Raw"
    
    if base_out.exists():
        shutil.rmtree(base_out, ignore_errors=True)
    
    # ML
    ml_src = root / "tests" / "fixtures" / "f3_03" / "f3_03_fixture.xlsx"
    ml_dst = base_out / "ML" / "Facturacion" / "ml_golden.xlsx"
    ml_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ml_src, ml_dst)
    
    # PARIS
    # C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\PARIS\Transacciones\Dropshipping\01-2025.xlsx
    paris_src = root / "01_Raw" / "PARIS" / "Transacciones" / "Dropshipping" / "01-2025.xlsx"
    paris_dst = base_out / "PARIS" / "Transacciones" / "Dropshipping" / "paris_golden.xlsx"
    paris_dst.parent.mkdir(parents=True, exist_ok=True)
    if paris_src.exists():
        df = pd.read_excel(paris_src, nrows=10)
        df.to_excel(paris_dst, index=False)
        print("PARIS done")
        
    # RIPLEY
    # C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\RIPLEY\Ciclos de facturacion\05-01-2026 - 13-01-2026\Exportar_datos (6).csv
    ripley_src = root / "01_Raw" / "RIPLEY" / "Ciclos de facturacion" / "05-01-2026 - 13-01-2026" / "Exportar_datos (6).csv"
    if not ripley_src.exists():
        # Fallback to finding one
        ripley_src = list((root / "01_Raw" / "RIPLEY").rglob("*.csv"))[0]
    ripley_dst = base_out / "RIPLEY" / ripley_src.parent.name / "ripley_golden.csv"
    ripley_dst.parent.mkdir(parents=True, exist_ok=True)
    if ripley_src.exists():
        df = pd.read_csv(ripley_src, sep=';', encoding='latin1', nrows=10)
        df.to_csv(ripley_dst, sep=';', encoding='latin1', index=False)
        print("RIPLEY done")
        
    # FALABELLA
    # C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\FALABELLA\Ordenes y Transacciones\1  abril   2026 al 5  abril   2026.xlsx
    fala_src = list((root / "01_Raw" / "FALABELLA").rglob("*.xlsx"))[0]
    fala_dst = base_out / "FALABELLA" / fala_src.parent.name / "falabella_golden.xlsx"
    fala_dst.parent.mkdir(parents=True, exist_ok=True)
    if fala_src.exists():
        df = pd.read_excel(fala_src, nrows=10)
        df.to_excel(fala_dst, index=False)
        print("FALABELLA done")

if __name__ == '__main__':
    main()
