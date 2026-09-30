with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'position:relative' in line and 'name-gate' in line:
        print(f"Line {i+1}: {line.strip()}")
        for j in range(max(0, i-5), min(len(lines), i+8)):
            print(f"  {j+1}: {lines[j].strip()}")
