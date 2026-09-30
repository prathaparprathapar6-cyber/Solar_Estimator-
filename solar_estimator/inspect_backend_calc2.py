import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('inv_cable, isolator = inverter_cable_and_isolator')
if idx != -1:
    print(text[idx:idx+3500])
