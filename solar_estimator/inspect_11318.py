with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(11315, 11370):
    if j < len(lines):
        print(f"{j+1}: {lines[j].rstrip()}")
