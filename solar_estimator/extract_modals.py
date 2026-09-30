with open("VoltRoof_Combined.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Extract modalStatutory20kW
idx_20k_start = text.find('<!-- KERC 20 kW Statutory Limitation Warning Modal -->')
if idx_20k_start == -1:
    idx_20k_start = text.find('<div class="name-gate" id="modalStatutory20kW"')
idx_20k_end = text.find('<!-- Admin User Manual & System Control Center Modal', idx_20k_start)
if idx_20k_end == -1:
    idx_20k_end = text.find('<div class="name-gate" id="modalAdminManual"', idx_20k_start)

statutory_html = text[idx_20k_start:idx_20k_end].strip()

# Extract modalAdminManual
idx_admin_start = text.find('<!-- Admin User Manual & System Control Center Modal', idx_20k_end - 100)
if idx_admin_start == -1:
    idx_admin_start = text.find('<div class="name-gate" id="modalAdminManual"')

# Find closing of modalAdminManual: search for next section or <aside class="sidebar"
idx_admin_end = text.find('<aside class="sidebar"', idx_admin_start)
if idx_admin_end == -1:
    idx_admin_end = text.find('<div class="mobile-bar"', idx_admin_start)

admin_html = text[idx_admin_start:idx_admin_end].strip()

print(f"Extracted statutory_html: length = {len(statutory_html)}")
print(f"Extracted admin_html: length = {len(admin_html)}")

with open("extracted_modals.html", "w", encoding="utf-8") as f:
    f.write(statutory_html + "\n\n" + admin_html)

print("Saved extracted_modals.html")
