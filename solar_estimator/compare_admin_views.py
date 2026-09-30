import re

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    up = f.read()

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    comb = f.read()

views_to_check = ['adminTeam', 'policyDesk', 'studio', 'contactUs', 'policyHub']

for v in views_to_check:
    print(f"\n==================== VIEW: {v} ====================")
    m_up = re.search(r'<div[^>]+id=["\']view_' + v + r'["\'][\s\S]*?(?=<div[^>]+id=["\']view_|\Z)', up)
    if not m_up:
        m_up = re.search(r'<div[^>]+data-view=["\']' + v + r'["\'][\s\S]*?(?=<div[^>]+data-view=|\Z)', up)
    print(f"Uploaded: found = {bool(m_up)}, length = {len(m_up.group(0)) if m_up else 0}")
    
    m_comb = re.search(r'<div[^>]+id=["\']view_' + v + r'["\'][\s\S]*?(?=<div[^>]+id=["\']view_|\Z)', comb)
    if not m_comb:
        m_comb = re.search(r'<div[^>]+data-view=["\']' + v + r'["\'][\s\S]*?(?=<div[^>]+data-view=|\Z)', comb)
    print(f"Combined: found = {bool(m_comb)}, length = {len(m_comb.group(0)) if m_comb else 0}")
