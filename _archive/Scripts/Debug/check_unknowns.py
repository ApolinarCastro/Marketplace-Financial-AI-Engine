import json
with open('REPOSITORY_REGISTRY.json', 'r') as f:
    data = json.load(f)

unknowns = [item['file'] for item in data if item['classification'] == 'UNKNOWN']
for u in unknowns:
    print(u)
