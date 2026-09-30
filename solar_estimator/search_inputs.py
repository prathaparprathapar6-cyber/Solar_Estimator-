import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, l in enumerate(lines):
    if '<input' in l or '<select' in l:
        print(f"L{idx+1}: {l.strip()[:110]}")
