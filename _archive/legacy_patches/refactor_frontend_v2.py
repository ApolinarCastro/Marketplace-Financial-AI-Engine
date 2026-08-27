import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject script tag if missing
    if 'api_client.js' not in html:
        html = html.replace('</head>', '    <script src="/shared/api_client.js"></script>\n</head>')

    # 2. Refactor await fetch -> await ApiClient.safeFetch
    pattern_await_json = r'(const|let)\s+([a-zA-Z0-9_]+)\s*=\s*await\s+fetch\((.*?)\);[\s\n]*(const|let)\s+([a-zA-Z0-9_]+)\s*=\s*await\s+\2\.json\(\);'
    html = re.sub(pattern_await_json, r'\4 \5 = await ApiClient.safeFetch(\3);', html)
    
    # Simple await fetch without immediate json() (e.g. run-audit)
    html = re.sub(r'await fetch\((.*?)\);', r'await ApiClient.safeFetch(\1);', html)
    
    # Normal fetch(url).then(r=>r.json()).then(data=>...)
    html = re.sub(
        r'fetch\((.*?)\)\s*\.then\([^\)]+=>[^\)]+\.json\(\)\)\s*\.then\(',
        r'ApiClient.safeFetch(\1).then(',
        html
    )

    # Convert fetch('/api/v4/periodos').then(...) to explicit initApp()
    if 'dashboard.html' in filepath:
        old_init = """        fetch('/api/v4/periodos')
            .then(r => r.json())
            .then(periodos => {
                const currentVal = periodSel.value;
                periodSel.innerHTML = periodos.map(p => `<option value="${p.periodo}"${p.periodo === currentVal ? ' selected' : ''}>${p.label}</option>`).join('');
                loadDashboard();
            })
            .catch(() => {
                periodSel.innerHTML = '<option value="">Periodos no disponibles</option>';
            });"""
        old_init_refactored = """        ApiClient.safeFetch('/api/v4/periodos').then(periodos => {
                const currentVal = periodSel.value;
                periodSel.innerHTML = periodos.map(p => `<option value="${p.periodo}"${p.periodo === currentVal ? ' selected' : ''}>${p.label}</option>`).join('');
                loadDashboard();
            })
            .catch(() => {
                periodSel.innerHTML = '<option value="">Periodos no disponibles</option>';
            });"""

        new_init = """        async function initApp() {
            try {
                const periodos = await ApiClient.getPeriodos();
                const currentVal = periodSel.value;
                periodSel.innerHTML = periodos.map(p => `<option value="${p.periodo}"${p.periodo === currentVal ? ' selected' : ''}>${p.label}</option>`).join('');
                
                const mp = document.getElementById('marketplace-selector').value;
                const periodo = periodSel.value;
                if (!mp || !periodo) {
                    console.error("Missing mandatory selectors");
                    return;
                }
                loadDashboard();
            } catch (e) {
                console.error("Initialization failed:", e);
                periodSel.innerHTML = '<option value="">Periodos no disponibles</option>';
            }
        }
        initApp();"""
        
        if old_init in html:
            html = html.replace(old_init, new_init)
        elif old_init_refactored in html:
            html = html.replace(old_init_refactored, new_init)

        # Apply CONTRACT_GUARD
        html = html.replace(
            "const summary = await ApiClient.safeFetch(`/api/v4/exec/summary?marketplace=${mp}&periodo=${periodo}`);",
            "const summary = await ApiClient.getSummary(mp, periodo);"
        )

    elif 'executive_dashboard.html' in filepath:
        old_init = """        fetch('/api/v4/periodos')
            .then(r => r.json())
            .then(periodos => {
                const sel = document.getElementById('exec-period');
                const currentVal = sel.value;
                sel.innerHTML = periodos.map(p => `<option value="${p.periodo}"${p.periodo === currentVal ? ' selected' : ''}>${p.label}</option>`).join('');
                onFilterChange();
            })
            .catch(() => {});"""
        old_init_refactored = """        ApiClient.safeFetch('/api/v4/periodos').then(periodos => {
                const sel = document.getElementById('exec-period');
                const currentVal = sel.value;
                sel.innerHTML = periodos.map(p => `<option value="${p.periodo}"${p.periodo === currentVal ? ' selected' : ''}>${p.label}</option>`).join('');
                onFilterChange();
            })
            .catch(() => {});"""
            
        new_init = """        async function initApp() {
            try {
                const periodos = await ApiClient.getPeriodos();
                const sel = document.getElementById('exec-period');
                const currentVal = sel.value;
                sel.innerHTML = periodos.map(p => `<option value="${p.periodo}"${p.periodo === currentVal ? ' selected' : ''}>${p.label}</option>`).join('');
                
                const period = sel.value;
                const mp = document.getElementById('exec-mp').value;
                if (!mp || !period) {
                    console.error("Missing mandatory selectors");
                    return;
                }
                onFilterChange();
            } catch(e) {
                console.error("Initialization failed:", e);
            }
        }
        initApp();"""
        
        if old_init in html:
            html = html.replace(old_init, new_init)
        elif old_init_refactored in html:
            html = html.replace(old_init_refactored, new_init)

        # Apply CONTRACT_GUARD
        if "const summary = await ApiClient.safeFetch(summaryUrl);" in html:
            html = html.replace(
                "const summary = await ApiClient.safeFetch(summaryUrl);",
                "const summary = await ApiClient.safeFetch(summaryUrl);\n            ApiClient.validateFinancialContract(summary, 'summary');"
            )
        html = html.replace(
            "const data = await ApiClient.safeFetch('/api/v4/exec/waterfall",
            "const rawWf = await ApiClient.safeFetch('/api/v4/exec/waterfall"
        )
        html = html.replace(
            "const rawWf = await ApiClient.safeFetch('/api/v4/exec/waterfall-v3?' + params.toString());",
            "const rawWf = await ApiClient.safeFetch('/api/v4/exec/waterfall-v3?' + params.toString());\n            const data = ApiClient.validateFinancialContract(rawWf, 'waterfall');"
        )

    # Replace any leftover fetch calls
    html = re.sub(r'(?<!ApiClient\.)fetch\(', 'ApiClient.safeFetch(', html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Refactored {filepath}")

for f in ['templates/dashboard.html', 'templates/executive_dashboard.html']:
    process_file(f)
