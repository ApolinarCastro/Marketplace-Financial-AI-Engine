import re

with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

fixed = re.sub(
    r'recEl\.innerHTML\s*=\s*<p class="text-xs text-slate-500 italic">No backend source available</p>;',
    r'recEl.innerHTML = <p class="text-xs text-slate-500 italic">No backend source available</p>;',
    content
)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(fixed)
print('Fixed in dashboard.html')
