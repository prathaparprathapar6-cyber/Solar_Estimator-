import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for m in re.finditer(r'(function\s+(?:handleAdminManualUpload|submitAdminManualUpload|handleManualFileSelected)[^{]*\{.*?\n\})', text, re.DOTALL):
    print(m.group(1))

print("\n=== SEARCH 'csSlideFile' ===")
for m in re.finditer(r'(.{0,100}csSlideFile.{0,100})', text):
    print(m.group(0))
