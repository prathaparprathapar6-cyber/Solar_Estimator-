import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="view-bom"')
idx_end = text.find('</section>', idx)
print(text[idx:idx_end+10])
