import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'<div class="grid-2" style="grid-template-columns:1\.75fr 1fr; margin-bottom:14px">(.*?)</div>\s*<!--', text, re.DOTALL)
if m:
    print("=== GRID-2 IN DASHBOARD ===")
    print(m.group(0)[:2500])

print("\n=== ADMIN DASHBOARD HTML ===")
m_adm = re.search(r'<section class="view admin-only" id="view-adminDashboard">(.*?)</section>', text, re.DOTALL)
if m_adm:
    print(m_adm.group(1)[:2500])
