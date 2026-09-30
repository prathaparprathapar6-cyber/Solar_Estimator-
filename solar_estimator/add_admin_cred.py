import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_admins = 'BUILTIN_ADMINS = ['
new_admins = 'BUILTIN_ADMINS = [\n  { username: "admin", emails: ["admin@voltroof.in", "admin@jnnce.ac.in"], mobile: "9999999999", password: "admin123", role: "super_admin" },'

if old_admins in text:
    text = text.replace(old_admins, new_admins, 1)
    with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully added admin / admin123 to BUILTIN_ADMINS in VoltRoof_Combined.html!")
else:
    print("old_admins not found!")
