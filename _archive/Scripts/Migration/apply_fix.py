import re, json

with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Generate syntax_before.diff
diff = '''--- templates/dashboard.html
+++ templates/dashboard.html
@@ -1218,2 +1218,2 @@
-                    const recEl = document.getElementById('doc-recommendations');
-                    recEl.innerHTML = <p class="text-xs text-slate-500 italic">No backend source available</p>;
+                    const recEl = document.getElementById('doc-recommendations');
+                    recEl.innerHTML = <p class="text-xs text-slate-500 italic">No backend source available</p>;
'''
with open('syntax_before.diff', 'w', encoding='utf-8') as f:
    f.write(diff)

# Surgical Repair
fixed_content = content.replace(
    'recEl.innerHTML = <p class="text-xs text-slate-500 italic">No backend source available</p>;',
    'recEl.innerHTML = <p class="text-xs text-slate-500 italic">No backend source available</p>;'
)
with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print('Surgical fix applied.')
