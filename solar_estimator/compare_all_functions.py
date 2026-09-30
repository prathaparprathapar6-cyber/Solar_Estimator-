import re

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    up = f.read()

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    comb = f.read()

funcs_up = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', up))
funcs_comb = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', comb))

print("Total functions in user_uploaded_latest.html:", len(funcs_up))
print("Total functions in VoltRoof_Combined.html:   ", len(funcs_comb))

missing_in_comb = funcs_up - funcs_comb
print("\nFunctions in user_uploaded_latest.html but MISSING in VoltRoof_Combined.html:")
for fn in sorted(missing_in_comb):
    print("  -", fn)

missing_in_up = funcs_comb - funcs_up
print(f"\nFunctions in VoltRoof_Combined.html but NOT in user_uploaded_latest.html (Count: {len(missing_in_up)}):")
for fn in sorted(missing_in_up)[:20]:
    print("  +", fn)
