with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
pos = text.find('function generatePlantBOM')
if pos != -1:
    print("=== generatePlantBOM in VoltRoof_Combined.html ===")
    print(text[pos:pos+3000].encode('ascii', errors='replace').decode('ascii'))

with open('solar_pv_estimator.py', 'r', encoding='utf-8', errors='ignore') as f:
    py_text = f.read()

pos2 = py_text.find('def generate_plant_bom')
if pos2 != -1:
    print("\n=== generate_plant_bom in solar_pv_estimator.py ===")
    print(py_text[pos2:pos2+3000].encode('ascii', errors='replace').decode('ascii'))
