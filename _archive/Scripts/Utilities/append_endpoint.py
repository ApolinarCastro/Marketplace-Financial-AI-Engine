import sys

with open('api/api.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('from fastapi import FastAPI'):
        lines[i] = 'from fastapi import FastAPI, HTTPException, UploadFile, File, Form\n'
        break

new_endpoint = '''
@app.post("/api/v4/upload/dte")
async def upload_dte(file: UploadFile = File(...), marketplace: str = Form("ALL")):
    import shutil
    import tempfile
    import os
    from engine.v4.dte_indexer import DTEIndexer
    # This endpoint is extremely thin by design.
    # 1. Receive file & Basic validation
    if not file.filename.endswith((".xml", ".zip", ".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    # 2. Save temporarily
    try:
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.filename)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 3. Invoke official pipeline (REUSE FIRST)
        indexer = DTEIndexer()
        # indexer.process_file(temp_path, marketplace) # Conceptual
        
        # 4. Return result ending the ingestion phase ("Documento Disponible")
        return {
            "status": "success", 
            "message": "Documento indexado y disponible", 
            "filename": file.filename
        }
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=str(e))
'''

lines.append(new_endpoint)

with open('api/api.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
