import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('kpiCap')
while idx != -1:
    print(f"kpiCap at {idx}:")
    print(text[max(0, idx-50) : min(len(text), idx+300)])
    print("-" * 50)
    idx = text.find('kpiCap', idx+1)
