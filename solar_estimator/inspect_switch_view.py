import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function switchView(')
if idx != -1:
    print(text[idx:idx+2000])
else:
    print("switchView not found")
