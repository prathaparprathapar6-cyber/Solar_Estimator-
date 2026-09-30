with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pos = 0
while True:
    pos = text.find('modalAdminManual', pos)
    if pos == -1:
        break
    line_start = text.rfind('\n', 0, pos)
    line_end = text.find('\n', pos)
    print(text[line_start:line_end].strip()[:100])
    pos += 1
