import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

matches = re.findall(r'id=["\'](adminPanel[A-Za-z0-9_\-]+)["\']', text)
print('All adminPanel IDs in file:', matches)

tabs = ['manual', 'pricing', 'visitors', 'feedback', 'users', 'audit', 'settings', 'tickets']
for t in tabs:
    pnl_id = 'adminPanel' + t.capitalize()
    print(f'{pnl_id} exists: {pnl_id in text}')
