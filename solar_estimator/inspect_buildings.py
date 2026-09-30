import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Search for building-related markup and JS in index.html:")
# Find building card template or building JS logic
bld_matches = re.findall(r'function\s+[a-zA-Z0-9_]*bld[a-zA-Z0-9_]*\s*\([^)]*\)', text, re.IGNORECASE)
print("Building functions:", bld_matches)

# Let's search for how sites and buildings are managed in JS
for line in text.splitlines():
    if any(k in line.lower() for k in ['site_data', 'sites =', 'currentsite', 'addbuilding', 'renderbuilding', 'modulespec', 'panelwatt', 'mcb']):
        print(line[:120])
