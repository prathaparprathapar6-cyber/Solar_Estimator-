with open('solar_pv_estimator.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i in range(2920, 2960):
    print(f"{i+1}: {lines[i].strip()[:100]}")
