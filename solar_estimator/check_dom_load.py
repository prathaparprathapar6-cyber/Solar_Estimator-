import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("--- Search for DOMContentLoaded or load handlers ---")
for m in re.finditer(r'(?:window\.addEventListener\([\'"]DOMContentLoaded[\'"]|window\.onload\s*=|document\.addEventListener\([\'"]DOMContentLoaded[\'"])[\s\S]*?(?=\n\})', text):
    print(m.group(0)[:600])
    print("="*50)
