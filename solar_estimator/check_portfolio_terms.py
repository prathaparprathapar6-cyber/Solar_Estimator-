import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if any(w in line.lower() for w in ['portfolio', 'multi-site', 'multisite']):
            print(f"{i+1}: {line.strip()[:110]}")
