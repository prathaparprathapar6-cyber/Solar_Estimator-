import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("=== ALL FILE INPUTS ===")
for m in re.finditer(r'<input[^>]*type=["\']file["\'][^>]*>', text):
    print(m.group(0))

print("\n=== UPLOAD BUTTONS / CLICK HANDLERS ===")
for m in re.finditer(r'(<(?:button|div|label)[^>]*(?:upload|browse|manualPdf|policyPdf)[^>]*>.*?</(?:button|div|label)>)', text, re.DOTALL | re.IGNORECASE):
    t = m.group(0).replace('\n', ' ')
    if len(t) < 300:
        print("  ", t)

print("\n=== UPLOAD JS FUNCTIONS ===")
for m in re.finditer(r'(function\s+(?:upload|handleFile|onFile|savePdf|saveManual|savePolicy)[^{]*\{.*?\n\})', text, re.DOTALL):
    print(m.group(1)[:400])
