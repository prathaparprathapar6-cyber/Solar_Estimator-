import re

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    up = f.read()

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    comb = f.read()

views_up = re.findall(r'<div[^>]+id=["\'](view-[^"\']+)["\']', up)
views_comb = re.findall(r'<div[^>]+id=["\'](view-[^"\']+)["\']', comb)

print("Views in uploaded:", sorted(set(views_up)))
print("Views in combined:", sorted(set(views_comb)))

for v in sorted(set(views_up)):
    m_up = re.search(r'<div[^>]+id=["\']' + v + r'["\'][\s\S]*?(?=<div class="view"|<div id="view-|\Z)', up)
    m_comb = re.search(r'<div[^>]+id=["\']' + v + r'["\'][\s\S]*?(?=<div class="view"|<div id="view-|\Z)', comb)
    len_up = len(m_up.group(0)) if m_up else 0
    len_comb = len(m_comb.group(0)) if m_comb else 0
    print(f"View {v:20s} -> Uploaded: {len_up:6,d} chars | Combined: {len_comb:6,d} chars")
