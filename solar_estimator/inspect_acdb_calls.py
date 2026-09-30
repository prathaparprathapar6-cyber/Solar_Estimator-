import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'select_acdb_components', text)]
print(f"Found {len(matches)} occurrences of select_acdb_components in solar_pv_estimator.py")
for idx in matches:
    print("---")
    print(text[max(0, idx-60):min(len(text), idx+140)])
