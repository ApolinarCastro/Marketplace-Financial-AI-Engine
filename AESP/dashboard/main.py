from fastapi import FastAPI
app = FastAPI(title="AESP Enterprise Dashboard")

@app.get("/")
def read_root():
    return {"status": "Enterprise Dashboard Runtime Active", "projects": ["marketplace"]}
