import os
import json

base = "data/db"
for item in os.listdir(base):
    if item.startswith("snapshot_"):
        path = os.path.join(base, item)
        for manifest_name in ["MANIFEST.json", "MANIFEST_V6.json"]:
            manifest_path = os.path.join(path, manifest_name)
            if os.path.exists(manifest_path):
                print(f"=== {item} ===")
                with open(manifest_path) as f:
                    try:
                        data = json.load(f)
                        print(json.dumps(data, indent=2))
                    except:
                        f.seek(0)
                        print(f.read())
                print()