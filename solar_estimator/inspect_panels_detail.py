import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'<div id="(adminPanel[^"]+)"[^>]*>', text)
indices = [m.start() for m in matches]
indices.append(text.find('</div>\n\n<script', indices[-1] if indices else 0))

for i in range(len(indices)-1):
    chunk = text[indices[i]:indices[i+1]]
    p_id = re.search(r'id="([^"]+)"', chunk).group(1)
    print(f"Panel: {p_id}, length: {len(chunk)} chars, preview: {chunk[:80].strip()}...")
