with open('generate_ux12_evidence.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'ui_text = await page.locator("#ux12-cash-bal").inner_text()',
    'ui_text = await page.locator("span.kpi-label:has-text(\'Disponible\') + div.kpi-value").inner_text()'
)

with open('generate_ux12_evidence.py', 'w', encoding='utf-8') as f:
    f.write(content)
