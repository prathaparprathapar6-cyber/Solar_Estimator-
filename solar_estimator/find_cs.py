import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('openContentStudio')
while idx != -1:
    print(text[max(0, idx-50):min(len(text), idx+200)])
    print("="*40)
    idx = text.find('openContentStudio', idx+1)
