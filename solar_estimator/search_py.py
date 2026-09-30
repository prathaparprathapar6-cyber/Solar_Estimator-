import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
while True:
    idx = text.find('VoltRoof_Combined.html', idx)
    if idx == -1:
        break
    print(f"At {idx}:")
    print(text[max(0, idx-100):min(len(text), idx+200)])
    print("="*40)
    idx += 22
