import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

for m in re.finditer(r'const\s+box\s*=\s*document\.getElementById\("loginSlideshow"\);', html):
    start = max(0, m.start() - 200)
    end = min(len(html), m.end() + 600)
    print("=== SNIPPET ===")
    print(html[start:end])
