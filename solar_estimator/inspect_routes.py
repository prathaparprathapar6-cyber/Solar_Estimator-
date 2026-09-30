import re

with open('solar_pv_estimator.py', 'r', encoding='utf-8', errors='ignore') as f:
    txt = f.read()

print("GET/POST API routes in solar_pv_estimator.py:")
for m in re.finditer(r'parsed\.path\s*==\s*["\'](/api[^"\']*)["\']', txt):
    print("  ", m.group(1))

for m in re.finditer(r'parsed\.path\.startswith\(["\'](/api[^"\']*)["\']\)', txt):
    print("  startswith: ", m.group(1))
