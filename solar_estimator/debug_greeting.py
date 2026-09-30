import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- Greeting inspection ---")
m = re.search(r'function updateRibbonGreeting\([^)]*\)\s*\{[\s\S]*?(?=\nfunction|\Z)', text)
if m: print("updateRibbonGreeting:\n", m.group(0))

m = re.search(r'function enterApp\([^)]*\)\s*\{[\s\S]*?(?=\nfunction|\Z)', text)
if m: print("enterApp:\n", m.group(0)[:800])

print("\n--- greet lines ---")
for i, l in enumerate(text.splitlines()):
    if 'greet' in l.lower() and ('html' in l or 'textcontent' in l or 'innerhtml' in l or 'pickgreeting' in l or 'updateribbongreeting' in l):
        print(f"Line {i+1}: {l.strip()[:100]}")
