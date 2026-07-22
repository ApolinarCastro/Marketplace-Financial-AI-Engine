import re

path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """    <script src="https://cdn.tailwindcss.com">
        // Exposed to global scope"""

replacement = """    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        body { background-color: #f8fafc; color: #334155; font-family: 'Outfit', sans-serif; }
        .surgical-card { background: white; border-radius: 0.75rem; border: 1px solid #e2e8f0; }
        .amount-pos { color: #047857; font-weight: 600; }
        .amount-neg { color: #dc2626; font-weight: 600; }
    </style>
    <script>
        // Exposed to global scope"""

if target in content:
    content = content.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed HTML head")
else:
    print("Target not found")
