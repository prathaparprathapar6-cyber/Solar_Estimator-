import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for p in ['adminPanelPricing', 'adminPanelUsers', 'adminPanelVisitors']:
    idx = text.find(f'id="{p}"')
    print(f"=== {p} ===")
    print(text[idx:idx+500])
