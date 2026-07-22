import re

with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace doc-recommendations innerHTML setting
rec_hardcode = '''const recEl = document.getElementById('doc-recommendations');
                    recEl.innerHTML = 
                        <p class="text-xs text-slate-600 border-l-2 border-amber-300 pl-2">Validar folios SII pendientes (Prioridad Alta)</p>
                        <p class="text-xs text-slate-600 border-l-2 border-indigo-300 pl-2 mt-1">Recopilar evidencias de anulacin</p>
                    ;'''
                    
new_rec = '''const recEl = document.getElementById('doc-recommendations');
                    recEl.innerHTML = <p class="text-xs text-slate-500 italic">No backend source available</p>;'''

# Try fixing encoding mismatch if needed
content = re.sub(r'const recEl = document.getElementById\(\'doc-recommendations\'\);.*?;', new_rec, content, flags=re.DOTALL)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated loadAnalyticLayers recommendations.")
