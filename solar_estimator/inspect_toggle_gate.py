import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function toggleGateAdminMode' in l:
        for j in range(i, min(len(lines), i+40)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
