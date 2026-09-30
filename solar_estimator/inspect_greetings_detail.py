import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- updateClock (6600) ---")
for j in range(6598, 6640):
    if j < len(lines):
        print(f'{j+1}: {lines[j].rstrip()}')

print("\n--- greeting lines (11050) ---")
for j in range(11048, 11085):
    if j < len(lines):
        print(f'{j+1}: {lines[j].rstrip()}')
