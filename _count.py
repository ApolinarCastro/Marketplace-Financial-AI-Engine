import os  
root = os.getcwd()  
skip = {'.git','__pycache__','.venv','node_modules','.mypy_cache','.ruff_cache','.pytest_cache','.agent','.agents','.claude','.claude-flow','.codex','.swarm','.github','_archive','Lib'}  
py_c = 0  
py_l = 0  
md_c = 0  
for r2,d,f in os.walk(root):  
    d[:] = [x for x in d if x not in skip]  
    for fn in f:  
        ext = os.path.splitext(fn)[1].lower()  
        if ext == '.py':  
            py_c += 1  
            py_l += sum(1 for _ in open(os.path.join(r2,fn), errors='replace'))  
        elif ext == '.md':  
            md_c += 1  
print('Python files:', py_c)  
print('Python lines:', py_l)  
print('Markdown files:', md_c)  
