import re

def refactor_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject script
    if 'api_client.js' not in html:
        html = html.replace('</head>', '    <script src="/shared/api_client.js"></script>\n</head>')

    # 2. Refactor fetch(xxx).then(res => res.json()).then(data => ...
    # to ApiClient.safeFetch(xxx).then(data => ...
    html = re.sub(
        r'fetch\((.*?)\)\s*\.then\([^\)]+=>[^\)]+\.json\(\)\)\s*\.then\(',
        r'ApiClient.safeFetch(\1).then(',
        html
    )

    # 3. Refactor await fetch
    # const res = await fetch(url);
    # const data = await res.json();
    # -> const data = await ApiClient.safeFetch(url);
    
    # Pattern: const/let var1 = await fetch(url); \n const/let var2 = await var1.json();
    pattern_await = r'(const|let)\s+([a-zA-Z0-9_]+)\s*=\s*await\s+fetch\((.*?)\);[\s\n]*(const|let)\s+([a-zA-Z0-9_]+)\s*=\s*await\s+\2\.json\(\);'
    html = re.sub(pattern_await, r'\4 \5 = await ApiClient.safeFetch(\3);', html)
    
    # What if they don't do json() immediately?
    # e.g., await fetch('/api/v4/run-audit...', { method: 'POST' });
    html = re.sub(r'await fetch\((.*?)\);', r'await ApiClient.safeFetch(\1);', html)
    
    # 4. Inject CONTRACT_GUARD in loadDashboard / loadExecutiveDashboard
    # For loadDashboard:
    if 'loadDashboard' in html and 'validateFinancialContract' not in html:
        # After summary fetch
        # We know fsData and summary are fetched.
        html = html.replace(
            "const summary = await ApiClient.safeFetch(`/api/v4/exec/summary?marketplace=${mp}&periodo=${periodo}`);",
            "const summary = await ApiClient.safeFetch(`/api/v4/exec/summary?marketplace=${mp}&periodo=${periodo}`);\n                ApiClient.validateFinancialContract(summary, 'summary');"
        )
    if 'loadExecutiveDashboard' in html and 'validateFinancialContract' not in html:
        html = html.replace(
            "const summary = await ApiClient.safeFetch(summaryUrl);",
            "const summary = await ApiClient.safeFetch(summaryUrl);\n            ApiClient.validateFinancialContract(summary, 'summary');"
        )
        # For waterfall: const data = await ApiClient.safeFetch('/api/v4/exec/waterfall...
        html = html.replace(
            "const data = await ApiClient.safeFetch('/api/v4/exec/waterfall",
            "const rawWf = await ApiClient.safeFetch('/api/v4/exec/waterfall"
        )
        html = html.replace(
            "const rawWf = await ApiClient.safeFetch('/api/v4/exec/waterfall-v3?' + params.toString());",
            "const rawWf = await ApiClient.safeFetch('/api/v4/exec/waterfall-v3?' + params.toString());\n            const data = ApiClient.validateFinancialContract(rawWf, 'waterfall');"
        )
        # Also line 401 in exec: 
        html = html.replace(
            "const wfRes = await fetch('/api/v4/exec/waterfall-v3'",
            "const data = await ApiClient.safeFetch('/api/v4/exec/waterfall-v3'"
        )

    # Any remaining raw fetch calls? (except in comments)
    html = re.sub(r'(?<!ApiClient\.)fetch\(', 'ApiClient.safeFetch(', html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

for f in ['templates/dashboard.html', 'templates/executive_dashboard.html']:
    refactor_template(f)
    print(f"Refactored {f}")
