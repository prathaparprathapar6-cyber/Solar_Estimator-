import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Inspect build_multi_site_report
idx = text.find('def build_multi_site_report')
if idx != -1:
    print(text[idx:idx+3500])
