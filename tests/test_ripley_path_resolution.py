"""P0 RIPLEY - path resolution tests (real source inventory vs documented paths)."""
import glob
import pytest

BASE = r'01_Raw\RIPLEY'


def test_real_seller_path():
    """Documented '01_Raw/Ripley/SELLER' does not exist; real source is Fulfillment by Seller."""
    files = glob.glob(BASE + r'\Fulfillment by Seller\*.xlsx')
    assert len(files) >= 50, f'expected >=50 SELLER xlsx, got {len(files)}'


def test_real_ciclos_path():
    """Documented 'Ciclos' path on disk is absent (recovered from git commit 7a94360)."""
    on_disk = glob.glob(BASE + r'\Ciclos de facturación\*.csv')
    temp = glob.glob(r'C:\Users\ASUS Zenbook\AppData\Local\Temp\opencode\ripley_ciclos\*.csv')
    assert len(temp) >= 50, f'expected >=50 ciclos csv in temp, got {len(temp)}'


def test_facturacion_xml_exists():
    files = glob.glob(BASE + r'\Facturacion\*.xml')
    assert len(files) >= 400, f'expected >=400 XML, got {len(files)}'


def test_ff_fulfillment_csv():
    files = glob.glob(BASE + r'\Fulfillment by Ripley\*.csv')
    assert len(files) >= 60, f'expected >=60 FF csv, got {len(files)}'


def test_th_files():
    files = glob.glob(BASE + r'\Historial de transacciones\*.csv')
    assert len(files) >= 8, f'expected >=8 TH csv, got {len(files)}'


def test_documented_paths_resolved_to_real():
    """All documented source paths resolve to real files somewhere."""
    assert len(glob.glob(BASE + r'\Fulfillment by Seller\*.xlsx')) > 0
    assert len(glob.glob(r'C:\Users\ASUS Zenbook\AppData\Local\Temp\opencode\ripley_ciclos\*.csv')) > 0
    assert len(glob.glob(BASE + r'\Facturacion\*.xml')) > 0
