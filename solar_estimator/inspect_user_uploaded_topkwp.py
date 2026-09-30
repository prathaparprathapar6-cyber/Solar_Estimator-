import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'topkwp' in l.lower():
        print(f'{i+1}: {l.strip()[:100]}')
