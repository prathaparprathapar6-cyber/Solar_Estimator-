import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pos = 0
while True:
    pos = text.find('.name-gate', pos)
    if pos == -1 or pos > 40000:
        break
    rule_start = text.rfind('\n', 0, pos)
    rule_end = text.find('}', pos)
    print(text[rule_start:rule_end+1])
    pos += 1
