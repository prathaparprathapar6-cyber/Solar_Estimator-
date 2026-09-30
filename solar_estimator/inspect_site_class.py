import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class SiteResult')
if idx != -1:
    print(text[idx:idx+2500])
