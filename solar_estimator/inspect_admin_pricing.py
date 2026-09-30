import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'(<section class="view admin-only" id="view-adminPricing">.*?</section>)', text, re.DOTALL)
if m:
    print("view-adminPricing HTML:")
    print(m.group(1)[:2000])

print("\n=== PRICING JS IN VoltRoof_Combined.html ===")
for m in re.finditer(r'(function\s+(?:loadPricing|savePricing|renderPricing|resetPricing)[^{]*\{.*?\n\})', text, re.DOTALL):
    print(m.group(1)[:400])
