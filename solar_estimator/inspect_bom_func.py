import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('def generate_plant_bom')
if idx != -1:
    print(text[idx:idx+3500])
