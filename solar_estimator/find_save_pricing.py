import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('Save &amp; Publish Pricing')
if idx == -1:
    idx = text.find('Save & Publish Pricing')
print("Snippet around Save & Publish Pricing:")
print(text[idx-300:idx+400])
