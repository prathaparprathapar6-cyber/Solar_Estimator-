import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Lines 1440 to 1520:")
for i in range(1439, 1515):
    print(f"{i+1}: {lines[i]}", end="")
