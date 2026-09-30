import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\DELL\Downloads\VoltRoof_Admin_Control_Center new.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
sections = re.findall(r'<section id="([^"]+)" class="view[^"]*">(.*?)(?=<section id=|</main>|</body>)', text, re.DOTALL)
print("Sections found in ACC:")
for sid, content in sections:
    print(f" - ID: {sid}, length: {len(content)} chars")
