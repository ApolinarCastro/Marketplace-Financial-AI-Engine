# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
XML_DIR = DATA_DIR / "xml"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = DATA_DIR / "outputs"

MARKETPLACES = [
    "mercadolibre",
    "ripley",
    "paris",
    "falabella",
    "shopify"
]

def ensure_dirs():
    for p in [RAW_DIR, XML_DIR, PROCESSED_DIR, OUTPUTS_DIR]:
        p.mkdir(parents=True, exist_ok=True)
    for m in MARKETPLACES:
        (RAW_DIR / m).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_dirs()
    print("Estructura de directorios sincronizada.")
