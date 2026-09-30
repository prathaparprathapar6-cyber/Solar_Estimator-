with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'await ' in line:
        # Check backwards for the enclosing function definition
        for j in range(i, max(0, i-40), -1):
            if 'function' in lines[j]:
                if 'async' not in lines[j]:
                    print(f"Line {j+1}: {lines[j].strip()} -> has await at line {i+1}: {line.strip()[:60]}")
                break
