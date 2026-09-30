import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'select_inverter_lt', text)]
print(f"Found {len(matches)} occurrences of select_inverter_lt in solar_pv_estimator.py")
for idx in matches:
    print("---")
    print(text[max(0, idx-80):min(len(text), idx+120)])
