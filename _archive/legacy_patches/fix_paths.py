import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if 'import os' not in text:
        text = 'import os\n' + text
        
    old_root_1 = 'Path(r"C:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine")'
    old_root_2 = 'Path(r"C:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine\\'
    new_root = 'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent))'
    
    # Replace ROOT exact match
    text = text.replace(old_root_1, new_root)
    
    # For xml_matcher and dte_indexer that append paths
    text = text.replace('Path(r"C:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine\\01_Raw', 'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw"')
    text = text.replace('Path(r"C:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine\\\\01_Raw', 'Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent)) / "01_Raw"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

fix_file('engine/v4/surgical_loader.py')
fix_file('engine/v4/surgical_xml_justifier.py')
fix_file('engine/v4/xml_matcher.py')
fix_file('engine/v4/dte_indexer.py')
