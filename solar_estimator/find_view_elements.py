import re

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'<div[^>]+class=["\'][^"\']*view[^"\']*["\'][^>]*>', text)
print("Elements with class containing 'view':", len(m))
for el in m[:20]:
    print(" ", el)
