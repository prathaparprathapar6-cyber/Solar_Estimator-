import re

with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Find switchAdminTab definition
idx = html.find("function switchAdminTab")
if idx != -1:
    print("switchAdminTab function:")
    print(html[idx:idx+800])

# Find modalAdminManual
idx2 = html.find('id="modalAdminManual"')
if idx2 != -1:
    print("\nmodalAdminManual HTML snippet:")
    print(html[idx2:idx2+1200])
