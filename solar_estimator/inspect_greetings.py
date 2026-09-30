import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'greetprefix' in l.lower() or 'updateclock' in l.lower() or 'randomgreeting' in l.lower():
        print(f'{i+1}: {l.strip()[:100]}')
