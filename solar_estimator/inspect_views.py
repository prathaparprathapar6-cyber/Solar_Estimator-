import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- SIDEBAR NAV ITEMS ---")
for i, line in enumerate(lines[:3500]):
    if 'nav-item' in line or 'data-view' in line or 'switchView' in line:
        print(f"{i+1}: {line.strip()[:100]}")

print("\n--- VIEW SECTIONS ---")
for i, line in enumerate(lines[:4000]):
    if '<section' in line and 'view' in line:
        print(f"{i+1}: {line.strip()[:100]}")
