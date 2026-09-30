import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'(<section class="view admin-only" id="view-adminVisitors">.*?</section>)', text, re.DOTALL)
if m:
    print("view-adminVisitors HTML:")
    print(m.group(1)[:2000])
