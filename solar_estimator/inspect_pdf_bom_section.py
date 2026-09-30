import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1840, 1925):
    print(f"{i+1}: {lines[i]}", end="")
