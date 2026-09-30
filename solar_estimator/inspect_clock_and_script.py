import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790335657134.html', 'r', encoding='utf-8') as f:
    orig = f.read()

print("Clock matches:")
for m in re.finditer(r'clock', orig, re.IGNORECASE):
    s = max(0, m.start() - 30)
    e = min(len(orig), m.end() + 30)
    print(repr(orig[s:e]))

print("\nScript tags in orig:")
for i, m in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>', orig, re.DOTALL | re.IGNORECASE)):
    print(f"Script {i}: len={len(m.group(1))}")
    print(repr(m.group(0)[:80]))

print("\nScript tags in VoltRoof_Combined.html:")
with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    comb = f.read()
for i, m in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>', comb, re.DOTALL | re.IGNORECASE)):
    print(f"Comb Script {i}: len={len(m.group(1))}")
    print(repr(m.group(0)[:80]))
