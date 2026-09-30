with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = list(re.finditer(r'\bdist\b', text))
print('Count of dist:', len(matches))
for m in matches[:20]:
    s = m.start()
    line = text[max(0, s-40):min(len(text), s+120)].replace('\n', ' ')
    print(line.encode('ascii', errors='replace').decode('ascii'))
