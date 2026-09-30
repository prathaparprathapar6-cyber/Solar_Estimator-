import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(2245, 2350):
    if j < len(lines):
        print(f'{j+1}: {lines[j].rstrip()}')
