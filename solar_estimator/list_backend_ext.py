import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("backend_ext.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
funcs = re.findall(r'def\s+([a-zA-Z0-9_]+)\s*\([^)]*\):', text)
print("Functions in backend_ext.py:")
for fn in funcs:
    print(" -", fn)
