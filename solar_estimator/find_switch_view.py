import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'function switchView|switchView\s*=', text)]
for idx in matches:
    print(f"At {idx}:")
    print(text[max(0, idx-20):min(len(text), idx+300)])
    print("="*40)
