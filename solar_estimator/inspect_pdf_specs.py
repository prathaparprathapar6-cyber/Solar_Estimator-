import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re
matches = [m.start() for m in re.finditer(r'def export_pdf', code)]
start_idx = matches[0]
pdf_code = code[start_idx:start_idx+35000]

# Check where inverter and module specs are drawn
lines = pdf_code.splitlines()
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['inverter', 'module', 'acdb', 'breaker', 'cable']):
        if any(w in line for w in ['cell(', 'draw_', 'text_color', 'table', 'BOMItem']):
            print(f"Line {i+start_idx}: {line[:110]}")
