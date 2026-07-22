with open('frontend/shared/api_client.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

script_tag = '<script>\n' + js_content + '\n</script>'

for f in ['templates/dashboard.html', 'templates/executive_dashboard.html']:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('<script src="/shared/api_client.js"></script>', script_tag)
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Injected JS successfully")
