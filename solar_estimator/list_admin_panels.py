import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
panels = re.findall(r'<div id="(adminPanel[^"]+)"', text)
print("Admin panels found in VoltRoof_Combined.html:")
for p in panels:
    print(" -", p)
