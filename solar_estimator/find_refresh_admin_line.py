with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'refreshAdminList' in line and 'function' in line:
        print(f"Line {i+1}: {line}")
