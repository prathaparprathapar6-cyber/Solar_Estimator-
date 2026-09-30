import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'(<div[^>]*id="adminNavSec".*?</div>\s*<div class="sidebar-user")', text, re.DOTALL)
if m:
    print("adminNavSec HTML:")
    print(m.group(0)[:2000])
else:
    # search where adminNavSec is
    idx = text.find('id="adminNavSec"')
    print(text[idx:idx+2000])
