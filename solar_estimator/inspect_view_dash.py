import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'<section class="view customer-only active" id="view-dashboard">(.*?)</section>', text, re.DOTALL)
if m:
    dash = m.group(1)
    print("Dashboard length:", len(dash))
    for line in dash.split('\n')[:80]:
        if '<img' in line or 'grid' in line or 'card' in line or 'banner' in line:
            print("  ", line.strip()[:100])

print("\n=== SEARCH FOR 'showcase' OR 'hero' ACROSS ENTIRE FILE ===")
for m in re.finditer(r'<[^>]+class="[^"]*(?:showcase|hero|preview|visualizer)[^"]*"[^>]*>', text, re.IGNORECASE):
    print("Tag:", m.group(0)[:120])
