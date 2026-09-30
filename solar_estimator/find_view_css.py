import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'(\.[a-zA-Z0-9_-]*view[a-zA-Z0-9_-]*\s*\{[^}]+\})', text[:50000])
for m in matches[:15]:
    print(m)
    print("="*40)
