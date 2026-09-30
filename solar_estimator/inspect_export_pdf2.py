import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Lines 1845 to 1925:")
for i in range(1844, 1925):
    print(f"{i+1}: {lines[i]}", end="")
