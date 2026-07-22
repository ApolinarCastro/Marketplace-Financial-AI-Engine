import sys
sys.path.insert(0, '.')
import json
from api.api import get_exec_waterfall, get_exec_cobros_breakdown

wf = get_exec_waterfall('ML', '2026-02')
cb = get_exec_cobros_breakdown('ML', '2026-02')

print('--- WATERFALL ---')
print('Neto:', wf['values'][5])
print('Costos Marketplace (Cobros):', wf['cobros'])
print('Ajustes Total (including Poscobros):', wf['values'][4])

print('\n--- BREAKDOWN ---')
for row in cb['matrix']:
    print(f"{row['concept']}: {row.get('ML', 0)}")
