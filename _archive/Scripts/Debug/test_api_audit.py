import urllib.request
import json

url = "http://127.0.0.1:8000/api/v4/auditoria?marketplace=PARIS"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
        print(f"Alerts fetched: {len(data)}")
        print(data)
except Exception as e:
    print(f"API Error: {e}")
