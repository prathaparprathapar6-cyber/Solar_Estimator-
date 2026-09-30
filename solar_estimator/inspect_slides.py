import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("=== LOGIN SLIDESHOW HTML ===")
m = re.search(r'(<div[^>]*id="loginSlideshow".*?</div>\s*</div>)', text, re.DOTALL)
if m:
    print(m.group(0)[:1500])

print("\n=== LOGIN SLIDESHOW CSS ===")
for m in re.finditer(r'(\.login-slide[^{]*\{[^}]+\})', text):
    print(m.group(1))

print("\n=== ANY OTHER SHOWCASE / SLIDESHOW IN HTML ===")
for m in re.finditer(r'(<(?:div|section)[^>]*(?:slide|showcase|hero|preview)[^>]*>)', text, re.IGNORECASE):
    print(m.group(0))

print("\n=== SLIDESHOW JS FUNCTIONS ===")
for m in re.finditer(r'(function\s+(?:goLoginSlide|tickLoginSlide|initSlideshow|renderSlides|csRender|csPublishShowcase)[^{]*\{.*?\n\})', text, re.DOTALL):
    print(m.group(1)[:400])
