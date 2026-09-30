import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('bomBody')
while idx != -1:
    print(f"bomBody at {idx}:")
    print(text[max(0, idx-50) : min(len(text), idx+600)])
    print("-" * 50)
    idx = text.find('bomBody', idx+1)
