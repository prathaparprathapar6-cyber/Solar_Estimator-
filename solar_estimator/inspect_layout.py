import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print("=== SEARCH 'unsaved changes' ===")
for m in re.finditer(r'(.{0,100}unsaved changes.{0,100})', html, re.IGNORECASE):
    print("Match:", m.group(1).replace('\n', ' '))

print("\n=== LOGIN SHOWCASE / SLIDESHOW CSS & HTML ===")
for m in re.finditer(r'(\.login[^{]*\{[^}]+\})', html):
    print(m.group(1))

for m in re.finditer(r'(#(?:gate|login|slide|showcase)[^{]*\{[^}]+\})', html, re.IGNORECASE):
    print(m.group(1))

print("\n=== RIGHT PANEL / MAIN LAYOUT ===")
for m in re.finditer(r'class="[^"]*(?:right|showcase|panel|split|content)[^"]*"', html):
    c = m.group(0)
    if any(k in c for k in ['right', 'showcase', 'preview', 'split']):
        print(c)
