with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="adminNavSec"')
print(text[idx+3000:idx+4500])
