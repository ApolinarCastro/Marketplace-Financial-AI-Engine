import re
with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('>PENDING<', '>-<')
content = content.replace("el.innerText = 'PENDING';", "el.innerText = '-';")
with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed PENDING hardcodes.")
