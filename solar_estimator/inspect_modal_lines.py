import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(12395, 12530):
    if i < len(lines):
        print(f"{i+1}: {lines[i].rstrip()[:120]}")
