import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function computeSite')
if idx != -1:
    print(text[idx:idx+3500])
else:
    # search for compute
    print("computeSite not found, looking for compute")
    for line in text.splitlines():
        if 'function compute' in line:
            print(line)
