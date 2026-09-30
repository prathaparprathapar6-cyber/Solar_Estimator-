with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(11285, 11335):
    print(f"{j+1}: {lines[j].rstrip()}")
