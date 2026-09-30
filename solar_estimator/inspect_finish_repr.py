with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(11280, 11365):
    print(f"{j+1}: {repr(lines[j])}")
