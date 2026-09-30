with open('solar_pv_estimator.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'class SolarAppRequestHandler' in line:
        print(f"Class starts at line {idx+1}")
    if 'def run_server' in line:
        print(f"run_server starts at line {idx+1}")
