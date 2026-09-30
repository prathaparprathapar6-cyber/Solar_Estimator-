import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'function\s+enterApp\s*\(.*?\)\s*\{.*?\n\}', text, re.DOTALL)
if m:
    print(m.group(0))
