import re

with open('api/api.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add StaticFiles import and validate_periodo function near the top, after FastAPI imports
import_insert = """
from fastapi.staticfiles import StaticFiles
import re

def validate_periodo(periodo: str | None) -> None:
    if not periodo:
        return
    if periodo in ("undefined", "null"):
        raise HTTPException(status_code=400, detail="Invalid periodo: " + periodo)
    if periodo != "YTD" and not re.match(r'^\d{4}-\d{2}$', periodo):
        raise HTTPException(status_code=400, detail="Invalid periodo format. Expected YYYY-MM or YTD.")
"""

# Insert after line 6: from fastapi.responses import HTMLResponse
if "from fastapi.staticfiles import StaticFiles" not in content:
    content = content.replace(
        "from fastapi.responses import HTMLResponse\n",
        "from fastapi.responses import HTMLResponse\n" + import_insert
    )

# 2. Mount static folder after CORS configuration
mount_insert = """
# Mount shared frontend assets
shared_dir = ROOT / "frontend" / "shared"
shared_dir.mkdir(parents=True, exist_ok=True)
app.mount("/shared", StaticFiles(directory=str(shared_dir)), name="shared")
"""
if "app.mount(\"/shared\"" not in content:
    content = content.replace(
        "allow_headers=[\"*\"],\n)\n",
        "allow_headers=[\"*\"],\n)\n" + mount_insert
    )

# 3. Add validate_periodo(periodo) to all endpoints receiving periodo
endpoints_with_periodo = re.findall(r'(def [a-zA-Z0-9_]+\([^)]*periodo: str \| None = None[^)]*\):)', content)
print("Endpoints to patch:", endpoints_with_periodo)

for endpoint in set(endpoints_with_periodo):
    # We want to insert validate_periodo(periodo) right after the function signature and db init
    # e.g.:
    # def func(...):
    #     db = DatabaseV4.get()
    # ->
    # def func(...):
    #     validate_periodo(periodo)
    #     db = DatabaseV4.get()
    
    # Need to find the exact signature and the next line
    pattern = re.escape(endpoint) + r'\n(\s*)'
    def repl(m):
        indent = m.group(1)
        if indent == "":
            indent = "    "
        return endpoint + "\n" + indent + "validate_periodo(periodo)\n" + indent
        
    if "validate_periodo(periodo)" not in content.split(endpoint)[1][:100]:
        content = re.sub(pattern, repl, content, count=1)

with open('api/api.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("api.py patched successfully.")
