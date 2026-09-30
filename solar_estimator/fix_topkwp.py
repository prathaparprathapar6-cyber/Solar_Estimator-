import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix line 5324
old_code = '    document.getElementById("topKwp").textContent = "— kWp";'
new_code = '''    const topBadge = document.getElementById("topKwpBadge");
    if (topBadge) topBadge.textContent = "— kWp";
    const topStatus = document.getElementById("topKwp");
    if (topStatus) topStatus.innerHTML = '<div class="dot"></div> All good';'''

if old_code in text:
    text = text.replace(old_code, new_code, 1)
    print("Replaced line 5324 successfully")
else:
    print("WARN: old_code not found")

with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved VoltRoof_Combined.html")
