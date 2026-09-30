import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    up = f.read()

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    comb = f.read()

def print_fn(text, fn_name):
    m = re.search(r'function\s+' + fn_name + r'\s*\([^)]*\)\s*\{[\s\S]*?(?=\nfunction|\Z)', text)
    if m:
        print(f"=== {fn_name} ===")
        print(m.group(0)[:1500])
    else:
        print(f"{fn_name} not found")

print("--- Uploaded ---")
print_fn(up, 'syncAdminNavVisibility')
print_fn(up, 'updateAdminUIState')

print("\n--- Combined ---")
print_fn(comb, 'syncAdminNavVisibility')
print_fn(comb, 'updateAdminUIState')
