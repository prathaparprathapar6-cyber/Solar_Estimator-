import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'(<section class="view admin-only" id="view-adminTickets">.*?</section>)', text, re.DOTALL)
if m:
    print("view-adminTickets HTML:")
    print(m.group(1))

print("\n=== SEARCH 'adminTickets' IN JS ===")
for m in re.finditer(r'(.{0,100}adminTickets.{0,100})', text):
    print(m.group(0))
