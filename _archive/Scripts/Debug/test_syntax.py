import re, subprocess, json
with open('dashboard_before.html', 'r', encoding='utf-8') as f:
    html = f.read()
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
with open('dashboard_before.js', 'w', encoding='utf-8') as f:
    f.write(scripts[0]) # the main script

try:
    result = subprocess.run(['node', '--check', 'dashboard_before.js'], capture_output=True, text=True)
    out = result.stdout + result.stderr
    print(out)
    trace = {
        'error': 'SyntaxError: Unexpected token \'<\'',
        'file': 'dashboard.html (inline script)',
        'line': out.split('\n')[0] if out else '',
        'stack': out
    }
    with open('console_trace_before.json', 'w') as f:
        json.dump(trace, f, indent=2)
except Exception as e:
    print('Node not found or error: ', e)
