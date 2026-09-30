import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'<div class="grid-2" style="grid-template-columns:1\.75fr 1fr; margin-bottom:14px">(.*?)<!-- /grid-2 -->|<!-- END GRID -->|</div>\s*<div class="card"', text, re.DOTALL)
if m:
    print("Full grid-2 content:")
    print(m.group(0)[:3000])
else:
    # let's search where grid-2 closes
    idx = text.find('grid-template-columns:1.75fr 1fr')
    print(text[idx:idx+2500])
