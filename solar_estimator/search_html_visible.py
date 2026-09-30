with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'>[^<]*(?:portfolio|multi-site|multi site)[^<]*<', text, re.IGNORECASE)
for m in matches:
    print(m)
