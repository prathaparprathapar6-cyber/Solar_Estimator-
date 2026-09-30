import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    text = f.read()

funcs = ['def generate_plant_bom', 'def build_building_result', 'def build_system_report', 'def build_multi_site_report']
for fn in funcs:
    idx = text.find(fn)
    print(f"=== {fn} at index {idx} ===")
    if idx != -1:
        print(text[idx:idx+1500])
