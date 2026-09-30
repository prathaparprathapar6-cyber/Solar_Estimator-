import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'const\s+LOGIN_SLIDES\s*=\s*\[(.*?)\];', text, re.DOTALL)
if m:
    print("LOGIN_SLIDES:", m.group(0)[:1000])

print("\n=== LOGIN HERO HTML ===")
m_hero = re.search(r'(<div class="login-hero".*?</div>\s*</div>\s*</div>)', text, re.DOTALL)
if m_hero:
    print(m_hero.group(0)[:1500])

print("\n=== LOGIN HERO CSS ===")
for m in re.finditer(r'(\.login-hero[^{]*\{[^}]+\})', text):
    print(m.group(1))

print("\n=== LOGIN PANE / GATE CARD CSS ===")
for m in re.finditer(r'(\.login-form-pane[^{]*\{[^}]+\})', text):
    print(m.group(1))
