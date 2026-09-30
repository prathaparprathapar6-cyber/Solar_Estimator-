import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="adminPanelPricing"')
idx_end = text.find('id="adminPanelVisitors"')
print(text[idx:idx_end])
