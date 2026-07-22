import urllib.request
import json

url = "http://127.0.0.1:8000/api/v4/ledger?marketplace=PARIS&limit=100"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
        print(f"Total entries fetched: {len(data['data'])}")
        estados = {}
        for row in data['data']:
            est = row.get('estado_xml')
            estados[est] = estados.get(est, 0) + 1
        print("API estado_xml distribution:", estados)
except Exception as e:
    print(f"API Error: {e}")
