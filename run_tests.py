# -*- coding: utf-8 -*-
import sys, subprocess, os

project_root = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine'
sys.path.insert(0, project_root)
os.chdir(project_root)

result = subprocess.run([
    r'C:\Progra~1\AutoClaw\resources\python\python.exe',
    '-m', 'pytest',
    'tests/',
    '-v', '--tb=short',
], capture_output=True, text=True, cwd=project_root,
   env={**os.environ, 'PYTHONPATH': project_root})

print('STDOUT:')
print(result.stdout[-8000:] if len(result.stdout) > 8000 else result.stdout)
print('')
print('STDERR:')
print(result.stderr[-3000:] if len(result.stderr) > 3000 else result.stderr)
print('Exit code: ' + str(result.returncode))