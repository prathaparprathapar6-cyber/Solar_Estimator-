with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="modalAdminDocPanel"')
panel_snippet = text[idx:idx+8000]

# Find all adminPanel IDs
import re
panels = re.findall(r'id=["\'](adminPanel[A-Za-z]+)["\']', panel_snippet)
print("Panels found:", panels)

# Check switchAdminTab code
idx_sw = text.find('function switchAdminTab')
print("\nswitchAdminTab code:")
print(text[idx_sw:idx_sw+600])
