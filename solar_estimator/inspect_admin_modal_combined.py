import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<div[^>]+id="modalAdminManual"[\s\S]*', text)
if m:
    admin_modal_content = m.group(0)
    print("Found modalAdminManual! Length:", len(admin_modal_content))
    
    # Find all tab buttons or tab panels
    tabs = re.findall(r'<button[^>]+onclick=[\'"][^\'"]*switchAdminTab\([\'"]([^\'"]+)[\'"][\s\S]*?>([\s\S]*?)</button>', admin_modal_content)
    print("\nAdmin Tabs:")
    for tab_id, tab_label in tabs:
        clean_label = re.sub(r'<[^>]+>', '', tab_label).strip()
        print(f"  Tab ID: '{tab_id:12s}' | Label: '{clean_label}'")
        
    panels = re.findall(r'<div[^>]+id=[\'"](adminPanel[^\'"]*)[\'"]', admin_modal_content)
    print("\nAdmin Panels:")
    for p in panels:
        print(f"  - {p}")
else:
    print("modalAdminManual not found")
