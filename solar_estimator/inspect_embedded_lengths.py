with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:45]):
    if 'EMBEDDED_' in l:
        var_name = l.split('=')[0].strip()
        print(f'{i+1}: {var_name} length = {len(l)}')
