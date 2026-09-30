import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="modalAdminManual"')
print("=== HTML around modalAdminManual ===")
print(text[idx-100:idx+350])

# Search for #modalAdminManual in <style>
print("\n=== CSS rules for modalAdminManual ===")
pos = 0
while True:
    pos = text.find('#modalAdminManual', pos)
    if pos == -1 or pos >= idx:
        break
    rule_start = text.rfind('\n', 0, pos)
    rule_end = text.find('}', pos)
    print(text[rule_start:rule_end+1])
    pos += 1
