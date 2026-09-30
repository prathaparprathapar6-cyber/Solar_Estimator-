import difflib

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f1:
    text1 = f1.readlines()
with open('solar_pv_estimator_standalone.py', 'r', encoding='utf-8') as f2:
    text2 = f2.readlines()

diff = list(difflib.unified_diff(text2, text1, fromfile='standalone', tofile='estimator', n=2))
for line in diff[:50]:
    print(line, end='')
if len(diff) > 50:
    print(f"\n... and {len(diff) - 50} more lines")
