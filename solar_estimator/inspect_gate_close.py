import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="nameGate"')
print("id=nameGate at:", idx)
idx_close = text.find('</div>\n</div>', idx)
print("nameGate close at:", idx_close)
if idx_close != -1:
    print(text[idx_close:idx_close+300])
