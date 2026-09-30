import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

m = re.search(r'(<div class="login-hero">.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
if m:
    print("login-hero snippet:")
    print(m.group(0))
