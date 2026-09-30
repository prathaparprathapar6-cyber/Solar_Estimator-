import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    up_text = f.read()

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    comb_text = f.read()

print("File sizes:")
print(f"  user_uploaded_latest.html: {len(up_text):,} bytes ({len(up_text.splitlines()):,} lines)")
print(f"  VoltRoof_Combined.html:    {len(comb_text):,} bytes ({len(comb_text.splitlines()):,} lines)")

def find_admin_features(text, label):
    print(f"\n==================== {label} ====================")
    # Search for admin modals / views
    modals = re.findall(r'<div[^>]+id=[\'"]([^\'"]*admin[^\'"]*|[^\'"]*pricing[^\'"]*|[^\'"]*cost[^\'"]*|[^\'"]*manual[^\'"]*)[\'"][^>]*>', text, re.IGNORECASE)
    print("Modals/Divs with admin/pricing/cost/manual:")
    for m in sorted(set(modals)):
        print(f"  - {m}")
        
    # Search for admin buttons in nav or header
    admin_btns = re.findall(r'<button[^>]+id=[\'"]([^\'"]*admin[^\'"]*|[^\'"]*pricing[^\'"]*|[^\'"]*policy[^\'"]*|[^\'"]*studio[^\'"]*)[\'"][^>]*>', text, re.IGNORECASE)
    print("Buttons with admin/pricing/policy/studio:")
    for b in sorted(set(admin_btns)):
        print(f"  - {b}")

    # Search for views (data-view)
    views = re.findall(r'data-view=[\'"]([^\'"]+)[\'"]', text)
    print("Views (data-view):", sorted(set(views)))

    # Search for pricing or cost input fields
    pricing_inputs = re.findall(r'<input[^>]+id=[\'"]([^\'"]*price[^\'"]*|[^\'"]*cost[^\'"]*|[^\'"]*rate[^\'"]*|[^\'"]*tariff[^\'"]*)[\'"][^>]*>', text, re.IGNORECASE)
    print(f"Pricing/Cost Inputs count: {len(pricing_inputs)}")
    for inp in sorted(list(set(pricing_inputs))):
        print(f"  - {inp}")

    # Search for functions related to admin / pricing
    funcs = re.findall(r'function\s+([a-zA-Z0-9_]*(?:admin|pricing|cost|rate|bom|pricing)[a-zA-Z0-9_]*)\s*\(', text, re.IGNORECASE)
    print("Functions count:", len(funcs))
    for fn in sorted(list(set(funcs))):
        print(f"  - {fn}")

find_admin_features(up_text, "USER UPLOADED LATEST")
find_admin_features(comb_text, "VOLTROOF COMBINED")
