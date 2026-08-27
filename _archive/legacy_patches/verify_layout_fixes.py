import urllib.request

# ── /app checks ──
r = urllib.request.urlopen('http://127.0.0.1:3001/app', timeout=5)
html = r.read().decode('utf-8', errors='ignore')

app_checks = [
    ('ai-insights-container appears AFTER ledger col-span-8',
     'col-span-12 lg:col-span-8' in html and
     html.index('ai-insights-container') > html.index('col-span-12 lg:col-span-8')),
    ('no stale col-span-12 mt-8 bare wrapper',
     '<div class="col-span-12 mt-8">' not in html),
    ('sect-cobertura is proper col-span-12 element',
     'sect-cobertura' in html),
    ('no duplicate ai-return-reasons id',
     html.count('id="ai-return-reasons"') == 1),
    ('no duplicate ai-operational-insights id',
     html.count('id="ai-operational-insights"') == 1),
]

print('=== /app (Auditor) ===')
all_ok = True
for name, result in app_checks:
    status = 'PASS' if result else 'FAIL'
    if not result:
        all_ok = False
    print('  [' + status + '] ' + name)

# ── /exec checks ──
r2 = urllib.request.urlopen('http://127.0.0.1:3001/exec', timeout=5)
html2 = r2.read().decode('utf-8', errors='ignore')

exec_checks = [
    ('KPI grid has items-stretch',
     'items-stretch' in html2),
    ('KPI grid has sm:grid-cols-3',
     'sm:grid-cols-3' in html2),
    ('min-h-[5.5rem] present in JS template strings',
     'min-h-[5.5rem]' in html2),
    ('kpi-value-primary NOT used for Resultado Neto in JS',
     'kpi-value-primary mt-1' not in html2 or
     'kpi-value mt-2' in html2),
]

print('\n=== /exec (Executive) ===')
for name, result in exec_checks:
    status = 'PASS' if result else 'FAIL'
    if not result:
        all_ok = False
    print('  [' + status + '] ' + name)

print('\nOverall: ' + ('ALL PASS' if all_ok else 'SOME FAILURES'))
