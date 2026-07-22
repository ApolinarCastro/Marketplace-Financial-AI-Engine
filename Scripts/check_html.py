import re, sys

files = ['templates/dashboard.html', 'templates/executive_dashboard.html']
ok = True
for path in files:
    with open(path, encoding='utf-8') as f:
        content = f.read()
    opens = len(re.findall(r'<div\b', content))
    closes = len(re.findall(r'</div>', content))
    delta = opens - closes
    status = 'OK' if delta == 0 else ('UNCLOSED ' + str(delta) if delta > 0 else 'EXTRA_CLOSE ' + str(-delta))
    print(path + ': divs open=' + str(opens) + ' close=' + str(closes) + ' -> ' + status)
    ids = re.findall(r'id="([^"]+)"', content)
    from collections import Counter
    dupes = {k: v for k, v in Counter(ids).items() if v > 1}
    if dupes:
        print('  DUPLICATE IDs: ' + str(list(dupes.keys())))
        ok = False
    else:
        print('  No duplicate IDs')
    if delta != 0:
        ok = False

sys.exit(0 if ok else 1)
