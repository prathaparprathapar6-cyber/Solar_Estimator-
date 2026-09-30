import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="bomTable"')
print("bomTable at:", idx)
if idx != -1:
    print(text[idx-200:idx+1500])

idx2 = text.find('renderBom')
print("renderBom at:", idx2)
if idx2 != -1:
    print(text[idx2-50:idx2+1500])
