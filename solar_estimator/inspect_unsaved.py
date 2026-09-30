import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("=== UNSAVED BANNER CSS ===")
for m in re.finditer(r'(\.unsaved-banner[^{]*\{[^}]+\})', text):
    print(m.group(1))

print("\n=== UNSAVED BANNER HTML ===")
for m in re.finditer(r'(<[^>]*class="[^"]*unsaved-banner[^"]*"[^>]*>.*?</[^>]+>)', text, re.DOTALL):
    print(m.group(1)[:500])

print("\n=== SHOWCASE / RIGHT SIDE IN MAIN APP ===")
# Look at user photo 2: "Both user and admin dashboard right-side showcase images are being cut into halves."
# Why did user say "Both user and admin dashboard right-side showcase images are being cut into halves"?
for m in re.finditer(r'(.{0,100}showcase.{0,100})', text, re.IGNORECASE):
    print("SHOWCASE:", m.group(1).replace('\n', ' '))
