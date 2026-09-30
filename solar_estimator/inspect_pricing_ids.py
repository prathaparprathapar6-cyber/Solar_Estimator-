import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
start = text.find('id="adminPanelPricing"')
end = text.find('id="adminPanelVisitors"')
pricing_html = text[start:end]

inputs = re.findall(r'<input[^>]+id="([^"]+)"', pricing_html)
print("Pricing inputs:")
for inp in inputs:
    print(" -", inp)
