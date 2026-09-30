import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'syncadminnavvisibility' in l.lower() or 'updateadminuistate' in l.lower():
        print(f"Line {i+1}: {l.strip()[:100]}")
