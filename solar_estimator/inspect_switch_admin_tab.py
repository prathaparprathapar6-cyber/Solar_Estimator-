import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('function switchAdminTab')
if start != -1:
    print(text[start:start+1200])
else:
    print("switchAdminTab not found")
