import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- SIDEBAR NAV (2350-2410) ---")
for i in range(2350, min(2410, len(lines))):
    print(f"{i+1}: {lines[i].rstrip()[:100]}")

print("\n--- CONTENT END / LAST VIEWS (3135-3165) ---")
for i in range(3135, min(3165, len(lines))):
    print(f"{i+1}: {lines[i].rstrip()[:100]}")
