with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'btntopadminmanual' in l.lower() or 'admin (adarsha)' in l.lower() or 'navadminmanual' in l.lower():
        print(f"Line {i+1}: {l.strip()[:100]}")
