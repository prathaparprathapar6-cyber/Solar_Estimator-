import re

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("SVG logo occurrences:")
for m in re.finditer(r'<svg viewBox="0 0 48 48"[^>]*>.*?</svg>', html, re.DOTALL):
    s = max(0, m.start() - 60)
    e = min(len(html), m.end() + 60)
    print("Match at", m.start(), ":")
    print(repr(html[s:e]))
    print("-" * 50)

print("\nFavicon / Link icons:")
for m in re.finditer(r'<link[^>]*icon[^>]*>', html):
    print(repr(m.group(0)))

print("\nLogo classes / IDs:")
for m in re.finditer(r'(id|class)=["\'][^"\']*logo[^"\']*["\']', html, re.IGNORECASE):
    s = max(0, m.start() - 30)
    e = min(len(html), m.end() + 30)
    print(repr(html[s:e]))
