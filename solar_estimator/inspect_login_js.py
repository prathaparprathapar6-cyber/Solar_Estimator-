import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

m = re.search(r'const\s+LOGIN_SLIDES\s*=\s*\[.*?(?=function|\n\n[A-Z])', html, re.DOTALL)
if m:
    print("LOGIN_SLIDES def:")
    print(m.group(0)[:1200])

for m in re.finditer(r'(function\s+(?:goLoginSlide|tickLoginSlide|buildLoginSlideArt)[^{]*\{.*?\n\})', html, re.DOTALL):
    print("\nFunc:")
    print(m.group(0)[:500])
