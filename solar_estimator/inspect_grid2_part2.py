import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('grid-template-columns:1.75fr 1fr')
print(text[idx+4000:idx+9000])
