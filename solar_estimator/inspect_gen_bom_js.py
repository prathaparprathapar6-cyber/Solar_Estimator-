import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('function generatePlantBom(')
idx2 = text.find('function onCalculateClick()')
print("generatePlantBom to onCalculateClick length:", idx2 - idx1)
print(text[idx1:idx1+1500])
