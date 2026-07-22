import re

path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """                // 2. Audit Alerts (now period-scoped)
                const alerts = await ApiClient.safeFetch('/api/v4/auditoria' + mkQuery);
                window._hasAuditAlerts = alerts.length > 0;"""

replacement = """                // 2. Audit Alerts (now period-scoped)
                let alerts = [];
                try {
                    alerts = await ApiClient.safeFetch('/api/v4/auditoria' + mkQuery);
                } catch(e) {
                    console.error("Auditoria error", e);
                }
                window._hasAuditAlerts = alerts.length > 0;"""

if target in content:
    content = content.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced auditoria fetch")
else:
    print("Target not found")
