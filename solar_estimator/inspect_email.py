import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('solar_pv_estimator.py', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'elif parsed\.path == "/api/send_email":.*?(?=elif parsed\.path|def run_server)', text, re.DOTALL)
if m:
    print("=== /api/send_email in solar_pv_estimator.py ===")
    print(m.group(0)[:2500])

print("\n=== SEARCH 'sendEmail' in VoltRoof_Combined.html ===")
with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

for m in re.finditer(r'(function\s+(?:sendEmail|mail|dispatchEmail)[^{]*\{.*?\n\})', html, re.DOTALL):
    print(m.group(1)[:300])
