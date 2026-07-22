import os  
root=os.getcwd()  
t=0; l=0  
for r2,d,f in os.walk(os.path.join(root,'tests')):  
    d[:] = [x for x in d if x not in {'.git','__pycache__','.venv'}]  
    for fn in f:  
        if fn.startswith('test_') and fn.endswith('.py'):  
            t += 1  
            l += sum(1 for _ in open(os.path.join(r2,fn),errors='replace'))  
print('Test files:', t, 'Test lines:', l)  
