with open('engine/v4/dte_indexer.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw"\\ML\\Documentos Recepcionados")',
    'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw" / "ML" / "Documentos Recepcionados"'
)
text = text.replace(
    'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw"\\PARIS\\Facturacion")',
    'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw" / "PARIS" / "Facturacion"'
)
text = text.replace(
    'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw"\\FALABELLA\\Documentos Recepcionados")',
    'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw" / "FALABELLA" / "Documentos Recepcionados"'
)
text = text.replace(
    'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw"\\RIPLEY\\XML")',
    'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw" / "RIPLEY" / "XML"'
)

with open('engine/v4/dte_indexer.py', 'w', encoding='utf-8') as f:
    f.write(text)
