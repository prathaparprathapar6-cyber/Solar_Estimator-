with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
print("=== Inputs matching dist or cable or grid ===")
for m in re.finditer(r'<input[^>]+(?:dist|cable|grid)[^>]+>', text, re.IGNORECASE):
    print(m.group(0))

print("\n=== Labels mentioning Distance or Grid or ACDB ===")
for m in re.finditer(r'<label[^>]*>[^<]*(?:Distance|ACDB|Grid)[^<]*</label>', text, re.IGNORECASE):
    print(m.group(0))
