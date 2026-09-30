import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(2280, 2315):
    print(f"{j+1}: {lines[j].rstrip()}")
