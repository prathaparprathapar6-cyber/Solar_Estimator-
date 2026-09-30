import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="studioBldgTabs"')
if idx != -1:
    print(text[idx-500:idx+2000])
