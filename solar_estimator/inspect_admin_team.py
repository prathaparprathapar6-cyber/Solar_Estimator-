import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'(<section class="view admin-only" id="view-adminTeam">.*?</section>)', text, re.DOTALL)
if m:
    print("view-adminTeam HTML:")
    print(m.group(1)[:2000])

print("\n=== AT FUNCTIONS (ADMIN TEAM) ===")
for m in re.finditer(r'(function\s+at[A-Z][a-zA-Z0-9]*[^{]*\{.*?\n\})', text, re.DOTALL):
    print(m.group(1)[:300])
