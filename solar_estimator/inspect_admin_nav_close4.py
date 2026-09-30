with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="adminNavSec"')
print(text[idx+5700:idx+6200])
